from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote_plus
import mimetypes
import pathlib
import json
import datetime
import socket
from threading import Thread


socket_host = '127.0.0.1'
socket_port = 5000


def send_data_to_socket(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data, (socket_host, socket_port))
    s.close()


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
        data = self.rfile.read()
        send_data_to_socket(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    
    def render_template(self, html_page):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(html_page, 'rb') as file:
            self.wfile.write(file.read())


def save_data_from_server(data):
    data = unquote_plus(data.decode())
    raw_params = data.split('&')
    data = {key: value for key, value in [
        param.split('=') for param in raw_params]}

    FILE_JSON = pathlib.Path().joinpath('storage/data.json')
    with open(FILE_JSON, 'r') as fh:
        records = json.load(fh)
        records[str(datetime.datetime.now())] = data

    with open(FILE_JSON, 'w+') as file:
        json.dump(records, file, indent=1)


def run_socket_server(host, port):
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_socket.bind((host, port))

    while True:
        message, address = s_socket.recvfrom(1024)
        save_data_from_server(message)
        if not message:
            break

    s_socket.close()


def run_http_server():

    address = ('127.0.0.1', 3000)
    httpd = HTTPServer(address, MyHandler)

    httpd.serve_forever()
    httpd.server_close()


if __name__ == '__main__':

    th_server = Thread(target=run_http_server)
    th_server.start()

    th_socket = Thread(target=run_socket_server, args=(socket_host, socket_port))
    th_socket.start()
