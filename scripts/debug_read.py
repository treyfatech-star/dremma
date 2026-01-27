import os

path = r"c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\templates\core\index.html"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if "adamawa" in line.lower():
            print(f"ADAMAWA found at {i+1}: {line.strip()}")
        if "illinois" in line.lower():
            print(f"ILLINOIS found at {i+1}: {line.strip()}")
