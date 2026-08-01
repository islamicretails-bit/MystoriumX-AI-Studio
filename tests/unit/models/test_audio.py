"""
MystoriumX AI Studio
Unit Tests - Audio Model

File:
tests/unit/models/test_audio.py
"""

from __future__ import annotations

from pathlib import Path

import pytest

from models.audio import (
    AudioFormat,
    AudioMetadata,
    AudioModel,
)


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def sample_audio_path() -> Path:
    """
    Provide sample audio path.
    """

    return Path(
        "data/audio/test_track.wav"
    )


@pytest.fixture
def audio_metadata() -> AudioMetadata:
    """
    Provide sample audio metadata.
    """

    return AudioMetadata(
        duration=120.5,
        sample_rate=48000,
        channels=2,
        bitrate=320000,
        format=AudioFormat.WAV,
    )


# ==============================================================================
# Audio Model Tests
# ==============================================================================


def test_audio_model_creation(
    sample_audio_path: Path,
    audio_metadata: AudioMetadata,
) -> None:
    """
    Test audio model initialization.
    """

    audio = AudioModel(
        path=sample_audio_path,
        metadata=audio_metadata,
    )

    assert (
        audio.path
        == sample_audio_path
    )

    assert (
        audio.metadata
        == audio_metadata
    )


def test_audio_metadata_values(
    audio_metadata: AudioMetadata,
) -> None:
    """
    Validate metadata fields.
    """

    assert (
        audio_metadata.duration
        == 120.5
    )

    assert (
        audio_metadata.sample_rate
        == 48000
    )

    assert (
        audio_metadata.channels
        == 2
    )

    assert (
        audio_metadata.format
        == AudioFormat.WAV
    )


def test_audio_model_invalid_duration() -> None:
    """
    Ensure invalid duration is rejected.
    """

    with pytest.raises(
        ValueError
    ):

        AudioMetadata(
            duration=-1,
            sample_rate=48000,
            channels=2,
            bitrate=320000,
            format=AudioFormat.WAV,
        )


def test_audio_model_serialization(
    sample_audio_path: Path,
    audio_metadata: AudioMetadata,
) -> None:
    """
    Test model serialization.
    """

    audio = AudioModel(
        path=sample_audio_path,
        metadata=audio_metadata,
    )

    data = audio.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert (
        "path"
        in data
    )

    assert (
        "metadata"
        in data
    )


def test_audio_model_string_representation(
    sample_audio_path: Path,
    audio_metadata: AudioMetadata,
) -> None:
    """
    Test string representation.
    """

    audio = AudioModel(
        path=sample_audio_path,
        metadata=audio_metadata,
    )

    result = str(
        audio
    )

    assert isinstance(
        result,
        str,
    )

    assert (
        "test_track"
        in result
    )
