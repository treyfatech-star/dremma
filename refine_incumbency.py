import os
import re
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campaign_site.settings')
django.setup()

from core.models import HomePage

FILE_PATH = r"core\templates\core\index.html"

def refine_content():
    print(f"Reading {FILE_PATH}...")
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(FILE_PATH, 'r', encoding='latin-1') as f:
            content = f.read()

    new_content = content
    
    replacements = [
        # Incumbency -> Aspirant/Foundation narrative
        (r"Under Dr\. Emmanuel N\. Musa’s leadership, our state is one of the best", 
         "Through the Emnamu Foundation, Dr. Emmanuel N. Musa has demonstrated the leadership to make our state one of the best"),
        
        (r"Adamawa Is Heading In The Right Direction", "A Vision to Lead Adamawa Forward"),
        
        (r"He’s creating jobs, balancing our budget, and protecting our freedoms", 
         "He will create jobs, balance our budget, and protect our freedoms"),
         
         (r"Discover how Dr\. Emmanuel N\. Musa is leading the way", 
          "Discover how Dr. Emmanuel N. Musa will lead the way"),
          
         (r"Learn More About Adamawa’ Progress", "Learn More About Dr. Musa's Vision"),
    ]

    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)

    if new_content != content:
        print("Writing refinements to index.html...")
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Refinements applied.")
    else:
        print("No further refinements needed.")

if __name__ == "__main__":
    refine_content()
