"""
MystoriumX AI Studio
Audio Player Component

File:
src/ui/components/audio_player.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import streamlit as st

from src.core.exceptions import AudioProcessingError
from src.core.security import ensure_safe_path
from src.ui.state import (
    SessionKeys,
    add_log,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Audio Player Models
# ==============================================================================


@dataclass(slots=True, frozen=True)
class AudioTrack:
    """
    Audio track information.
    """

    path: Path

    title: str

    duration: Optional[float] = None

    sample_rate: Optional[int] = None

    format: Optional[str] = None


@dataclass(slots=True, frozen=True)
class AudioPlayerConfig:
    """
    Audio player configuration.
    """

    autoplay: bool = False

    loop: bool = False

    format: str = "audio/wav"


# ==============================================================================
# Audio Player Component
# ==============================================================================


class AudioPlayer:
    """
    Streamlit audio player component.
    """

    def __init__(
        self,
        config: AudioPlayerConfig | None = None,
    ) -> None:

        self.config = (
            config
            if config
            else AudioPlayerConfig()
        )


    def render(
        self,
        track: AudioTrack,
    ) -> None:
        """
        Render audio player.
        """

        self._validate_track(
            track
        )

        try:

            audio_bytes = (
                track.path.read_bytes()
            )

            st.audio(
                audio_bytes,
                format=self.config.format,
                loop=self.config.loop,
            )

            st.caption(
                track.title
            )

            add_log(
                f"Playing audio: {track.title}"
            )

            logger.info(
                "Audio rendered: %s",
                track.path,
            )

        except Exception as exc:

            logger.exception(
                "Audio playback failed."
            )

            raise AudioProcessingError(
                "Unable to render audio player."
            ) from exc


    def _validate_track(
        self,
        track: AudioTrack,
    ) -> None:
        """
        Validate audio track.
        """

        path = ensure_safe_path(
            track.path
        )
# ==============================================================================
# Audio Player State Management
# ==============================================================================


def set_audio_track(
    track: AudioTrack,
) -> None:
    """
    Store active audio track in session state.
    """

    if not isinstance(
        track,
        AudioTrack,
    ):
        raise TypeError(
            "Invalid audio track."
        )

    st.session_state[
        SessionKeys.GENERATED_AUDIO
    ] = track

    add_log(
        f"Audio track loaded: {track.title}"
    )

    logger.info(
        "Audio track stored: %s",
        track.title,
    )


def get_audio_track() -> Optional[AudioTrack]:
    """
    Return active audio track.
    """

    track = st.session_state.get(
        SessionKeys.GENERATED_AUDIO
    )

    if isinstance(
        track,
        AudioTrack,
    ):
        return track

    return None


def clear_audio_track() -> None:
    """
    Remove active audio track.
    """

    if SessionKeys.GENERATED_AUDIO in st.session_state:

        del st.session_state[
            SessionKeys.GENERATED_AUDIO
        ]

        add_log(
            "Audio track cleared."
        )

        logger.info(
            "Audio track removed."
        )


# ==============================================================================
# Audio Loading Helpers
# ==============================================================================


def create_audio_track(
    audio_path: Path,
    title: str | None = None,
) -> AudioTrack:
    """
    Create audio track object.
    """

    audio_path = ensure_safe_path(
        audio_path
    )

    if not audio_path.exists():

        raise AudioProcessingError(
            f"Audio file not found: {audio_path}"
        )

    return AudioTrack(
        path=audio_path,
        title=(
            title
            if title
            else audio_path.stem
        ),
        format=audio_path.suffix.lower(),
    )


def render_audio_player(
    track: AudioTrack | None = None,
) -> None:
    """
    Render public audio player.
    """

    if track is None:

        track = get_audio_track()

    if track is None:

        st.info(
            "No generated audio available."
        )

        return

    player = AudioPlayer()

    player.render(
        track
    )
  # ==============================================================================
# Audio Information UI
# ==============================================================================


def show_audio_information(
    track: AudioTrack,
) -> None:
    """
    Display audio track information.
    """

    if not isinstance(
        track,
        AudioTrack,
    ):
        raise TypeError(
            "Invalid audio track."
        )

    details = {
        "Title": track.title,
        "File": track.path.name,
        "Format": (
            track.format
            or track.path.suffix
        ),
    }

    if track.duration is not None:
        details["Duration"] = (
            f"{track.duration:.2f} seconds"
        )

    if track.sample_rate is not None:
        details["Sample Rate"] = (
            f"{track.sample_rate} Hz"
        )

    st.json(
        details
    )


# ==============================================================================
# Default Instance
# ==============================================================================


_audio_player = AudioPlayer()


def play_audio(
    audio_path: Path,
    title: str | None = None,
) -> None:
    """
    Load and play audio.
    """

    try:

        track = create_audio_track(
            audio_path,
            title,
        )

        set_audio_track(
            track
        )

        _audio_player.render(
            track
        )

    except Exception as exc:

        logger.exception(
            "Unable to play audio."
        )

        st.error(
            str(exc)
        )


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "AudioTrack",
    "AudioPlayerConfig",
    "AudioPlayer",
    "create_audio_track",
    "set_audio_track",
    "get_audio_track",
    "clear_audio_track",
    "render_audio_player",
    "show_audio_information",
    "play_audio",
]
        if not path.exists():

            raise AudioProcessingError(
                f"Audio file missing: {path}"
            )

        if not path.is_file():

            raise AudioProcessingError(
                "Audio path is not a file."
            )
          
