from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        # Placeholder for your external analysis service URL
        # YOU MUST REPLACE THIS WITH THE ACTUAL URL OF YOUR DEPLOYED CORE ANALYSIS SERVICE
        external_analysis_url = "https://your-external-analysis-service.com/analyze"

        try:
            response = requests.post(external_analysis_url, json=data)
            response.raise_for_status() # Raise an exception for HTTP errors

            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)

        except requests.exceptions.RequestException as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Failed to connect to external analysis service: {e}"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
