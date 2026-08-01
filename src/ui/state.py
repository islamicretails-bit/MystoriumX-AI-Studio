"""
MystoriumX AI Studio
UI State Management

File:
src/ui/state.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

import streamlit as st

from src.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


# ==============================================================================
# UI Pipeline State
# ==============================================================================


class PipelineStatus(str, Enum):
    """
    Pipeline execution status.
    """

    IDLE = "idle"
    INITIALIZING = "initializing"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class PipelineStage(str, Enum):
    """
    Pipeline processing stages.
    """

    UPLOAD = "upload"
    VIDEO_ANALYSIS = "video_analysis"
    FRAME_EXTRACTION = "frame_extraction"
    SCENE_DETECTION = "scene_detection"
    IMAGE_ANALYSIS = "image_analysis"
    PROMPT_ENHANCEMENT = "prompt_enhancement"
    MUSIC_PROMPT = "music_prompt"
    MUSIC_GENERATION = "music_generation"
    AUDIO_PROCESSING = "audio_processing"
    MASTERING = "mastering"
    WAVEFORM = "waveform"
    ANALYTICS = "analytics"
    EXPORT = "export"


# ==============================================================================
# State Models
# ==============================================================================


@dataclass(slots=True)
class ProgressState:
    """
    Pipeline progress state.
    """

    status: PipelineStatus = PipelineStatus.IDLE

    current_stage: PipelineStage = (
        PipelineStage.UPLOAD
    )

    progress: float = 0.0

    message: str = ""

    error: Optional[str] = None

    completed_stages: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True)
class ProjectUIState:
    """
    Main Streamlit UI state.
    """

    project_id: Optional[str] = None

    project_name: str = (
        "Untitled Project"
    )

    uploaded_video: Optional[str] = None

    generated_audio: Optional[str] = None

    waveform_path: Optional[str] = None

    analytics: Dict[str, Any] = field(
        default_factory=dict
    )

    settings: Dict[str, Any] = field(
        default_factory=dict
    )

    progress: ProgressState = field(
        default_factory=ProgressState
    )
  # ==============================================================================
# Streamlit State Keys
# ==============================================================================


class SessionKeys:
    """
    Centralized Streamlit session state keys.
    """

    PROJECT = "mx_project_state"

    PROGRESS = "mx_progress_state"

    LOGS = "mx_logs"

    SETTINGS = "mx_settings"

    INITIALIZED = "mx_initialized"

    UPLOADED_FILE = "mx_uploaded_file"

    GENERATED_AUDIO = "mx_generated_audio"

    WAVEFORM = "mx_waveform"

    ANALYTICS = "mx_analytics"


# ==============================================================================
# Session State Initialization
# ==============================================================================


def initialize_state() -> None:
    """
    Initialize all required Streamlit session states.
    """

    if st.session_state.get(
        SessionKeys.INITIALIZED,
        False,
    ):
        return

    st.session_state[
        SessionKeys.PROJECT
    ] = ProjectUIState()

    st.session_state[
        SessionKeys.PROGRESS
    ] = ProgressState()

    st.session_state[
        SessionKeys.LOGS
    ] = []

    st.session_state[
        SessionKeys.SETTINGS
    ] = {}

    st.session_state[
        SessionKeys.UPLOADED_FILE
    ] = None

    st.session_state[
        SessionKeys.GENERATED_AUDIO
    ] = None

    st.session_state[
        SessionKeys.WAVEFORM
    ] = None

    st.session_state[
        SessionKeys.ANALYTICS
    ] = {}

    st.session_state[
        SessionKeys.INITIALIZED
    ] = True

    logger.info(
        "MystoriumX UI state initialized."
    )


# ==============================================================================
# State Accessors
# ==============================================================================


def get_project_state() -> ProjectUIState:
    """
    Return current project UI state.
    """

    initialize_state()

    state = st.session_state.get(
        SessionKeys.PROJECT
    )

    if not isinstance(
        state,
        ProjectUIState,
    ):
        raise ValidationError(
            "Invalid project UI state."
        )

    return state


def update_project_state(
    state: ProjectUIState,
) -> None:
    """
    Update project UI state.
    """

    if not isinstance(
        state,
        ProjectUIState,
    ):
        raise ValidationError(
            "Invalid project state object."
        )

    st.session_state[
        SessionKeys.PROJECT
    ] = state


def get_progress_state() -> ProgressState:
    """
    Return pipeline progress state.
    """

    initialize_state()

    progress = st.session_state.get(
        SessionKeys.PROGRESS
    )

    if not isinstance(
        progress,
        ProgressState,
    ):
        raise ValidationError(
            "Invalid progress state."
        )

    return progress


def update_progress(
    progress: ProgressState,
) -> None:
    """
    Update pipeline progress.
    """

    st.session_state[
        SessionKeys.PROGRESS
    ] = progress
  # ==============================================================================
# Progress Management
# ==============================================================================


def set_pipeline_status(
    status: PipelineStatus,
    message: str = "",
) -> None:
    """
    Update pipeline execution status.
    """

    progress = get_progress_state()

    progress.status = status
    progress.message = message

    update_progress(progress)


def set_current_stage(
    stage: PipelineStage,
    message: str = "",
) -> None:
    """
    Update current pipeline stage.
    """

    progress = get_progress_state()

    progress.current_stage = stage
    progress.message = message

    update_progress(progress)


def update_progress_value(
    value: float,
) -> None:
    """
    Update progress percentage.
    """

    if value < 0 or value > 1:
        raise ValidationError(
            "Progress value must be between 0 and 1."
        )

    progress = get_progress_state()

    progress.progress = value

    update_progress(progress)


def complete_stage(
    stage: PipelineStage,
) -> None:
    """
    Mark pipeline stage as completed.
    """

    progress = get_progress_state()

    stage_name = stage.value

    if stage_name not in progress.completed_stages:
        progress.completed_stages.append(
            stage_name
        )

    update_progress(progress)


def set_error(
    message: str,
) -> None:
    """
    Store pipeline error state.
    """

    progress = get_progress_state()

    progress.status = PipelineStatus.FAILED

    progress.error = message

    progress.message = message

    update_progress(progress)


# ==============================================================================
# Logs Management
# ==============================================================================


def add_log(
    message: str,
) -> None:
    """
    Add UI log entry.
    """

    initialize_state()

    logs = st.session_state.get(
        SessionKeys.LOGS,
        [],
    )

    timestamped = (
        f"{utc_timestamp()} | {message}"
    )

    logs.append(timestamped)

    st.session_state[
        SessionKeys.LOGS
    ] = logs


def get_logs() -> list[str]:
    """
    Return UI logs.
    """

    initialize_state()

    return list(
        st.session_state.get(
            SessionKeys.LOGS,
            [],
        )
    )


def clear_logs() -> None:
    """
    Clear UI logs.
    """

    st.session_state[
        SessionKeys.LOGS
    ] = []


# ==============================================================================
# Serialization
# ==============================================================================


def export_state() -> Dict[str, Any]:
    """
    Export current state as dictionary.
    """

    initialize_state()

    project = get_project_state()

    progress = get_progress_state()

    return {
        "project": asdict(project),
        "progress": asdict(progress),
        "logs": get_logs(),
        "analytics": st.session_state.get(
            SessionKeys.ANALYTICS,
            {},
        ),
    }


def utc_timestamp() -> str:
    """
    Return formatted UTC timestamp.
    """

    from datetime import datetime

    return datetime.utcnow().isoformat()


__all__ = [
    "PipelineStatus",
    "PipelineStage",
    "ProgressState",
    "ProjectUIState",
    "SessionKeys",
    "initialize_state",
    "get_project_state",
    "update_project_state",
    "get_progress_state",
    "update_progress",
    "set_pipeline_status",
    "set_current_stage",
    "update_progress_value",
    "complete_stage",
    "set_error",
    "add_log",
    "get_logs",
    "clear_logs",
    "export_state",
]
