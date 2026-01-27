import re

FILE_PATH = r"core\templates\core\index.html"

def final_cleanup():
    print(f"Reading {FILE_PATH}...")
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(FILE_PATH, 'r', encoding='latin-1') as f:
            content = f.read()

    # Twitter handle fix
    new_content = content.replace('content="@jbpritzker"', 'content="@dremmanuelnmusa"')
    
    # Home page link fix (exact match to avoid breaking assets)
    new_content = new_content.replace('href="https://jbpritzker.com/"', 'href="/"')
    new_content = new_content.replace('href="https://jbpritzker.com"', 'href="/"')
    
    # Canonical/OG URL fix
    new_content = new_content.replace('content="https://jbpritzker.com/"', 'content="/"')
    
    if new_content != content:
        print("Writing final cleanup changes...")
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Cleanup done.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    final_cleanup()
