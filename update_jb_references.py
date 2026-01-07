import re
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campaign_site.settings')
django.setup()

from core.models import HomePage

FILE_PATH = r"core\templates\core\index.html"

def update_jb_references():
    print(f"Reading {FILE_PATH}...")
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(FILE_PATH, 'r', encoding='latin-1') as f:
            content = f.read()

    new_content = content
    
    # Specific replacements based on findings
    # Case insensitive "TeamJB" -> "TeamDrEmmanuelNMusa"
    new_content = re.sub(r'TeamJB', 'TeamDrEmmanuelNMusa', new_content, flags=re.IGNORECASE)
    
    # Just in case "JB" appears as a whole word somewhere we missed
    new_content = re.sub(r'\bJB\b', 'Dr. Emmanuel N. Musa', new_content)
    
    if new_content != content:
        print("Writing changes to index.html...")
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated index.html.")
    else:
        print("No changes needed in index.html.")

    # Update Database
    print("Checking database...")
    home_page = HomePage.objects.first()
    if home_page:
        updated = False
        # Check all text fields
        for field in home_page._meta.fields:
            if field.get_internal_type() in ['CharField', 'TextField']:
                value = getattr(home_page, field.name)
                if value and isinstance(value, str):
                    new_value = re.sub(r'TeamJB', 'TeamDrEmmanuelNMusa', value, flags=re.IGNORECASE)
                    new_value = re.sub(r'\bJB\b', 'Dr. Emmanuel N. Musa', new_value)
                    
                    if new_value != value:
                        setattr(home_page, field.name, new_value)
                        updated = True
                        print(f"Updated field {field.name}")
        
        if updated:
            home_page.save()
            print("Database record updated.")
        else:
            print("No database changes needed.")

if __name__ == "__main__":
    update_jb_references()
