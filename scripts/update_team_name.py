import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campaign_site.settings')
django.setup()

from core.models import HomePage

def update_team_name():
    home_page = HomePage.objects.first()
    if not home_page:
        print("No HomePage found.")
        return

    updated = False

    # Check all text fields for "TeamJB"
    for field in home_page._meta.fields:
        if field.get_internal_type() in ['CharField', 'TextField']:
            value = getattr(home_page, field.name)
            if value and isinstance(value, str) and "TeamJB" in value:
                print(f"Found 'TeamJB' in {field.name}: '{value}'")
                new_value = value.replace("TeamJB", "TeamDr.Emmanuel")
                setattr(home_page, field.name, new_value)
                updated = True
                print(f"Updated {field.name} to: '{new_value}'")

    if updated:
        home_page.save()
        print("HomePage updated successfully.")
    else:
        print("No remaining 'TeamJB' found in HomePage.")

if __name__ == "__main__":
    update_team_name()
