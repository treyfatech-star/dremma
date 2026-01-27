import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campaign_site.settings')
django.setup()

from core.models import HomePage

def replace_in_file(file_path):
    print(f"Processing {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"Read {len(content)} chars from {file_path}")
        print(f"First 100 chars: {content[:100]}")
        if "Illinois" in content:
            print("Found 'Illinois' in content")
        else:
            print("Did NOT find 'Illinois' in content")

        # Replace Illinoisan first to avoid partial match issues
        new_content = content.replace("Illinoisan", "Adamawaian")
        new_content = new_content.replace("Illinois", "Adamawa")

        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes needed for {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def update_db():
    print("Updating Database...")
    try:
        # Get all HomePage objects
        home_pages = HomePage.objects.all()

        if not home_pages.exists():
            print("No HomePage objects found. Creating one...")
            HomePage.objects.create(
                title="JB for Governor - Official Campaign Website of Adamawa Governor JB Pritzker",
                notification_text="Join the team to re-elect JB",
                notification_url="https://action.jbpritzker.com/a/teamjb",
                hero_title="A Leader for Every Adamawaian",
                hero_description="No matter where you live in Adamawa or what your background is, JB has been hard at work to ensure that you, your family, and your community will thrive.",
                hero_button_text="Learn More About JB",
                hero_button_url="https://jbpritzker.com/meet-jb-pritzker/"
            )
            print("Created new HomePage object.")
        else:
            for hp in home_pages:
                updated = False
                if "Illinois" in hp.title:
                    hp.title = hp.title.replace("Illinois", "Adamawa")
                    updated = True
                if "Illinois" in hp.hero_title:
                    hp.hero_title = hp.hero_title.replace("Illinoisan", "Adamawaian").replace("Illinois", "Adamawa")
                    updated = True
                if "Illinois" in hp.hero_description:
                    hp.hero_description = hp.hero_description.replace("Illinois", "Adamawa")
                    updated = True

                # Also force update to defaults if they match the old default exactly,
                # just in case the replace missed something or logic above is insufficient
                if hp.hero_title == "A Leader for Every Illinoisan":
                     hp.hero_title = "A Leader for Every Adamawaian"
                     updated = True

                if updated:
                    hp.save()
                    print(f"Updated HomePage object ID {hp.id}")
                else:
                    print(f"HomePage object ID {hp.id} already up to date.")

    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == "__main__":
    base_dir = os.getcwd()

    # 1. Update Template
    template_path = os.path.join(base_dir, 'core', 'templates', 'core', 'index.html')
    replace_in_file(template_path)

    # 2. Update Migration
    migration_path = os.path.join(base_dir, 'core', 'migrations', '0001_initial.py')
    replace_in_file(migration_path)

    # 3. Update Database
    update_db()

    print("Done.")
