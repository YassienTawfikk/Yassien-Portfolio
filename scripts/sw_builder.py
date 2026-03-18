"""
Service Worker Builder — collects precache manifest and injects into SW template.
"""
import os
import json


def collect_shell_assets():
    """
    Returns the UI shell assets to precache.
    Only includes structural assets (HTML, CSS, JS) — NOT images.
    Images are lazy-cached by the fetch handler at runtime.
    """
    return [
        '/',
        '/index.html',
        '/projects.html',
        '/credentials.html',
        '/skills.html',
        '/about.html',
        '/education.html',
        '/society.html',
        '/contact.html',
        '/css/base/global.css',
        '/css/base/normalize.css',
        '/css/components/modals.css',
        '/css/components/preloader.css',
        '/js/core/navbar.js',
        '/js/core/preloader.js',
        '/js/utils/gallery.js',
        '/js/utils/modal_utils.js',
        '/js/utils/navbar_toggle.js',
    ]


def inject_sw(project_root, output_dir):
    """
    Read the SW template, inject shell precache list, write to output.
    """
    sw_src = os.path.join(project_root, 'static', 'sw.js')
    sw_dest = os.path.join(output_dir, 'sw.js')

    if not os.path.exists(sw_src):
        print("⚠ Service Worker template not found, skipping injection.")
        return

    precache_list = collect_shell_assets()

    with open(sw_src, 'r') as f:
        sw_content = f.read()

    js_array = json.dumps(precache_list, indent=4)
    sw_content = sw_content.replace(
        'const PRECACHE_URLS = [];',
        f'const PRECACHE_URLS = {js_array};'
    )

    with open(sw_dest, 'w') as f:
        f.write(sw_content)

    print(f"✓ Service Worker injected with {len(precache_list)} shell assets "
          f"(images lazy-cached at runtime).")
