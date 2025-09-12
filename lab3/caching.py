import http.server
import socketserver
import os
import hashlib
import time
from email.utils import formatdate, parsedate_to_datetime

PORT = 8080
FILENAME = "index.html"

class CachingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != f"/{FILENAME}":
            self.send_error(404, "File Not Found")
            return

        # Read file content
        try:
            with open(FILENAME, "rb") as f:
                content = f.read()
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
            return

        # Generate ETag (MD5 hash of file content)
        etag = hashlib.md5(content).hexdigest()

        # Get Last-Modified time
        last_mod_time = os.path.getmtime(FILENAME)
        last_modified = formatdate(last_mod_time, usegmt=True)

        # Check request headers
        if_none_match = self.headers.get("If-None-Match")
        if_modified_since = self.headers.get("If-Modified-Since")

        # Validate caching headers
        if (
            if_none_match == etag or
            (
                if_modified_since and
                parsedate_to_datetime(if_modified_since).timestamp() >= last_mod_time
            )
        ):
            self.send_response(304)
            self.end_headers()
            return

        # Send 200 OK with content
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("ETag", etag)
        self.send_header("Last-Modified", last_modified)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CachingHandler) as httpd:
        print(f"📦 Serving '{FILENAME}' with caching support on port {PORT}...")
        httpd.serve_forever()
