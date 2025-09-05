from http.server import BaseHTTPRequestHandler
import json
from .engine_config import ENGINE_METHODS  # Import the centralized engine methods


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Return the list of currently implemented engines."""
        engines = list(ENGINE_METHODS.keys())  # Fetch engines from the centralized dictionary
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"engines": engines}).encode())
