import logging

from backend.ai.stt import SpeechToText
from backend.ai.llm import LLM
from backend.ai.tts import TextToSpeech


logger = logging.getLogger(__name__)


class AudioPipeline:
    """
    Complete AI pipeline.

    Utterance
        ↓
    STT
        ↓
    LLM
        ↓
    TTS
        ↓
    PCM Frames
    """

    def __init__(self):

        self.stt = SpeechToText()

        self.llm = LLM()

        self.tts = TextToSpeech()

    async def process(
        self,
        utterance: bytes
    ):

        #
        # STT
        #

        text = await self.stt.transcribe(
            utterance
        )

        logger.info(
            "USER : %s",
            text
        )

        #
        # LLM
        #

        response = await self.llm.generate(
            text
        )

        logger.info(
            "BOT : %s",
            response
        )

        #
        # TTS
        #
        # IMPORTANT
        #
        # Returns a LIST of PCM frames,
        # NOT one giant byte string.
        #

        frames = await self.tts.synthesize(
            response
        )

        return frames