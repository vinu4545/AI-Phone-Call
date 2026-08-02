class SpeechState:
    """
    Tracks the current speech state.

    Future:

    Idle
        ↓

    Speech Started
        ↓

    Recording
        ↓

    Speech Ended
        ↓

    Whisper
        ↓

    Idle
    """

    def __init__(self):

        self.in_speech = False

        self.silence_frames = 0

        self.speech_frames = 0

    # -----------------------------------------------------

    def reset(self):

        self.in_speech = False

        self.silence_frames = 0

        self.speech_frames = 0