import asyncio
import logging

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

from backend.media.media_session import MediaSession
from backend.media.audio_receiver import AudioReceiver
from backend.media.audio_sender import AudioSender
from backend.audio.audio_processor import AudioProcessor


# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# WebSocket Server
# ---------------------------------------------------------

class WebSocketServer:

    def __init__(
        self,
        host="0.0.0.0",
        port=9000
    ):
        self.host = host
        self.port = port

    # -----------------------------------------------------
    # Handle WebSocket Connection
    # -----------------------------------------------------

    async def handle_connection(self, websocket):

        client = websocket.remote_address

        logger.info("=" * 60)
        logger.info("NEW WEBSOCKET CONNECTION")
        logger.info("Client : %s", client)
        logger.info("=" * 60)

        session = None
        receiver_task = None
        processor_task = None
        sender_task = None

        try:

            # -------------------------------------------------
            # Create Media Session
            # -------------------------------------------------

            logger.info("Creating media session...")

            session = MediaSession(websocket)

            logger.info("Media session created.")

            # -------------------------------------------------
            # Create Components
            # -------------------------------------------------

            logger.info("Initializing audio components...")

            receiver = AudioReceiver(session)
            processor = AudioProcessor(session)
            sender = AudioSender(session)

            logger.info("Audio components initialized.")

            # -------------------------------------------------
            # Start Background Tasks
            # -------------------------------------------------

            logger.info("Starting AudioReceiver...")

            receiver_task = asyncio.create_task(
                receiver.start()
            )

            logger.info("Starting AudioProcessor...")

            processor_task = asyncio.create_task(
                processor.start()
            )

            logger.info("Starting AudioSender...")

            sender_task = asyncio.create_task(
                sender.start()
            )

            logger.info("=" * 60)
            logger.info("MEDIA PIPELINE STARTED")
            logger.info("Receiver  : RUNNING")
            logger.info("Processor : RUNNING")
            logger.info("Sender    : RUNNING")
            logger.info("=" * 60)

            # -------------------------------------------------
            # Wait Until WebSocket Closes
            # -------------------------------------------------

            await websocket.wait_closed()

            logger.info("WebSocket connection closed by client.")

        except ConnectionClosed as e:

            logger.info(
                "WebSocket connection closed: %s",
                e
            )

        except asyncio.CancelledError:

            logger.info(
                "WebSocket handler cancelled."
            )

            raise

        except Exception:

            logger.exception(
                "ERROR INSIDE WEBSOCKET CONNECTION"
            )

        finally:

            logger.info("=" * 60)
            logger.info("CLEANING UP SESSION")
            logger.info("=" * 60)

            # -------------------------------------------------
            # Cancel Background Tasks
            # -------------------------------------------------

            tasks = [
                receiver_task,
                processor_task,
                sender_task
            ]

            for task in tasks:

                if task is not None and not task.done():

                    logger.info(
                        "Cancelling task: %s",
                        task.get_name()
                    )

                    task.cancel()

            # -------------------------------------------------
            # Wait for Tasks to Finish
            # -------------------------------------------------

            valid_tasks = [
                task for task in tasks
                if task is not None
            ]

            if valid_tasks:

                await asyncio.gather(
                    *valid_tasks,
                    return_exceptions=True
                )

            # -------------------------------------------------
            # Close Media Session
            # -------------------------------------------------

            if session is not None:

                try:

                    await session.close()

                    logger.info(
                        "Media session closed."
                    )

                except Exception:

                    logger.exception(
                        "Error while closing media session."
                    )

            logger.info(
                "Session destroyed."
            )

            logger.info("=" * 60)


    # -----------------------------------------------------
    # Start Server
    # -----------------------------------------------------

    async def start(self):

        logger.info("=" * 60)
        logger.info("STARTING WEBSOCKET SERVER")
        logger.info("=" * 60)

        logger.info(
            "Host : %s",
            self.host
        )

        logger.info(
            "Port : %d",
            self.port
        )

        try:

            async with serve(
                self.handle_connection,
                self.host,
                self.port,

                # Allow large audio messages
                max_size=None,

                # Don't limit queued messages
                max_queue=None,
            ):

                logger.info("=" * 60)
                logger.info(
                    "WEBSOCKET SERVER STARTED"
                )

                logger.info(
                    "Listening on ws://%s:%d",
                    self.host,
                    self.port
                )

                logger.info("=" * 60)

                # Keep server alive forever
                await asyncio.Future()

        except OSError:

            logger.exception(
                "Could not start WebSocket server."
            )

        except Exception:

            logger.exception(
                "WebSocket server crashed."
            )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    server = WebSocketServer(
        host="0.0.0.0",
        port=9000
    )

    try:

        asyncio.run(
            server.start()
        )

    except KeyboardInterrupt:

        logger.info(
            "WebSocket server stopped by user."
        )


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()