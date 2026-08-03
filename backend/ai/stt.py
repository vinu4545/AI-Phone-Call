import logging


logger = logging.getLogger(__name__)


class SpeechToText:
    """
    Temporary STT.

    Later:
        Faster-Whisper

    For now:
        Always returns a dummy sentence.
    """

    def __init__(self):

        logger.info("SpeechToText Initialized")

    async def transcribe(
        self,
        pcm: bytes
    ):

        logger.info(
            "STT received %d bytes",
            len(pcm)
        )

        #
        # Temporary
        #

        text = "Hello"

        logger.info(
            "STT -> %s",
            text
        )

        return text