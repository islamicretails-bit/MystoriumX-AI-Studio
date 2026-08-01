"""
MystoriumX AI Studio
Utility Module

File:
src/utils/video_utils.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2

from src.core.exceptions import VideoProcessingError
from src.core.security import ensure_safe_path

logger = logging.getLogger(__name__)


# ==============================================================================
# Video Metadata
# ==============================================================================


@dataclass(slots=True, frozen=True)
class VideoMetadata:
    """
    Video metadata container.
    """

    path: Path
    width: int
    height: int
    fps: float
    frame_count: int
    duration: float
    codec: str

    @property
    def resolution(self) -> str:
        return f"{self.width}x{self.height}"

    @property
    def aspect_ratio(self) -> float:
        if self.height == 0:
            return 0.0
        return self.width / self.height


# ==============================================================================
# Metadata Reader
# ==============================================================================


def read_video_metadata(
    video_path: Path,
) -> VideoMetadata:
    """
    Read metadata from a video file.
    """

    video_path = ensure_safe_path(video_path)

    if not video_path.exists():
        raise VideoProcessingError(
            f"Video file not found: {video_path}"
        )

    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise VideoProcessingError(
            f"Unable to open video: {video_path}"
        )

    try:
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

        duration = (
            frame_count / fps
            if fps > 0
            else 0.0
        )

        fourcc = int(
            capture.get(cv2.CAP_PROP_FOURCC)
        )

        codec = "".join(
            [
                chr((fourcc >> (8 * i)) & 0xFF)
                for i in range(4)
            ]
        ).strip()

        return VideoMetadata(
            path=video_path,
            width=width,
            height=height,
            fps=fps,
            frame_count=frame_count,
            duration=duration,
            codec=codec,
        )

    finally:
        capture.release()


# ==============================================================================
# Frame Utilities
# ==============================================================================


def frame_to_timestamp(
    frame_number: int,
    fps: float,
) -> float:
    """
    Convert a frame number to seconds.
    """

    if fps <= 0:
        raise VideoProcessingError(
            "FPS must be greater than zero."
        )

    return frame_number / fps


def timestamp_to_frame(
    timestamp: float,
    fps: float,
) -> int:
    """
    Convert seconds to a frame index.
    """

    if fps <= 0:
        raise VideoProcessingError(
            "FPS must be greater than zero."
        )

    return int(timestamp * fps)
  # ==============================================================================
# Resolution Utilities
# ==============================================================================


def is_hd(
    metadata: VideoMetadata,
) -> bool:
    """
    Return True if video is at least HD.
    """

    return (
        metadata.width >= 1280
        and metadata.height >= 720
    )


def is_full_hd(
    metadata: VideoMetadata,
) -> bool:
    """
    Return True if video is Full HD.
    """

    return (
        metadata.width >= 1920
        and metadata.height >= 1080
    )


def is_4k(
    metadata: VideoMetadata,
) -> bool:
    """
    Return True if video is 4K.
    """

    return (
        metadata.width >= 3840
        and metadata.height >= 2160
    )


def total_frames(
    metadata: VideoMetadata,
) -> int:
    """
    Return total frame count.
    """

    return metadata.frame_count


# ==============================================================================
# Duration Utilities
# ==============================================================================


def video_duration(
    metadata: VideoMetadata,
) -> float:
    """
    Return duration in seconds.
    """

    return metadata.duration


def fps_to_frame_interval(
    fps: float,
) -> float:
    """
    Return seconds between frames.
    """

    if fps <= 0:
        raise VideoProcessingError(
            "FPS must be greater than zero."
        )

    return 1.0 / fps


# ==============================================================================
# Validation Utilities
# ==============================================================================


def validate_video_file(
    video_path: Path,
) -> None:
    """
    Validate that a video exists and is readable.
    """

    video_path = ensure_safe_path(video_path)

    if not video_path.exists():
        raise VideoProcessingError(
            f"Video file not found: {video_path}"
        )

    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        capture.release()

        raise VideoProcessingError(
            f"Unable to open video: {video_path}"
        )

    capture.release()
  # ==============================================================================
# Video Helpers
# ==============================================================================


def frame_exists(
    metadata: VideoMetadata,
    frame_number: int,
) -> bool:
    """
    Check whether a frame index is valid.
    """

    return (
        0 <= frame_number < metadata.frame_count
    )


def clamp_frame(
    metadata: VideoMetadata,
    frame_number: int,
) -> int:
    """
    Clamp a frame index to a valid range.
    """

    if metadata.frame_count <= 0:
        return 0

    return max(
        0,
        min(frame_number, metadata.frame_count - 1),
    )


def resolution_string(
    metadata: VideoMetadata,
) -> str:
    """
    Return formatted resolution string.
    """

    return f"{metadata.width}×{metadata.height}"


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "VideoMetadata",
    "read_video_metadata",
    "frame_to_timestamp",
    "timestamp_to_frame",
    "is_hd",
    "is_full_hd",
    "is_4k",
    "total_frames",
    "video_duration",
    "fps_to_frame_interval",
    "validate_video_file",
    "frame_exists",
    "clamp_frame",
    "resolution_string",
]
