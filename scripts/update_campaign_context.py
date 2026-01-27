import os
import re
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campaign_site.settings')
django.setup()

from core.models import HomePage

FILE_PATH = r"core\templates\core\index.html"
MODELS_PATH = r"core\models.py"

def update_file_content(file_path, replacements):
    print(f"Reading {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()

    new_content = content
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)

    if new_content != content:
        print(f"Writing changes to {file_path}...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated.")
        return True
    else:
        print(f"No changes needed for {file_path}.")
        return False

def main():
    # 1. Update index.html
    replacements_html = [
        # Re-election to Election
        (r"re-elect\s+", "elect "),
        (r"re-election", "election"),
        
        # Governor title adjustments
        # "Official Campaign Website of Adamawa Governor" -> "... Gubernatorial Candidate"
        (r"Official Campaign Website of Adamawa Governor", "Official Campaign Website of Gubernatorial Candidate"),
        
        # "Governor Dr. Emmanuel N. Musa" -> "Emnamu Foundation President Dr. Emmanuel N. Musa" (Specific heading)
        (r">Governor Dr\. Emmanuel N\. Musa<", ">Emnamu Foundation President Dr. Emmanuel N. Musa<"),
        
        # General "Adamawa Governor Dr. Emmanuel N. Musa" -> "Dr. Emmanuel N. Musa" (to avoid calling him Governor)
        (r"Adamawa Governor Dr\. Emmanuel N\. Musa", "Dr. Emmanuel N. Musa"),
        
        # Fix "Governor" usages that imply incumbency
        (r"Governor", "Candidate"), # This is risky. Let's be more specific.
    ]
    
    # Let's be safer with "Governor" replacement.
    # We want to remove "Governor" where it refers to him as the current one.
    # But we want to keep "Governor" if it says "Candidate for Governor".
    
    # Revised Replacements
    safe_replacements = [
        (r"re-elect\s+", "elect "),
        (r"re-election", "election"),
        (r"Official Campaign Website of Adamawa Governor", "Official Campaign Website of Gubernatorial Candidate"),
        (r">Governor Dr\. Emmanuel N\. Musa<", ">Emnamu Foundation President Dr. Emmanuel N. Musa<"),
        # Replace "Adamawa Governor Dr. Emmanuel N. Musa" with just the name or candidate title
        (r"Adamawa Governor Dr\. Emmanuel N\. Musa", "Gubernatorial Candidate Dr. Emmanuel N. Musa"),
        # Notification text: "Join the team to elect..." (handled by re-elect above)
    ]

    update_file_content(FILE_PATH, safe_replacements)

    # 2. Update models.py (Defaults)
    replacements_models = [
        (r'default="Dr. Emmanuel N. Musa for Governor - Official Campaign Website of Adamawa Governor Dr. Emmanuel N. Musa"', 
         'default="Dr. Emmanuel N. Musa for Governor - Official Campaign Website of Gubernatorial Candidate Dr. Emmanuel N. Musa"'),
        (r'default="Join the team to re-elect Dr. Emmanuel N. Musa"', 
         'default="Join the team to elect Dr. Emmanuel N. Musa"'),
         # Update description to include Emnamu Foundation President
         (r'default="No matter where you live in Adamawa or what your background is, Dr. Emmanuel N. Musa has been hard at work',
          'default="No matter where you live in Adamawa or what your background is, Emnamu Foundation President Dr. Emmanuel N. Musa has been hard at work'),
    ]
    update_file_content(MODELS_PATH, replacements_models)

    # 3. Update Database
    print("Checking database...")
    home_page = HomePage.objects.first()
    if home_page:
        updated = False
        
        # Title
        if "Adamawa Governor" in home_page.title:
            home_page.title = home_page.title.replace("Adamawa Governor", "Gubernatorial Candidate")
            updated = True
            
        # Notification
        if "re-elect" in home_page.notification_text.lower():
            home_page.notification_text = re.sub(r"re-elect", "elect", home_page.notification_text, flags=re.IGNORECASE)
            updated = True

        # Hero Description
        if "Emnamu Foundation President" not in home_page.hero_description:
            # Simple prepend or replace name
            if "Dr. Emmanuel N. Musa" in home_page.hero_description:
                home_page.hero_description = home_page.hero_description.replace("Dr. Emmanuel N. Musa", "Emnamu Foundation President Dr. Emmanuel N. Musa")
                updated = True
        
        if updated:
            home_page.save()
            print("Database record updated.")
        else:
            print("No database changes needed.")

if __name__ == "__main__":
    main()
