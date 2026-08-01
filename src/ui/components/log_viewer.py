"""
MystoriumX AI Studio
Log Viewer Component

File:
src/ui/components/log_viewer.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import streamlit as st

from src.ui.state import (
    add_log,
    clear_logs,
    get_logs,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Log Models
# ==============================================================================


class LogLevel(str, Enum):
    """
    Application log levels.
    """

    INFO = "INFO"

    WARNING = "WARNING"

    ERROR = "ERROR"

    DEBUG = "DEBUG"


@dataclass(slots=True, frozen=True)
class LogEntry:
    """
    Structured log entry.
    """

    message: str

    level: LogLevel = LogLevel.INFO

    timestamp: Optional[str] = None


@dataclass(slots=True, frozen=True)
class LogViewerConfig:
    """
    Log viewer configuration.
    """

    height: int = 350

    show_controls: bool = True

    max_entries: int = 500


# ==============================================================================
# Log Viewer Component
# ==============================================================================


class LogViewer:
    """
    Streamlit application log viewer.
    """

    def __init__(
        self,
        config: LogViewerConfig | None = None,
    ) -> None:

        self.config = (
            config
            if config
            else LogViewerConfig()
        )


    def render(
        self,
        logs: Optional[list[str]] = None,
    ) -> None:
        """
        Render log viewer.
        """

        if logs is None:
            logs = get_logs()

        logs = logs[
            -self.config.max_entries:
        ]

        if self.config.show_controls:

            self._render_controls()


        if not logs:

            st.info(
                "No logs available."
            )

            return


        self._render_logs(
            logs
        )


    def _render_logs(
        self,
        logs: list[str],
    ) -> None:
        """
        Display logs.
        """

        content = "\n".join(
            logs
        )

        st.text_area(
            "System Logs",
            value=content,
            height=self.config.height,
            disabled=True,
        )

        logger.debug(
            "Displayed %s log entries.",
            len(logs),
        )


    def _render_controls(
        self,
    ) -> None:
        """
        Render log controls.
        """

        if st.button(
            "Clear Logs"
        ):

            clear_logs()

            add_log(
                "Logs cleared by user."
            )

            st.rerun()
          # ==============================================================================
# Log Management Helpers
# ==============================================================================


def add_structured_log(
    entry: LogEntry,
) -> None:
    """
    Add structured log entry.
    """

    if not isinstance(
        entry,
        LogEntry,
    ):
        raise TypeError(
            "Invalid log entry."
        )

    prefix = entry.level.value

    if entry.timestamp:

        message = (
            f"{entry.timestamp} "
            f"[{prefix}] "
            f"{entry.message}"
        )

    else:

        message = (
            f"[{prefix}] "
            f"{entry.message}"
        )

    add_log(
        message
    )


def get_filtered_logs(
    level: LogLevel | None = None,
) -> list[str]:
    """
    Return filtered logs.
    """

    logs = get_logs()

    if level is None:
        return logs

    marker = (
        f"[{level.value}]"
    )

    return [
        log
        for log in logs
        if marker in log
    ]


def log_info(
    message: str,
) -> None:
    """
    Add information log.
    """

    add_structured_log(
        LogEntry(
            message=message,
            level=LogLevel.INFO,
        )
    )


def log_warning(
    message: str,
) -> None:
    """
    Add warning log.
    """

    add_structured_log(
        LogEntry(
            message=message,
            level=LogLevel.WARNING,
        )
    )


def log_error(
    message: str,
) -> None:
    """
    Add error log.
    """

    add_structured_log(
        LogEntry(
            message=message,
            level=LogLevel.ERROR,
        )
    )


# ==============================================================================
# Public Renderer
# ==============================================================================


def render_log_viewer(
    logs: Optional[list[str]] = None,
) -> None:
    """
    Render default log viewer.
    """

    viewer = LogViewer()

    viewer.render(
        logs
    )
  # ==============================================================================
# Log Export Utilities
# ==============================================================================


def export_logs() -> str:
    """
    Export current logs as text.
    """

    logs = get_logs()

    return "\n".join(
        logs
    )


def download_logs() -> None:
    """
    Provide log download button.
    """

    content = export_logs()

    if not content:

        st.warning(
            "No logs available for export."
        )

        return


    st.download_button(
        label="Download Logs",
        data=content,
        file_name="mysteriumx_logs.txt",
        mime="text/plain",
    )


# ==============================================================================
# Default Instance
# ==============================================================================


_log_viewer = LogViewer()


def show_logs() -> None:
    """
    Public log viewer entry point.
    """

    try:

        _log_viewer.render()

    except Exception as exc:

        logger.exception(
            "Log viewer failed."
        )

        st.error(
            str(exc)
        )


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "LogLevel",
    "LogEntry",
    "LogViewerConfig",
    "LogViewer",
    "add_structured_log",
    "get_filtered_logs",
    "log_info",
    "log_warning",
    "log_error",
    "render_log_viewer",
    "export_logs",
    "download_logs",
    "show_logs",
]
