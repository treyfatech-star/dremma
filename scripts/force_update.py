import os

FILE_PATH = r"c:\Users\HP ELITEBOOK 840- G3\Desktop\webaudit\campiagn\core\templates\core\index.html"

def force_update():
    print(f"Reading {FILE_PATH}...")
    if not os.path.exists(FILE_PATH):
        print("File does not exist!")
        return

    with open(FILE_PATH, 'rb') as f:
        content_bytes = f.read()
    
    try:
        content = content_bytes.decode('utf-8')
        print("Decoded as UTF-8")
    except UnicodeDecodeError:
        content = content_bytes.decode('latin-1')
        print("Decoded as Latin-1")
        
    print(f"Content length: {len(content)}")
    print(f"First 100 chars: {repr(content[:100])}")
    
    count_illinois = content.count("Illinois")
    count_illinoisan = content.count("Illinoisan")
    print(f"Found 'Illinois': {count_illinois}")
    print(f"Found 'Illinoisan': {count_illinoisan}")
    
    if count_illinois == 0 and count_illinoisan == 0:
        print("No replacements needed.")
        return

    new_content = content.replace("Illinoisan", "Adamawaian")
    new_content = new_content.replace("Illinois", "Adamawa")
    
    print("Writing changes...")
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Done writing.")

if __name__ == "__main__":
    force_update()
