# api/index.py
import json
import os
from http.server import BaseHTTPRequestHandler

try:
    with open('marks.txt', 'r') as f:
        marks_data = {}
        for line in f:
            name, mark = line.strip().split(',')
            marks_data[name] = int(mark)
except FileNotFoundError:
    print("marks.txt not found. Make sure it's in the same directory as this script.")
    exit(1) # Exit if the file isn't there

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
