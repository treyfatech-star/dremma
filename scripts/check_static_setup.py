import os

FILE_PATH = r"c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\templates\core\index.html"

def check_static():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    has_load_static = "{% load static %}" in content
    has_static_usage = "{% static" in content
    
    print(f"Has {{% load static %}}: {has_load_static}")
    print(f"Has {{% static ... %}}: {has_static_usage}")
    
    if has_static_usage and not has_load_static:
        print("Adding {% load static %} to the top...")
        new_content = "{% load static %}\n" + content
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Added.")
    elif not has_static_usage:
        print("WARNING: No {% static %} tags found! Assets might be hardcoded.")

if __name__ == "__main__":
    check_static()
