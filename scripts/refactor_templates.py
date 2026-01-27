import os

file_path = 'core/templates/core/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split content
# We look for <main id="brx-content"> and </main>
start_marker = '<main id="brx-content">'
end_marker = '</main>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find markers")
    exit(1)

# Header includes the opening <main> tag to match the structure, 
# OR we put the <main> tag in base.html and content block inside it.
# Let's put <main> in base.html.

header_part = content[:start_idx + len(start_marker)]
index_content = content[start_idx + len(start_marker):end_idx]
footer_part = content[end_idx:]

# Create base.html
base_content = f"""{header_part}
    {{% block content %}}{{ % endblock %}}
{footer_part}"""

# Create new index.html
new_index_content = f"""{{% extends 'core/base.html' %}}

{{% block content %}}
{index_content}
{{% endblock %}}"""

# Write files
with open('core/templates/core/base.html', 'w', encoding='utf-8') as f:
    f.write(base_content)

with open('core/templates/core/index.html', 'w', encoding='utf-8') as f:
    f.write(new_index_content)

print("Created base.html and updated index.html")
