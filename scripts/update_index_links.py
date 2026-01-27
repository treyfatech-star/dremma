import os

file_path = 'core/templates/core/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('https://dremmanuelnmusa.com/meet-dr-emmanuel-n-musa/', "{% url 'meet_candidate' %}"),
    # Add other potential links if they exist in the body
    ('https://jbpritzker.com/accomplishments/', "{% url 'accomplishments' %}"),
    ('https://jbpritzker.com/meet-christian-mitchell/', "{% url 'meet_running_mate' %}"),
    ('https://jbpritzker.com/news-updates/', "{% url 'news_list' %}"),
    ("{% static 'core/at.js' %}", "/static/core/at.js"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated links in index.html")
