import socket, time

m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
m_socket.bind(('localhost', 10000))
m_socket.listen(5)

print(m_socket.getsockname())

while True:
    conn, adr = m_socket.accept()

    buf = conn.recv(64)
    if len(buf) > 0:
        print(buf)
        