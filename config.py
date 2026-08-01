# ============================================================
# MystoriumX AI Studio
# Core Layer - Application Configuration
#
# File:
# app/core/config.py
#
# Responsibility:
# Central configuration management.
#
# Features:
# - Application settings
# - Directory paths
# - AI model configuration
# - Audio settings
# - Environment management
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path
from dataclasses import dataclass
from typing import List
import os
import logging



logger = logging.getLogger(
    "MystoriumX.Config"
)



# ============================================================
# Base Directory
# ============================================================

BASE_DIR = Path(
    __file__
).resolve().parent.parent.parent



# ============================================================
# Application Settings
# ============================================================

@dataclass(frozen=True)
class AppSettings:
    """
    Main application configuration.
    """


    app_name: str = (
        "MystoriumX AI Studio"
    )


    version: str = (
        "1.0.0"
    )


    environment: str = (
        os.getenv(
            "ENVIRONMENT",
            "production"
        )
    )


    debug: bool = (

        os.getenv(
            "DEBUG",
            "false"
        ).lower()

        ==

        "true"

    )



# ============================================================
# Storage Settings
# ============================================================

@dataclass(frozen=True)
class StorageSettings:
    """
    File storage configuration.
    """


    base_path: Path = (

        BASE_DIR

        /

        "storage"

    )


    projects_folder: str = (
        "projects"
    )


    temp_folder: str = (
        "temp"
    )


    upload_folder: str = (
        "uploads"
    )


    output_folder: str = (
        "outputs"
    )



# ============================================================
# AI Model Settings
# ============================================================

@dataclass(frozen=True)
class AISettings:
    """
    Machine learning model configuration.
    """


    musicgen_model: str = (

        "facebook/musicgen-medium"

    )


    vision_model: str = (

        "opencv"

    )


    device: str = (

        os.getenv(

            "AI_DEVICE",

            "cpu"

        )

    )


    supported_models: List[str] = (

        None

    )



# ============================================================
# Audio Settings
# ============================================================

@dataclass(frozen=True)
class AudioSettings:
    """
    Professional audio configuration.
    """


    sample_rate: int = (
        48000
    )


    target_lufs: float = (
        -14.0
    )


    true_peak_limit: float = (
        -1.0
    )


    supported_formats: List[str] = (

        None

    )



# ============================================================
# Video Settings
# ============================================================

@dataclass(frozen=True)
class VideoSettings:
    """
    Video processing configuration.
    """


    supported_formats: List[str] = (

        None

    )


    default_scene_threshold: float = (
        35.0
    )


    frame_sampling_rate: int = (
        5
    )



# ============================================================
# Configuration Loader
# ============================================================

class ConfigManager:
    """
    Central configuration provider.

    Provides access to:

    - Application settings
    - AI settings
    - Audio settings
    - Storage settings

    """



    def __init__(
        self
    ) -> None:


        self.app = (
            AppSettings()
        )


        self.storage = (
            StorageSettings()
        )


        self.ai = (
            AISettings()
        )


        self.audio = (
            AudioSettings()
        )


        self.video = (
            VideoSettings()
        )


        logger.info(
            "Configuration loaded"
        )



    # ========================================================
    # Create Required Paths
    # ========================================================

    def initialize_directories(
        self
    ) -> None:

        """
        Create application folders.
        """


        directories = [

            self.storage.base_path,

            self.storage.base_path
            /
            self.storage.projects_folder,

            self.storage.base_path
            /
            self.storage.temp_folder

        ]



        for directory in directories:

            directory.mkdir(

                parents=True,

                exist_ok=True

            )



    # ========================================================
    # Export Configuration
    # ========================================================

    def to_dict(
        self
    ) -> dict:

        """
        Return configuration dictionary.
        """


        return {


            "application":

                self.app.app_name,


            "version":

                self.app.version,


            "environment":

                self.app.environment,


            "music_model":

                self.ai.musicgen_model,


            "device":

                self.ai.device,


            "sample_rate":

                self.audio.sample_rate,


            "target_lufs":

                self.audio.target_lufs

        }



# ============================================================
# Global Configuration Instance
# ============================================================

settings = ConfigManager()

settings.initialize_directories()
