"""
MystoriumX AI Studio
Utility Module

File:
src/utils/audio_utils.py

Part 1/3
"""

from __future__ import annotations

import logging
import math
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np

from src.core.exceptions import AudioProcessingError
from src.core.security import ensure_safe_path

logger = logging.getLogger(__name__)


# ==============================================================================
# Audio Metadata
# ==============================================================================


@dataclass(slots=True, frozen=True)
class AudioMetadata:
    """
    Audio file metadata.
    """

    path: Path
    duration: float
    sample_rate: int
    channels: int
    sample_width: int
    frame_count: int

    @property
    def bit_depth(self) -> int:
        return self.sample_width * 8


# ==============================================================================
# Audio File Utilities
# ==============================================================================


def read_audio_metadata(
    audio_path: Path,
) -> AudioMetadata:
    """
    Read metadata from a WAV audio file.
    """

    audio_path = ensure_safe_path(audio_path)

    if not audio_path.exists():
        raise AudioProcessingError(
            f"Audio file not found: {audio_path}"
        )

    try:
        with wave.open(str(audio_path), "rb") as wav:

            frame_count = wav.getnframes()
            sample_rate = wav.getframerate()
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()

            duration = (
                frame_count / sample_rate
                if sample_rate
                else 0.0
            )

            return AudioMetadata(
                path=audio_path,
                duration=duration,
                sample_rate=sample_rate,
                channels=channels,
                sample_width=sample_width,
                frame_count=frame_count,
            )

    except wave.Error as exc:
        raise AudioProcessingError(
            f"Invalid WAV file: {audio_path}"
        ) from exc


# ==============================================================================
# Audio Level Utilities
# ==============================================================================


def db_to_linear(
    db: float,
) -> float:
    """
    Convert decibels to linear gain.
    """

    return math.pow(
        10.0,
        db / 20.0,
    )


def linear_to_db(
    gain: float,
) -> float:
    """
    Convert linear gain to decibels.
    """

    if gain <= 0:
        return float("-inf")

    return 20.0 * math.log10(gain)


def normalize_audio(
    samples: np.ndarray,
    peak: float = 0.99,
) -> np.ndarray:
    """
    Peak-normalize an audio buffer.
    """

    if samples.size == 0:
        return samples

    maximum = np.max(np.abs(samples))

    if maximum == 0:
        return samples

    scale = peak / maximum

    logger.debug(
        "Normalizing audio with scale %.6f",
        scale,
    )

    return samples * scale


# ==============================================================================
# RMS Utilities
# ==============================================================================


def calculate_rms(
    samples: np.ndarray,
) -> float:
    """
    Calculate RMS level.
    """

    if samples.size == 0:
        return 0.0

    return float(
        np.sqrt(
            np.mean(
                np.square(samples)
            )
        )
    )
  # ==============================================================================
# Peak & Loudness Utilities
# ==============================================================================


def calculate_peak(
    samples: np.ndarray,
) -> float:
    """
    Calculate the absolute peak value.
    """

    if samples.size == 0:
        return 0.0

    return float(
        np.max(
            np.abs(samples)
        )
    )


def calculate_peak_db(
    samples: np.ndarray,
) -> float:
    """
    Calculate peak level in dBFS.
    """

    peak = calculate_peak(samples)

    return linear_to_db(peak)


def calculate_rms_db(
    samples: np.ndarray,
) -> float:
    """
    Calculate RMS level in dBFS.
    """

    rms = calculate_rms(samples)

    return linear_to_db(rms)


# ==============================================================================
# Channel Utilities
# ==============================================================================


def is_mono(
    metadata: AudioMetadata,
) -> bool:
    """
    Return True if audio is mono.
    """

    return metadata.channels == 1


def is_stereo(
    metadata: AudioMetadata,
) -> bool:
    """
    Return True if audio is stereo.
    """

    return metadata.channels == 2


def duration_to_samples(
    duration_seconds: float,
    sample_rate: int,
) -> int:
    """
    Convert duration to sample count.
    """

    return int(
        duration_seconds * sample_rate
    )


def samples_to_duration(
    samples: int,
    sample_rate: int,
) -> float:
    """
    Convert sample count to seconds.
    """

    if sample_rate <= 0:
        return 0.0

    return samples / sample_rate


# ==============================================================================
# Buffer Utilities
# ==============================================================================


def pad_audio(
    samples: np.ndarray,
    target_length: int,
) -> np.ndarray:
    """
    Zero-pad an audio buffer.
    """

    if len(samples) >= target_length:
        return samples

    padding = target_length - len(samples)

    return np.pad(
        samples,
        (0, padding),
        mode="constant",
    )


def trim_audio(
    samples: np.ndarray,
    target_length: int,
) -> np.ndarray:
    """
    Trim an audio buffer.
    """

    if len(samples) <= target_length:
        return samples

    return samples[:target_length]
  # ==============================================================================
# Validation Utilities
# ==============================================================================


def validate_sample_rate(
    sample_rate: int,
) -> None:
    """
    Validate audio sample rate.
    """

    if sample_rate <= 0:
        raise AudioProcessingError(
            "Sample rate must be greater than zero."
        )


def validate_channels(
    channels: int,
) -> None:
    """
    Validate channel count.
    """

    if channels not in (1, 2):
        raise AudioProcessingError(
            f"Unsupported channel count: {channels}"
        )


def validate_bit_depth(
    bit_depth: int,
) -> None:
    """
    Validate PCM bit depth.
    """

    if bit_depth not in (8, 16, 24, 32):
        raise AudioProcessingError(
            f"Unsupported bit depth: {bit_depth}"
        )


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "AudioMetadata",
    "read_audio_metadata",
    "db_to_linear",
    "linear_to_db",
    "normalize_audio",
    "calculate_rms",
    "calculate_peak",
    "calculate_peak_db",
    "calculate_rms_db",
    "is_mono",
    "is_stereo",
    "duration_to_samples",
    "samples_to_duration",
    "pad_audio",
    "trim_audio",
    "validate_sample_rate",
    "validate_channels",
    "validate_bit_depth",
]
