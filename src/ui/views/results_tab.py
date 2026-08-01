"""
MystoriumX AI Studio
Results Tab View

File:
src/ui/views/results_tab.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import streamlit as st

from src.ui.components.audio_player import (
    render_audio_player,
    show_audio_information,
)
from src.ui.components.waveform_viewer import (
    render_waveform,
    show_waveform_statistics,
)
from src.ui.state import (
    get_project_state,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Results Configuration
# ==============================================================================


@dataclass(slots=True, frozen=True)
class ResultsTabConfig:
    """
    Results tab configuration.
    """

    title: str = (
        "Production Results"
    )

    show_audio: bool = True

    show_waveform: bool = True

    show_analytics: bool = True


# ==============================================================================
# Results View
# ==============================================================================


class ResultsTab:
    """
    Generated output results dashboard.
    """

    def __init__(
        self,
        config: Optional[ResultsTabConfig] = None,
    ) -> None:

        self.config = (
            config
            if config
            else ResultsTabConfig()
        )


    def render(
        self,
    ) -> None:
        """
        Render results dashboard.
        """

        st.header(
            self.config.title
        )

        project = get_project_state()

        self._render_project_summary(
            project
        )


        if self.config.show_audio:

            self._render_audio_section()


        if self.config.show_waveform:

            self._render_waveform_section()


        if self.config.show_analytics:

            self._render_analytics_section()
          # ==============================================================================
# Project Summary
# ==============================================================================


    def _render_project_summary(
        self,
        project,
    ) -> None:
        """
        Render project information.
        """

        st.subheader(
            "Project Summary"
        )

        summary = {
            "Project Name": project.project_name,
            "Project ID": project.project_id,
            "Video": project.uploaded_video,
            "Audio": project.generated_audio,
        }

        st.json(
            summary
        )


# ==============================================================================
# Audio Results
# ==============================================================================


    def _render_audio_section(
        self,
    ) -> None:
        """
        Render generated audio section.
        """

        st.subheader(
            "Generated Audio"
        )

        try:

            render_audio_player()

            from src.ui.components.audio_player import (
                get_audio_track,
            )

            track = get_audio_track()

            if track:

                show_audio_information(
                    track
                )


        except Exception as exc:

            logger.exception(
                "Audio results rendering failed."
            )

            st.warning(
                str(exc)
            )


# ==============================================================================
# Waveform Results
# ==============================================================================


    def _render_waveform_section(
        self,
    ) -> None:
        """
        Render waveform section.
        """

        st.subheader(
            "Audio Waveform"
        )

        try:

            render_waveform()

            from src.ui.components.waveform_viewer import (
                get_waveform,
            )

            waveform = get_waveform()

            if waveform:

                show_waveform_statistics(
                    waveform
                )


        except Exception as exc:

            logger.exception(
                "Waveform rendering failed."
            )

            st.warning(
                str(exc)
            )
          # ==============================================================================
# Analytics Results
# ==============================================================================


    def _render_analytics_section(
        self,
    ) -> None:
        """
        Render production analytics.
        """

        st.subheader(
            "Production Analytics"
        )

        project = get_project_state()

        analytics: Dict[str, Any] = (
            project.analytics
        )

        if not analytics:

            st.info(
                "Analytics data not available yet."
            )

            return


        st.json(
            analytics
        )


# ==============================================================================
# Export Information
# ==============================================================================


    def _render_export_information(
        self,
        export_path: Optional[str],
    ) -> None:
        """
        Display export result information.
        """

        if not export_path:

            return


        st.success(
            "Export completed."
        )


        st.code(
            export_path
        )


# ==============================================================================
# Public Renderer
# ==============================================================================


def render_results_tab() -> None:
    """
    Render results tab entry point.
    """

    try:

        view = ResultsTab()

        view.render()


    except Exception as exc:

        logger.exception(
            "Results tab rendering failed."
        )

        st.error(
            str(exc)
        )


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "ResultsTabConfig",
    "ResultsTab",
    "render_results_tab",
]
