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

                #
                # Wait for audio produced by the processor
                #
                pcm = await self.session.get_outgoing_audio()

                if pcm is None:
                    continue

                logger.info(
                    "Sender -> %d bytes",
                    len(pcm)
                )

                await websocket.send(pcm)

        except ConnectionClosed:

            logger.info("WebSocket closed while sending audio.")

        except Exception:

            logger.exception("Unexpected error inside AudioSender")

        finally:

            self.session.running = False

            logger.info("AudioSender stopped")