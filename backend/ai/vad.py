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

    def process(self, pcm: bytes):
        """
        Detect whether the given PCM audio contains speech.

        Parameters
        ----------
        pcm : bytes
            16-bit signed PCM mono audio sampled at 8000 Hz.

        Returns
        -------
        dict
            {
                "speech": True/False
            }
        """

        #
        # Convert raw PCM bytes -> int16 numpy array
        #
        samples = np.frombuffer(
            pcm,
            dtype=np.int16
        )

        #
        # Convert int16 -> float32 (-1.0 to 1.0)
        #
        samples = samples.astype(np.float32) / 32768.0

        #
        # Convert numpy array -> Torch tensor
        #
        audio = torch.from_numpy(samples)

        #
        # Run Silero VAD
        #
        timestamps = get_speech_timestamps(
            audio,
            self.model,
            sampling_rate=self.SAMPLE_RATE
        )

        return {
            "speech": len(timestamps) > 0
        }