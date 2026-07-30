import logging

from websockets.exceptions import ConnectionClosed

from backend.media.media_session import MediaSession


logger = logging.getLogger(__name__)


class AudioReceiver:

    def __init__(self, session: MediaSession):
        self.session = session

    async def start(self):

        logger.info("AudioReceiver started")

        websocket = self.session.websocket

        try:

            while self.session.running:

                message = await websocket.recv()

                #
                # FreeSWITCH occasionally sends text frames.
                #
                if isinstance(message, str):

                    logger.info("Receiver -> TEXT : %s", message)

                    continue

                pcm = bytes(message)

                logger.info(
                    "Receiver -> %d bytes",
                    len(pcm)
                )

                await self.session.push_incoming_audio(pcm)

        except ConnectionClosed:

            logger.info("WebSocket closed by peer.")

        except Exception:

            logger.exception("Unexpected error inside AudioReceiver")

        finally:

            self.session.running = False

            logger.info("AudioReceiver stopped")