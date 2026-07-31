import logging


logger = logging.getLogger(__name__)


class AudioBuffer:
    """
    Buffers raw PCM frames.

    FreeSWITCH sends:
        20 ms
        320 bytes
        PCM16
        8 kHz
        mono

    We accumulate them until we have enough audio
    for VAD/STT.
    """

    FRAME_SIZE = 320

    SAMPLE_RATE = 8000

    BYTES_PER_SECOND = SAMPLE_RATE * 2

    def __init__(self):

        self.buffer = bytearray()

    def append(self, pcm: bytes):

        self.buffer.extend(pcm)

    def size(self):

        return len(self.buffer)

    def duration_ms(self):

        return len(self.buffer) / self.BYTES_PER_SECOND * 1000

    def read(self):

        return bytes(self.buffer)

    def clear(self):

        self.buffer.clear()

    def has_audio(self, milliseconds: int):

        required = int(
            self.BYTES_PER_SECOND * milliseconds / 1000
        )

        return len(self.buffer) >= required