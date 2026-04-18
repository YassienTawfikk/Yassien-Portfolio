import os
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9_]', '_', text)
    text = re.sub(r'_+', '_', text)
    return text.strip('_')

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(root_dir, 'content')
    projects_json_path = os.path.join(content_dir, 'projects.json')
    config_path = os.path.join(content_dir, 'config.json')
    out_dir = os.path.join(content_dir, 'projects')
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(projects_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    projects = data.get('Projects', [])
    image_host = config.get('image_host', 'https://i.postimg.cc/')
    
    domain_map = {}
    for d_key, d_val in config['taxonomies']['domains'].items():
        domain_map[d_val['name']] = d_key
        
    cat_map = {}
    for c_key, c_val in config['taxonomies']['categories'].items():
        cat_map[c_val] = c_key
        
    import yaml

    for p in projects:
        # Simplify image URL
        img = p.get('overview_image', '')
        if img.startswith(image_host):
            img = img.replace(image_host, '')
            
        domain_name = p.get('domain', {}).get('name', '')
        d_id = domain_map.get(domain_name, None)
        
        cat_name = p.get('category', '')
        c_id = cat_map.get(cat_name, None)
        
        frontmatter = {
            'title': p.get('title'),
            'short_description': p.get('short_description'),
            'overview_image_id': img,
            'year': p.get('year')
        }
        if d_id: frontmatter['domain_id'] = d_id
        if c_id: frontmatter['category_id'] = c_id
        
        for optional_field in ['github_link', 'live_demo', 'video_demo', 'order']:
            val = p.get(optional_field)
            if val is not None:
                frontmatter[optional_field] = val
                
        for list_field in ['tech_stack', 'tags', 'highlights']:
            val = p.get(list_field)
            if val is not None:
                frontmatter[list_field] = val

        md_content = f"---\n{yaml.dump(frontmatter, sort_keys=False).strip()}\n---\n\n{p.get('long_description', '')}\n"
        
        filename = slugify(p['title']) + '.md'
        with open(os.path.join(out_dir, filename), 'w', encoding='utf-8') as f:
            f.write(md_content)
            
    print(f"Migrated {len(projects)} projects to {out_dir}")

if __name__ == '__main__':
    main()
