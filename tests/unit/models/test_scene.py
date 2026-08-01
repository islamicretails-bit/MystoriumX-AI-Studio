"""
MystoriumX AI Studio
Unit Tests - Scene Model

File:
tests/unit/models/test_scene.py
"""

from __future__ import annotations

from pathlib import Path

import pytest

from models.scene import (
    Scene,
    SceneFrame,
    SceneMetadata,
)


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def scene_frame() -> SceneFrame:
    """
    Provide sample scene frame.
    """

    return SceneFrame(
        frame_number=120,
        timestamp=4.5,
        image_path=Path(
            "data/frames/frame_120.jpg"
        ),
    )


@pytest.fixture
def scene_metadata() -> SceneMetadata:
    """
    Provide sample scene metadata.
    """

    return SceneMetadata(
        start_time=0.0,
        end_time=12.5,
        confidence=0.94,
        description=(
            "Dark cinematic mountain landscape"
        ),
    )


@pytest.fixture
def sample_scene(
    scene_frame: SceneFrame,
    scene_metadata: SceneMetadata,
) -> Scene:

    """
    Provide sample scene object.
    """

    return Scene(
        scene_id="scene_001",
        frames=[
            scene_frame
        ],
        metadata=scene_metadata,
    )


# ==============================================================================
# Scene Creation Tests
# ==============================================================================


def test_scene_creation(
    sample_scene: Scene,
) -> None:
    """
    Validate scene initialization.
    """

    assert (
        sample_scene.scene_id
        == "scene_001"
    )

    assert (
        len(
            sample_scene.frames
        )
        == 1
    )


def test_scene_frame_values(
    scene_frame: SceneFrame,
) -> None:
    """
    Validate frame information.
    """

    assert (
        scene_frame.frame_number
        == 120
    )

    assert (
        scene_frame.timestamp
        == 4.5
    )

    assert isinstance(
        scene_frame.image_path,
        Path,
    )


def test_scene_metadata_values(
    scene_metadata: SceneMetadata,
) -> None:
    """
    Validate metadata.
    """

    assert (
        scene_metadata.confidence
        == 0.94
    )

    assert (
        scene_metadata.end_time
        >
        scene_metadata.start_time
    )


# ==============================================================================
# Validation Tests
# ==============================================================================


def test_scene_invalid_confidence() -> None:
    """
    Ensure confidence range validation.
    """

    with pytest.raises(
        ValueError
    ):

        SceneMetadata(
            start_time=0,
            end_time=10,
            confidence=1.5,
            description="Invalid",
        )


def test_scene_invalid_time_range() -> None:
    """
    Ensure invalid timestamps are rejected.
    """

    with pytest.raises(
        ValueError
    ):

        SceneMetadata(
            start_time=20,
            end_time=10,
            confidence=0.8,
            description="Invalid range",
        )


# ==============================================================================
# Serialization Tests
# ==============================================================================


def test_scene_serialization(
    sample_scene: Scene,
) -> None:
    """
    Validate scene dictionary conversion.
    """

    data = sample_scene.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert (
        data["scene_id"]
        ==
        "scene_001"
    )

    assert (
        "metadata"
        in data
    )


def test_scene_string_output(
    sample_scene: Scene,
) -> None:
    """
    Validate string representation.
    """

    result = str(
        sample_scene
    )

    assert isinstance(
        result,
        str,
    )

    assert (
        "scene_001"
        in result
    )
