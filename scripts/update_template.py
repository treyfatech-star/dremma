import os
import re

BASE_DIR = os.getcwd()
TEMPLATE_FILE = os.path.join(BASE_DIR, 'core', 'templates', 'core', 'index.html')

if not os.path.exists(TEMPLATE_FILE):
    print(f"File not found: {TEMPLATE_FILE}")
    exit(1)

with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Add load static if missing
if '{% load static %}' not in content:
    content = '{% load static %}\n' + content

# Replace assets/ links
# We need to handle:
# href="assets/file.ext" -> href="{% static 'core/file.ext' %}"
# src="assets/file.ext" -> src="{% static 'core/file.ext' %}"
# content="assets/file.ext" -> content="{% static 'core/file.ext' %}"

def replace_static(match):
    prefix = match.group(1) # src= or href= or content=
    quote = match.group(2)  # " or '
    path = match.group(3)   # assets/filename.ext
    
    filename = path.replace('assets/', '', 1)
    # Remove leading slash if present
    if filename.startswith('/'): filename = filename[1:]
    
    return f'{prefix}{quote}{{% static "core/{filename}" %}}{quote}'

# Regex to match src/href/content attributes pointing to assets/
# attributes can be src, href, content
# quotes can be ' or "
pattern = re.compile(r'(src=|href=|content=)(["\'])(assets/[^"\']*?)(["\'])')

new_content = pattern.sub(replace_static, content)

with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {TEMPLATE_FILE}")
