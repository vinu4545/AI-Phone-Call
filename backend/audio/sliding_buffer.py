from collections import deque


class SlidingBuffer:
    """
    Keeps only the latest N milliseconds of audio.

    Used ONLY for VAD.

    FreeSWITCH:
        PCM16
        8 kHz
        mono
        320 bytes = 20 ms
    """

    SAMPLE_RATE = 8000
    BYTES_PER_SECOND = SAMPLE_RATE * 2

    FRAME_MS = 20
    FRAME_BYTES = 320

    def __init__(self, window_ms: int = 500):

        self.window_ms = window_ms

        self.max_frames = window_ms // self.FRAME_MS

        self.frames = deque(maxlen=self.max_frames)

    # -----------------------------------------------------

    def append(self, pcm: bytes):

        self.frames.append(pcm)

    # -----------------------------------------------------

    def is_full(self):

        return len(self.frames) == self.max_frames

    # -----------------------------------------------------

    def read(self):

        return b"".join(self.frames)

    # -----------------------------------------------------

    def clear(self):

        self.frames.clear()

    # -----------------------------------------------------

    def duration_ms(self):

        return len(self.frames) * self.FRAME_MS

    # -----------------------------------------------------

    def size(self):

        return len(self.frames) * self.FRAME_BYTES