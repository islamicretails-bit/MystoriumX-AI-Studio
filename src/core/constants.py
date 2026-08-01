"""
MystoriumX AI Studio
Core Constants

File:
src/core/constants.py

Production Ready
Python 3.11
"""

from __future__ import annotations

from pathlib import Path
from typing import Final


# ==============================================================================
# Application
# ==============================================================================

APP_NAME: Final[str] = "MystoriumX AI Studio"
APP_VERSION: Final[str] = "1.0.0"
APP_AUTHOR: Final[str] = "MystoriumX"
APP_DESCRIPTION: Final[str] = (
    "Hollywood Grade AI Documentary Audio Production Platform"
)

ORGANIZATION_NAME: Final[str] = "MystoriumX"

DEFAULT_LANGUAGE: Final[str] = "en"

DEFAULT_TIMEZONE: Final[str] = "UTC"


# ==============================================================================
# Paths
# ==============================================================================

ROOT_DIRECTORY: Final[Path] = Path(__file__).resolve().parents[2]

ASSETS_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "assets"
CONFIG_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "configs"
DATA_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "data"
MODEL_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "models"

UPLOAD_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "uploads"
EXPORT_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "exports"

CACHE_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "cache"
TEMP_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "temp"
LOG_DIRECTORY: Final[Path] = ROOT_DIRECTORY / "logs"

FRAME_DIRECTORY: Final[Path] = DATA_DIRECTORY / "frames"
SCENE_DIRECTORY: Final[Path] = DATA_DIRECTORY / "scenes"
PROMPT_DIRECTORY: Final[Path] = DATA_DIRECTORY / "prompts"
MUSIC_DIRECTORY: Final[Path] = DATA_DIRECTORY / "music"
WAVEFORM_DIRECTORY: Final[Path] = DATA_DIRECTORY / "waveforms"
ANALYTICS_DIRECTORY: Final[Path] = DATA_DIRECTORY / "analytics"


# ==============================================================================
# Supported Formats
# ==============================================================================

SUPPORTED_VIDEO_EXTENSIONS: Final[tuple[str, ...]] = (
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".m4v",
)

SUPPORTED_AUDIO_EXTENSIONS: Final[tuple[str, ...]] = (
    ".wav",
    ".mp3",
    ".aac",
    ".ogg",
    ".flac",
)

SUPPORTED_IMAGE_EXTENSIONS: Final[tuple[str, ...]] = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
)


# ==============================================================================
# Audio
# ==============================================================================

DEFAULT_SAMPLE_RATE: Final[int] = 48_000

DEFAULT_CHANNELS: Final[int] = 2

DEFAULT_BIT_DEPTH: Final[int] = 24

DEFAULT_TARGET_LUFS: Final[float] = -14.0

DEFAULT_TRUE_PEAK_DBTP: Final[float] = -1.0

DEFAULT_OUTPUT_FORMAT: Final[str] = "wav"

DEFAULT_WAVEFORM_WIDTH: Final[int] = 1600
DEFAULT_WAVEFORM_HEIGHT: Final[int] = 350


# ==============================================================================
# AI Models
# ==============================================================================

DEFAULT_MUSIC_MODEL: Final[str] = "musicgen-large"

DEFAULT_PROMPT_MODEL: Final[str] = "llama3"

DEFAULT_IMAGE_MODEL: Final[str] = "blip2"

DEFAULT_SCENE_MODEL: Final[str] = "pyannote"

DEFAULT_DEVICE: Final[str] = "auto"


# ==============================================================================
# Processing
# ==============================================================================

DEFAULT_BATCH_SIZE: Final[int] = 1

DEFAULT_WORKERS: Final[int] = 4

DEFAULT_FRAME_EXTRACTION_RATE: Final[float] = 1.0

DEFAULT_SCENE_THRESHOLD: Final[float] = 0.35

DEFAULT_MIN_SCENE_DURATION: Final[float] = 1.0

DEFAULT_MAX_PROMPT_LENGTH: Final[int] = 1024

DEFAULT_MAX_MUSIC_DURATION: Final[int] = 300


# ==============================================================================
# Logging
# ==============================================================================

LOG_FORMAT: Final[str] = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

DEFAULT_LOG_LEVEL: Final[str] = "INFO"

LOG_FILE_NAME: Final[str] = "mystoriumx.log"

MAX_LOG_FILE_SIZE_MB: Final[int] = 20

LOG_BACKUP_COUNT: Final[int] = 10


# ==============================================================================
# Streamlit
# ==============================================================================

PAGE_TITLE: Final[str] = APP_NAME

PAGE_ICON: Final[str] = "🎬"

PAGE_LAYOUT: Final[str] = "wide"

INITIAL_SIDEBAR_STATE: Final[str] = "expanded"


# ==============================================================================
# Upload Limits
# ==============================================================================

MAX_UPLOAD_SIZE_MB: Final[int] = 2048

MAX_VIDEO_DURATION_SECONDS: Final[int] = 60 * 60 * 4

MAX_AUDIO_DURATION_SECONDS: Final[int] = 60 * 60


# ==============================================================================
# Export
# ==============================================================================

EXPORT_AUDIO: Final[bool] = True
EXPORT_WAVEFORM: Final[bool] = True
EXPORT_ANALYTICS: Final[bool] = True
EXPORT_SCENE_JSON: Final[bool] = True
EXPORT_PROJECT_JSON: Final[bool] = True


# ==============================================================================
# Security
# ==============================================================================

VERIFY_SSL: Final[bool] = True

SANITIZE_FILENAMES: Final[bool] = True

MAX_FILENAME_LENGTH: Final[int] = 255


# ==============================================================================
# Pipeline
# ==============================================================================

PIPELINE_STAGES: Final[tuple[str, ...]] = (
    "Upload",
    "Video Analysis",
    "Frame Extraction",
    "Scene Detection",
    "Image Analysis",
    "Prompt Enhancement",
    "Music Prompt Builder",
    "Music Generation",
    "Audio Processing",
    "Mastering",
    "Waveform Generation",
    "Analytics",
    "Export",
)


# ==============================================================================
# Exit Codes
# ==============================================================================

EXIT_SUCCESS: Final[int] = 0
EXIT_FAILURE: Final[int] = 1


__all__ = [
    name
    for name in globals()
    if name.isupper()
]
