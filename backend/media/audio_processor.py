import logging

from backend.media.media_session import MediaSession

from backend.audio.speech_detector import SpeechDetector
from backend.ai.audio_pipeline import AudioPipeline


logger = logging.getLogger(__name__)


class AudioProcessor:

    def __init__(
        self,
        session: MediaSession
    ):

        self.session = session

        self.detector = SpeechDetector()

        self.pipeline = AudioPipeline()

    async def start(self):

        logger.info("AudioProcessor Started")

        try:

            while self.session.running:

                #
                # Receive one PCM frame.
                #

                pcm = await self.session.get_incoming_audio()

                #
                # Ask SpeechDetector whether
                # an utterance has completed.
                #

                utterance = self.detector.process(
                    pcm
                )

                #
                # No complete utterance yet.
                #

                if utterance is None:

                    #
                    # TEMPORARY ECHO
                    #
                    # This will be removed once
                    # TTS is implemented.
                    #

                    await self.session.push_outgoing_audio(
                        pcm
                    )

                    continue

                logger.info(
                    "=" * 60
                )

                logger.info(
                    "Complete Utterance Detected"
                )

                logger.info(
                    "Size : %d bytes",
                    len(utterance)
                )

                logger.info(
                    "=" * 60
                )

                #
                # Run complete AI pipeline.
                #

                frames = await self.pipeline.process(
                    utterance
                )

                #
                # Stream every PCM frame.
                #

                if frames:

                    for frame in frames:

                        await self.session.push_outgoing_audio(
                            frame
                        )

        except Exception:

            logger.exception(
                "AudioProcessor crashed."
            )

        finally:

            logger.info(
                "AudioProcessor stopped."
            )