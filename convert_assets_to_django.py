import os
import re

FILE_PATH = r"c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\templates\core\index.html"

def convert_assets():
    print(f"Reading {FILE_PATH}...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add {% load static %} if missing
    if "{% load static %}" not in content:
        print("Adding {% load static %}...")
        content = "{% load static %}\n" + content
        
    # 2. Replace href="assets/..." and src="assets/..."
    # Group 1: attr name (href or src)
    # Group 2: quote
    # Group 3: path (anything except quote)
    # Group 4: quote
    pattern = r'(href|src)=([\'"])assets/([^"\']+)([\'"])'
    
    def replacement(match):
        attr = match.group(1)
        quote = match.group(2)
        path = match.group(3)
        # normalized to {% static 'core/path' %}
        return f'{attr}={quote}{{% static \'core/{path}\' %}}{quote}'
        
    new_content, count = re.subn(pattern, replacement, content)
    
    print(f"Replaced {count} asset links.")
    
    if content != new_content:
        print("Writing changes...")
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Done.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    convert_assets()
