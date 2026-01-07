import re
from bs4 import BeautifulSoup

file_path = r'c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\templates\core\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

# 1. Remove the old "Join #Team..." section if it exists
# Target id="brxe-mucjuw"
old_section = soup.find('div', id='brxe-mucjuw')
if old_section:
    old_section.decompose()

# Also aggressively look for any "Join #Team" headers to avoid duplication
for h3 in soup.find_all('h3'):
    if h3.string and 'Join #Team' in h3.string:
        # Find the top-level template wrapper
        parent = h3.find_parent('div', class_='brxe-template')
        if parent:
            parent.decompose()

# 2. Define the new section HTML
new_html = """
<div class="brxe-template" id="brxe-professional-join">
    <section class="brxe-section" style="padding: 0; background-color: #002855;">
        <div class="brxe-container" style="display: flex; flex-wrap: wrap; width: 100%; max-width: 100%; padding: 0; margin: 0;">
            <!-- Left Column: Join Form -->
            <div class="brxe-block" style="background-color: #002855; color: white; padding: 5rem 5%; flex: 1 1 500px; display: flex; flex-direction: column; justify-content: center;">
                <h2 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 2rem; color: white; line-height: 1.1;">Join #TeamJB</h2>
                <form action="{% url 'signup' %}" method="POST" style="display: grid; gap: 1rem;">
                    {% csrf_token %}
                    <input type="hidden" name="source" value="homepage_new_section">
                    
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <div style="flex: 1 1 200px;">
                            <label for="first_name_new" style="display: block; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 1px; color: white;">First Name</label>
                            <input type="text" id="first_name_new" name="first_name" required style="width: 100%; padding: 0.75rem; border: none; background-color: white; color: black;">
                        </div>
                        <div style="flex: 1 1 200px;">
                            <label for="last_name_new" style="display: block; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 1px; color: white;">Last Name</label>
                            <input type="text" id="last_name_new" name="last_name" required style="width: 100%; padding: 0.75rem; border: none; background-color: white; color: black;">
                        </div>
                    </div>

                    <div>
                        <label for="postal_code_new" style="display: block; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 1px; color: white;">Postal Code</label>
                        <input type="text" id="postal_code_new" name="postal_code" style="width: 100%; padding: 0.75rem; border: none; background-color: white; color: black;">
                    </div>

                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <div style="flex: 1 1 200px;">
                            <label for="email_new" style="display: block; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 1px; color: white;">Email</label>
                            <input type="email" id="email_new" name="email" placeholder="email@email.com" required style="width: 100%; padding: 0.75rem; border: none; background-color: white; color: #333;">
                        </div>
                        <div style="flex: 1 1 200px;">
                            <label for="mobile_phone_new" style="display: block; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 1px; color: white;">Mobile Phone</label>
                            <div style="display: flex; align-items: center; background: white; padding: 0;">
                                <img src="https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg" style="width: 25px; margin: 0 0.5rem;">
                                <span style="color: #333; margin-right: 0.5rem;">▼</span>
                                <input type="tel" id="mobile_phone_new" name="mobile_phone" style="width: 100%; padding: 0.75rem 0; border: none; outline: none; background-color: white; color: black;">
                            </div>
                        </div>
                    </div>

                    <button type="submit" style="background-color: #F7D54A; color: #002855; border: none; padding: 1rem; font-weight: 900; letter-spacing: 1px; text-transform: uppercase; margin-top: 1rem; cursor: pointer; width: 100%; font-size: 1rem;">Sign Up</button>
                </form>
            </div>

            <!-- Right Column: Connect & Action -->
            <div class="brxe-block" style="display: flex; flex-direction: column; flex: 1 1 500px;">
                <!-- Top: Get Connected -->
                <div style="background-color: #0099FF; padding: 5rem; color: white; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                    <h2 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 1.5rem; color: white; line-height: 1.1;">Get Connected</h2>
                    <div style="display: flex; gap: 1.5rem; font-size: 2rem; flex-wrap: wrap;">
                        <a href="#" style="color: white; text-decoration: none;"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" style="color: white; text-decoration: none;"><i class="fab fa-x-twitter"></i></a>
                        <a href="#" style="color: white; text-decoration: none;"><i class="fab fa-instagram"></i></a>
                        <a href="#" style="color: white; text-decoration: none;"><i class="fab fa-youtube"></i></a>
                        <a href="#" style="color: white; text-decoration: none;"><i class="fab fa-threads"></i></a>
                        <a href="#" style="color: white; text-decoration: none;"><i class="fab fa-tiktok"></i></a>
                    </div>
                </div>

                <!-- Bottom: Take Action -->
                <div style="background-color: #F7D54A; padding: 5rem; color: #002855; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                    <h2 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 1.5rem; color: #002855; line-height: 1.1;">Take Action</h2>
                    <a href="#" style="background-color: #0099FF; color: white; padding: 1rem 2.5rem; font-weight: 700; text-transform: uppercase; text-decoration: none; width: fit-content; font-size: 1rem; border: none;">Learn More</a>
                </div>
            </div>
        </div>
    </section>
</div>
"""

# Parse the new HTML
new_soup = BeautifulSoup(new_html, 'html.parser')

# 3. Append to the correct location
# We want it before {% endblock %}
# Find the text node containing "{% endblock %}"
# Note: BS4 might parse Django tags as text strings.
# We look for the last occurrence if possible, or just the one in the main scope.
# The structure is {% block content %} ... {% endblock %}
# Since we parsed the whole file, {% endblock %} should be a string at the end of the soup (or near it).

found = False
for string in soup.find_all(string=True):
    if '{% endblock %}' in string:
        # We found it. Insert before this string.
        # But `string` is immutable in some contexts, let's use insert_before on the NavigableString
        string.insert_before(new_soup)
        found = True
        break

if not found:
    # Fallback: Just append to the soup.
    # But we need to make sure {% endblock %} is there.
    # If we couldn't find it, maybe it's not there?
    # Let's just append it.
    soup.append(new_soup)
    # And maybe append {% endblock %} if we suspect it's missing?
    # No, safer to just append the content.

# 4. Save
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Professional section added successfully.")
