import logging

from backend.audio.sliding_buffer import SlidingBuffer
from backend.audio.utterance_buffer import UtteranceBuffer
from backend.audio.speech_state import SpeechState

from backend.ai.vad import VoiceActivityDetector


logger = logging.getLogger(__name__)


class SpeechDetector:
    """
    Responsible ONLY for detecting complete user utterances.

    Input:
        20 ms PCM frame

    Output:
        None
        OR
        Complete utterance bytes
    """

    #
    # Number of consecutive silent
    # VAD windows before speech ends.
    #
    SILENCE_THRESHOLD = 4

    def __init__(self):

        self.sliding_buffer = SlidingBuffer()

        self.utterance_buffer = UtteranceBuffer()

        self.state = SpeechState()

        self.vad = VoiceActivityDetector()

    # --------------------------------------------------

    def process(self, pcm: bytes):

        #
        # Feed sliding window.
        #
        self.sliding_buffer.append(pcm)

        #
        # Wait until
        # 500 ms is accumulated.
        #
        if not self.sliding_buffer.is_full():

            return None

        chunk = self.sliding_buffer.read()

        result = self.vad.process(chunk)

        speech = result["speech"]

        #
        # -----------------------------
        # SPEECH
        # -----------------------------
        #
        if speech:

            self.state.silence_frames = 0

            if not self.state.in_speech:

                logger.info(
                    "Speech Started"
                )

                self.state.in_speech = True

            self.utterance_buffer.append(pcm)

            return None

        #
        # -----------------------------
        # SILENCE
        # -----------------------------
        #
        if self.state.in_speech:

            self.state.silence_frames += 1

            if (
                self.state.silence_frames
                < self.SILENCE_THRESHOLD
            ):

                return None

            logger.info(
                "Speech Finished"
            )

            utterance = self.utterance_buffer.read()

            self.utterance_buffer.clear()

            self.state.reset()

            return utterance

        return None