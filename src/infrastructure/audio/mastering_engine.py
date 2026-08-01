"""
MystoriumX AI Studio

Professional Audio Mastering Engine

Responsible for:
- Cinematic audio mastering
- Loudness normalization
- Compression
- EQ processing
- True peak limiting
- Production-ready export

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


class MasteringEngineError(Exception):
    """
    Base mastering engine exception.
    """



class AudioMasteringError(MasteringEngineError):
    """
    Raised when mastering fails.
    """



# ============================================================
# Audio Processor Contract
# ============================================================


class AudioProcessorProtocol(Protocol):
    """
    Contract for low-level audio processing backend.

    Can be implemented using:
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
# Mastering Configuration
# ============================================================


@dataclass(slots=True)
class MasteringConfig:
    """
    Professional mastering settings.
    """

    target_lufs: float = -14.0

    true_peak_limit: float = -1.0

    sample_rate: int = 48000

    channels: int = 2


    compression_enabled: bool = True

    compression_ratio: float = 3.0

    compression_threshold: float = -18.0


    eq_enabled: bool = True

    low_gain: float = 1.5

    mid_gain: float = 0.0

    high_gain: float = 2.0


    metadata: Optional[
        Dict[str, Any]
    ] = None



# ============================================================
# Mastering Engine
# ============================================================


class MasteringEngine:
    """
    Production audio mastering engine.

    Converts raw generated music into
    professional cinematic soundtrack.
    """

    def __init__(
        self,
        processor: AudioProcessorProtocol,
        config: Optional[MasteringConfig] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:


        self.processor = processor


        self.config = (
            config
            if config
            else MasteringConfig()
        )


        self.logger = logger or logging.getLogger(
            self.__class__.__name__
        )



    # ========================================================
    # Public API
    # ========================================================


    def master(
        self,
        audio_path: Path,
        output_path: Path,
    ) -> Path:
        """
        Execute complete mastering chain.
        """

        self._validate_input(
            audio_path,
            output_path,
        )


        self.logger.info(
            "Starting audio mastering process"
        )


        try:

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )


            settings = (
                self._build_mastering_settings()
            )


            mastered_file = (
                self.processor.process(
                    input_path=audio_path,
                    output_path=output_path,
                    settings=settings,
                )
            )


            self._validate_output(
                mastered_file
            )


            self.logger.info(
                "Audio mastering completed"
            )


            return mastered_file


        except Exception as exc:

            self.logger.exception(
                "Audio mastering failed"
            )


            raise AudioMasteringError(
                f"Mastering failed: {exc}"
            ) from exc
              # ========================================================
    # Mastering Chain Builder
    # ========================================================


    def _build_mastering_settings(
        self,
    ) -> Dict[str, Any]:
        """
        Build complete mastering configuration.

        This configuration is passed to
        the underlying audio processor.
        """

        settings: Dict[str, Any] = {

            "sample_rate":
                self.config.sample_rate,


            "channels":
                self.config.channels,


            "loudness": {

                "enabled": True,

                "target_lufs":
                    self.config.target_lufs,

                "true_peak_limit":
                    self.config.true_peak_limit,
            },


            "compression": {

                "enabled":
                    self.config.compression_enabled,

                "ratio":
                    self.config.compression_ratio,

                "threshold":
                    self.config.compression_threshold,
            },


            "eq": {

                "enabled":
                    self.config.eq_enabled,

                "low_gain":
                    self.config.low_gain,

                "mid_gain":
                    self.config.mid_gain,

                "high_gain":
                    self.config.high_gain,
            },
        }


        return settings



    # ========================================================
    # Validation
    # ========================================================


    def _validate_input(
        self,
        audio_path: Path,
        output_path: Path,
    ) -> None:
        """
        Validate input and output paths.
        """

        if not audio_path.exists():

            raise AudioMasteringError(
                f"Input audio not found: {audio_path}"
            )


        if not audio_path.is_file():

            raise AudioMasteringError(
                "Input audio path is not a file"
            )


        if not isinstance(
            output_path,
            Path
        ):

            raise AudioMasteringError(
                "Output path must be pathlib.Path"
            )



    def _validate_output(
        self,
        output_path: Path,
    ) -> None:
        """
        Validate mastered output.
        """

        if not output_path.exists():

            raise AudioMasteringError(
                "Mastered audio file was not created"
            )


        if not output_path.is_file():

            raise AudioMasteringError(
                "Mastered output is not a file"
            )


        size = output_path.stat().st_size


        if size <= 0:

            raise AudioMasteringError(
                "Mastered audio file is empty"
            )



    # ========================================================
    # Individual Processing Configuration
    # ========================================================


    def get_loudness_settings(
        self,
    ) -> Dict[str, Any]:
        """
        Return loudness normalization settings.
        """

        return {

            "target_lufs":
                self.config.target_lufs,


            "true_peak_limit":
                self.config.true_peak_limit,


            "normalization":
                "EBU R128",
        }



    def get_compression_settings(
        self,
    ) -> Dict[str, Any]:
        """
        Return compressor configuration.
        """

        return {

            "enabled":
                self.config.compression_enabled,


            "threshold":
                self.config.compression_threshold,


            "ratio":
                self.config.compression_ratio,


            "purpose":
                "cinematic_dynamic_control",
        }



    def get_eq_settings(
        self,
    ) -> Dict[str, Any]:
        """
        Return equalizer configuration.
        """

        return {

            "enabled":
                self.config.eq_enabled,


            "low_frequency_gain":
                self.config.low_gain,


            "mid_frequency_gain":
                self.config.mid_gain,


            "high_frequency_gain":
                self.config.high_gain,
        }
          # ========================================================
    # Cinematic Mastering Profiles
    # ========================================================


    def apply_cinematic_profile(
        self,
        profile: str = "documentary",
    ) -> None:
        """
        Apply predefined cinematic mastering profiles.

        Available profiles:
        - documentary
        - trailer
        - emotional
        - ambient
        """

        profiles: Dict[str, Dict[str, Any]] = {

            "documentary": {

                "target_lufs": -14.0,

                "true_peak_limit": -1.0,

                "compression_ratio": 3.0,

                "low_gain": 1.5,

                "high_gain": 2.0,
            },


            "trailer": {

                "target_lufs": -10.0,

                "true_peak_limit": -1.0,

                "compression_ratio": 5.0,

                "low_gain": 3.0,

                "high_gain": 3.0,
            },


            "emotional": {

                "target_lufs": -16.0,

                "true_peak_limit": -1.5,

                "compression_ratio": 2.0,

                "low_gain": 1.0,

                "high_gain": 1.5,
            },


            "ambient": {

                "target_lufs": -18.0,

                "true_peak_limit": -2.0,

                "compression_ratio": 1.8,

                "low_gain": 0.5,

                "high_gain": 1.0,
            },
        }



        if profile not in profiles:

            raise AudioMasteringError(
                f"Unknown mastering profile: {profile}"
            )


        selected = profiles[profile]


        self.config.target_lufs = (
            selected["target_lufs"]
        )

        self.config.true_peak_limit = (
            selected["true_peak_limit"]
        )

        self.config.compression_ratio = (
            selected["compression_ratio"]
        )

        self.config.low_gain = (
            selected["low_gain"]
        )

        self.config.high_gain = (
            selected["high_gain"]
        )


        self.logger.info(
            f"Applied mastering profile: {profile}"
        )



    # ========================================================
    # Configuration Export
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return current mastering configuration.
        """

        return {

            "target_lufs":
                self.config.target_lufs,


            "true_peak_limit":
                self.config.true_peak_limit,


            "sample_rate":
                self.config.sample_rate,


            "channels":
                self.config.channels,


            "compression": {

                "enabled":
                    self.config.compression_enabled,

                "ratio":
                    self.config.compression_ratio,

                "threshold":
                    self.config.compression_threshold,
            },


            "eq": {

                "enabled":
                    self.config.eq_enabled,

                "low_gain":
                    self.config.low_gain,

                "mid_gain":
                    self.config.mid_gain,

                "high_gain":
                    self.config.high_gain,
            },
        }



    # ========================================================
    # Service Diagnostics
    # ========================================================


    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return engine health status.
        """

        return {

            "service":
                "MasteringEngine",


            "status":
                "healthy",


            "target_lufs":
                self.config.target_lufs,


            "sample_rate":
                self.config.sample_rate,


            "channels":
                self.config.channels,
        }



    # ========================================================
    # Metadata Builder
    # ========================================================


    def build_mastering_metadata(
        self,
        source_file: Path,
        output_file: Path,
    ) -> Dict[str, Any]:
        """
        Create mastering process metadata.
        """

        return {

            "source":
                str(source_file),


            "output":
                str(output_file),


            "mastering":

                self.get_configuration(),
        }
