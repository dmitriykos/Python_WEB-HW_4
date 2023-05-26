from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote_plus
import mimetypes
import pathlib
import json
import datetime
import socket
from threading import Thread



class MyHandler(BaseHTTPRequestHandler):

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            self.render_template('index.html')
        elif url.path == '/message':
            self.render_template('message.html')
        else:
            if pathlib.Path().joinpath(url.path[1:]).exists():
                self.send_static()
            else:
                self.render_template('error.html')
             
    def do_POST(self):
        raw_data = self.rfile.read()
        data = unquote_plus(raw_data.decode())
        data = self.parse_form_data(data)
        print(data)

    def parse_form_data(self, data):
        raw_params = data.split('&')
        data = {key: value for key, value in [param.split('=') for param in raw_params]}
        return data
    
    
    FILE_JSON = pathlib.Path().joinpath('storage/data.json')
    
    def save_data_from_server(data):
        with open(FILE_JSON, 'r') as fh:
        all_records = json.load(fh)
        new_record = {srt(datetime.datetime.now()): parse_form_data()}
        all_records = all_records.update(new_record)
        with open(FILE_JSON, 'w') as file:
            json.dump(all_records, file)
        
        
        
        
        

    def render_template(self, html_page):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(html_page, 'rb') as file:
            self.wfile.write(file.read())

# socket
def send_data_to_socket(data):
    c_socket = socket.socket()
    



if __name__ == '__main__':

    server = HTTPServer(('localhost', 3000), MyHandler)
    server.serve_forever()
