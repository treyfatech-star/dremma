import shutil
import os

BASE_DIR = os.getcwd()
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
STATIC_CORE_DIR = os.path.join(BASE_DIR, 'core', 'static', 'core')

# Ensure destination exists
os.makedirs(STATIC_CORE_DIR, exist_ok=True)

if os.path.exists(ASSETS_DIR):
    print(f"Moving files from {ASSETS_DIR} to {STATIC_CORE_DIR}")
    for item in os.listdir(ASSETS_DIR):
        src = os.path.join(ASSETS_DIR, item)
        dst = os.path.join(STATIC_CORE_DIR, item)
        
        if os.path.exists(dst):
            print(f"Skipping {item}, already exists in destination")
            continue
            
        try:
            shutil.move(src, dst)
            print(f"Moved {item}")
        except Exception as e:
            print(f"Error moving {item}: {e}")
    
    # Try to remove assets dir if empty
    try:
        os.rmdir(ASSETS_DIR)
        print("Removed empty assets directory")
    except OSError:
        print("Assets directory not empty, could not remove")
else:
    print("Assets directory does not exist (already moved?)")

# Check index.html
TEMPLATE_INDEX = os.path.join(BASE_DIR, 'core', 'templates', 'core', 'index.html')
ROOT_INDEX = os.path.join(BASE_DIR, 'index.html')

if os.path.exists(TEMPLATE_INDEX):
    print(f"Template index.html exists at {TEMPLATE_INDEX}")
else:
    print(f"Template index.html MISSING at {TEMPLATE_INDEX}")
    if os.path.exists(ROOT_INDEX):
        print("Found index.html in root, moving it...")
        # We should probably run the migration logic again if it's here
        # But let's just move it for now to be safe
        os.makedirs(os.path.dirname(TEMPLATE_INDEX), exist_ok=True)
        shutil.copy(ROOT_INDEX, TEMPLATE_INDEX)
        print("Copied root index.html to template dir")

