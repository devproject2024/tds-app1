# api/index.py
import json
import os
from http.server import BaseHTTPRequestHandler

try:
    with open('marks.json', 'r') as f:
        marks_data = json.load(f)  # Load JSON data directly
except FileNotFoundError:
    print("marks.json not found. Make sure it's in the same directory.")
    exit(1)
except json.JSONDecodeError:
    print("Invalid JSON format in marks.json")
    exit(1)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # Enable CORS
        self.end_headers()

        path = self.path
        if "?" in path:
            query = path.split("?", 1)[1]
            params = {}
            for param in query.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    if key == "name":  # Handle multiple 'name' parameters
                        if 'name' not in params:
                            params['name'] = []
                        params['name'].append(value)
        else:
            params = {}

        if 'name' in params and isinstance(params['name'], list):  # Check if name is a list
            names = params['name']
            marks = []
            for name in names:
                if name in marks_data:
                    marks.append(marks_data[name])

            response = {"marks": marks}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else: # Handles cases without params or incorrect params gracefully
            response = {"marks": []} # Return empty if nothing specified. 
            self.wfile.write(json.dumps(response).encode('utf-8')) 
        return
