import socket

HOST = "127.0.0.1"
PORT = 8021
PASSWORD = "ClueCon"

sock = socket.create_connection((HOST, PORT))

banner = sock.recv(4096).decode()
print("CONNECTED")
print(banner)

sock.sendall(f"auth {PASSWORD}\n\n".encode())

reply = sock.recv(4096).decode()
print(reply)

sock.sendall(b"api status\n\n")

status = sock.recv(8192).decode()
print(status)

sock.close()