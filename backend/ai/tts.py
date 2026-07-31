import logging

logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Text-to-Speech engine.

    Later this will wrap Kokoro.
    """

    def __init__(self):

        logger.info("Initializing Text-to-Speech")

    async def synthesize(self, text: str):

        """
        Convert text into PCM audio.

        Placeholder.
        """

        return b""