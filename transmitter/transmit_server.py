# From https://realpython.com/python-sockets/

import time
import data_to_send
import sys
import socket

if len(sys.argv) > 1:
    HOST = sys.argv[1]  # Standard loopback interface address (localhost)
    PORT = sys.argv[2]  # Port to listen on (non-privileged ports are > 1023)
else:
    HOST = None
    PORT = None

if HOST is None:
    HOST = "128.84.124.129"  # The server's hostname or IP address
if PORT is None:
    PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
