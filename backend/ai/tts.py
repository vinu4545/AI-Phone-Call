import base64
import json
import wave
import audioop

from pathlib import Path

import logging

logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Temporary TTS.

    Instead of generating speech,
    this loads hello.wav and converts it into the
    JSON format expected by mod_audio_stream.
    """

    SAMPLE_RATE = 8000
    CHANNELS = 1
    SAMPLE_WIDTH = 2

    def __init__(self):

        #
        # Project Root
        #
        project_root = Path(__file__).resolve().parents[2]

        self.wav_path = (
            project_root
            / "recordings"
            / "hello.wav"
        )

        logger.info(
            "Temporary TTS initialized."
        )

        logger.info(
            "WAV : %s",
            self.wav_path
        )

    # ---------------------------------------------------------

    async def synthesize(
        self,
        text: str
    ) -> str:

        logger.info(
            "TTS Input : %s",
            text
        )

        if not self.wav_path.exists():

            raise FileNotFoundError(
                self.wav_path
            )

        #
        # Read WAV
        #
        with wave.open(
            str(self.wav_path),
            "rb"
        ) as wav:

            channels = wav.getnchannels()

            sample_width = wav.getsampwidth()

            sample_rate = wav.getframerate()

            pcm = wav.readframes(
                wav.getnframes()
            )

        logger.info(
            "Original WAV : %d Hz | %d Ch | %d bytes",
            sample_rate,
            channels,
            len(pcm)
        )

        #
        # Convert Stereo → Mono
        #
        if channels != self.CHANNELS:

            pcm = audioop.tomono(
                pcm,
                sample_width,
                0.5,
                0.5
            )

        #
        # Convert sample width
        #
        if sample_width != self.SAMPLE_WIDTH:

            pcm = audioop.lin2lin(
                pcm,
                sample_width,
                self.SAMPLE_WIDTH
            )

        #
        # Convert sample rate
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
            "PCM Bytes : %d",
            len(pcm)
        )

        #
        # Base64 Encode
        #
        audio_b64 = base64.b64encode(
            pcm
        ).decode()

        logger.info(
            "Base64 Size : %d",
            len(audio_b64)
        )

        #
        # Build JSON
        #
        payload = {

            "type": "streamAudio",

            "data": {

                "audioDataType": "raw",

                "sampleRate": self.SAMPLE_RATE,

                "audioData": audio_b64

            }

        }

        logger.info(
            "Playback JSON Created."
        )

        return json.dumps(
            payload
        )