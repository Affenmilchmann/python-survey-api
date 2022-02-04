from os import pardir
import socket
from urllib.parse import urlparse
from urllib.parse import parse_qs

HOST = 'localhost'
PORT = 10000

class ApiManager:
    def __init__(self) -> None:
        pass

    def listenLoop(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    data = conn.recv(1024)
                    print(self.formReqParams(data))
                    if not data:
                        break
                    conn.send(b'HTTP/1.0 200 OK\n')
                    conn.send(b'Content-Type: text/html\n')
                    conn.send(b'\n')
                    conn.send(b"""
                        <html>
                        <body>
                        <h1>Hello World</h1> this is my server!
                        </body>
                        </html>
                    """)
                    conn.close()

    def formReqParams(self, req: bytes) -> dict:
        req_str = req.decode('utf-8').split('\r\n')[0]
        if req_str == '': return {}
        params = req_str.split(' ')
        parsed_url = urlparse(params[1])
        out_dict = {
            'method': params[0],
            'url': parsed_url.path,
            'args': parse_qs(parsed_url.query)
        }
        return out_dict
