import os
import re
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campaign_site.settings')
django.setup()

from core.models import HomePage

FILE_PATH = r"c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\templates\core\index.html"

def update_file():
    print(f"Reading {FILE_PATH}...")
    if not os.path.exists(FILE_PATH):
        print("File does not exist!")
        return

    # Read with fallback encoding
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(FILE_PATH, 'r', encoding='latin-1') as f:
            content = f.read()

    # Replacements
    # 1. JB Pritzker (case insensitive)
    # Use regex for case insensitive replacement of specific phrase
    new_content = re.sub(r'jb\s+pritzker', 'Dr. Emmanuel N. Musa', content, flags=re.IGNORECASE)
    
    # 2. JB (standalone, or followed/preceded by space/punctuation)
    # We want to avoid replacing inside URLs if possible, but the request is broad.
    # However, replacing "jb" in "jbpritzker.com" might break links if they are functional.
    # But usually we want to change the displayed text.
    # Let's replace "JB" when it is likely a name.
    
    # Replace "JB" (Case sensitive)
    # We replace "JB" not followed by "Pritzker" (since we already handled that)
    # And not part of a URL like "jbpritzker.com" -> "jbpritzker" is "jb" + "pritzker".
    # Since we already replaced "JB Pritzker", "jbpritzker" remains as "jbpritzker".
    # If we replace "JB" globally, "jbpritzker.com" -> "Dr. Emmanuel N. MusaPritzker.com" (bad).
    # So we should be careful with "JB".
    
    # Strategy: Replace "JB" only when it's a whole word.
    # \bJB\b
    new_content = re.sub(r'\bJB\b', 'Dr. Emmanuel N. Musa', new_content)
    
    # Also "jb" (lowercase) as whole word? "jb" might be used in some contexts?
    # The user said "jb Pritzker".
    # I'll replace "jb" as whole word too, but maybe only if it looks like a name?
    # In "jbpritzker.com", "jbpritzker" is one word. So \bjb\b won't match.
    # So \bjb\b is safe for "jbpritzker.com".
    # But "meet-jb-pritzker" -> "jb" is a word there (separated by hyphens).
    # "meet-jb-pritzker" -> "meet-Dr. Emmanuel N. Musa-pritzker" (if we replaced JB Pritzker first? No, "jb-pritzker" has a hyphen).
    # My previous regex `jb\s+pritzker` handles spaces. It won't match "jb-pritzker".
    
    # Let's handle "jb-pritzker" specifically?
    # "meet-jb-pritzker" -> "meet-dr-emmanuel-n-musa"
    new_content = new_content.replace("jb-pritzker", "dr-emmanuel-n-musa")
    new_content = new_content.replace("JB-Pritzker", "Dr-Emmanuel-N-Musa")
    
    # Now replace "JB" whole word
    new_content = re.sub(r'\bJB\b', 'Dr. Emmanuel N. Musa', new_content)
    
    # Replace "Pritzker" if it remains?
    # "Governor Pritzker" -> "Governor Dr. Emmanuel N. Musa"
    # "Pritzker" -> "Dr. Emmanuel N. Musa"
    # But again, avoid URLs "jbpritzker.com".
    # \bPritzker\b
    new_content = re.sub(r'\bPritzker\b', 'Dr. Emmanuel N. Musa', new_content)
    
    # Fix potential double "Dr. Emmanuel N. Musa Dr. Emmanuel N. Musa" if "JB Pritzker" was replaced by two separate rules?
    # No, I did `jb\s+pritzker` first.
    # If I have "JB Pritzker", `jb\s+pritzker` matches it -> "Dr. Emmanuel N. Musa".
    # If I have "JB-Pritzker", explicit replace handles it.
    # If I have "JB", `\bJB\b` handles it.
    # If I have "Pritzker", `\bPritzker\b` handles it.
    
    print("Writing changes...")
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("File updated.")

def update_db():
    print("Updating Database...")
    try:
        home_page = HomePage.objects.first()
        if home_page:
            # Helper to replace text
            def replace_text(text):
                if not text: return text
                t = re.sub(r'jb\s+pritzker', 'Dr. Emmanuel N. Musa', text, flags=re.IGNORECASE)
                t = t.replace("jb-pritzker", "dr-emmanuel-n-musa")
                t = re.sub(r'\bJB\b', 'Dr. Emmanuel N. Musa', t)
                t = re.sub(r'\bPritzker\b', 'Dr. Emmanuel N. Musa', t)
                return t

            home_page.title = replace_text(home_page.title)
            home_page.notification_text = replace_text(home_page.notification_text)
            home_page.hero_title = replace_text(home_page.hero_title)
            home_page.hero_description = replace_text(home_page.hero_description)
            home_page.hero_button_text = replace_text(home_page.hero_button_text)
            # Don't change URLs in DB unless necessary? 
            # hero_button_url="https://jbpritzker.com/meet-jb-pritzker/"
            # We can update the URL text if it's visible, but it's a URL field.
            # I'll leave URLs alone in DB to ensure they still work (pointing to original site if needed), 
            # OR update them if they are internal?
            # They point to jbpritzker.com.
            # If I change the URL to something invalid, it breaks.
            # But the user said "CHANGE jb Pritzker to Dr. Emmanuel N. Musa".
            # I'll change the text fields.
            
            home_page.save()
            print("Database updated.")
        else:
            print("No HomePage object found.")
    except Exception as e:
        print(f"Error updating DB: {e}")

if __name__ == "__main__":
    update_file()
    update_db()
