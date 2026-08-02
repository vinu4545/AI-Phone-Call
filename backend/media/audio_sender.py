import logging

from websockets.exceptions import ConnectionClosed

from backend.media.media_session import MediaSession


logger = logging.getLogger(__name__)


class AudioSender:

    def __init__(self, session: MediaSession):

        self.session = session

    async def start(self):

        logger.info("=" * 60)
        logger.info("AudioSender Started")
        logger.info("=" * 60)

        websocket = self.session.websocket

        try:

            while self.session.running:

                #
                # Wait until some component
                # (currently AudioProcessor)
                # places PCM in the outgoing queue.
                #
                pcm = await self.session.get_outgoing_audio()

                if not pcm:
                    continue

                #
                # Send PCM to FreeSWITCH.
                #
                await websocket.send(pcm)

                logger.info(
                    "Sender -> %d bytes",
                    len(pcm)
                )

        except ConnectionClosed:

            logger.info(
                "WebSocket closed while sending."
            )

        except Exception:

            logger.exception(
                "AudioSender crashed."
            )

        finally:

            logger.info(
                "AudioSender Stopped"
            )