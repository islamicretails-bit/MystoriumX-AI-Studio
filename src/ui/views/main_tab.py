"""
MystoriumX AI Studio
Main Tab View

File:
src/ui/views/main_tab.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import streamlit as st

from src.services.orchestrator import Orchestrator
from src.ui.components.progress_tracker import (
    render_progress_tracker,
)
from src.ui.components.upload_zone import (
    UploadedFileInfo,
    render_upload_zone,
    show_upload_status,
)
from src.ui.state import (
    PipelineStatus,
    add_log,
    set_pipeline_status,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Main View Configuration
# ==============================================================================


@dataclass(slots=True, frozen=True)
class MainTabConfig:
    """
    Main tab configuration.
    """

    title: str = (
        "MystoriumX AI Studio"
    )

    subtitle: str = (
        "Hollywood-grade AI Documentary Audio Production"
    )


# ==============================================================================
# Main Tab View
# ==============================================================================


class MainTab:
    """
    Main Streamlit application tab.
    """

    def __init__(
        self,
        orchestrator: Optional[Orchestrator] = None,
        config: Optional[MainTabConfig] = None,
    ) -> None:

        self.orchestrator = orchestrator

        self.config = (
            config
            if config
            else MainTabConfig()
        )


    def render(
        self,
    ) -> None:
        """
        Render main application view.
        """

        self._render_header()

        uploaded = render_upload_zone()

        show_upload_status(
            uploaded
        )

        render_progress_tracker()

        self._render_actions(
            uploaded
        )
      # ==============================================================================
# Header Rendering
# ==============================================================================


    def _render_header(
        self,
    ) -> None:
        """
        Render main page header.
        """

        st.title(
            self.config.title
        )

        st.caption(
            self.config.subtitle
        )


# ==============================================================================
# Action Controls
# ==============================================================================


    def _render_actions(
        self,
        uploaded: Optional[UploadedFileInfo],
    ) -> None:
        """
        Render pipeline action controls.
        """

        if uploaded is None:

            st.warning(
                "Upload a video before starting."
            )

            return


        if st.button(
            "Start AI Production Pipeline",
            type="primary",
        ):

            self._start_pipeline(
                uploaded
            )


    def _start_pipeline(
        self,
        uploaded: UploadedFileInfo,
    ) -> None:
        """
        Start document audio pipeline.
        """

        try:

            set_pipeline_status(
                PipelineStatus.INITIALIZING,
                "Initializing AI pipeline...",
            )

            add_log(
                "Pipeline execution requested."
            )


            if self.orchestrator is None:

                raise RuntimeError(
                    "Orchestrator service unavailable."
                )


            result = (
                self.orchestrator.process(
                    uploaded.name
                )
            )


            set_pipeline_status(
                PipelineStatus.COMPLETED,
                "Production completed successfully.",
            )

            add_log(
                "Pipeline completed successfully."
            )


            st.success(
                "AI documentary audio created."
            )


            st.json(
                result
            )


        except Exception as exc:

            logger.exception(
                "Pipeline execution failed."
            )

            set_pipeline_status(
                PipelineStatus.FAILED,
                str(exc),
            )

            st.error(
                str(exc)
            )
          # ==============================================================================
# Public Renderer
# ==============================================================================


def render_main_tab(
    orchestrator: Optional[Orchestrator] = None,
) -> None:
    """
    Render main tab entry point.
    """

    try:

        view = MainTab(
            orchestrator=orchestrator
        )

        view.render()


    except Exception as exc:

        logger.exception(
            "Main tab rendering failed."
        )

        st.error(
            str(exc)
        )


# ==============================================================================
# Utility Actions
# ==============================================================================


def show_pipeline_information() -> None:
    """
    Display pipeline overview.
    """

    st.info(
        """
        Pipeline:

        Upload Video
        ↓
        Scene Analysis
        ↓
        AI Prompt Enhancement
        ↓
        Music Generation
        ↓
        Audio Processing
        ↓
        Mastering
        ↓
        Export
        """
    )


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "MainTabConfig",
    "MainTab",
    "render_main_tab",
    "show_pipeline_information",
]
