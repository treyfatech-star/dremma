import os
import requests
import re

BASE_URL = "https://jbpritzker.com/wp-content/themes/bricks/assets/fonts/"
LOCAL_FONTS_DIR = r"c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\static\core\fonts"
CSS_DIR = r"c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\static\core"

FONTS_TO_DOWNLOAD = [
    "ionicons/ionicons.woff2",
    "ionicons/ionicons.woff",
    "ionicons/ionicons.ttf",
    "fontawesome/fa-brands-400.woff2",
    "fontawesome/fa-brands-400.ttf",
    "fontawesome/fa-solid-900.woff2",
    "fontawesome/fa-solid-900.ttf",
    "fontawesome/fa-regular-400.woff2",
    "fontawesome/fa-regular-400.ttf"
]

def download_fonts():
    if not os.path.exists(LOCAL_FONTS_DIR):
        os.makedirs(LOCAL_FONTS_DIR)

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    for font_path in FONTS_TO_DOWNLOAD:
        url = BASE_URL + font_path
        local_path = os.path.join(LOCAL_FONTS_DIR, font_path.replace("/", os.sep))

        # Create subdir if needed
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        print(f"Downloading {url} to {local_path}...")
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(r.content)
                print("Success.")
            else:
                print(f"Failed: {r.status_code}")
        except Exception as e:
            print(f"Error: {e}")

def fix_css_paths():
    print("Fixing CSS paths...")
    for filename in os.listdir(CSS_DIR):
        if filename.endswith(".css"):
            file_path = os.path.join(CSS_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace ../../fonts with fonts
            if "../../fonts" in content:
                print(f"Fixing {filename}...")
                new_content = content.replace("../../fonts", "fonts")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("Fixed.")

if __name__ == "__main__":
    download_fonts()
    fix_css_paths()
