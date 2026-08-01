"""
MystoriumX AI Studio

Waveform Generation Engine

Responsible for:
- Audio waveform visualization
- Audio analysis data generation
- Timeline representation
- Visualization export

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
from typing import Any, Dict, List, Optional, Protocol



# ============================================================
# Exceptions
# ============================================================


class WaveformGeneratorError(Exception):
    """
    Base waveform generator exception.
    """



class WaveformGenerationError(WaveformGeneratorError):
    """
    Raised when waveform generation fails.
    """



# ============================================================
# Audio Analyzer Contract
# ============================================================


class WaveformBackendProtocol(Protocol):
    """
    Low level waveform backend.

    Implementations:
    - Librosa
    - FFmpeg
    - Matplotlib
    - Custom DSP engine
    """

    def generate(
        self,
        audio_path: Path,
        output_path: Path,
        settings: Dict[str, Any],
    ) -> Path:
        ...



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class WaveformConfig:
    """
    Waveform generation settings.
    """

    image_format: str = "png"

    width: int = 1920

    height: int = 600

    dpi: int = 150

    samples: int = 5000

    include_grid: bool = True

    include_timeline: bool = True



# ============================================================
# Waveform Generator
# ============================================================


class WaveformGenerator:
    """
    Production waveform visualization service.

    Creates professional waveform assets
    for documentary audio projects.
    """

    def __init__(
        self,
        backend: WaveformBackendProtocol,
        config: Optional[WaveformConfig] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:


        self.backend = backend


        self.config = (

            config

            if config

            else WaveformConfig()
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


    def generate(
        self,
        audio_path: Path,
        output_path: Path,
    ) -> Path:
        """
        Generate waveform image.
        """

        self._validate_input(
            audio_path,
            output_path,
        )


        self.logger.info(
            "Generating waveform visualization"
        )


        try:

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )


            settings = (
                self._build_settings()
            )


            waveform_file = (

                self.backend.generate(
                    audio_path=audio_path,
                    output_path=output_path,
                    settings=settings,
                )

            )


            self._validate_output(
                waveform_file
            )


            self.logger.info(
                "Waveform generation completed"
            )


            return waveform_file


        except Exception as exc:

            self.logger.exception(
                "Waveform generation failed"
            )


            raise WaveformGenerationError(
                f"Unable to generate waveform: {exc}"
            ) from exc
              # ========================================================
    # Settings Builder
    # ========================================================


    def _build_settings(
        self,
    ) -> Dict[str, Any]:
        """
        Build waveform generation settings.
        """

        return {

            "format":
                self.config.image_format,


            "width":
                self.config.width,


            "height":
                self.config.height,


            "dpi":
                self.config.dpi,


            "samples":
                self.config.samples,


            "grid":
                self.config.include_grid,


            "timeline":
                self.config.include_timeline,

        }



    # ========================================================
    # Validation
    # ========================================================


    def _validate_input(
        self,
        audio_path: Path,
        output_path: Path,
    ) -> None:
        """
        Validate audio input.
        """

        if not audio_path.exists():

            raise WaveformGenerationError(
                f"Audio file not found: {audio_path}"
            )


        if not audio_path.is_file():

            raise WaveformGenerationError(
                "Audio path is not a file"
            )


        if not isinstance(
            output_path,
            Path,
        ):

            raise WaveformGenerationError(
                "Output path must be pathlib.Path"
            )



    def _validate_output(
        self,
        output_path: Path,
    ) -> None:
        """
        Validate generated waveform.
        """

        if not output_path.exists():

            raise WaveformGenerationError(
                "Waveform image was not created"
            )


        if not output_path.is_file():

            raise WaveformGenerationError(
                "Waveform output is not a file"
            )


        if output_path.stat().st_size <= 0:

            raise WaveformGenerationError(
                "Waveform file is empty"
            )



    # ========================================================
    # Waveform Data Generation
    # ========================================================


    def generate_waveform_data(
        self,
        samples: List[float],
    ) -> Dict[str, Any]:
        """
        Convert raw audio samples into
        visualization data.
        """

        if not samples:

            raise WaveformGenerationError(
                "Audio samples cannot be empty"
            )


        peak = max(
            abs(value)
            for value in samples
        )


        average = (

            sum(
                abs(value)
                for value in samples
            )

            /

            len(samples)

        )


        return {

            "sample_count":
                len(samples),


            "peak_amplitude":
                peak,


            "average_amplitude":
                average,


            "normalized":
                True,

        }



    # ========================================================
    # Timeline Builder
    # ========================================================


    def create_timeline(
        self,
        duration: float,
        points: int = 100,
    ) -> List[float]:
        """
        Create timeline points
        for waveform visualization.
        """

        if duration <= 0:

            raise WaveformGenerationError(
                "Duration must be greater than zero"
            )


        if points <= 0:

            raise WaveformGenerationError(
                "Timeline points must be positive"
            )


        step = duration / points


        return [

            round(
                index * step,
                3
            )

            for index in range(
                points + 1
            )

        ]



    # ========================================================
    # Visualization Profiles
    ========================================================


    def apply_profile(
        self,
        profile: str = "documentary",
    ) -> None:
        """
        Apply waveform visualization profile.
        """

        profiles: Dict[str, Dict[str, Any]] = {

            "documentary": {

                "width": 1920,

                "height": 600,

                "samples": 5000,
            },


            "social_media": {

                "width": 1080,

                "height": 1080,

                "samples": 3000,
            },


            "preview": {

                "width": 1280,

                "height": 400,

                "samples": 2000,
            },
        }



        if profile not in profiles:

            raise WaveformGenerationError(
                f"Unknown waveform profile: {profile}"
            )


        selected = profiles[profile]


        self.config.width = (
            selected["width"]
        )


        self.config.height = (
            selected["height"]
        )


        self.config.samples = (
            selected["samples"]
        )


        self.logger.info(
            f"Applied waveform profile: {profile}"
        )
          # ========================================================
    # Configuration Access
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return current waveform configuration.
        """

        return {

            "image_format":
                self.config.image_format,


            "width":
                self.config.width,


            "height":
                self.config.height,


            "dpi":
                self.config.dpi,


            "samples":
                self.config.samples,


            "include_grid":
                self.config.include_grid,


            "include_timeline":
                self.config.include_timeline,

        }



    # ========================================================
    # Metadata Generation
    # ========================================================


    def build_metadata(
        self,
        audio_file: Path,
        waveform_file: Path,
    ) -> Dict[str, Any]:
        """
        Create waveform generation metadata.
        """

        return {

            "source_audio":
                str(audio_file),


            "waveform_output":
                str(waveform_file),


            "configuration":
                self.get_configuration(),

        }



    # ========================================================
    # Waveform Analysis Helpers
    # ========================================================


    def calculate_peaks(
        self,
        samples: List[float],
        segments: int = 100,
    ) -> List[float]:
        """
        Calculate waveform peak values
        for visualization segments.
        """

        if not samples:

            raise WaveformGenerationError(
                "Samples cannot be empty"
            )


        if segments <= 0:

            raise WaveformGenerationError(
                "Segments must be positive"
            )


        segment_size = max(
            1,
            len(samples) // segments
        )


        peaks: List[float] = []


        for index in range(
            0,
            len(samples),
            segment_size
        ):

            segment = samples[
                index:
                index + segment_size
            ]


            peak = max(
                abs(value)
                for value in segment
            )


            peaks.append(
                peak
            )


        return peaks



    # ========================================================
    # Diagnostics
    # ========================================================


    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return generator health status.
        """

        return {

            "service":
                "WaveformGenerator",


            "status":
                "healthy",


            "backend":
                self.backend.__class__.__name__,


            "format":
                self.config.image_format,

        }



    # ========================================================
    # Service Information
    # ========================================================


    def get_information(
        self,
    ) -> Dict[str, Any]:
        """
        Return service information.
        """

        return {

            "service":
                "Waveform Generation Engine",


            "purpose":
                "Create cinematic audio visualization",


            "architecture":
                "Clean Architecture",


            "pipeline_stage":
                "Audio Visualization",

        }



    # ========================================================
    # Format Support
    # ========================================================


    def is_supported_audio(
        self,
        audio_file: Path,
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

            audio_file.suffix.lower()

            in

            supported_formats

        )
