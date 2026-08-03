import logging

from backend.audio.sliding_buffer import SlidingBuffer
from backend.audio.utterance_buffer import UtteranceBuffer
from backend.audio.speech_state import SpeechState

from backend.ai.vad import VoiceActivityDetector


logger = logging.getLogger(__name__)


class SpeechDetector:
    """
    Detects complete user utterances.

    Input:
        20 ms PCM frame

    Output:
        None
        OR
        Complete utterance bytes
    """

    #
    # Number of consecutive silent VAD windows
    # required before speech is considered finished.
    #
    SILENCE_THRESHOLD = 4

    def __init__(self):

        logger.info("=" * 60)
        logger.info("Initializing SpeechDetector")
        logger.info("=" * 60)

        self.sliding_buffer = SlidingBuffer()

        self.utterance_buffer = UtteranceBuffer()

        self.state = SpeechState()

        self.vad = VoiceActivityDetector()

    # --------------------------------------------------

    def process(
        self,
        pcm: bytes
    ):

        logger.info(
            "SpeechDetector <- %d bytes",
            len(pcm)
        )

        #
        # Append every incoming frame
        # to the sliding buffer.
        #
        self.sliding_buffer.append(pcm)

        logger.info(
            "Sliding Buffer : %.0f ms",
            self.sliding_buffer.duration_ms()
        )

        #
        # Need at least 500 ms
        # before running VAD.
        #
        if not self.sliding_buffer.is_full():

            logger.info(
                "Waiting for 500 ms..."
            )

            return None

        #
        # Read the latest
        # 500 ms chunk.
        #
        chunk = self.sliding_buffer.read()

        logger.info(
            "Running VAD on %d bytes",
            len(chunk)
        )

        result = self.vad.process(chunk)

        speech = result["speech"]

        logger.info(
            "VAD Result : %s",
            "SPEECH" if speech else "SILENCE"
        )

        #
        # ---------------------------------
        # SPEECH DETECTED
        # ---------------------------------
        #
        if speech:

            #
            # Reset silence counter.
            #
            self.state.silence_frames = 0

            #
            # First speech frame.
            #
            if not self.state.in_speech:

                logger.info("=" * 60)
                logger.info("Speech Started")
                logger.info("=" * 60)

                self.state.in_speech = True

            #
            # Save the incoming frame.
            #
            self.utterance_buffer.append(pcm)

            logger.info(
                "Utterance Buffer : %d bytes",
                self.utterance_buffer.size()
            )

            return None

        #
        # ---------------------------------
        # SILENCE
        # ---------------------------------
        #
        if self.state.in_speech:

            self.state.silence_frames += 1

            logger.info(
                "Silence Count : %d",
                self.state.silence_frames
            )

            #
            # Wait until enough silence.
            #
            if self.state.silence_frames < self.SILENCE_THRESHOLD:

                return None

            logger.info("=" * 60)
            logger.info("Speech Finished")
            logger.info("=" * 60)

            utterance = self.utterance_buffer.read()

            logger.info(
                "Returning Utterance : %d bytes",
                len(utterance)
            )

            #
            # Reset for next utterance.
            #
            self.utterance_buffer.clear()

            self.state.reset()

            return utterance

        #
        # Still silence.
        #
        return None