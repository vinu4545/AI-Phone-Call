import logging

logger = logging.getLogger(__name__)


class LLM:
    """
    Language Model.

    Later this will call OpenAI / Ollama / Gemini.
    """

    def __init__(self):

        logger.info("Initializing LLM")

    async def generate(self, text: str):

        """
        Generate assistant response.
        """

        return ""