"""
Service Worker Builder — collects precache manifest and injects into SW template.
"""
import os
import json


def collect_shell_assets(output_dir):
    """
    Returns the UI shell assets to precache.
    Only includes structural assets (HTML, CSS, JS) — NOT images.
    Images are lazy-cached by the fetch handler at runtime.
    """
    shell_assets = [
        '/',
        '/index.html',
        '/projects.html',
        '/credentials.html',
        '/skills.html',
        '/about.html',
        '/education.html',
        '/society.html',
        '/contact.html',
    ]

    for asset_root in ('css', 'js'):
        root_path = os.path.join(output_dir, asset_root)
        if not os.path.exists(root_path):
            continue

        for current_root, _, files in os.walk(root_path):
            for filename in sorted(files):
                if filename.startswith('.'):
                    continue

                absolute_path = os.path.join(current_root, filename)
                relative_path = os.path.relpath(absolute_path, output_dir)
                shell_assets.append('/' + relative_path.replace(os.sep, '/'))

    return sorted(set(shell_assets), key=shell_assets.index)


def inject_sw(project_root, output_dir):
    """
    Read the SW template, inject shell precache list, write to output.
    """
    sw_src = os.path.join(project_root, 'static', 'sw.js')
    sw_dest = os.path.join(output_dir, 'sw.js')

    if not os.path.exists(sw_src):
        print("⚠ Service Worker template not found, skipping injection.")
        return

    precache_list = collect_shell_assets(output_dir)

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
