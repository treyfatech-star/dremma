import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campaign_site.settings')
django.setup()

from core.models import HomePage

# Update Database
try:
    home_page = HomePage.objects.first()
    if home_page:
        home_page.title = home_page.title.replace("Illinois", "Adamawa")
        home_page.hero_title = home_page.hero_title.replace("Illinoisan", "Adamawaian").replace("Illinois", "Adamawa")
        home_page.hero_description = home_page.hero_description.replace("Illinois", "Adamawa")
        home_page.save()
        print("Updated HomePage object in database.")
    else:
        print("No HomePage object found.")
except Exception as e:
    print(f"Error updating database: {e}")

# Update Template
TEMPLATE_FILE = os.path.join(os.getcwd(), 'core', 'templates', 'core', 'index.html')

with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Illinoisan first to avoid partial match issues
content = content.replace("Illinoisan", "Adamawaian")
content = content.replace("Illinois", "Adamawa")

print(f"Writing to {TEMPLATE_FILE}")
with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {TEMPLATE_FILE} with Adamawa replacements")
