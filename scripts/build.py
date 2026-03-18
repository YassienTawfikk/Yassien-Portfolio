"""
Build orchestrator — coordinates content loading, asset copying,
service worker injection, and template rendering.
"""
import os
import shutil
from jinja2 import Environment, FileSystemLoader
from content_loader import load_data, validate_content, process_projects
from sw_builder import inject_sw

# ── Configuration ────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, 'content')
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'theme', 'templates')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'public')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'theme', 'static')

# Pages to render: (template, output_filename)
PAGES = [
    ('home.html', 'index.html'),
    ('projects.html', 'projects.html'),
    ('about.html', 'about.html'),
    ('credentials.html', 'credentials.html'),
    ('skills.html', 'skills.html'),
    ('education.html', 'education.html'),
    ('society.html', 'society.html'),
    ('contact.html', 'contact.html'),
]


def setup_output():
    """Clean and recreate the output directory, copy static assets."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    for subdir in ['css', 'js', 'images', 'documents']:
        src = os.path.join(STATIC_DIR, subdir)
        if os.path.exists(src):
            shutil.copytree(src, os.path.join(OUTPUT_DIR, subdir))


def render_pages(site_data):
    """Render all Jinja2 templates with site data."""
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    for template_name, output_name in PAGES:
        template = env.get_template(template_name)
        html = template.render(**site_data)
        with open(os.path.join(OUTPUT_DIR, output_name), 'w') as f:
            f.write(html)


def build():
    print("Building static site...")

    # 1. Load & validate content
    site_data = load_data(DATA_DIR)
    validate_content(site_data)

    # 2. Process projects into template-ready context
    site_data = process_projects(site_data)

    # 3. Copy static assets
    setup_output()

    # 4. Inject Service Worker
    inject_sw(PROJECT_ROOT, OUTPUT_DIR)

    # 5. Render pages
    render_pages(site_data)

    print("Build complete. Output in public/")


if __name__ == "__main__":
    build()
