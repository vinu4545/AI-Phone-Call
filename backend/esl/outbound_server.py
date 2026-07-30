import socketserver

from backend.esl.call_handler import CallHandler
from backend.config.config import OUTBOUND_HOST, OUTBOUND_PORT


class ESLRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("\n" + "=" * 60)
        print("Incoming Connection")
        print("=" * 60)

        try:
            CallHandler(self.request).handle()
            print("Handler finished.")

        except Exception as e:
            print(f"Handler Error: {e}")
            import traceback
            traceback.print_exc()


class ThreadedTCPServer(socketserver.ThreadingMixIn,
                        socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():

    server = ThreadedTCPServer(
        (OUTBOUND_HOST, OUTBOUND_PORT),
        ESLRequestHandler,
    )

    print("=" * 60)
    print("Outbound ESL Server")
    print(f"Listening on {OUTBOUND_HOST}:{OUTBOUND_PORT}")
    print("=" * 60)

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nStopping server...")

    finally:
        server.server_close()


if __name__ == "__main__":
    main()