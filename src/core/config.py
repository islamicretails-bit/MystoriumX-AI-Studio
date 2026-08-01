"""
MystoriumX AI Studio
Core Configuration

File:
src/core/config.py

Part 1/3
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)


# ==============================================================================
# Base Directories
# ==============================================================================


@dataclass(slots=True, frozen=True)
class DirectoryConfig:
    """
    Central directory configuration.
    """

    root: Path

    assets: Path
    configs: Path
    data: Path
    models: Path

    src: Path

    exports: Path
    uploads: Path
    temp: Path
    cache: Path
    logs: Path

    frames: Path
    scenes: Path
    prompts: Path
    waveform: Path
    music: Path
    analytics: Path

    @classmethod
    def create(cls, root: Optional[Path] = None) -> "DirectoryConfig":

        root_dir = (
            root
            if root is not None
            else Path(__file__).resolve().parents[2]
        )

        return cls(
            root=root_dir,
            assets=root_dir / "assets",
            configs=root_dir / "configs",
            data=root_dir / "data",
            models=root_dir / "models",
            src=root_dir / "src",
            exports=root_dir / "exports",
            uploads=root_dir / "uploads",
            temp=root_dir / "temp",
            cache=root_dir / "cache",
            logs=root_dir / "logs",
            frames=root_dir / "data" / "frames",
            scenes=root_dir / "data" / "scenes",
            prompts=root_dir / "data" / "prompts",
            waveform=root_dir / "data" / "waveforms",
            music=root_dir / "data" / "music",
            analytics=root_dir / "data" / "analytics",
        )

    def ensure_directories(self) -> None:

        directories = (
            self.assets,
            self.configs,
            self.data,
            self.exports,
            self.uploads,
            self.temp,
            self.cache,
            self.logs,
            self.frames,
            self.scenes,
            self.prompts,
            self.waveform,
            self.music,
            self.analytics,
        )

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def to_dict(self) -> Dict[str, str]:
        return {
            key: str(value)
            for key, value in self.__dict__.items()
        }


# ==============================================================================
# Application Configuration
# ==============================================================================


@dataclass(slots=True)
class ApplicationConfig:
    """
    Core application configuration.
    """

    application_name: str = "MystoriumX AI Studio"

    version: str = "1.0.0"

    organization: str = "MystoriumX"

    debug: bool = False

    environment: str = "production"

    streamlit_title: str = "MystoriumX AI Studio"

    page_icon: str = "🎬"

    page_layout: str = "wide"

    max_upload_size_mb: int = 2048

    allowed_video_extensions: tuple[str, ...] = (
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
        ".m4v",
    )

    allowed_audio_extensions: tuple[str, ...] = (
        ".wav",
        ".mp3",
        ".aac",
        ".ogg",
        ".flac",
    )

    auto_save: bool = True

    auto_cleanup: bool = False

    telemetry_enabled: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


# ==============================================================================
# AI Configuration
# ==============================================================================


@dataclass(slots=True)
class AIConfig:

    default_model: str = "musicgen-large"

    prompt_enhancer_model: str = "llama3"

    image_caption_model: str = "blip2"

    scene_model: str = "pyannote"

    max_prompt_length: int = 1024

    max_music_duration: int = 300

    random_seed: Optional[int] = None

    enable_gpu: bool = True

    enable_half_precision: bool = True

    device: str = "auto"

    batch_size: int = 1

    num_workers: int = 4

    cache_models: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


# ==============================================================================
# Audio Configuration
# ==============================================================================


@dataclass(slots=True)
class AudioConfig:

    sample_rate: int = 48000

    channels: int = 2

    bit_depth: int = 24

    target_lufs: float = -14.0

    true_peak_dbtp: float = -1.0

    output_format: str = "wav"

    normalize: bool = True

    enable_mastering: bool = True

    enable_compression: bool = True

    enable_equalizer: bool = True

    enable_limiter: bool = True

    enable_voice_ducking: bool = True

    export_waveform: bool = True

    waveform_width: int = 1600

    waveform_height: int = 350

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()
      # ==============================================================================
# Video Configuration
# ==============================================================================


@dataclass(slots=True)
class VideoConfig:

    supported_extensions: tuple[str, ...] = (
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
        ".m4v",
    )

    preferred_extension: str = ".mp4"

    max_resolution_width: int = 7680
    max_resolution_height: int = 4320

    default_frame_extraction_rate: float = 1.0
    scene_detection_threshold: float = 0.35
    minimum_scene_duration: float = 1.0

    image_analysis_batch_size: int = 8

    save_keyframes: bool = True
    save_scene_frames: bool = True

    ffmpeg_threads: int = 4

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


# ==============================================================================
# Export Configuration
# ==============================================================================


@dataclass(slots=True)
class ExportConfig:

    export_audio: bool = True
    export_waveform: bool = True
    export_analytics: bool = True
    export_scene_json: bool = True
    export_project_json: bool = True

    overwrite_existing: bool = False

    audio_format: str = "wav"

    waveform_image_format: str = "png"

    analytics_format: str = "json"

    compression_enabled: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


# ==============================================================================
# Logging Configuration
# ==============================================================================


@dataclass(slots=True)
class LoggingConfig:

    level: str = "INFO"

    log_filename: str = "mystoriumx.log"

    log_format: str = (
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )

    console_logging: bool = True

    file_logging: bool = True

    max_file_size_mb: int = 20

    backup_count: int = 10

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


# ==============================================================================
# Security Configuration
# ==============================================================================


@dataclass(slots=True)
class SecurityConfig:

    allow_remote_models: bool = False

    verify_ssl: bool = True

    sanitize_filenames: bool = True

    maximum_filename_length: int = 255

    allowed_protocols: tuple[str, ...] = (
        "https",
        "file",
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


# ==============================================================================
# Runtime Configuration
# ==============================================================================


@dataclass(slots=True)
class RuntimeConfig:

    application: ApplicationConfig = field(
        default_factory=ApplicationConfig
    )

    directories: DirectoryConfig = field(
        default_factory=DirectoryConfig.create
    )

    ai: AIConfig = field(
        default_factory=AIConfig
    )

    audio: AudioConfig = field(
        default_factory=AudioConfig
    )

    video: VideoConfig = field(
        default_factory=VideoConfig
    )

    export: ExportConfig = field(
        default_factory=ExportConfig
    )

    logging: LoggingConfig = field(
        default_factory=LoggingConfig
    )

    security: SecurityConfig = field(
        default_factory=SecurityConfig
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def initialize(self) -> None:
        """
        Prepare runtime environment.
        """

        self.directories.ensure_directories()

        os.environ.setdefault(
            "PYTHONUTF8",
            "1",
        )

        logger.info(
            "Runtime configuration initialized."
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "application": self.application.to_dict(),
            "directories": self.directories.to_dict(),
            "ai": self.ai.to_dict(),
            "audio": self.audio.to_dict(),
            "video": self.video.to_dict(),
            "export": self.export.to_dict(),
            "logging": self.logging.to_dict(),
            "security": self.security.to_dict(),
            "metadata": self.metadata,
        }
      # ==============================================================================
# Global Configuration
# ==============================================================================


_config_instance: RuntimeConfig | None = None


def get_config() -> RuntimeConfig:
    """
    Returns the singleton RuntimeConfig instance.
    """

    global _config_instance

    if _config_instance is None:
        _config_instance = RuntimeConfig()
        _config_instance.initialize()

    return _config_instance


def reload_config() -> RuntimeConfig:
    """
    Recreate the global configuration instance.
    """

    global _config_instance

    _config_instance = RuntimeConfig()
    _config_instance.initialize()

    return _config_instance


config = get_config()


# ==============================================================================
# Environment Helpers
# ==============================================================================


def get_environment_variable(
    name: str,
    default: Optional[str] = None,
) -> Optional[str]:
    """
    Read an environment variable.
    """

    return os.getenv(name, default)


def is_debug_mode() -> bool:
    """
    Returns True when debug mode is enabled.
    """

    return config.application.debug


def is_production() -> bool:
    """
    Returns True when running in production.
    """

    return (
        config.application.environment.lower()
        == "production"
    )


def is_development() -> bool:
    """
    Returns True when running in development.
    """

    return (
        config.application.environment.lower()
        == "development"
    )


def project_root() -> Path:
    """
    Returns the project root directory.
    """

    return config.directories.root


def uploads_directory() -> Path:
    return config.directories.uploads


def exports_directory() -> Path:
    return config.directories.exports


def logs_directory() -> Path:
    return config.directories.logs


def frames_directory() -> Path:
    return config.directories.frames


def scenes_directory() -> Path:
    return config.directories.scenes


def prompts_directory() -> Path:
    return config.directories.prompts


def music_directory() -> Path:
    return config.directories.music


def waveform_directory() -> Path:
    return config.directories.waveform


def analytics_directory() -> Path:
    return config.directories.analytics


__all__ = [
    "ApplicationConfig",
    "AIConfig",
    "AudioConfig",
    "VideoConfig",
    "ExportConfig",
    "LoggingConfig",
    "SecurityConfig",
    "DirectoryConfig",
    "RuntimeConfig",
    "config",
    "get_config",
    "reload_config",
    "get_environment_variable",
    "is_debug_mode",
    "is_production",
    "is_development",
    "project_root",
    "uploads_directory",
    "exports_directory",
    "logs_directory",
    "frames_directory",
    "scenes_directory",
    "prompts_directory",
    "music_directory",
    "waveform_directory",
    "analytics_directory",
]
