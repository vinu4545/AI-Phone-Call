import asyncio
import logging

from websockets.server import serve
from websockets.exceptions import ConnectionClosed

from backend.media.media_session import MediaSession
from backend.media.audio_receiver import AudioReceiver
from backend.media.audio_sender import AudioSender


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class WebSocketServer:

    def __init__(
        self,
        host="0.0.0.0",
        port=9000
    ):
        self.host = host
        self.port = port

    async def handle_connection(self, websocket):

        client = websocket.remote_address

        logging.info("=" * 60)
        logging.info("NEW WEBSOCKET CONNECTION")
        logging.info("Client : %s", client)

        session = MediaSession(websocket)

        receiver = AudioReceiver(session)
        sender = AudioSender(session)

        receiver_task = asyncio.create_task(
            receiver.start()
        )

        sender_task = asyncio.create_task(
            sender.start()
        )

        try:

            await websocket.wait_closed()

        except ConnectionClosed:

            logging.info("Connection closed.")

        finally:

            receiver_task.cancel()
            sender_task.cancel()

            await session.close()

            logging.info("Session destroyed.")

    async def start(self):

        async with serve(
            self.handle_connection,
            self.host,
            self.port,
            max_size=None,
            max_queue=None,
        ):

            logging.info("=" * 60)
            logging.info(
                "Listening on ws://%s:%d",
                self.host,
                self.port
            )
            logging.info("=" * 60)

            await asyncio.Future()


def main():

    server = WebSocketServer()

    asyncio.run(server.start())


if __name__ == "__main__":
    main()