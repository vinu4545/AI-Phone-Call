import logging


logger = logging.getLogger(__name__)


class LLM:
    """
    Temporary LLM.

    Later:
        Gemini
        OpenAI
        Ollama

    For now:
        Returns a fixed response.
    """

    def __init__(self):

        logger.info("LLM Initialized")

    async def generate(
        self,
        prompt: str
    ):

        logger.info(
            "LLM Prompt -> %s",
            prompt
        )

        response = (
            "Hello. This is Orbit Services."
        )

        logger.info(
            "LLM Response -> %s",
            response
        )

        return response