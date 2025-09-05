from http.server import BaseHTTPRequestHandler
import http.client
import json
import os
from deep_translator import GoogleTranslator, MicrosoftTranslator
from swiftshadow import QuickProxy

class handler(BaseHTTPRequestHandler):
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
            translated_text = "Error"
            
            if not text:
                self.send_error_response(400, "Text parameter 'q' is required")
                return
            
            # Perform translation
            if engine == 'microsoft':
                # translator = MicrosoftTranslator(source=source, target=target)
                conn = http.client.HTTPSConnection("microsoft-translator-text.p.rapidapi.com")

                payload = f'[{{"Text": "{text}"}}]'

                headers = {
                    'x-rapidapi-key': os.getenv("MSFT_ENV_VAR"),
                    'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
                    'Content-Type': "application/json"
                }

                print(os.getenv("MSFT_ENV_VAR"))

                conn.request("POST", f"/translate?to={target}&api-version=3.0&profanityAction=NoAction&textType=plain", payload, headers)

                res = conn.getresponse()
                data = res.read()

                translated_text = data.decode("utf-8")
            else:
                httpProxy = QuickProxy(protocol='http')
                httpsProxy = QuickProxy(protocol='https')

                proxies = {
                    "http": f"{httpProxy.ip}:{httpProxy.port}",
                    "https": f"{httpsProxy.ip}:{httpsProxy.port}"
                }

                translator = GoogleTranslator(source=source, target=target, proxies=proxies)
                translated_text = translator.translate(text)
            
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
        
        error_response = {"error": message}
        self.wfile.write(json.dumps(error_response).encode())
