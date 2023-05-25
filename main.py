from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote_plus
import mimetypes

class MyHandler(BaseHTTPRequestHandler):

    def go_GET(self):
        url = urlparse(self.path)

        if url.path == '/':
            self.render_template('index.html')
        elif url.path == '/message':
            self.render_template('message.html')
        else:
            self.render_template('error.html')


    def do_POST(self):
        raw_data = self.rfile.read()
        data = unquote_plus(raw_data.decode())
        data = self.parse_fro

    def parse_from_data(self, data):
        raw_data = data.split('&')
        data = {key: value}

    def render_template(self, html_page):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(html_page, 'rb') as file:
            self.wfile.write(file.read())

if __name__ == '__main__':
    server = HTTPServer(('localhost', 3000), MyHandler)
    server.serve_forever()
