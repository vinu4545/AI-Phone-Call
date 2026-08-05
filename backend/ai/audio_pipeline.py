import logging

from backend.ai.stt import SpeechToText
from backend.ai.llm import LLM
from backend.ai.tts import TextToSpeech


logger = logging.getLogger(__name__)


class AudioPipeline:
    """
    Complete AI Pipeline.

    Utterance
        ↓
    STT
        ↓
    LLM
        ↓
    TTS
        ↓
    JSON Playback
    """

    def __init__(self):

        self.stt = SpeechToText()

        self.llm = LLM()

        self.tts = TextToSpeech()

        logger.info(
            "AudioPipeline Initialized"
        )

    async def process(
        self,
        utterance: bytes
    ):

        #
        # -------------------------
        # STT
        # -------------------------
        #

        text = await self.stt.transcribe(
            utterance
        )

        logger.info(
            "USER : %s",
            text
        )

        #
        # -------------------------
        # LLM
        # -------------------------
        #

        response = await self.llm.generate(
            text
        )

        logger.info(
            "BOT : %s",
            response
        )

        #
        # -------------------------
        # TTS
        # -------------------------
        #

        playback_json = await self.tts.synthesize(
            response
        )

        logger.info(
            "Playback JSON Ready."
        )

        return playback_json