from dataclasses import dataclass


@dataclass(slots=True)
class AudioFrame:
    """
    One PCM frame.

    PCM16
    Mono
    8kHz
    20 ms
    """

    pcm: bytes

    sample_rate: int = 8000

    channels: int = 1

    frame_ms: int = 20