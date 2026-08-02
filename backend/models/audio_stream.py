from dataclasses import dataclass
from typing import Iterable

from backend.models.audio_frame import AudioFrame


@dataclass
class AudioStream:

    frames: Iterable[AudioFrame]