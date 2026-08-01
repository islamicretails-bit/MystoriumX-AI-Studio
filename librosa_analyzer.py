# ============================================================
# MystoriumX AI Studio
# DSP Layer - Librosa Audio Intelligence Analyzer
#
# File:
# app/infrastructure/dsp/librosa_analyzer.py
#
# Responsibility:
# Advanced audio feature extraction and
# cinematic soundtrack intelligence.
#
# Technology:
# - Librosa
# - NumPy
#
# ============================================================


from __future__ import annotations


from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import logging


import numpy as np

import librosa



logger = logging.getLogger(
    "MystoriumX.LibrosaAnalyzer"
)



# ============================================================
# Audio Feature Model
# ============================================================

@dataclass
class AudioFeatures:
    """
    Stores extracted audio intelligence.
    """

    duration: float

    tempo: float

    spectral_centroid: float

    spectral_bandwidth: float

    spectral_rolloff: float

    zero_crossing_rate: float

    rms_energy: float

    mfcc_features: List[float]

    mood_score: float



# ============================================================
# Librosa Analyzer
# ============================================================

class LibrosaAnalyzer:
    """
    Advanced audio analysis engine.

    Provides:

    - Spectral analysis
    - Energy measurement
    - Tempo detection
    - MFCC extraction
    - Mood estimation

    Future:

    - AI emotion classifier
    - Music similarity engine
    - Soundtrack recommendation

    """



    def __init__(
        self
    ) -> None:


        logger.info(
            "Librosa Analyzer initialized"
        )



    # ========================================================
    # Main Analysis
    # ========================================================

    def analyze(
        self,
        audio_file: Path
    ) -> AudioFeatures:

        """
        Extract complete audio feature set.

        Args:

            audio_file:
                Audio input path.

        Returns:

            AudioFeatures object.

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



            tempo = self._calculate_tempo(

                audio,

                sr

            )



            spectral_centroid = float(

                np.mean(

                    librosa.feature.spectral_centroid(

                        y=audio,

                        sr=sr

                    )

                )

            )



            spectral_bandwidth = float(

                np.mean(

                    librosa.feature.spectral_bandwidth(

                        y=audio,

                        sr=sr

                    )

                )

            )



            spectral_rolloff = float(

                np.mean(

                    librosa.feature.spectral_rolloff(

                        y=audio,

                        sr=sr

                    )

                )

            )



            zero_crossing = float(

                np.mean(

                    librosa.feature.zero_crossing_rate(

                        audio

                    )

                )

            )



            rms = float(

                np.mean(

                    librosa.feature.rms(

                        y=audio

                    )

                )

            )



            mfcc = (

                librosa.feature.mfcc(

                    y=audio,

                    sr=sr,

                    n_mfcc=13

                )

            )



            mfcc_average = (

                np.mean(

                    mfcc,

                    axis=1

                )

                .tolist()

            )



            mood_score = (

                self._estimate_mood(

                    rms,

                    tempo,

                    spectral_centroid

                )

            )



            return AudioFeatures(

                duration=float(duration),

                tempo=float(tempo),

                spectral_centroid=spectral_centroid,

                spectral_bandwidth=spectral_bandwidth,

                spectral_rolloff=spectral_rolloff,

                zero_crossing_rate=zero_crossing,

                rms_energy=rms,

                mfcc_features=mfcc_average,

                mood_score=mood_score

            )



        except Exception as error:


            logger.exception(

                "Librosa analysis failed"

            )

            raise error



    # ========================================================
    # Tempo Detection
    # ========================================================

    def _calculate_tempo(
        self,
        audio,
        sample_rate: int
    ) -> float:

        """
        Calculate BPM.
        """


        tempo, _ = librosa.beat.beat_track(

            y=audio,

            sr=sample_rate

        )


        return float(tempo)



    # ========================================================
    # Mood Estimation
    # ========================================================

    def _estimate_mood(
        self,
        energy: float,
        tempo: float,
        brightness: float
    ) -> float:

        """
        Estimate cinematic mood intensity.

        Range:
        0.0 - 10.0

        Future:
        Neural emotion model.

        """


        score = 0.0



        score += min(

            energy * 20,

            4.0

        )


        score += min(

            tempo / 40,

            3.0

        )


        score += min(

            brightness / 3000,

            3.0

        )


        return round(

            score,

            2

        )



    # ========================================================
    # Export Features
    # ========================================================

    def to_dict(
        self,
        features: AudioFeatures
    ) -> Dict:

        """
        Convert audio features into dictionary.
        """


        return {


            "duration":

                features.duration,


            "tempo":

                features.tempo,


            "spectral_centroid":

                features.spectral_centroid,


            "spectral_bandwidth":

                features.spectral_bandwidth,


            "spectral_rolloff":

                features.spectral_rolloff,


            "zero_crossing_rate":

                features.zero_crossing_rate,


            "rms_energy":

                features.rms_energy,


            "mfcc":

                features.mfcc_features,


            "mood_score":

                features.mood_score

        }



    # ========================================================
    # Validation
    # ========================================================

    def _validate_audio(
        self,
        audio_file: Path
    ) -> None:

        """
        Validate audio file.
        """


        if not audio_file.exists():

            raise FileNotFoundError(

                f"Audio file not found: {audio_file}"

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
