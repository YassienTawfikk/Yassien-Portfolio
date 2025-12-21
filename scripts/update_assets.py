
import json
import os
import re

CONTENT_DIR = 'content'
IMAGES_DIR = 'theme/static/images'

def normalize(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def update_projects():
    projects_path = os.path.join(CONTENT_DIR, 'projects.json')
    with open(projects_path, 'r') as f:
        data = json.load(f)

    project_images = os.listdir(os.path.join(IMAGES_DIR, 'projects'))
    # meaningful map: normalized_name -> filename
    img_map = {normalize(f.split('.')[0]): f for f in project_images}

    for project in data['Projects']:
        title_norm = normalize(project['title'])
        # Special case handling if needed, or fuzzy match
        if title_norm in img_map:
            project['overview_image'] = f"/images/projects/{img_map[title_norm]}"
            print(f"Updated {project['title']} -> {project['overview_image']}")
        else:
            print(f"WARNING: Could not find image for {project['title']} (norm: {title_norm})")

    with open(projects_path, 'w') as f:
        json.dump(data, f, indent=4)

def update_json_generic(filename, folder_name):
    path = os.path.join(CONTENT_DIR, filename)
    with open(path, 'r') as f:
        content = f.read()

    # Regex to find image URLs
    # Look for https://.../filename.ext and replace with /images/folder_name/filename.avif
    # We assume the basename matches (excluding extension)
    
    # Get available images in that folder
    available_imgs = os.listdir(os.path.join(IMAGES_DIR, folder_name))
    img_map = {f.split('.')[0]: f for f in available_imgs}

    def replace_url(match):
        url = match.group(0)
        basename = url.split('/')[-1].split('.')[0]
        if basename in img_map:
            return f"/images/{folder_name}/{img_map[basename]}"
        return url

    # Regex for standard image URLs
    new_content = re.sub(r'https?://[^\s"]+\.(jpg|jpeg|png|avif)', replace_url, content)
    
    with open(path, 'w') as f:
        f.write(new_content)
    print(f"Updated {filename}")

if __name__ == "__main__":
    print("Updating project images...")
    update_projects()
    
    print("Updating about.json...")
    update_json_generic('about.json', 'about')
    
    print("Updating contact.json...")
    update_json_generic('contact.json', 'contact')
    
    print("Updating credentials.json...")
    update_json_generic('credentials.json', 'certificates')
