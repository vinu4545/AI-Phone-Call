import logging

from websockets.exceptions import ConnectionClosed

from backend.media.media_session import MediaSession


logger = logging.getLogger(__name__)


class AudioReceiver:

    def __init__(self, session: MediaSession):

        self.session = session

    async def start(self):

        logger.info("AudioReceiver Started")

        websocket = self.session.websocket

        try:

            while self.session.running:

                #
                # Receive one frame
                #
                message = await websocket.recv()

                #
                # Ignore text frames.
                #
                if isinstance(message, str):

                    logger.debug(
                        "TEXT FRAME -> %s",
                        message
                    )

                    continue

                pcm = bytes(message)

                logger.info(
                    "Receiver -> %d bytes",
                    len(pcm)
                )

                #
                # Push to processing queue.
                #
                await self.session.push_incoming_audio(
                    pcm
                )

        except ConnectionClosed:

            logger.info(
                "WebSocket Closed."
            )

        except Exception:

            logger.exception(
                "Receiver crashed."
            )

        finally:

            self.session.running = False

            logger.info(
                "AudioReceiver Stopped"
            )