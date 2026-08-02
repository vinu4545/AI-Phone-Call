class UtteranceBuffer:
    """
    Stores one complete user utterance.

    Starts:
        Speech Start

    Ends:
        Speech End

    Passed to Whisper.
    """

    def __init__(self):

        self.buffer = bytearray()

    # -----------------------------------------------------

    def append(self, pcm: bytes):

        self.buffer.extend(pcm)

    # -----------------------------------------------------

    def read(self):

        return bytes(self.buffer)

    # -----------------------------------------------------

    def clear(self):

        self.buffer.clear()

    # -----------------------------------------------------

    def empty(self):

        return len(self.buffer) == 0

    # -----------------------------------------------------

    def size(self):

        return len(self.buffer)

    # -----------------------------------------------------

    def duration_ms(self):

        return len(self.buffer) / 16000 * 1000