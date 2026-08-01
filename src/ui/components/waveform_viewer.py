"""
MystoriumX AI Studio
Waveform Viewer Component

File:
src/ui/components/waveform_viewer.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import streamlit as st

from src.core.exceptions import AudioProcessingError
from src.core.security import ensure_safe_path
from src.ui.state import (
    SessionKeys,
    add_log,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Waveform Models
# ==============================================================================


@dataclass(slots=True, frozen=True)
class WaveformData:
    """
    Waveform data container.
    """

    samples: list[float]

    sample_rate: int

    duration: float

    channels: int = 1


@dataclass(slots=True, frozen=True)
class WaveformViewerConfig:
    """
    Waveform viewer configuration.
    """

    height: int = 300

    max_points: int = 2000

    show_axis: bool = True


# ==============================================================================
# Waveform Viewer Component
# ==============================================================================


class WaveformViewer:
    """
    Streamlit waveform visualization component.
    """

    def __init__(
        self,
        config: WaveformViewerConfig | None = None,
    ) -> None:

        self.config = (
            config
            if config
            else WaveformViewerConfig()
        )


    def render(
        self,
        waveform: WaveformData,
    ) -> None:
        """
        Render waveform visualization.
        """

        if not waveform.samples:
            raise AudioProcessingError(
                "Waveform data is empty."
            )

        chart_data = self._prepare_samples(
            waveform.samples
        )

        st.line_chart(
            chart_data,
            height=self.config.height,
        )

        add_log(
            "Waveform rendered."
        )

        logger.info(
            "Waveform displayed successfully."
        )


    def _prepare_samples(
        self,
        samples: list[float],
    ) -> list[float]:
        """
        Reduce waveform points for UI.
        """

        if len(samples) <= self.config.max_points:
            return samples

        indexes = np.linspace(
            0,
            len(samples) - 1,
            self.config.max_points,
            dtype=int,
        )

        return [
            samples[index]
            for index in indexes
        ]
      # ==============================================================================
# Waveform File Loader
# ==============================================================================


def load_waveform_file(
    waveform_path: Path,
    sample_rate: int,
    duration: float,
) -> WaveformData:
    """
    Load waveform data from generated waveform file.
    """

    waveform_path = ensure_safe_path(
        waveform_path
    )

    if not waveform_path.exists():

        raise AudioProcessingError(
            f"Waveform file not found: {waveform_path}"
        )

    try:

        data = np.load(
            waveform_path
        )

        samples = (
            data.tolist()
            if isinstance(
                data,
                np.ndarray,
            )
            else list(data)
        )

        waveform = WaveformData(
            samples=samples,
            sample_rate=sample_rate,
            duration=duration,
        )

        st.session_state[
            SessionKeys.WAVEFORM
        ] = waveform

        logger.info(
            "Waveform loaded: %s",
            waveform_path,
        )

        return waveform

    except Exception as exc:

        logger.exception(
            "Waveform loading failed."
        )

        raise AudioProcessingError(
            "Unable to load waveform data."
        ) from exc


# ==============================================================================
# Waveform State Management
# ==============================================================================


def set_waveform(
    waveform: WaveformData,
) -> None:
    """
    Store waveform data.
    """

    if not isinstance(
        waveform,
        WaveformData,
    ):
        raise TypeError(
            "Invalid waveform object."
        )

    st.session_state[
        SessionKeys.WAVEFORM
    ] = waveform

    add_log(
        "Waveform data stored."
    )


def get_waveform() -> Optional[WaveformData]:
    """
    Return stored waveform.
    """

    waveform = st.session_state.get(
        SessionKeys.WAVEFORM
    )

    if isinstance(
        waveform,
        WaveformData,
    ):
        return waveform

    return None


def clear_waveform() -> None:
    """
    Remove waveform state.
    """

    if SessionKeys.WAVEFORM in st.session_state:

        del st.session_state[
            SessionKeys.WAVEFORM
        ]

        add_log(
            "Waveform cleared."
        )

        logger.info(
            "Waveform state cleared."
        )
      # ==============================================================================
# Waveform Display Helpers
# ==============================================================================


def render_waveform(
    waveform: WaveformData | None = None,
) -> None:
    """
    Render waveform viewer.
    """

    if waveform is None:

        waveform = get_waveform()

    if waveform is None:

        st.info(
            "No waveform data available."
        )

        return

    viewer = WaveformViewer()

    viewer.render(
        waveform
    )


def waveform_statistics(
    waveform: WaveformData,
) -> dict[str, float | int]:
    """
    Generate waveform statistics.
    """

    samples = np.asarray(
        waveform.samples,
        dtype=float,
    )

    if samples.size == 0:

        return {
            "samples": 0,
            "peak": 0.0,
            "rms": 0.0,
        }

    peak = float(
        np.max(
            np.abs(samples)
        )
    )

    rms = float(
        np.sqrt(
            np.mean(
                np.square(samples)
            )
        )
    )

    return {
        "samples": int(
            samples.size
        ),
        "peak": peak,
        "rms": rms,
        "duration": waveform.duration,
        "sample_rate": waveform.sample_rate,
    }


def show_waveform_statistics(
    waveform: WaveformData,
) -> None:
    """
    Display waveform analytics.
    """

    st.json(
        waveform_statistics(
            waveform
        )
    )


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "WaveformData",
    "WaveformViewerConfig",
    "WaveformViewer",
    "load_waveform_file",
    "set_waveform",
    "get_waveform",
    "clear_waveform",
    "render_waveform",
    "waveform_statistics",
    "show_waveform_statistics",
]
