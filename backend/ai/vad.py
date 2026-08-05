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
    Silero Voice Activity Detector.

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

        logger.info("Silero VAD Loaded.")
        logger.info("=" * 60)

    def process(self, pcm: bytes):

        logger.info("Running VAD on %d bytes", len(pcm))

        #
        # Convert bytes -> int16
        #
        samples = np.frombuffer(
            pcm,
            dtype=np.int16
        )

        logger.info(
            "PCM Stats | Samples=%d | Min=%d | Max=%d | MeanAbs=%.2f",
            len(samples),
            int(samples.min()) if len(samples) else 0,
            int(samples.max()) if len(samples) else 0,
            float(np.abs(samples).mean()) if len(samples) else 0.0,
        )

        #
        # Normalize to [-1, 1]
        #
        samples = samples.astype(np.float32) / 32768.0

        audio = torch.from_numpy(samples)

        #
        # NEW LOGS
        #
        logger.info(
            "Tensor Shape : %s",
            tuple(audio.shape)
        )

        logger.info(
            "Tensor dtype : %s",
            audio.dtype
        )

        logger.info(
            "Tensor Min   : %.5f",
            float(audio.min())
        )

        logger.info(
            "Tensor Max   : %.5f",
            float(audio.max())
        )

        logger.info(
            "Tensor MeanAbs : %.5f",
            float(audio.abs().mean())
        )

        logger.info("Running Silero VAD...")

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