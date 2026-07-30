import asyncio
import logging


logger = logging.getLogger(__name__)


class MediaSession:

    def __init__(self, websocket):

        # ----------------------------
        # Network
        # ----------------------------
        self.websocket = websocket

        # ----------------------------
        # Audio Queues
        # ----------------------------
        self.incoming_audio = asyncio.Queue()

        self.outgoing_audio = asyncio.Queue()

        # ----------------------------
        # Future metadata
        # ----------------------------
        self.call_uuid = None

        self.esl_connection = None

        # ----------------------------
        # Session State
        # ----------------------------
        self.running = True

    # ====================================================
    # Incoming Audio
    # ====================================================

    async def push_incoming_audio(self, pcm: bytes):

        await self.incoming_audio.put(pcm)

    async def get_incoming_audio(self) -> bytes:

        return await self.incoming_audio.get()

    # ====================================================
    # Outgoing Audio
    # ====================================================

    async def push_outgoing_audio(self, pcm: bytes):

        await self.outgoing_audio.put(pcm)

    async def get_outgoing_audio(self) -> bytes:

        return await self.outgoing_audio.get()

    # ====================================================
    # Cleanup
    # ====================================================

    async def close(self):

        logger.info("Closing media session")

        self.running = False

        while not self.incoming_audio.empty():
            self.incoming_audio.get_nowait()

        while not self.outgoing_audio.empty():
            self.outgoing_audio.get_nowait()

        logger.info("Media session closed")