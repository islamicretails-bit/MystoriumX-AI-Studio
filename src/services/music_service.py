"""
MystoriumX AI Studio

Music Generation Service

Responsible for:
- AI cinematic music generation
- Prompt processing
- Model coordination
- Output file handling

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


class MusicServiceError(Exception):
    """
    Base music service exception.
    """



class MusicGenerationError(MusicServiceError):
    """
    Raised when music generation fails.
    """



# ============================================================
# Model Provider Contract
# ============================================================


class MusicGeneratorProtocol(Protocol):
    """
    Interface for AI music generation engines.

    Examples:
    - Stable Audio
    - MusicGen
    - Custom AI model
    """

    def generate(
        self,
        prompt: str,
        duration: float,
        output_path: Path,
    ) -> Path:
        ...



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class MusicGenerationConfig:
    """
    AI music generation settings.
    """

    model_name: str = "cinematic-ai"

    quality: str = "high"

    sample_rate: int = 48000

    channels: int = 2

    format: str = "wav"

    temperature: float = 0.8

    metadata: Dict[str, Any] = None


# ============================================================
# Music Service
# ============================================================


class MusicService:
    """
    Production AI music generation service.

    This service acts as an abstraction layer between
    the application and AI music generation models.
    """

    def __init__(
        self,
        generator: MusicGeneratorProtocol,
        config: Optional[MusicGenerationConfig] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:

        self.generator = generator

        self.config = (
            config
            if config
            else MusicGenerationConfig()
        )

        self.logger = logger or logging.getLogger(
            self.__class__.__name__
        )



    # ========================================================
    # Public API
    # ========================================================


    def generate(
        self,
        prompt: str,
        duration: float,
        output_path: Path,
    ) -> Path:
        """
        Generate cinematic soundtrack.

        Parameters:
            prompt:
                Cinematic music description

            duration:
                Track duration seconds

            output_path:
                Final audio output location
        """

        self._validate_request(
            prompt,
            duration,
            output_path,
        )


        self.logger.info(
            "Starting cinematic music generation"
        )


        try:

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )


            generated_file = self.generator.generate(
                prompt=prompt,
                duration=duration,
                output_path=output_path,
            )


            self._validate_output(
                generated_file
            )


            self.logger.info(
                "Music generation completed successfully"
            )


            return generated_file


        except Exception as exc:

            self.logger.exception(
                "Music generation failed"
            )


            raise MusicGenerationError(
                f"Unable to generate music: {exc}"
            ) from exc
              # ========================================================
    # Validation Layer
    # ========================================================


    def _validate_request(
        self,
        prompt: str,
        duration: float,
        output_path: Path,
    ) -> None:
        """
        Validate music generation request.
        """

        if not prompt:
            raise MusicGenerationError(
                "Music prompt cannot be empty"
            )


        if not prompt.strip():
            raise MusicGenerationError(
                "Music prompt contains no valid text"
            )


        if duration <= 0:
            raise MusicGenerationError(
                "Duration must be greater than zero"
            )


        if not isinstance(
            output_path,
            Path
        ):
            raise MusicGenerationError(
                "Output path must be pathlib.Path"
            )



    def _validate_output(
        self,
        output_path: Path,
    ) -> None:
        """
        Validate generated audio file.
        """

        if not output_path.exists():

            raise MusicGenerationError(
                "Generated audio file does not exist"
            )


        if not output_path.is_file():

            raise MusicGenerationError(
                "Generated output is not a file"
            )


        file_size = output_path.stat().st_size


        if file_size <= 0:

            raise MusicGenerationError(
                "Generated audio file is empty"
            )



    # ========================================================
    # Prompt Preparation
    # ========================================================


    def prepare_cinematic_prompt(
        self,
        prompt: str,
        style: Optional[str] = None,
        emotion: Optional[str] = None,
    ) -> str:
        """
        Enhance raw prompt into cinematic music direction.

        Example:

        Input:
            dark mystery music

        Output:
            cinematic dark orchestral soundtrack
            with emotional tension...
        """

        self.logger.info(
            "Preparing cinematic music prompt"
        )


        enhanced_prompt = prompt.strip()



        if style:

            enhanced_prompt += (
                f", cinematic style: {style}"
            )


        if emotion:

            enhanced_prompt += (
                f", emotional tone: {emotion}"
            )


        enhanced_prompt += (
            ", Hollywood documentary soundtrack,"
            " professional orchestral arrangement,"
            " immersive atmosphere,"
            " cinematic dynamics"
        )


        return enhanced_prompt



    # ========================================================
    # Generation Metadata
    # ========================================================


    def build_generation_metadata(
        self,
        prompt: str,
        duration: float,
    ) -> Dict[str, Any]:
        """
        Create generation metadata.

        Used for:
        - project history
        - analytics
        - export package
        """

        return {

            "model":
                self.config.model_name,


            "quality":
                self.config.quality,


            "sample_rate":
                self.config.sample_rate,


            "channels":
                self.config.channels,


            "format":
                self.config.format,


            "duration":
                duration,


            "prompt":
                prompt,


            "temperature":
                self.config.temperature,
        }



    # ========================================================
    # Advanced Generation Control
    # ========================================================


    def generate_with_style(
        self,
        prompt: str,
        duration: float,
        output_path: Path,
        style: Optional[str] = None,
        emotion: Optional[str] = None,
    ) -> Path:
        """
        Generate music with cinematic style controls.
        """

        cinematic_prompt = (
            self.prepare_cinematic_prompt(
                prompt=prompt,
                style=style,
                emotion=emotion,
            )
        )


        return self.generate(
            prompt=cinematic_prompt,
            duration=duration,
            output_path=output_path,
        )
          # ========================================================
    # Batch Music Generation
    # ========================================================


    def generate_multiple_tracks(
        self,
        tracks: list[Dict[str, Any]],
    ) -> list[Path]:
        """
        Generate multiple cinematic tracks.

        Used for:
        - documentary chapters
        - scene based soundtracks
        - multi-track projects
        """

        generated_files: list[Path] = []


        self.logger.info(
            "Starting batch music generation"
        )


        for track in tracks:

            prompt = track.get(
                "prompt"
            )

            duration = track.get(
                "duration",
                60.0
            )

            output_path = track.get(
                "output_path"
            )


            if not prompt or not output_path:

                raise MusicGenerationError(
                    "Invalid batch track configuration"
                )


            generated = self.generate(
                prompt=prompt,
                duration=duration,
                output_path=output_path,
            )


            generated_files.append(
                generated
            )


        self.logger.info(
            "Batch music generation completed"
        )


        return generated_files



    # ========================================================
    # Documentary Soundtrack Builder
    # ========================================================


    def create_documentary_score(
        self,
        scenes: list[Dict[str, Any]],
        output_directory: Path,
    ) -> list[Path]:
        """
        Create multiple soundtrack pieces
        from documentary scenes.

        Each scene receives its own
        cinematic music layer.
        """

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )


        tracks: list[Dict[str, Any]] = []


        for index, scene in enumerate(
            scenes,
            start=1
        ):

            scene_description = scene.get(
                "description",
                "cinematic documentary scene"
            )


            emotion = scene.get(
                "emotion",
                "dramatic"
            )


            output_path = (
                output_directory
                /
                f"scene_{index}_score.{self.config.format}"
            )


            tracks.append(
                {
                    "prompt":
                        scene_description,

                    "duration":
                        scene.get(
                            "duration",
                            60.0
                        ),

                    "output_path":
                        output_path,

                    "emotion":
                        emotion,
                }
            )


        return self.generate_multiple_tracks(
            tracks
        )



    # ========================================================
    # Service Status
    # ========================================================


    def health_check(self) -> Dict[str, Any]:
        """
        Return service health information.

        Used by:
        - Streamlit dashboard
        - monitoring
        - diagnostics
        """

        status = {

            "service":
                "MusicService",

            "status":
                "healthy",

            "model":
                self.config.model_name,

            "quality":
                self.config.quality,

            "sample_rate":
                self.config.sample_rate,
        }


        return status



    # ========================================================
    # Internal Helpers
    # ========================================================


    def _normalize_metadata(
        self,
        metadata: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Normalize optional metadata.
        """

        if metadata is None:

            return {}


        return metadata



    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return current service configuration.
        """

        return {

            "model_name":
                self.config.model_name,

            "quality":
                self.config.quality,

            "sample_rate":
                self.config.sample_rate,

            "channels":
                self.config.channels,

            "format":
                self.config.format,

            "temperature":
                self.config.temperature,
        }
