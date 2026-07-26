import socket
from backend.config.config import *

class ESLClient:

    def __init__(self):
        self.sock = None

    def connect(self):
        self.sock = socket.create_connection((FS_HOST, FS_PORT))

        banner = self.sock.recv(4096).decode()

        print("=" * 50)
        print("Connected to FreeSWITCH")
        print("=" * 50)
        print(banner)

        self.send(f"auth {FS_PASSWORD}")

        print(self.receive())

    def send(self, command):
        self.sock.sendall((command + "\n\n").encode())

    def receive(self):
        return self.sock.recv(8192).decode()