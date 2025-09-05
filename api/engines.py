from http.server import BaseHTTPRequestHandler
import json
from api.translate import handler as TranslateHandler  # Import the translate handler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Return the list of currently implemented engines."""
        engines = list(TranslateHandler().ENGINE_METHODS.keys())  # Dynamically fetch engines
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"engines": engines}).encode())
