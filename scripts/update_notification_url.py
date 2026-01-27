import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campaign_site.settings')
django.setup()

from core.models import HomePage

try:
    home_page = HomePage.objects.first()
    if home_page:
        home_page.notification_url = "/signup/"
        home_page.save()
        print("Updated HomePage notification_url to /signup/")
    else:
        print("No HomePage object found.")
except Exception as e:
    print(f"Error updating database: {e}")
