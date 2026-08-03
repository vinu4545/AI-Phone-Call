import logging
import wave
import audioop
from pathlib import Path


logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Temporary TTS.

    Ignores the input text and returns the contents
    of hello.wav as PCM frames.

    Later this file will be replaced by Kokoro.
    """

    SAMPLE_RATE = 8000
    CHANNELS = 1
    SAMPLE_WIDTH = 2          # PCM16
    FRAME_SIZE = 320          # 20 ms @ 8kHz PCM16 mono

    def __init__(self):

        self.wav_path = Path(
            "/home/vinay-gaddam/Documents/Orbit_Services/AI-Phone-Call/recordings/hello.wav"
        )

        logger.info(
            "Temporary TTS initialized."
        )

    async def synthesize(
        self,
        text: str
    ):

        logger.info(
            "TTS -> \"%s\"",
            text
        )

        if not self.wav_path.exists():

            logger.error(
                "WAV file not found: %s",
                self.wav_path
            )

            return []

        with wave.open(str(self.wav_path), "rb") as wav:

            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()

            pcm = wav.readframes(
                wav.getnframes()
            )

        #
        # Convert to mono if required.
        #
        if channels != self.CHANNELS:

            pcm = audioop.tomono(
                pcm,
                sample_width,
                0.5,
                0.5
            )

        #
        # Convert sample width.
        #
        if sample_width != self.SAMPLE_WIDTH:

            pcm = audioop.lin2lin(
                pcm,
                sample_width,
                self.SAMPLE_WIDTH
            )

        #
        # Convert sample rate.
        #
        if sample_rate != self.SAMPLE_RATE:

            pcm, _ = audioop.ratecv(
                pcm,
                self.SAMPLE_WIDTH,
                self.CHANNELS,
                sample_rate,
                self.SAMPLE_RATE,
                None
            )

        logger.info(
            "Generated %d PCM bytes",
            len(pcm)
        )

        #
        # Split into 20 ms frames.
        #
        frames = []

        for i in range(
            0,
            len(pcm),
            self.FRAME_SIZE
        ):

            frame = pcm[i:i + self.FRAME_SIZE]

            #
            # Pad final frame.
            #
            if len(frame) < self.FRAME_SIZE:

                frame += b"\x00" * (
                    self.FRAME_SIZE - len(frame)
                )

            frames.append(frame)

        logger.info(
            "Returning %d audio frames",
            len(frames)
        )

        return frames