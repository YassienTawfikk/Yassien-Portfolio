import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

# Configuration
# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, 'content')
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'theme', 'templates')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'public')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'theme', 'static')

def setup_directories(site_data):
    """Create output directory and copy assets."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    # Copy Static Assets
    # Structure: theme/static/css -> public/css
    # Structure: theme/static/js -> public/js
    
    if os.path.exists(os.path.join(STATIC_DIR, 'css')):
        shutil.copytree(os.path.join(STATIC_DIR, 'css'), os.path.join(OUTPUT_DIR, 'css'))
    
    if os.path.exists(os.path.join(STATIC_DIR, 'js')):
        shutil.copytree(os.path.join(STATIC_DIR, 'js'), os.path.join(OUTPUT_DIR, 'js'))

    # Copy Images and Documents
    if os.path.exists(os.path.join(STATIC_DIR, 'images')):
        shutil.copytree(os.path.join(STATIC_DIR, 'images'), os.path.join(OUTPUT_DIR, 'images'))
    if os.path.exists(os.path.join(STATIC_DIR, 'documents')):
        shutil.copytree(os.path.join(STATIC_DIR, 'documents'), os.path.join(OUTPUT_DIR, 'documents'))
    
    # Copy Service Worker
    # Check both potential locations (root or static) just in case, but moved to theme/static likely?
    # Actually SW was in project_root/static/sw.js. We haven't moved 'static' folder in root yet.
    # The user asked to organize "assets" -> "theme/static".
    # Existing "static" folder in root (containing sw.js) is different.
    
    # --- SERVICE WORKER INJECTION ---
    sw_src = os.path.join(PROJECT_ROOT, 'static', 'sw.js')
    sw_dest = os.path.join(OUTPUT_DIR, 'sw.js')
    
    if os.path.exists(sw_src):
        # 1. Collect all images to pre-cache
        precache_list = [
            '/', 
            '/index.html', 
            '/projects.html', 
            '/css/base/global.css',
            '/css/base/normalize.css',
            '/js/core/navbar.js',
            '/js/core/preloader.js'
        ]
        
        # From Projects
        projects = site_data.get('projects', {}).get('Projects', [])
        for p in projects:
            if p.get('overview_image'):
                precache_list.append(p['overview_image'])
        
        # From Credentials (Certificates)
        certs = site_data.get('credentials', {}).get('coursesAndCertificates', {}).get('items', [])
        trainings = site_data.get('credentials', {}).get('fieldExperience', {}).get('items', [])
        for item in certs + trainings:
            if item.get('certificateImage'):
                precache_list.append(item['certificateImage'])
                
        # From Home/About
        home = site_data.get('home', {})
        if home.get('profile photo'): precache_list.append(home['profile photo'])
        
        about = site_data.get('about', {})
        if about.get('image_01'): precache_list.append(about['image_01'])
        if about.get('image_02'): precache_list.append(about['image_02'])
        if about.get('image_03'): precache_list.append(about['image_03'])
        
        # Deduplicate
        precache_list = list(set(precache_list))
        
        # 2. Read SW template
        with open(sw_src, 'r') as f:
            sw_content = f.read()
            
        # 3. Inject list
        js_array = json.dumps(precache_list, indent=4)
        sw_content = sw_content.replace('const PRECACHE_URLS = [];', f'const PRECACHE_URLS = {js_array};')
        
        # 4. Write to public/sw.js
        with open(sw_dest, 'w') as f:
            f.write(sw_content)
        print(f"Service Worker injected with {len(precache_list)} assets.")

    return DATA_DIR, TEMPLATE_DIR, OUTPUT_DIR

def load_data():
    """Load all JSON data from data directory."""
    data = {}
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            key = filename.replace('.json', '')
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                data[key] = json.load(f)
    return data

def build():
    print("Building static site...")
    
    # Load Data FIRST
    site_data = load_data()
    
    # Then setup directories with data
    setup_directories(site_data)
    
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    
    # --- Projects Logic ---
    projects_list = site_data.get('projects', {}).get('Projects', [])
    
    def get_project_domain(title, tags):
        tags_str = " ".join(tags).lower()
        title_lower = title.lower()
        if "soundprints" in title_lower or "audiophileeq" in title_lower: return "Audio & Signal Processing", "fa-solid fa-wave-square"
        if "lifestream" in title_lower: return "Mobile & IoT System", "fa-solid fa-mobile-screen"
        if "sequencealignx" in title_lower: return "Biomedical Engineering", "fa-solid fa-heart-pulse"
        if "smartretailregressor" in title_lower or "predictiloan" in title_lower: return "Data Science & analytics", "fa-solid fa-chart-line"
        if "game" in tags_str: return "Game Development", "fa-solid fa-gamepad"
        if "medical" in tags_str or "biomedical" in tags_str or "healthcare" in tags_str:
            if "ai" in tags_str or "learning" in tags_str: return "Medical AI", "fa-solid fa-brain"
            return "Biomedical Engineering", "fa-solid fa-heart-pulse"
        if "deep learning" in tags_str or "machine learning" in tags_str or "data" in tags_str: return "AI & Data Science", "fa-solid fa-robot"
        if "computer vision" in tags_str or "image" in tags_str: return "Computer Vision", "fa-solid fa-eye"
        if "embedded" in tags_str or "hardware" in tags_str or "iot" in tags_str: return "Embedded Systems", "fa-solid fa-microchip"
        if "audio" in tags_str or "signal" in tags_str: return "Signal Processing", "fa-solid fa-wave-square"
        if "web" in tags_str or "mobile" in tags_str or "app" in tags_str: return "Web & Mobile App", "fa-solid fa-laptop-code"
        return "Software Engineering", "fa-solid fa-code"

    # Enlighten projects with domain info
    for p in projects_list:
        d_name, d_icon = get_project_domain(p.get("title", ""), p.get("tags", []))
        p['domain_name'] = d_name
        p['domain_icon'] = d_icon

    featured_projects = [p for p in projects_list if p.get("live_demo")]
    featured_video_projects = [p for p in projects_list if p.get("video_demo") and not p.get("live_demo")]
    other_projects = [p for p in projects_list if not p.get("live_demo") and not p.get("video_demo")]

    categories = {
        "AI & Data Science": [],
        "Computer Vision & Image Processing": [],
        "Biomedical & Signal Processing": [],
        "Web, Mobile & Software": [],
        "Embedded Systems & IoT": [],
        "Game Development": []
    }

    for p in other_projects:
        tags_str = " ".join(p.get("tags", [])).lower()
        title = p.get("title", "").lower()
        
        if "lifestream" in title or "soundprints" in title:
            categories["Web, Mobile & Software"].append(p)
            continue
        if "facevector" in title:
            categories["Computer Vision & Image Processing"].append(p)
            continue
        
        if "game" in tags_str:
            categories["Game Development"].append(p)
        elif any(kw in tags_str for kw in ["deep learning", "machine learning", "data", "regression", "prediction", "analytics", "svm", "forest", "xgboost", "ml"]):
            categories["AI & Data Science"].append(p)
        elif "computer vision" in tags_str or "image" in tags_str:
            categories["Computer Vision & Image Processing"].append(p)
        elif "embedded" in tags_str or "arduino" in tags_str:
            categories["Embedded Systems & IoT"].append(p)
        elif "medical" in tags_str or "biomedical" in tags_str or "signal" in tags_str or "audio" in tags_str:
            categories["Biomedical & Signal Processing"].append(p)
        else:
            categories["Web, Mobile & Software"].append(p)

    # Pass Processed Data to Context
    site_data['projects_context'] = {
        'featured_projects': featured_projects,
        'featured_video_projects': featured_video_projects,
        'categories': categories
    }

    # Define pages to build
    pages = [
        ('home.html', 'index.html'),
        ('projects.html', 'projects.html'),
        ('about.html', 'about.html'),
        ('credentials.html', 'credentials.html'),
        ('skills.html', 'skills.html'),
        ('education.html', 'education.html'),
        ('society.html', 'society.html'),
        ('contact.html', 'contact.html'),
    ]
    
    # Check if we have templates before trying to render
    if not os.path.exists(os.path.join(TEMPLATE_DIR, 'components')):
         os.makedirs(os.path.join(TEMPLATE_DIR, 'components'))

    # Temporary: Create a dummy index.html if no templates exist yet to verify build script runs
    if not pages:
        with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
             f.write('<h1>Work in Progress</h1>')

    for template_name, output_name in pages:
        template = env.get_template(template_name)
        output = template.render(**site_data)
        
        with open(os.path.join(OUTPUT_DIR, output_name), 'w') as f:
            f.write(output)
            
    print("Build complete. Output in public/")

if __name__ == "__main__":
    build()
