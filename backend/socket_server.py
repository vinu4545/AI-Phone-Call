import socket

HOST = "127.0.0.1"
PORT = 8084

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print("=" * 60)
print("AI Voice Agent Socket Server")
print(f"Listening on {HOST}:{PORT}")
print("=" * 60)

while True:

    conn, addr = server.accept()

    print("\n")
    print("=" * 60)
    print("NEW CALL")
    print("=" * 60)

    print("From:", addr)

    while True:

        data = conn.recv(4096)

        if not data:
            break

        message = data.decode(errors="ignore")

        print(message)

    conn.close()

    print("Call Finished")