import logging

from backend.media.media_session import MediaSession

from backend.audio.speech_detector import SpeechDetector

from backend.ai.audio_pipeline import AudioPipeline


logger = logging.getLogger(__name__)


class AudioProcessor:

    """
    Complete AI processing pipeline.

    AudioReceiver
            ↓
    SpeechDetector
            ↓
    STT
            ↓
    LLM
            ↓
    TTS
            ↓
    JSON Playback
            ↓
    FreeSWITCH
    """

    def __init__(
        self,
        session: MediaSession
    ):

        self.session = session

        self.detector = SpeechDetector()

        self.pipeline = AudioPipeline()

        logger.info(
            "AudioProcessor Initialized"
        )

    async def start(self):

        logger.info(
            "AudioProcessor Started"
        )

        try:

            while self.session.running:

                #
                # Receive one 20ms frame.
                #
                pcm = await self.session.get_incoming_audio()

                #
                # Ask SpeechDetector whether
                # one complete utterance has ended.
                #
                utterance = self.detector.process(
                    pcm
                )

                #
                # Keep listening until an
                # utterance is completed.
                #
                if utterance is None:

                    continue

                logger.info(
                    "=" * 60
                )

                logger.info(
                    "Complete Utterance Detected"
                )

                logger.info(
                    "Utterance Size : %d bytes",
                    len(utterance)
                )

                logger.info(
                    "=" * 60
                )

                #
                # Run AI Pipeline.
                #
                playback_json = await self.pipeline.process(
                    utterance
                )

                if playback_json is None:

                    logger.warning(
                        "Pipeline returned no playback."
                    )

                    continue

                logger.info(
                    "Sending playback JSON to FreeSWITCH..."
                )

                #
                # IMPORTANT
                #
                # mod_audio_stream expects a
                # TEXT websocket message,
                # NOT binary PCM.
                #
                await self.session.send_json(
                    playback_json
                )

                logger.info(
                    "Playback JSON sent."
                )

        except Exception:

            logger.exception(
                "AudioProcessor crashed."
            )

        finally:

            logger.info(
                "AudioProcessor stopped."
            )