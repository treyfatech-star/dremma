import os
import re

FILE_PATH = r"core\templates\core\index.html"

def refine_file():
    print(f"Reading {FILE_PATH}...")
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(FILE_PATH, 'r', encoding='latin-1') as f:
            content = f.read()

    # Social Media Replacements
    replacements = [
        (r'facebook\.com/jbpritzker', 'facebook.com/dremmanuelnmusa'),
        (r'x\.com/jbpritzker', 'x.com/dremmanuelnmusa'),
        (r'instagram\.com/jbpritzker', 'instagram.com/dremmanuelnmusa'),
        (r'youtube\.com/@jbpritzker', 'youtube.com/@dremmanuelnmusa'),
        (r'threads\.net/@jbpritzker', 'threads.net/@dremmanuelnmusa'),
        (r'bsky\.app/profile/jbpritzker', 'bsky.app/profile/dremmanuelnmusa'),
        (r'tiktok\.com/@teamjb_hq', 'tiktok.com/@teamdremmanuelnmusa_hq'),
        (r'twitter\.com/jbpritzker', 'twitter.com/dremmanuelnmusa'),
        (r'twitter:site" content="@jbpritzker', 'twitter:site" content="@dremmanuelnmusa'),
        (r'action\.jbpritzker\.com/a/teamjb', 'action.dremmanuelnmusa.com/a/teamdremmanuelnmusa'), # Fake but consistent
        (r'jbpritzker\.com/meet-dr-emmanuel-n-musa', 'dremmanuelnmusa.com/meet-dr-emmanuel-n-musa'), # Just to change the visual link if visible, or internal
    ]

    new_content = content
    for old_re, new_str in replacements:
        new_content = re.sub(old_re, new_str, new_content, flags=re.IGNORECASE)

    # Specific cleanups
    # Replace the main site URL with a placeholder or local reference where appropriate, 
    # but be careful not to break asset loading if assets are still hotlinked.
    # Assets usually match wp-content.
    # We want to change href="https://jbpritzker.com/" to href="/"
    
    # Use regex to avoid replacing wp-content URLs
    # Match href="https://jbpritzker.com/..." but NOT wp-content
    
    # Simple strategy: Replace "https://jbpritzker.com/" with "/" only if it's exactly that or followed by something that isn't wp-content
    # But for now, let's stick to the social media and obvious name handles.
    
    if new_content != content:
        print("Writing changes...")
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Refinements applied.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    refine_file()
