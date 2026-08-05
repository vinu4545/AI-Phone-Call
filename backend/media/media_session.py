import asyncio
import logging

logger = logging.getLogger(__name__)


class MediaSession:
    """
    Represents one phone call.

    Incoming audio:
        FreeSWITCH
            ↓
        AudioReceiver
            ↓
        incoming_audio Queue

    Outgoing audio:
        AudioProcessor
            ↓
        websocket.send(JSON)

    There is NO outgoing queue anymore.
    """

    def __init__(self, websocket):

        self.websocket = websocket

        #
        # Incoming PCM frames
        #
        self.incoming_audio = asyncio.Queue()

        #
        # Call state
        #
        self.running = True

    # -----------------------------------------------------

    async def push_incoming_audio(
        self,
        pcm: bytes
    ):

        await self.incoming_audio.put(pcm)

    # -----------------------------------------------------

    async def get_incoming_audio(self):

        return await self.incoming_audio.get()

    # -----------------------------------------------------

    async def send_json(
        self,
        payload: str
    ):
        """
        Send JSON message to mod_audio_stream.

        Playback uses TEXT messages,
        not binary websocket frames.
        """

        await self.websocket.send(payload)

    # -----------------------------------------------------

    async def close(self):

        logger.info("Closing MediaSession")

        self.running = False

        while not self.incoming_audio.empty():

            self.incoming_audio.get_nowait()

        logger.info("MediaSession Closed")