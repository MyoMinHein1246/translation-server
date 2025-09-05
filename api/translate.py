from http.server import BaseHTTPRequestHandler
import json
from .engine_config import ENGINE_METHODS
from swiftshadow import QuickProxy


class handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ENGINE_METHODS = ENGINE_METHODS  # Use the centralized engine methods
        super().__init__(*args, **kwargs)

    def do_POST(self):
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract parameters
            text = data.get('q', '')
            source = data.get('source', 'auto')
            target = data.get('target', 'en')
            engine = data.get('engine', 'google')

            if not text:
                self.send_error_response(400, "Text parameter 'q' is required")
                return

            # Perform translation based on the selected engine
            if engine not in self.ENGINE_METHODS:
                self.send_error_response(400, f"Unsupported engine: {engine}")
                return

            translated_text = self.perform_translation(engine, text, source, target)

            # Send response
            response = {
                "translatedText": translated_text,
                "source": source,
                "target": target,
                "engine": engine
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_error_response(500, str(e))

    def perform_translation(self, engine, text, source, target):
        """Perform translation based on the selected engine."""
        if engine in self.ENGINE_METHODS:
            return self.ENGINE_METHODS[engine](text, source, target, proxies=self.get_proxies())
        else:
            raise ValueError(f"Unsupported engine: {engine}")

    def get_proxies(self):
        """Get proxy settings."""
        httpProxy = QuickProxy(countries=['SG', 'TH', 'MM', 'JP'], protocol='http')
        httpsProxy = QuickProxy(countries=['SG', 'TH', 'MM', 'JP'], protocol='https')

        return {
            "http": f"{httpProxy.ip}:{httpProxy.port}",
            "https": f"{httpsProxy.ip}:{httpsProxy.port}"
        }

