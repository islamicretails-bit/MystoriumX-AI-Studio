"""
MystoriumX AI Studio

Professional Audio Processing Engine

Responsible for:
- Audio preprocessing
- Format preparation
- Sample rate conversion
- Channel management
- Processing pipeline preparation

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Protocol



# ============================================================
# Exceptions
# ============================================================


class AudioProcessorError(Exception):
    """
    Base audio processor exception.
    """



class AudioProcessingError(AudioProcessorError):
    """
    Raised when audio processing fails.
    """



# ============================================================
# Backend Processor Contract
# ============================================================


class AudioBackendProtocol(Protocol):
    """
    Low-level audio backend contract.

    Implementations:
    - FFmpeg
    - Librosa
    - PyDub
    - Custom DSP engine
    """

    def process(
        self,
        input_path: Path,
        output_path: Path,
        settings: Dict[str, Any],
    ) -> Path:
        ...



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class AudioProcessingConfig:
    """
    Audio processing settings.
    """

    sample_rate: int = 48000

    channels: int = 2

    output_format: str = "wav"

    normalize: bool = True

    remove_noise: bool = False

    enhance_clarity: bool = True

    metadata: Optional[
        Dict[str, Any]
    ] = None



# ============================================================
# Audio Processor
# ============================================================


class AudioProcessor:
    """
    Production audio processing service.

    Prepares AI generated audio for
    professional mastering.
    """

    def __init__(
        self,
        backend: AudioBackendProtocol,
        config: Optional[AudioProcessingConfig] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:


        self.backend = backend


        self.config = (

            config

            if config

            else AudioProcessingConfig()
        )


        self.logger = (

            logger

            if logger

            else logging.getLogger(
                self.__class__.__name__
            )
        )



    # ========================================================
    # Public API
    # ========================================================


    def process(
        self,
        audio_path: Path,
        output_path: Path,
    ) -> Path:
        """
        Execute audio processing pipeline.
        """

        self._validate_input(
            audio_path,
            output_path,
        )


        self.logger.info(
            "Starting audio processing"
        )


        try:

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )


            settings = (
                self._build_processing_settings()
            )


            processed_audio = (

                self.backend.process(
                    input_path=audio_path,
                    output_path=output_path,
                    settings=settings,
                )

            )


            self._validate_output(
                processed_audio
            )


            self.logger.info(
                "Audio processing completed"
            )


            return processed_audio


        except Exception as exc:

            self.logger.exception(
                "Audio processing failed"
            )


            raise AudioProcessingError(
                f"Processing failed: {exc}"
            ) from exc
              # ========================================================
    # Processing Settings Builder
    # ========================================================


    def _build_processing_settings(
        self,
    ) -> Dict[str, Any]:
        """
        Build audio processing configuration.
        """

        return {

            "sample_rate":
                self.config.sample_rate,


            "channels":
                self.config.channels,


            "format":
                self.config.output_format,


            "normalization": {

                "enabled":
                    self.config.normalize,

            },


            "noise_reduction": {

                "enabled":
                    self.config.remove_noise,

            },


            "enhancement": {

                "enabled":
                    self.config.enhance_clarity,

            },
        }



    # ========================================================
    # Validation Layer
    # ========================================================


    def _validate_input(
        self,
        audio_path: Path,
        output_path: Path,
    ) -> None:
        """
        Validate input audio file.
        """

        if not audio_path.exists():

            raise AudioProcessingError(
                f"Audio file not found: {audio_path}"
            )


        if not audio_path.is_file():

            raise AudioProcessingError(
                "Audio input path is not a file"
            )


        if not isinstance(
            output_path,
            Path,
        ):

            raise AudioProcessingError(
                "Output path must be pathlib.Path"
            )



    def _validate_output(
        self,
        output_path: Path,
    ) -> None:
        """
        Validate processed output.
        """

        if not output_path.exists():

            raise AudioProcessingError(
                "Processed audio was not created"
            )


        if not output_path.is_file():

            raise AudioProcessingError(
                "Processed output is not a file"
            )


        if output_path.stat().st_size <= 0:

            raise AudioProcessingError(
                "Processed audio file is empty"
            )



    # ========================================================
    # Audio Enhancement Controls
    # ========================================================


    def enable_noise_reduction(
        self,
    ) -> None:
        """
        Enable noise reduction processing.
        """

        self.config.remove_noise = True


        self.logger.info(
            "Noise reduction enabled"
        )



    def disable_noise_reduction(
        self,
    ) -> None:
        """
        Disable noise reduction processing.
        """

        self.config.remove_noise = False


        self.logger.info(
            "Noise reduction disabled"
        )



    def enable_normalization(
        self,
    ) -> None:
        """
        Enable audio normalization.
        """

        self.config.normalize = True



    def disable_normalization(
        self,
    ) -> None:
        """
        Disable normalization.
        """

        self.config.normalize = False



    def enable_clarity_enhancement(
        self,
    ) -> None:
        """
        Enable clarity enhancement.
        """

        self.config.enhance_clarity = True



    def disable_clarity_enhancement(
        self,
    ) -> None:
        """
        Disable clarity enhancement.
        """

        self.config.enhance_clarity = False



    # ========================================================
    # Metadata Generation
    # ========================================================


    def build_metadata(
        self,
        source_file: Path,
        output_file: Path,
    ) -> Dict[str, Any]:
        """
        Create processing metadata.
        """

        return {

            "source":
                str(source_file),


            "output":
                str(output_file),


            "processing":

                self._build_processing_settings(),

        }
          # ========================================================
    # Processing Profiles
    # ========================================================


    def apply_profile(
        self,
        profile: str = "documentary",
    ) -> None:
        """
        Apply predefined audio processing profiles.

        Profiles:
        - documentary
        - voice_focused
        - cinematic
        - clean
        """

        profiles: Dict[str, Dict[str, Any]] = {


            "documentary": {

                "normalize":
                    True,

                "remove_noise":
                    False,

                "enhance_clarity":
                    True,
            },


            "voice_focused": {

                "normalize":
                    True,

                "remove_noise":
                    True,

                "enhance_clarity":
                    True,
            },


            "cinematic": {

                "normalize":
                    True,

                "remove_noise":
                    False,

                "enhance_clarity":
                    True,
            },


            "clean": {

                "normalize":
                    False,

                "remove_noise":
                    True,

                "enhance_clarity":
                    False,
            },

        }



        if profile not in profiles:

            raise AudioProcessingError(
                f"Unknown audio profile: {profile}"
            )


        selected = profiles[profile]


        self.config.normalize = (
            selected["normalize"]
        )


        self.config.remove_noise = (
            selected["remove_noise"]
        )


        self.config.enhance_clarity = (
            selected["enhance_clarity"]
        )


        self.logger.info(
            f"Applied audio profile: {profile}"
        )



    # ========================================================
    # Configuration Access
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return current processor configuration.
        """

        return {

            "sample_rate":
                self.config.sample_rate,


            "channels":
                self.config.channels,


            "output_format":
                self.config.output_format,


            "normalize":
                self.config.normalize,


            "remove_noise":
                self.config.remove_noise,


            "enhance_clarity":
                self.config.enhance_clarity,

        }



    # ========================================================
    # Diagnostics
    # ========================================================


    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return service health status.
        """

        return {

            "service":
                "AudioProcessor",


            "status":
                "healthy",


            "sample_rate":
                self.config.sample_rate,


            "channels":
                self.config.channels,


            "backend":
                self.backend.__class__.__name__,

        }



    # ========================================================
    # Audio Information
    # ========================================================


    def get_processing_summary(
        self,
    ) -> Dict[str, Any]:
        """
        Return processing summary.
        """

        return {

            "engine":
                "MystoriumX Audio Processor",


            "purpose":
                "Prepare generated audio for mastering",


            "configuration":
                self.get_configuration(),

        }



    # ========================================================
    # File Support Validation
    # ========================================================


    def is_supported_format(
        self,
        file_path: Path,
    ) -> bool:
        """
        Check supported audio formats.
        """

        supported_formats = {

            ".wav",

            ".mp3",

            ".flac",

            ".ogg",

        }


        return (
            file_path.suffix.lower()
            in supported_formats
        )
