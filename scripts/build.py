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
    
    # Logic to use pre-defined domain/category from JSON
    # Map 'domain' object to flat structure if needed by template, 
    # but template likely accesses p.domain.name / p.domain.icon?
    # Let's check template usage.
    # Template: {{ project.domain_name }} / {{ project.domain_icon }} ?
    # Wait, the previous build.py did:
    # p['domain_name'] = d_name
    # p['domain_icon'] = d_icon
    # So the template expects these keys directly on the project object.
    # I should map p['domain']['name'] -> p['domain_name'] to maintain compatibility
    # OR update template. Updating template is cleaner long term, but mapping here is safer short term.
    # User asked: "add the project domain page in the @[content/projects.json] instead of making it in the html file"
    # Actually, if I update template to use `project.domain.name`, it is cleaner.
    # But for now, let's keep compatibility by re-assigning for the template if needed, 
    # OR just fix the template too. 
    # Let's check template content again.
    # theme/templates/components/project_card.html was imported. I need to check that file.
    # I didn't read project_card.html!
    
    # I'll stick to mapping in build.py for now to be safe, or just check the template in a second.
    # Better to map in build.py for now to ensure minimal breakage.
    
    for p in projects_list:
        if 'domain' in p:
            p['domain_name'] = p['domain']['name']
            p['domain_icon'] = p['domain']['icon']

    featured_projects = [p for p in projects_list if p.get("live_demo")]
    # featured_video_projects removed per request. Now all non-live projects go to categories.
    other_projects = [p for p in projects_list if not p.get("live_demo")]

    categories = {
        "AI & Data Science": [],
        "Computer Vision & Image Processing": [],
        "Biomedical & Signal Processing": [],
        "Web, Mobile & Software": [],
        "Embedded Systems & IoT": [],
        "Game Development": []
    }

    for p in other_projects:
        cat = p.get('category', 'Web, Mobile & Software')
        if cat in categories:
            categories[cat].append(p)
        else:
            # Fallback or create new category if user adds custom one in JSON
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(p)

    # Sort projects within each category by 'order' (default 99 for low priority)
    for cat in categories:
        categories[cat].sort(key=lambda x: x.get('order', 99))

    # Pass Processed Data to Context
    site_data['projects_context'] = {
        'featured_projects': featured_projects,
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
