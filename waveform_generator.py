# ============================================================
# MystoriumX AI Studio
# DSP Layer - Waveform Generator & Audio Analytics
#
# File:
# app/infrastructure/dsp/waveform_generator.py
#
# Responsibility:
# Generate waveform data, audio statistics,
# and visual analytics for documentary soundtrack.
#
# Technology:
# - Librosa
# - SoundFile
# - NumPy
#
# ============================================================


from __future__ import annotations


from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


import logging


import numpy as np


import librosa


import soundfile as sf



logger = logging.getLogger(
    "MystoriumX.WaveformGenerator"
)



# ============================================================
# Audio Analytics Model
# ============================================================

@dataclass
class AudioAnalytics:
    """
    Stores audio analysis information.
    """

    duration_seconds: float

    sample_rate: int

    channels: int

    peak_amplitude: float

    rms_energy: float

    zero_crossing_rate: float

    tempo: float



# ============================================================
# Waveform Generator
# ============================================================

class WaveformGenerator:
    """
    Professional audio visualization engine.

    Features:

    - Waveform extraction
    - RMS analysis
    - Peak detection
    - Tempo estimation
    - Audio statistics

    Future:

    - Spectrogram generation
    - Mel-frequency analysis
    - AI audio quality scoring

    """



    def __init__(
        self
    ) -> None:


        logger.info(
            "Waveform Generator initialized"
        )



    # ========================================================
    # Generate Waveform
    # ========================================================

    def generate_waveform(
        self,
        audio_file: Path,
        points: int = 2000
    ) -> List[float]:

        """
        Generate waveform amplitude points.

        Args:

            audio_file:
                Input audio path.

            points:
                Number of waveform samples.

        Returns:

            List of amplitude values.

        """


        self._validate_audio(
            audio_file
        )


        try:


            audio, sample_rate = (
                librosa.load(

                    str(audio_file),

                    sr=None,

                    mono=True

                )
            )


            waveform = (

                np.interp(

                    np.linspace(

                        0,

                        len(audio),

                        points

                    ),

                    np.arange(

                        len(audio)

                    ),

                    audio

                )

            )


            return waveform.tolist()



        except Exception as error:


            logger.exception(

                "Waveform generation failed"

            )

            raise error



    # ========================================================
    # Audio Analysis
    # ========================================================

    def analyze_audio(
        self,
        audio_file: Path
    ) -> AudioAnalytics:

        """
        Extract professional audio metrics.
        """


        self._validate_audio(
            audio_file
        )


        try:


            audio, sr = librosa.load(

                str(audio_file),

                sr=None,

                mono=True

            )


            duration = (

                librosa.get_duration(

                    y=audio,

                    sr=sr

                )

            )


            peak = float(

                np.max(

                    np.abs(audio)

                )

            )


            rms = float(

                np.sqrt(

                    np.mean(

                        audio ** 2

                    )

                )

            )


            zcr = float(

                np.mean(

                    librosa.feature.zero_crossing_rate(

                        audio

                    )

                )

            )


            tempo, _ = librosa.beat.beat_track(

                y=audio,

                sr=sr

            )


            return AudioAnalytics(

                duration_seconds=

                    float(duration),


                sample_rate=

                    sr,


                channels=

                    1,


                peak_amplitude=

                    peak,


                rms_energy=

                    rms,


                zero_crossing_rate=

                    zcr,


                tempo=

                    float(tempo)

            )



        except Exception as error:


            logger.exception(

                "Audio analysis failed"

            )

            raise error



    # ========================================================
    # Export Analytics
    # ========================================================

    def analytics_to_dict(
        self,
        analytics: AudioAnalytics
    ) -> Dict:

        """
        Convert analytics into JSON format.
        """


        return {


            "duration_seconds":

                analytics.duration_seconds,


            "sample_rate":

                analytics.sample_rate,


            "channels":

                analytics.channels,


            "peak_amplitude":

                analytics.peak_amplitude,


            "rms_energy":

                analytics.rms_energy,


            "zero_crossing_rate":

                analytics.zero_crossing_rate,


            "tempo":

                analytics.tempo

        }



    # ========================================================
    # Validation
    # ========================================================

    def _validate_audio(
        self,
        audio_file: Path
    ) -> None:

        """
        Validate audio input.
        """


        if not audio_file.exists():

            raise FileNotFoundError(

                f"Audio not found: {audio_file}"

            )


        supported = [

            ".wav",

            ".mp3",

            ".flac",

            ".m4a"

        ]


        if audio_file.suffix.lower() not in supported:


            raise ValueError(

                "Unsupported audio format"

            )
