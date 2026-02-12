import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "public"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    # Ensure we are in the project root or adjust path if run from scripts/
    # This script assumes it's run from project root via `python3 scripts/server.py`
    # checking if public exists in current cwd
    if not os.path.exists(DIRECTORY):
        # Try to find project root if run from scripts folder
        if os.path.exists(os.path.join("..", DIRECTORY)):
            os.chdir("..")
        else:
            print(f"Error: Could not find '{DIRECTORY}' directory.")
            exit(1)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
