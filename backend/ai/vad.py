import logging

import numpy as np
import torch

from silero_vad import load_silero_vad
from silero_vad import get_speech_timestamps


logger = logging.getLogger(__name__)


class VoiceActivityDetector:
    """
    Voice Activity Detector using Silero VAD.
    """

    SAMPLE_RATE = 8000

    def __init__(self):

        logger.info("Loading Silero VAD...")

        self.model = load_silero_vad()

        logger.info("Silero VAD Loaded.")

    import logging

import numpy as np
import torch

from silero_vad import (
    load_silero_vad,
    get_speech_timestamps,
)


logger = logging.getLogger(__name__)


class VoiceActivityDetector:
    """
    Voice Activity Detector using Silero VAD.

    Input:
        PCM16
        Mono
        8000 Hz

    Output:
        {
            "speech": bool
        }
    """

    SAMPLE_RATE = 8000

    def __init__(self):

        logger.info("=" * 60)
        logger.info("Loading Silero VAD...")
        logger.info("=" * 60)

        self.model = load_silero_vad()

        logger.info("Silero VAD Loaded Successfully.")

    # -------------------------------------------------------------

    def process(
        self,
        pcm: bytes
    ):

        #
        # Raw PCM -> int16
        #
        samples = np.frombuffer(
            pcm,
            dtype=np.int16
        )

        #
        # Nothing received.
        #
        if len(samples) == 0:

            logger.warning(
                "Received empty PCM buffer."
            )

            return {
                "speech": False
            }

        #
        # Debug information
        #
        logger.info(
            "PCM Stats | Samples=%d | Min=%d | Max=%d | MeanAbs=%.2f",
            len(samples),
            samples.min(),
            samples.max(),
            np.abs(samples).mean(),
        )

        #
        # Convert to float32
        #
        samples = (
            samples.astype(np.float32)
            / 32768.0
        )

        #
        # Numpy -> Torch
        #
        audio = torch.from_numpy(
            samples
        )

        logger.info(
            "Running Silero VAD..."
        )

        timestamps = get_speech_timestamps(
            audio,
            self.model,
            sampling_rate=self.SAMPLE_RATE,
        )

        logger.info(
            "Speech Timestamps : %s",
            timestamps,
        )

        speech = len(timestamps) > 0

        logger.info(
            "Speech Detected : %s",
            speech,
        )

        return {
            "speech": speech
        }