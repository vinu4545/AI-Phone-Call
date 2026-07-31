import logging

from backend.media.media_session import MediaSession

from backend.audio.audio_buffer import AudioBuffer

from backend.ai.vad import VoiceActivityDetector
from backend.ai.stt import SpeechToText
from backend.ai.llm import LLM
from backend.ai.tts import TextToSpeech


logger = logging.getLogger(__name__)


class AudioProcessor:

    def __init__(self, session: MediaSession):

        self.session = session

        #
        # Audio Buffer
        #
        self.buffer = AudioBuffer()

        #
        # AI Pipeline
        #
        self.vad = VoiceActivityDetector()
        self.stt = SpeechToText()
        self.llm = LLM()
        self.tts = TextToSpeech()

    async def start(self):

        logger.info("AudioProcessor started")

        try:

            while self.session.running:

                #
                # Read one 20 ms PCM frame
                #
                pcm = await self.session.get_incoming_audio()

                #
                # Add it to the audio buffer
                #
                self.buffer.append(pcm)

                logger.info(
                    "Buffered %.0f ms (%d bytes)",
                    self.buffer.duration_ms(),
                    self.buffer.size()
                )

                #
                # Temporary echo so the caller still hears
                # their own audio while we're developing.
                #
                await self.session.push_outgoing_audio(pcm)

                #
                # Once we have at least 500 ms of audio,
                # run Voice Activity Detection.
                #
                if self.buffer.has_audio(500):

                    logger.info("500 ms audio accumulated.")

                    #
                    # Read buffered audio
                    #
                    chunk = self.buffer.read()

                    #
                    # Run Silero VAD
                    #
                    result = self.vad.process(chunk)

                    logger.info("VAD -> %s", result)

        except Exception:

            logger.exception("AudioProcessor crashed")

        finally:

            logger.info("AudioProcessor stopped")