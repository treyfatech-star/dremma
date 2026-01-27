import sys
with open('deps_status.txt', 'w') as f:
    try:
        import requests
        f.write("requests: installed\n")
    except ImportError:
        f.write("requests: missing\n")
    
    try:
        import bs4
        f.write("bs4: installed\n")
    except ImportError:
        f.write("bs4: missing\n")
