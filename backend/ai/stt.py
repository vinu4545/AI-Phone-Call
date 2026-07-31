import logging

logger = logging.getLogger(__name__)


class SpeechToText:
    """
    Speech-to-Text engine.

    Later this will call Whisper.
    """

    def __init__(self):

        logger.info("Initializing Speech-to-Text")

    async def transcribe(self, pcm: bytes):

        """
        Convert PCM to text.

        Placeholder.
        """

        return ""