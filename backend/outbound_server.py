import socket

HOST = "127.0.0.1"
PORT = 8084

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print(f"Listening on {HOST}:{PORT}")

while True:

    conn, addr = server.accept()

    print("=" * 60)
    print("Incoming FreeSWITCH Connection")
    print(addr)

    while True:

        data = conn.recv(4096)

        if not data:
            break

        print(data.decode(errors="ignore"))

    conn.close()

    print("Connection closed")