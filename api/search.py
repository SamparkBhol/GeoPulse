from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

from geocoding import search_location

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        query_params = parse_qs(urlparse(self.path).query)
        query = query_params.get('query', [None])[0]

        if query:
            results = search_location(query)
            self.wfile.write(json.dumps(results).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({"error": "Query parameter is missing"}).encode('utf-8'))
