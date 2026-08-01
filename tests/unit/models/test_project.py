"""
MystoriumX AI Studio
Unit Tests - Project Model

File:
tests/unit/models/test_project.py
"""

from __future__ import annotations

from pathlib import Path

import pytest

from models.project import (
    Project,
    ProjectStatus,
)


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def sample_project() -> Project:
    """
    Provide sample project instance.
    """

    return Project(
        project_id="project_001",
        name="Ancient Mysteries Documentary",
        video_path=Path(
            "data/videos/input.mp4"
        ),
        status=ProjectStatus.CREATED,
    )


# ==============================================================================
# Creation Tests
# ==============================================================================


def test_project_creation(
    sample_project: Project,
) -> None:
    """
    Validate project initialization.
    """

    assert (
        sample_project.project_id
        ==
        "project_001"
    )

    assert (
        sample_project.name
        ==
        "Ancient Mysteries Documentary"
    )


def test_project_default_status(
    sample_project: Project,
) -> None:
    """
    Validate initial status.
    """

    assert (
        sample_project.status
        ==
        ProjectStatus.CREATED
    )


def test_project_video_path(
    sample_project: Project,
) -> None:
    """
    Validate video path.
    """

    assert isinstance(
        sample_project.video_path,
        Path,
    )

    assert (
        sample_project.video_path.name
        ==
        "input.mp4"
    )


# ==============================================================================
# State Management Tests
# ==============================================================================


def test_project_status_update(
    sample_project: Project,
) -> None:
    """
    Validate project status changes.
    """

    sample_project.update_status(
        ProjectStatus.PROCESSING
    )

    assert (
        sample_project.status
        ==
        ProjectStatus.PROCESSING
    )


def test_project_completion_status(
    sample_project: Project,
) -> None:
    """
    Validate completed state.
    """

    sample_project.update_status(
        ProjectStatus.COMPLETED
    )

    assert (
        sample_project.status
        ==
        ProjectStatus.COMPLETED
    )


# ==============================================================================
# Validation Tests
# ==============================================================================


def test_project_empty_id_validation() -> None:
    """
    Ensure empty project id is rejected.
    """

    with pytest.raises(
        ValueError
    ):

        Project(
            project_id="",
            name="Test",
            video_path=Path(
                "video.mp4"
            ),
            status=ProjectStatus.CREATED,
        )


def test_project_empty_name_validation() -> None:
    """
    Ensure empty name is rejected.
    """

    with pytest.raises(
        ValueError
    ):

        Project(
            project_id="project_002",
            name="",
            video_path=Path(
                "video.mp4"
            ),
            status=ProjectStatus.CREATED,
        )


# ==============================================================================
# Serialization Tests
# ==============================================================================


def test_project_serialization(
    sample_project: Project,
) -> None:
    """
    Validate project serialization.
    """

    data = sample_project.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert (
        data["project_id"]
        ==
        "project_001"
    )

    assert (
        "status"
        in data
    )


def test_project_string_representation(
    sample_project: Project,
) -> None:
    """
    Validate string output.
    """

    result = str(
        sample_project
    )

    assert isinstance(
        result,
        str,
    )

    assert (
        "project_001"
        in result
    )
