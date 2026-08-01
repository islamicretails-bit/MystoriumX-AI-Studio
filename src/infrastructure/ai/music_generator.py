"""
MystoriumX AI Studio

AI Music Generation Engine

Responsible for:
- Creating cinematic music
- Managing AI music generation requests
- Producing documentary soundtracks

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging

from dataclasses import dataclass, field

from pathlib import Path

from typing import Any, Dict, List, Optional, Protocol



# ============================================================
# Exceptions
# ============================================================


class MusicGeneratorError(Exception):
    """
    Base music generator exception.
    """



class MusicGenerationError(MusicGeneratorError):
    """
    Raised when music generation fails.
    """



# ============================================================
# Music Backend Contract
# ============================================================


class MusicBackendProtocol(Protocol):
    """
    AI music generation backend contract.

    Implementations:
    - Local AI music model
    - Cloud music API
    - Diffusion music engine
    """

    def generate(
        self,
        prompt: str,
        settings: Dict[str, Any],
    ) -> Path:
        ...



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class MusicGeneratorConfig:
    """
    Music generation configuration.
    """

    output_directory: Path

    sample_rate: int = 48000

    default_duration: int = 120

    audio_format: str = "wav"

    quality: str = "high"



# ============================================================
# Generation Request
# ============================================================


@dataclass(slots=True)
class MusicRequest:
    """
    AI music generation request.
    """

    prompt: str

    duration: int

    mood: str = "cinematic"

    genre: str = "documentary"

    instruments: List[str] = field(
        default_factory=list
    )



# ============================================================
# Music Generator
# ============================================================


class MusicGenerator:
    """
    Production AI music generation service.

    Creates cinematic documentary
    soundtracks from AI prompts.
    """

    def __init__(
        self,
        backend: MusicBackendProtocol,

        config: MusicGeneratorConfig,

        logger: Optional[
            logging.Logger
        ] = None,

    ) -> None:


        self.backend = backend


        self.config = config


        self.logger = (

            logger

            if logger

            else logging.getLogger(
                self.__class__.__name__
            )

        )


        self.history: List[
            Dict[str, Any]
        ] = []



    # ========================================================
    # Generate Music
    # ========================================================


    def generate(
        self,
        request: MusicRequest,
    ) -> Path:
        """
        Generate cinematic music track.
        """

        self._validate_request(
            request
        )


        self.logger.info(
            "Starting AI music generation"
        )


        try:

            settings = (
                self._build_settings(
                    request
                )
            )


            output = self.backend.generate(

                request.prompt,

                settings,

            )


            self._store_history(
                request,
                output,
            )


            return output



        except Exception as exc:

            self.logger.exception(
                "Music generation failed"
            )


            raise MusicGenerationError(

                f"Unable to generate music: {exc}"

            ) from exc
              # ========================================================
    # Settings Builder
    # ========================================================


    def _build_settings(
        self,
        request: MusicRequest,
    ) -> Dict[str, Any]:
        """
        Build AI music generation settings.
        """

        return {

            "duration":
                request.duration,


            "mood":
                request.mood,


            "genre":
                request.genre,


            "instruments":
                request.instruments,


            "sample_rate":
                self.config.sample_rate,


            "audio_format":
                self.config.audio_format,


            "quality":
                self.config.quality,

        }



    # ========================================================
    # Request Validation
    # ========================================================


    def _validate_request(
        self,
        request: MusicRequest,
    ) -> None:
        """
        Validate music generation request.
        """

        if not request.prompt.strip():

            raise MusicGeneratorError(
                "Music prompt cannot be empty"
            )


        if request.duration <= 0:

            raise MusicGeneratorError(
                "Duration must be positive"
            )


        if request.duration > 3600:

            raise MusicGeneratorError(
                "Maximum duration exceeded"
            )



    # ========================================================
    # Cinematic Presets
    # ========================================================


    def apply_preset(
        self,
        preset: str = "documentary",
    ) -> Dict[str, Any]:
        """
        Return cinematic music preset.

        Presets:
        - documentary
        - thriller
        - emotional
        - epic
        """

        presets = {


            "documentary": {

                "mood":
                    "cinematic",

                "genre":
                    "orchestral",

                "instruments": [

                    "strings",

                    "piano",

                    "ambient pads",

                ],

            },


            "thriller": {

                "mood":
                    "dark tension",

                "genre":
                    "cinematic thriller",

                "instruments": [

                    "low strings",

                    "deep drums",

                    "synth textures",

                ],

            },


            "emotional": {

                "mood":
                    "emotional",

                "genre":
                    "dramatic",

                "instruments": [

                    "piano",

                    "violin",

                    "soft strings",

                ],

            },


            "epic": {

                "mood":
                    "heroic",

                "genre":
                    "epic orchestral",

                "instruments": [

                    "choir",

                    "brass",

                    "orchestra",

                ],

            },

        }


        if preset not in presets:

            raise MusicGeneratorError(

                f"Unknown preset: {preset}"

            )


        return presets[preset]



    # ========================================================
    # Prompt Preparation
    # ========================================================


    def prepare_prompt(
        self,
        request: MusicRequest,
    ) -> str:
        """
        Create enhanced music prompt.
        """

        instruments = ", ".join(

            request.instruments

        )


        return (

            f"Cinematic {request.genre} music, "

            f"mood: {request.mood}, "

            f"duration: {request.duration} seconds, "

            f"instruments: {instruments}. "

            f"Documentary quality soundtrack."

        )



    # ========================================================
    # History Storage
    # ========================================================


    def _store_history(
        self,
        request: MusicRequest,
        output: Path,
    ) -> None:
        """
        Store generation record.
        """

        self.history.append(

            {

                "prompt":
                    request.prompt,


                "output":
                    str(output),


                "duration":
                    request.duration,


                "mood":
                    request.mood,


            }

        )
          # ========================================================
    # Generation History
    # ========================================================


    def get_history(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return music generation history.
        """

        return self.history



    # ========================================================
    # Clear History
    # ========================================================


    def clear_history(
        self,
    ) -> None:
        """
        Clear generation records.
        """

        self.history.clear()



    # ========================================================
    # Metadata Creation
    # ========================================================


    def create_metadata(
        self,
        request: MusicRequest,
        output_file: Path,
    ) -> Dict[str, Any]:
        """
        Create generated audio metadata.
        """

        return {

            "file":
                str(output_file),


            "prompt":
                request.prompt,


            "duration":
                request.duration,


            "mood":
                request.mood,


            "genre":
                request.genre,


            "instruments":
                request.instruments,


            "quality":
                self.config.quality,

        }



    # ========================================================
    # Configuration
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return generator configuration.
        """

        return {

            "output_directory":
                str(
                    self.config.output_directory
                ),


            "sample_rate":
                self.config.sample_rate,


            "default_duration":
                self.config.default_duration,


            "audio_format":
                self.config.audio_format,


            "quality":
                self.config.quality,

        }



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
                "MusicGenerator",


            "status":
                "healthy",


            "backend":
                self.backend.__class__.__name__,


            "generated_tracks":
                len(
                    self.history
                ),

        }



    # ========================================================
    # Information
    # ========================================================


    def get_information(
        self,
    ) -> Dict[str, Any]:
        """
        Return service information.
        """

        return {

            "service":
                "AI Cinematic Music Generator",


            "purpose":
                "Generate documentary soundtracks using AI",


            "pipeline_stage":
                "AI Music Generation",

        }



    # ========================================================
    # Output Validation
    # ========================================================


    def validate_output(
        self,
        output_file: Path,
    ) -> bool:
        """
        Validate generated audio file.
        """

        if not output_file.exists():

            return False


        if not output_file.is_file():

            return False


        if output_file.stat().st_size <= 0:

            return False


        return True
