import os
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser
import re
import sys
import time

LOG_FILE = 'clone_debug.log'

def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{time.ctime()}: {msg}\n")
    print(msg)

TARGET_URL = 'https://www.jbpritzker.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
}

class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'link' and 'href' in attrs_dict:
            rel = attrs_dict.get('rel', '').lower()
            if 'stylesheet' in rel or 'icon' in rel:
                self.resources.append(attrs_dict['href'])
        elif tag == 'script' and 'src' in attrs_dict:
            self.resources.append(attrs_dict['src'])
        elif tag == 'img' and 'src' in attrs_dict:
            self.resources.append(attrs_dict['src'])

def download_resource(url, folder):
    if not url: return None
    if url.startswith('//'):
        full_url = 'https:' + url
    elif url.startswith('http'):
        full_url = url
    else:
        full_url = urllib.parse.urljoin(TARGET_URL, url)

    try:
        parsed = urllib.parse.urlparse(full_url)
        path_filename = os.path.basename(parsed.path)
        if not path_filename:
            path_filename = 'resource_' + str(abs(hash(full_url)))

        # simple sanitization
        path_filename = re.sub(r'[<>:"/\\|?*]', '_', path_filename)

        local_path = os.path.join(folder, path_filename)

        if not os.path.exists(local_path):
            log(f"Downloading {full_url} to {local_path}")
            req = urllib.request.Request(full_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as r:
                content = r.read()
                with open(local_path, 'wb') as f:
                    f.write(content)

        return f'{folder}/{path_filename}'
    except Exception as e:
        log(f"Failed to download {full_url}: {e}")
        return url

def main():
    log("Script started")
    try:
        log(f"Fetching {TARGET_URL}...")
        req = urllib.request.Request(TARGET_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            html_content = r.read().decode('utf-8', errors='ignore')
        log("Main page fetched successfully")
    except Exception as e:
        log(f"Failed to fetch main page: {e}")
        return

    try:
        if not os.path.exists('assets'):
            os.makedirs('assets')
            log("Created assets directory")
    except Exception as e:
        log(f"Failed to create directory: {e}")
        return

    parser = ResourceParser()
    parser.feed(html_content)

    unique_resources = set(parser.resources)
    log(f"Found {len(unique_resources)} resources to download")

    new_html = html_content

    for url in unique_resources:
        local_path = download_resource(url, 'assets')
        if local_path and local_path != url:
            new_html = new_html.replace(f'"{url}"', f'"{local_path}"')
            new_html = new_html.replace(f"'{url}'", f"'{local_path}'")

    try:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        log("index.html written successfully")
    except Exception as e:
        log(f"Failed to write index.html: {e}")

    log("Script finished")

if __name__ == "__main__":
    main()
