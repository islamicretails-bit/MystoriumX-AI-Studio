"""
MystoriumX AI Studio
UI Theme System

File:
src/ui/theme.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Final

import streamlit as st

logger = logging.getLogger(__name__)


# ==============================================================================
# Theme Configuration
# ==============================================================================


@dataclass(slots=True, frozen=True)
class ThemeConfig:
    """
    UI theme configuration.
    """

    name: str

    primary_color: str

    background_color: str

    secondary_background: str

    text_color: str

    border_color: str

    success_color: str

    warning_color: str

    error_color: str

    font_family: str


# ==============================================================================
# Default Theme
# ==============================================================================


MYSTORIUMX_THEME: Final[ThemeConfig] = ThemeConfig(
    name="MystoriumX Dark Cinema",

    primary_color="#00C2FF",

    background_color="#0B0F19",

    secondary_background="#111827",

    text_color="#F8FAFC",

    border_color="#334155",

    success_color="#22C55E",

    warning_color="#F59E0B",

    error_color="#EF4444",

    font_family="Inter, sans-serif",
)


# ==============================================================================
# Theme CSS Builder
# ==============================================================================


def build_theme_css(
    theme: ThemeConfig = MYSTORIUMX_THEME,
) -> str:
    """
    Generate application CSS.
    """

    return f"""
    <style>

    html, body, [class*="css"] {{
        font-family: {theme.font_family};
        color: {theme.text_color};
    }}

    .stApp {{
        background-color: {theme.background_color};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {theme.secondary_background};
    }}

    .mx-card {{
        background:
        {theme.secondary_background};

        border:
        1px solid {theme.border_color};

        border-radius:
        12px;

        padding:
        1.2rem;

        margin-bottom:
        1rem;
    }}

    .mx-title {{
        color:
        {theme.primary_color};

        font-size:
        2rem;

        font-weight:
        700;
    }}

    .mx-success {{
        color:
        {theme.success_color};
    }}

    .mx-warning {{
        color:
        {theme.warning_color};
    }}

    .mx-error {{
        color:
        {theme.error_color};
    }}

    </style>
    """
  # ==============================================================================
# Theme Management
# ==============================================================================


class ThemeManager:
    """
    Streamlit theme manager.
    """

    def __init__(
        self,
        theme: ThemeConfig = MYSTORIUMX_THEME,
    ) -> None:

        self.theme = theme


    def apply(
        self,
    ) -> None:
        """
        Apply theme CSS to Streamlit application.
        """

        try:

            st.markdown(
                build_theme_css(
                    self.theme
                ),
                unsafe_allow_html=True,
            )

            logger.info(
                "Theme applied: %s",
                self.theme.name,
            )

        except Exception:

            logger.exception(
                "Failed to apply UI theme."
            )

            raise


    def get_theme(
        self,
    ) -> ThemeConfig:
        """
        Return current theme configuration.
        """

        return self.theme


    def update_theme(
        self,
        theme: ThemeConfig,
    ) -> None:
        """
        Update active theme.
        """

        if not isinstance(
            theme,
            ThemeConfig,
        ):
            raise TypeError(
                "Invalid theme configuration."
            )

        self.theme = theme


# ==============================================================================
# UI Components Styling
# ==============================================================================


def card(
    content: str,
) -> str:
    """
    Create a styled UI card.
    """

    return f"""
    <div class="mx-card">
        {content}
    </div>
    """


def title(
    text: str,
) -> str:
    """
    Create a styled title.
    """

    return f"""
    <div class="mx-title">
        {text}
    </div>
    """


def success_message(
    text: str,
) -> str:
    """
    Create success message.
    """

    return f"""
    <div class="mx-success">
        {text}
    </div>
    """


def warning_message(
    text: str,
) -> str:
    """
    Create warning message.
    """

    return f"""
    <div class="mx-warning">
        {text}
    </div>
    """


def error_message(
    text: str,
) -> str:
    """
    Create error message.
    """

    return f"""
    <div class="mx-error">
        {text}
    </div>
    """
  # ==============================================================================
# Global Theme Instance
# ==============================================================================


_theme_manager = ThemeManager()


def apply_theme() -> None:
    """
    Apply default MystoriumX theme.
    """

    _theme_manager.apply()


def get_current_theme() -> ThemeConfig:
    """
    Return active UI theme.
    """

    return _theme_manager.get_theme()


def set_theme(
    theme: ThemeConfig,
) -> None:
    """
    Replace active UI theme.
    """

    _theme_manager.update_theme(theme)


# ==============================================================================
# Streamlit Page Configuration
# ==============================================================================


def configure_page(
    title_text: str = "MystoriumX AI Studio",
    icon: str = "🎬",
    layout: str = "wide",
) -> None:
    """
    Configure Streamlit page settings.
    """

    try:

        st.set_page_config(
            page_title=title_text,
            page_icon=icon,
            layout=layout,
            initial_sidebar_state="expanded",
        )

        logger.info(
            "Streamlit page configured."
        )

    except Exception:

        logger.exception(
            "Unable to configure Streamlit page."
        )

        raise


# ==============================================================================
# Exports
# ==============================================================================


__all__ = [
    "ThemeConfig",
    "ThemeManager",
    "MYSTORIUMX_THEME",
    "build_theme_css",
    "apply_theme",
    "get_current_theme",
    "set_theme",
    "configure_page",
    "card",
    "title",
    "success_message",
    "warning_message",
    "error_message",
]
