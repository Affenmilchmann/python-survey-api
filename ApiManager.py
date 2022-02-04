import socket

class ApiManager:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 10000))
        self.socket.listen(5)

    def listenLoop(self) -> None:
        while True:
            conn, adr = self.socket.accept()
            buf = conn.recv(64)
            if len(buf) > 0:
                print(buf)