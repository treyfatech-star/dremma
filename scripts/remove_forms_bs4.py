import os
from bs4 import BeautifulSoup
import re

file_path = r'c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\templates\core\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

# 1. Remove NGP forms (class="ngp-form") and associated scripts
ngp_forms = soup.find_all('div', class_='ngp-form')
for form in ngp_forms:
    # Remove the form div
    parent = form.parent
    # Check if parent is just a wrapper like "brxe-gwaxbj"
    if parent and parent.get('id') == 'brxe-gwaxbj':
        parent.decompose()
    else:
        # Just remove the form itself and previous siblings if they are NGP scripts
        # This is harder with BS4 navigation sometimes, but let's try to remove the form first
        form.decompose()

# Also remove specific NGP scripts if they are left dangling
# Search for scripts with src containing 'everyaction'
scripts = soup.find_all('script', src=re.compile(r'everyaction\.com'))
for script in scripts:
    script.decompose()
    
# Remove CSS links for everyaction
links = soup.find_all('link', href=re.compile(r'everyaction\.com'))
for link in links:
    link.decompose()

# 2. Remove the manual "Join the Team" form block
# It has class "brxe-block gd-action"
manual_blocks = soup.find_all('div', class_='gd-action')
for block in manual_blocks:
    block.decompose()

# 3. Remove the lower "Join #TeamJB" section
# Find the h3 with text "Join #TeamJB" and remove its parent section
headers = soup.find_all('h3', string=re.compile(r'Join #TeamJB', re.I))
for header in headers:
    # The header is inside a div, which is inside a container, which is inside a section
    # Let's traverse up to find the section
    section = header.find_parent('section')
    if section:
        # Check if it wraps the whole template div or just the section
        # The structure is <div class="brxe-template"><section ...>
        # We can remove the section or the wrapping div if it's the only thing
        # Let's remove the section
        section.decompose()

# 4. Just to be safe, find ANY remaining <form> tags and remove them or their containers
forms = soup.find_all('form')
for form in forms:
    # If the form is still there (meaning it wasn't caught by above logic)
    # Remove it.
    # Check if it's inside a section we might want to keep? 
    # User said "remove all the forms".
    # I'll decompose the form tag itself.
    form.decompose()

# Save the file
# Note: BS4 might prettify or change formatting. 
# Since the original file was minified/long lines, we should be careful.
# But for now, correctness of removal is more important.
# We'll use str(soup) which won't prettify unless we ask.
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Forms removed successfully.")
