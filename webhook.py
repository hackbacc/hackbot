########################### REVIEW LATER ################################
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)

        body = json.loads(body)
        if body['repository']['full_name'] == 'hackbacc/hackbot':
            pass

        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 6006), SimpleHTTPRequestHandler)
httpd.serve_forever()

