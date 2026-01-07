import os
import shutil
import re

# Paths
BASE_DIR = os.getcwd()
CORE_DIR = os.path.join(BASE_DIR, 'core')
STATIC_DIR = os.path.join(CORE_DIR, 'static', 'core')
TEMPLATE_DIR = os.path.join(CORE_DIR, 'templates', 'core')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
INDEX_FILE = os.path.join(BASE_DIR, 'index.html')

# Create directories
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# Move assets
if os.path.exists(ASSETS_DIR):
    print(f"Moving assets from {ASSETS_DIR} to {STATIC_DIR}")
    for item in os.listdir(ASSETS_DIR):
        s = os.path.join(ASSETS_DIR, item)
        d = os.path.join(STATIC_DIR, item)
        if os.path.isdir(s):
            shutil.move(s, d)
        else:
            shutil.move(s, d)
    # Remove empty assets dir
    try:
        os.rmdir(ASSETS_DIR)
    except:
        pass
else:
    print("Assets directory not found!")

# Process and Move index.html
if os.path.exists(INDEX_FILE):
    print(f"Processing and moving {INDEX_FILE}")
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add load static
    if '{% load static %}' not in content:
        content = '{% load static %}\n' + content
    
    # Replace asset links
    # Pattern: Look for src="assets/..." or href="assets/..."
    # We assume the clone script used "assets/" prefix
    
    def replace_static(match):
        prefix = match.group(1) # src=" or href="
        path = match.group(2)   # assets/filename.ext
        quote = match.group(3)  # " or '
        
        # Remove assets/ prefix for the static tag
        filename = path.replace('assets/', '', 1)
        if filename.startswith('/'): filename = filename[1:]
        
        return f'{prefix}{{% static "core/{filename}" %}}{quote}'

    # Regex for "assets/..."
    # We match: (src=|href=)(['"])assets/(.*?)(['"])
    pattern = re.compile(r'(src=|href=|content=)(["\'])assets/(.*?)(["\'])')
    content = pattern.sub(replace_static, content)
    
    # Write to template dir
    dest_file = os.path.join(TEMPLATE_DIR, 'index.html')
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Remove original index.html
    os.remove(INDEX_FILE)
    print(f"Moved processed index.html to {dest_file}")
else:
    print("index.html not found!")

print("Migration complete.")
