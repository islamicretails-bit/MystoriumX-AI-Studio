"""
MystoriumX AI Studio
Advanced Tab View

File:
src/ui/views/advanced_tab.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import streamlit as st

from src.core.config import get_settings
from src.ui.components.log_viewer import (
    render_log_viewer,
)
from src.ui.state import (
    export_state,
    get_project_state,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Advanced Configuration
# ==============================================================================


@dataclass(slots=True, frozen=True)
class AdvancedTabConfig:
    """
    Advanced tab configuration.
    """

    title: str = (
        "Advanced Controls"
    )

    show_settings: bool = True

    show_system_info: bool = True

    show_logs: bool = True


# ==============================================================================
# Advanced View
# ==============================================================================


class AdvancedTab:
    """
    Advanced application controls.
    """

    def __init__(
        self,
        config: Optional[AdvancedTabConfig] = None,
    ) -> None:

        self.config = (
            config
            if config
            else AdvancedTabConfig()
        )


    def render(
        self,
    ) -> None:
        """
        Render advanced tab.
        """

        st.header(
            self.config.title
        )


        if self.config.show_settings:

            self._render_settings()


        if self.config.show_system_info:

            self._render_system_information()


        if self.config.show_logs:

            self._render_logs()
          # ==============================================================================
# Settings Section
# ==============================================================================


    def _render_settings(
        self,
    ) -> None:
        """
        Render application settings.
        """

        st.subheader(
            "Application Settings"
        )

        try:

            settings = get_settings()

            settings_data: Dict[str, Any] = (
                settings.model_dump()
                if hasattr(
                    settings,
                    "model_dump",
                )
                else vars(settings)
            )

            st.json(
                settings_data
            )


        except Exception as exc:

            logger.exception(
                "Settings rendering failed."
            )

            st.warning(
                str(exc)
            )


# ==============================================================================
# System Information
# ==============================================================================


    def _render_system_information(
        self,
    ) -> None:
        """
        Render system diagnostics.
        """

        st.subheader(
            "System Information"
        )

        state = export_state()

        system_info = {
            "Project State":
                state.get(
                    "project",
                    {},
                ),

            "Pipeline State":
                state.get(
                    "progress",
                    {},
                ),
        }


        st.json(
            system_info
        )


# ==============================================================================
# Logs Section
# ==============================================================================


    def _render_logs(
        self,
    ) -> None:
        """
        Render application logs.
        """

        st.subheader(
            "System Logs"
        )

        render_log_viewer()
      # ==============================================================================
# Advanced Export Controls
# ==============================================================================


    def _render_export_controls(
        self,
    ) -> None:
        """
        Render state export controls.
        """

        st.subheader(
            "Export Diagnostics"
        )

        try:

            state = export_state()

            export_data = (
                str(state)
            )

            st.download_button(
                label="Export Session State",
                data=export_data,
                file_name="mysteriumx_session_state.json",
                mime="application/json",
            )


        except Exception as exc:

            logger.exception(
                "State export failed."
            )

            st.error(
                str(exc)
            )


# ==============================================================================
# Public Renderer
# ==============================================================================


def render_advanced_tab() -> None:
    """
    Render advanced tab entry point.
    """

    try:

        view = AdvancedTab()

        view.render()

    except Exception as exc:

        logger.exception(
            "Advanced tab rendering failed."
        )

        st.error(
            str(exc)
        )


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "AdvancedTabConfig",
    "AdvancedTab",
    "render_advanced_tab",
]
