"""
Content Loader — loads, validates, and transforms JSON content data.
"""
import os
import json
import sys


def _validate_required(obj, fields, context):
    """Validate that an object has required fields. Returns list of errors."""
    errors = []
    for field in fields:
        if field not in obj or obj[field] is None:
            errors.append(f"  Missing required field '{field}' in {context}")
    return errors


def validate_content(data):
    """
    Validates loaded JSON content for structural correctness.
    Prints warnings for non-critical issues, exits on critical errors.
    """
    errors = []
    warnings = []

    # ── Projects ─────────────────────────────────────────────
    projects = data.get('projects', {}).get('Projects', [])
    for i, p in enumerate(projects):
        ctx = f"projects[{i}] ('{p.get('title', 'untitled')}')"
        errors += _validate_required(p, ['title', 'short_description', 'domain'], ctx)

        if 'domain' in p:
            if not isinstance(p['domain'], dict):
                errors.append(f"  'domain' must be an object in {ctx}")
            else:
                errors += _validate_required(p['domain'], ['name', 'icon'], ctx + '.domain')

    # ── Credentials ──────────────────────────────────────────
    creds = data.get('credentials', {})
    for section_key in ['fieldExperience', 'coursesAndCertificates']:
        items = creds.get(section_key, {}).get('items', [])
        for i, item in enumerate(items):
            ctx = f"credentials.{section_key}[{i}]"
            if section_key == 'fieldExperience':
                errors += _validate_required(item, ['role', 'organization'], ctx)
            else:
                errors += _validate_required(item, ['title', 'issuer'], ctx)

    # ── Contact ──────────────────────────────────────────────
    contact = data.get('contact', {})
    direct = contact.get('direct_contact', {})
    if not direct.get('email'):
        warnings.append("  contact.json: missing 'direct_contact.email' field")

    # ── Education ────────────────────────────────────────────
    edu = data.get('education', {})
    if not edu:
        warnings.append("  education.json: file is empty or missing")

    # ── Report ───────────────────────────────────────────────
    if warnings:
        print(f"⚠ Content warnings ({len(warnings)}):")
        for w in warnings:
            print(w)

    if errors:
        print(f"\n✗ Content validation failed ({len(errors)} errors):")
        for e in errors:
            print(e)
        sys.exit(1)

    print(f"✓ Content validated ({len(projects)} projects, "
          f"{len(creds.get('fieldExperience', {}).get('items', []))} experiences, "
          f"{len(creds.get('coursesAndCertificates', {}).get('items', []))} certificates)")


def load_data(data_dir):
    """Load all JSON files from the content directory and Markdown from projects."""
    import datetime
    import frontmatter
    import markdown
    
    data = {}
    config_path = os.path.join(data_dir, 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            data['config'] = json.load(f)
            
    # Load JSON files
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            key = filename.replace('.json', '')
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                data[key] = json.load(f)

    # Load Markdown projects
    projects_dir = os.path.join(data_dir, 'projects')
    projects_list = []
    if os.path.exists(projects_dir):
        for filename in os.listdir(projects_dir):
            if filename.endswith('.md'):
                with open(os.path.join(projects_dir, filename), 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    proj = post.metadata
                    proj['long_description'] = markdown.markdown(post.content)
                    
                    config = data.get('config', {})
                    image_host = config.get('image_host', '')
                    if 'overview_image_id' in proj:
                        img_id = proj['overview_image_id']
                        if img_id.startswith('http://') or img_id.startswith('https://'):
                            proj['overview_image'] = img_id
                        else:
                            proj['overview_image'] = image_host + img_id
                    
                    if 'domain_id' in proj:
                        domain_info = config.get('taxonomies', {}).get('domains', {}).get(proj['domain_id'], {})
                        proj['domain'] = {
                            'name': domain_info.get('name', ''),
                            'icon': domain_info.get('icon', '')
                        }
                        
                    if 'category_id' in proj:
                        proj['category'] = config.get('taxonomies', {}).get('categories', {}).get(proj['category_id'], '')
                        
                    projects_list.append(proj)
                    
    data['projects'] = {'Projects': projects_list}

    # Automatically calculate age based on 2003
    if 'about' in data and 'description' in data['about']:
        current_year = datetime.datetime.now().year
        age = current_year - 2003
        data['about']['description'] = data['about']['description'].replace('{age}', str(age))
        
    return data


def process_projects(site_data):
    """
    Transforms raw project data into categorized, sorted context
    ready for template rendering.
    """
    projects_list = site_data.get('projects', {}).get('Projects', [])

    # Flatten domain object for template compatibility
    for p in projects_list:
        if 'domain' in p:
            p['domain_name'] = p['domain']['name']
            p['domain_icon'] = p['domain']['icon']

    featured_projects = [p for p in projects_list if p.get('live_demo')]
    other_projects = [p for p in projects_list if not p.get('live_demo')]

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
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    # Sort featured projects deterministically
    featured_projects.sort(key=lambda x: (x.get('order', 99), x.get('title', '')))

    # Sort by 'order' and 'title' within each category
    for cat in categories:
        categories[cat].sort(key=lambda x: (x.get('order', 99), x.get('title', '')))

    site_data['projects_context'] = {
        'featured_projects': featured_projects,
        'categories': categories
    }

    return site_data
