import asyncio
import logging

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

from backend.media.media_session import MediaSession
from backend.media.audio_receiver import AudioReceiver
from backend.media.audio_sender import AudioSender
from backend.media.audio_processor import AudioProcessor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class WebSocketServer:

    def __init__(self,
                 host="0.0.0.0",
                 port=9000):

        self.host = host
        self.port = port

    async def handle_connection(self, websocket):

        logger.info("=" * 60)
        logger.info("NEW CALL CONNECTED")
        logger.info("=" * 60)

        session = MediaSession(websocket)

        receiver = AudioReceiver(session)
        processor = AudioProcessor(session)
        sender = AudioSender(session)

        tasks = [

            asyncio.create_task(
                receiver.start(),
                name="AudioReceiver"
            ),

            asyncio.create_task(
                processor.start(),
                name="AudioProcessor"
            ),

            asyncio.create_task(
                sender.start(),
                name="AudioSender"
            )

        ]

        try:

            await websocket.wait_closed()

        except ConnectionClosed:

            logger.info("Caller disconnected.")

        finally:

            logger.info("=" * 60)
            logger.info("Stopping media pipeline")
            logger.info("=" * 60)

            session.running = False

            #
            # Cancel all background tasks.
            #
            for task in tasks:

                if not task.done():

                    task.cancel()

            #
            # Wait for cancellation.
            #
            await asyncio.gather(
                *tasks,
                return_exceptions=True
            )

            #
            # Cleanup.
            #
            await session.close()

            logger.info("=" * 60)
            logger.info("CALL FINISHED")
            logger.info("=" * 60)

    async def start(self):

        logger.info("=" * 60)
        logger.info("Media WebSocket Server")
        logger.info("=" * 60)

        async with serve(

            self.handle_connection,

            self.host,

            self.port,

            max_size=None,

            max_queue=None,

        ):

            logger.info(
                "Listening on ws://%s:%d",
                self.host,
                self.port
            )

            await asyncio.Future()


def main():

    asyncio.run(
        WebSocketServer().start()
    )


if __name__ == "__main__":

    main()