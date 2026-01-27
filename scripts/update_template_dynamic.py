import os

BASE_DIR = os.getcwd()
TEMPLATE_FILE = os.path.join(BASE_DIR, 'core', 'templates', 'core', 'index.html')

with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Title
content = content.replace(
    '<title>JB for Governor - Official Campaign Website of Illinois Governor JB Pritzker</title>',
    '<title>{{ home_page.title }}</title>'
)

# Replace Notification Bar
# Searching for the specific link and text
content = content.replace(
    '<a href="https://action.jbpritzker.com/a/teamjb">Join the team to re-elect JB</a>',
    '<a href="{{ home_page.notification_url }}">{{ home_page.notification_text }}</a>'
)

# Replace Hero Title
# Note: The original has <em>Every</em>. We'll assume the user puts that in the admin field if they want it.
# We need to match the exact string in the file.
content = content.replace(
    '<h2 id="brxe-dnwxnf" class="brxe-heading">A Leader for<em>Every</em> Illinoisan</h2>',
    '<h2 id="brxe-dnwxnf" class="brxe-heading">{{ home_page.hero_title|safe }}</h2>'
)

# Replace Hero Description
content = content.replace(
    'No matter where you live in Illinois or what your background is, JB has been hard at work to ensure that you, your family, and your community will thrive.',
    '{{ home_page.hero_description }}'
)

# Replace Hero Button
# This is a bit more complex, let's do it in two parts
content = content.replace(
    'href="https://jbpritzker.com/meet-jb-pritzker/"',
    'href="{{ home_page.hero_button_url }}"'
)

content = content.replace(
    '<span class="text">Learn More About JB</span>',
    '<span class="text">{{ home_page.hero_button_text }}</span>'
)

with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {TEMPLATE_FILE} with dynamic variables")
