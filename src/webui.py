import os
import functools
from http import HTTPStatus
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from os.path import dirname, join
from io import BytesIO

class Server(SimpleHTTPRequestHandler):
    def __init__(self, handle_left_motor, handle_right_motor, finish_loop, *args, **kwargs):
        self.handle_left_motor = handle_left_motor
        self.handle_right_motor = handle_right_motor
        self.finish_loop = finish_loop
        self.protocol_version = "HTTP/1.1"
        super().__init__(*args, **kwargs)

    def log_request(self, code='-', size='-'):
        pass

    def do_POST(self):
        ctype = self.headers['content-type']
        clen = int(self.headers['content-length'])
        text = self.rfile.read(clen).decode('utf-8')

        print("POST:", text)
        match text[0]:
            case "L":
                self.handle_left_motor(float(text[1:]))
            case "R":
                self.handle_right_motor(float(text[1:]))
            case "Q":
                self.finish_loop[0] = 1
            case _:
                print("unknown post")

        self.send_response(200)
        self.end_headers()

def start_server(handle_left_motor, handle_right_motor):
    finish_loop = [0]
    server = HTTPServer(("0.0.0.0", 8000), functools.partial(Server, handle_left_motor, handle_right_motor, finish_loop))
    try:
        while finish_loop[0] == 0:
            server.handle_request()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    def handle(v):
        pass

    start_server(handle, handle)
