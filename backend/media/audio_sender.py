import logging
from websockets.exceptions import ConnectionClosed

from backend.media.media_session import MediaSession


logger = logging.getLogger(__name__)


class AudioSender:

    def __init__(self, session: MediaSession):
        self.session = session

    async def start(self):

        logger.info("AudioSender started")

        websocket = self.session.websocket

        try:

            while self.session.running:

                # Wait until some component (e.g. TTS)
                # places PCM audio into the outgoing queue.
                pcm = await self.session.get_outgoing_audio()

                if not pcm:
                    continue

                await websocket.send(pcm)

                logger.debug(
                    "Sent %d bytes",
                    len(pcm)
                )

        except ConnectionClosed:

            logger.info("WebSocket closed while sending audio.")

        except Exception:

            logger.exception("Unexpected error inside AudioSender")

        finally:

            self.session.running = False

            logger.info("AudioSender stopped")