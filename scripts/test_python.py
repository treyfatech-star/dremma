import sys
import os

print("Python version:", sys.version)

try:
    import requests
    print("requests is available")
except ImportError:
    print("requests is NOT available")

try:
    import bs4
    print("bs4 is available")
except ImportError:
    print("bs4 is NOT available")

try:
    # Try to connect to the site
    import urllib.request
    with urllib.request.urlopen('https://jbpritzker.com/', timeout=5) as response:
        print("Connection to jbpritzker.com successful, status:", response.status)
except Exception as e:
    print("Connection failed:", e)

with open('test_output.txt', 'w') as f:
    f.write("Test script ran successfully.\n")
