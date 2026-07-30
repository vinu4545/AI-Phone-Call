import logging

from backend.media.media_session import MediaSession


logger = logging.getLogger(__name__)


class AudioProcessor:

    def __init__(self, session: MediaSession):

        self.session = session

    async def start(self):

        logger.info("AudioProcessor started")

        try:

            while self.session.running:

                #
                # Read one PCM frame
                #
                pcm = await self.session.get_incoming_audio()

                logger.info(
                    "Processor -> %d bytes",
                    len(pcm)
                )

                #
                # Temporary Echo
                #
                # Later this becomes:
                #
                # PCM
                #   ↓
                # VAD
                #   ↓
                # STT
                #   ↓
                # LLM
                #   ↓
                # TTS
                #   ↓
                # Outgoing Queue
                #

                await self.session.push_outgoing_audio(pcm)

        except Exception:

            logger.exception("AudioProcessor crashed")

        finally:

            logger.info("AudioProcessor stopped")