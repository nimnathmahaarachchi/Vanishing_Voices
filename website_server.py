
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit
import argparse
import json
import mimetypes

from animals.animal_information import ANIMALS
from check_animal_populations import get_populations

ROOT = Path(__file__).resolve().parent  # ROOT is this project's folder, even if the terminal was opened somewhere else.
IMAGES = (ROOT / 'images').resolve()  # The full path to the folder holding the animal photographs.
# Allow only the public pages and assets.
PAGE_FILES = {'website-layout/main-page.html', 'website-layout/sources-page.html', 'website-layout/about-page.html'}
PAGE_FILES.update('animals/' + animal['slug'] + '-page.html' for animal in ANIMALS)  # Add one allowed page address for each animal's slug, e.g. tiger-page.html.
OTHER_FILES = {'website-layout/website-style.css', 'website-layout/website-actions.js', 'website-layout/leaf-icon.svg'}
MAPS = (ROOT / 'maps').resolve()


class AnimalWebsiteHandler(BaseHTTPRequestHandler):  # This handles the browser's requests for pages, images, and population data.
    server_version = 'VanishingVoices/1.0'

    def send_bytes(self, body, content_type, status=200, cache='no-cache', head=False):
        self.send_response(status)  # The HTTP result: 200 means success, 404 means the address was not found.
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))  # Tell the browser how many bytes are in the response body.
        self.send_header('Cache-Control', cache)
        self.send_header('X-Content-Type-Options', 'nosniff')  # Ask the browser to use the declared file type instead of guessing it.
        self.end_headers()
        if not head:  # HEAD requests get the headers only; GET requests also get the content.
            self.wfile.write(body)

    # Validate the species before starting a source check.
    def population_response(self, query, head):
        params = parse_qs(query)  # Turn species=tiger&refresh=1 into a dictionary of lists.
        slug = params.get('species', [None])[0]  # Take the requested animal name; None means check all species.
        force = params.get('refresh', ['0'])[0] == '1'  # refresh=1 asks for a new check, subject to the cache's minimum wait.
        if slug and slug not in {animal['slug'] for animal in ANIMALS}:
            self.send_bytes(b'{"error":"Unknown species"}', 'application/json', 400, head=head)
            return
        data = get_populations(slug, force) if not head else {'records': []}
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')  # Convert the Python dictionary to JSON text, then UTF-8 bytes for the browser.
        self.send_bytes(body, 'application/json; charset=utf-8', cache='no-store', head=head)

    def route(self, head=False):
        url = urlsplit(self.path)  # Separate the page path from the query after the question mark.
        path = unquote(url.path).rstrip('/') or '/'  # Decode URL escapes such as %20 and remove trailing slashes; keep / for home.
        if path == '/api/populations':
            self.population_response(url.query, head)
            return
        filename = 'website-layout/main-page.html' if path == '/' else path.lstrip('/')
        # Resolve the path before checking that it stays inside an allowed folder.
        target = (ROOT / filename).resolve()
        root_file = filename in PAGE_FILES or filename in OTHER_FILES
        image_file = path.startswith('/images/') and target.is_relative_to(IMAGES)  # Only allow image paths that resolve inside the images folder.
        map_file = path.startswith('/maps/') and target.is_relative_to(MAPS) and target.suffix == '.svg'
        if (root_file or image_file or map_file) and target.is_relative_to(ROOT) and target.is_file():
            content_type = mimetypes.guess_type(target.name)[0] or 'application/octet-stream'  # Work out the file type from its extension, e.g. .css becomes text/css.
            if target.suffix == '.html':
                content_type = 'text/html; charset=utf-8'
            cache = 'no-cache' if target.suffix == '.html' else 'public, max-age=3600'  # Recheck HTML before reuse; other assets can be reused for 3600 seconds (1 hour).
            self.send_bytes(target.read_bytes(), content_type, cache=cache, head=head)
            return
        page = b'''
        <!doctype html><html lang="en"><head><meta charset="utf-8">
        <title>Page not found</title></head><body>
        
        <h1>Page not found</h1><p>The requested address does not exist.</p>
        
        <a href="/website-layout/main-page.html">Return to Vanishing Voices</a></body></html>'''
        self.send_bytes(page, 'text/html; charset=utf-8', 404, head=head)

    def do_GET(self):
        self.route()

    def do_HEAD(self):
        self.route(head=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the animal website on this computer.')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--host', default='127.0.0.1')
    args = parser.parse_args()  # Read terminal options such as --port 5056.
    server = ThreadingHTTPServer((args.host, args.port), AnimalWebsiteHandler)  # Each incoming request can run in its own thread.
    print(f'Open http://{args.host}:{args.port}/', flush=True)
    try:
        server.serve_forever()  # Keep listening until the server is stopped, usually with Ctrl+C.
    except KeyboardInterrupt:
        print('\nWebsite stopped.')
    finally:
        server.server_close()  # Release the server's socket when it stops.
