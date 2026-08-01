"""
MystoriumX AI Studio
Progress Tracker Component

File:
src/ui/components/progress_tracker.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import streamlit as st

from src.ui.state import (
    PipelineStage,
    PipelineStatus,
    ProgressState,
    get_progress_state,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Progress Models
# ==============================================================================


@dataclass(slots=True, frozen=True)
class ProgressTrackerConfig:
    """
    Progress tracker configuration.
    """

    show_percentage: bool = True

    show_stage: bool = True

    show_message: bool = True

    show_completed: bool = True


# ==============================================================================
# Progress Tracker Component
# ==============================================================================


class ProgressTracker:
    """
    Streamlit pipeline progress tracker.
    """

    def __init__(
        self,
        config: ProgressTrackerConfig | None = None,
    ) -> None:

        self.config = (
            config
            if config
            else ProgressTrackerConfig()
        )


    def render(
        self,
        state: Optional[ProgressState] = None,
    ) -> None:
        """
        Render progress UI.
        """

        if state is None:
            state = get_progress_state()

        self._render_status(
            state
        )

        self._render_progress(
            state
        )

        self._render_details(
            state
        )


    def _render_status(
        self,
        state: ProgressState,
    ) -> None:
        """
        Render pipeline status.
        """

        status = state.status

        if status == PipelineStatus.COMPLETED:

            st.success(
                "Pipeline completed successfully."
            )

        elif status == PipelineStatus.FAILED:

            st.error(
                state.error
                or "Pipeline failed."
            )

        elif status == PipelineStatus.PROCESSING:

            st.info(
                "Processing pipeline..."
            )

        else:

            st.info(
                "Waiting for execution."
            )
          # ==============================================================================
# Progress Rendering
# ==============================================================================


    def _render_progress(
        self,
        state: ProgressState,
    ) -> None:
        """
        Render progress bar.
        """

        progress_value = max(
            0.0,
            min(
                state.progress,
                1.0,
            ),
        )

        st.progress(
            progress_value
        )

        if self.config.show_percentage:

            percentage = (
                progress_value * 100
            )

            st.caption(
                f"Progress: {percentage:.1f}%"
            )


    def _render_details(
        self,
        state: ProgressState,
    ) -> None:
        """
        Render pipeline details.
        """

        if self.config.show_stage:

            st.write(
                f"Current Stage: "
                f"{state.current_stage.value}"
            )

        if self.config.show_message and state.message:

            st.write(
                state.message
            )

        if (
            self.config.show_completed
            and state.completed_stages
        ):

            st.write(
                "Completed Stages:"
            )

            for stage in state.completed_stages:

                st.checkbox(
                    stage,
                    value=True,
                    disabled=True,
                )


# ==============================================================================
# Helper Functions
# ==============================================================================


def render_progress_tracker(
    state: ProgressState | None = None,
) -> None:
    """
    Render default progress tracker.
    """

    tracker = ProgressTracker()

    tracker.render(
        state
    )


def pipeline_stage_label(
    stage: PipelineStage,
) -> str:
    """
    Convert pipeline stage to display label.
    """

    return (
        stage.value
        .replace("_", " ")
        .title()
    )
  # ==============================================================================
# Progress Status Helpers
# ==============================================================================


def progress_summary(
    state: ProgressState,
) -> dict[str, str | float | list[str]]:
    """
    Generate progress summary.
    """

    return {
        "status": state.status.value,
        "stage": state.current_stage.value,
        "progress": state.progress,
        "message": state.message,
        "completed": state.completed_stages,
    }


def show_progress_summary(
    state: ProgressState | None = None,
) -> None:
    """
    Display progress summary.
    """

    if state is None:

        state = get_progress_state()

    st.json(
        progress_summary(
            state
        )
    )


def reset_progress_display() -> None:
    """
    Reset progress display container.
    """

    st.empty()

    logger.info(
        "Progress display reset."
    )


# ==============================================================================
# Default Instance
# ==============================================================================


_progress_tracker = ProgressTracker()


def track_pipeline_progress() -> None:
    """
    Public pipeline progress entry.
    """

    try:

        _progress_tracker.render()

    except Exception as exc:

        logger.exception(
            "Progress rendering failed."
        )

        st.error(
            str(exc)
        )


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "ProgressTrackerConfig",
    "ProgressTracker",
    "render_progress_tracker",
    "pipeline_stage_label",
    "progress_summary",
    "show_progress_summary",
    "reset_progress_display",
    "track_pipeline_progress",
]
