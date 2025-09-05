from http.server import BaseHTTPRequestHandler
import json
from deep_translator import GoogleTranslator

class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to log to stdout (visible in Vercel logs)
        print("%s - - [%s] %s\n" %
              (self.client_address[0],
               self.log_date_time_string(),
               format%args))

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            text = data.get('q', '')
            if not text:
                raise ValueError("Missing 'q' parameter")
            
            # Attempt detection
            translator = GoogleTranslator(source='auto', target='en')
            detected_lang = translator.source
            response = {"language": detected_lang}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            # Log the exception
            self.log_message("Exception in /api/detect: %s", str(e))
            self.send_error_response(500, str(e))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())
