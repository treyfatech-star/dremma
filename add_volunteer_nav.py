
import os

base_path = r'c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\templates\core\base.html'

with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the Volunteer list item
volunteer_li = '<li class="menu-item menu-item-type-post_type menu-item-object-page bricks-menu-item"><a href="{% url \'volunteer\' %}">Volunteer</a></li>'

# 1. Update Main Menu (#menu-header)
# Look for News & Updates and append Volunteer after it
news_item_main = '<li id="menu-item-174" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-174 bricks-menu-item"><a href="{% url \'news_list\' %}">News &amp; Updates</a></li>'
if news_item_main in content:
    content = content.replace(news_item_main, news_item_main + '\n' + volunteer_li)
else:
    print("Could not find Main Menu News item")

# 2. Update Mobile Menu (#menu-header-1) and Offcanvas (#menu-header-2)
# These share the same HTML structure for the News item
news_item_mobile = '<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-174 bricks-menu-item"><a href="{% url \'news_list\' %}">News &amp; Updates</a></li>'

# We replace all occurrences (should be 2: mobile and offcanvas)
if content.count(news_item_mobile) >= 2:
    content = content.replace(news_item_mobile, news_item_mobile + '\n' + volunteer_li)
else:
    print(f"Found {content.count(news_item_mobile)} occurrences of Mobile/Offcanvas News item (expected at least 2)")

# 3. Update Footer Menu (#menu-footer-primary)
# Footer has a different ID
news_item_footer = '<li id="menu-item-836" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-836 bricks-menu-item"><a href="{% url \'news_list\' %}">News &amp; Updates</a></li>'
if news_item_footer in content:
    content = content.replace(news_item_footer, news_item_footer + '\n' + volunteer_li)
else:
    print("Could not find Footer Menu News item")

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating base.html")
