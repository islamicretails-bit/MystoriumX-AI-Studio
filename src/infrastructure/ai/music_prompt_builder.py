"""
MystoriumX AI Studio

AI Music Prompt Builder

Responsible for:
- Creating cinematic music prompts
- Converting scene intelligence into
  professional soundtrack instructions

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging

from dataclasses import dataclass, field

from typing import Any, Dict, List, Optional



# ============================================================
# Exceptions
# ============================================================


class MusicPromptBuilderError(Exception):
    """
    Base music prompt builder exception.
    """



class PromptBuildError(MusicPromptBuilderError):
    """
    Raised when prompt creation fails.
    """



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class MusicPromptConfig:
    """
    Music prompt configuration.
    """

    cinematic: bool = True

    documentary: bool = True

    emotional: bool = True

    detail_level: str = "high"



# ============================================================
# Music Prompt Request
# ============================================================


@dataclass(slots=True)
class MusicPromptRequest:
    """
    Input data for music prompt generation.
    """

    scene_description: str

    mood: str = "cinematic"

    genre: str = "documentary"

    duration: int = 120

    instruments: List[str] = field(
        default_factory=list
    )



# ============================================================
# Music Prompt Builder
# ============================================================


class MusicPromptBuilder:
    """
    Production cinematic music prompt builder.

    Converts documentary scenes into
    AI music generation prompts.
    """

    def __init__(
        self,
        config: Optional[
            MusicPromptConfig
        ] = None,

        logger: Optional[
            logging.Logger
        ] = None,

    ) -> None:


        self.config = (

            config

            if config

            else MusicPromptConfig()

        )


        self.logger = (

            logger

            if logger

            else logging.getLogger(
                self.__class__.__name__
            )

        )



    # ========================================================
    # Build Prompt
    # ========================================================


    def build(
        self,
        request: MusicPromptRequest,
    ) -> str:
        """
        Create final AI music prompt.
        """

        self._validate_request(
            request
        )


        self.logger.info(
            "Building music prompt"
        )


        try:

            return (

                self._create_structure(
                    request
                )

            )


        except Exception as exc:

            raise PromptBuildError(

                f"Unable to build music prompt: {exc}"

            ) from exc
              # ========================================================
    # Prompt Structure Creator
    # ========================================================


    def _create_structure(
        self,
        request: MusicPromptRequest,
    ) -> str:
        """
        Create structured cinematic music prompt.
        """

        instruments = (

            ", ".join(
                request.instruments
            )

            if request.instruments

            else "orchestral instruments"

        )


        style = self._build_style()


        return (

            f"Create a {request.genre} "

            f"cinematic soundtrack. "

            f"Scene: {request.scene_description}. "

            f"Mood: {request.mood}. "

            f"Duration: {request.duration} seconds. "

            f"Instruments: {instruments}. "

            f"Style: {style}. "

            "Professional Hollywood documentary "

            "audio production quality."

        )



    # ========================================================
    # Style Builder
    # ========================================================


    def _build_style(
        self,
    ) -> str:
        """
        Build cinematic style description.
        """

        styles = []


        if self.config.cinematic:

            styles.append(
                "cinematic atmosphere"
            )


        if self.config.documentary:

            styles.append(
                "documentary storytelling"
            )


        if self.config.emotional:

            styles.append(
                "emotional depth"
            )


        styles.append(

            f"{self.config.detail_level} detail"

        )


        return ", ".join(
            styles
        )



    # ========================================================
    # Mood Mapping
    # ========================================================


    def map_mood(
        self,
        scene_mood: str,
    ) -> Dict[str, Any]:
        """
        Convert scene mood into
        music characteristics.
        """

        mood_library = {


            "dark": {

                "tempo":
                    "slow",

                "instruments": [

                    "deep strings",

                    "ambient drones",

                    "low percussion",

                ],

            },


            "emotional": {

                "tempo":
                    "medium",

                "instruments": [

                    "piano",

                    "violin",

                    "soft strings",

                ],

            },


            "epic": {

                "tempo":
                    "powerful",

                "instruments": [

                    "orchestra",

                    "brass",

                    "choir",

                ],

            },


            "mysterious": {

                "tempo":
                    "slow",

                "instruments": [

                    "ambient pads",

                    "dark synth",

                    "textures",

                ],

            },


            "cinematic": {

                "tempo":
                    "dynamic",

                "instruments": [

                    "strings",

                    "piano",

                    "percussion",

                ],

            },

        }


        return mood_library.get(

            scene_mood.lower(),

            mood_library["cinematic"]

        )



    # ========================================================
    # Instrument Recommendation
    # ========================================================


    def recommend_instruments(
        self,
        mood: str,
    ) -> List[str]:
        """
        Recommend instruments based
        on emotional direction.
        """

        mapping = self.map_mood(
            mood
        )


        return mapping[
            "instruments"
        ]



    # ========================================================
    # Request Validation
    # ========================================================


    def _validate_request(
        self,
        request: MusicPromptRequest,
    ) -> None:
        """
        Validate prompt request.
        """

        if not request.scene_description.strip():

            raise MusicPromptBuilderError(

                "Scene description required"

            )


        if request.duration <= 0:

            raise MusicPromptBuilderError(

                "Duration must be positive"

            )
              # ========================================================
    # Scene Intelligence Conversion
    # ========================================================


    def from_scene_analysis(
        self,
        scene_data: Dict[str, Any],
    ) -> MusicPromptRequest:
        """
        Convert AI scene analysis into
        music prompt request.
        """

        description = scene_data.get(
            "description",
            ""
        )


        mood = scene_data.get(
            "mood",
            "cinematic"
        )


        genre = scene_data.get(
            "genre",
            "documentary"
        )


        instruments = self.recommend_instruments(
            mood
        )


        return MusicPromptRequest(

            scene_description=description,

            mood=mood,

            genre=genre,

            instruments=instruments,

        )



    # ========================================================
    # Batch Prompt Generation
    # ========================================================


    def build_batch(
        self,
        requests: List[
            MusicPromptRequest
        ],
    ) -> List[str]:
        """
        Generate multiple music prompts.
        """

        prompts: List[str] = []


        for request in requests:

            prompts.append(

                self.build(
                    request
                )

            )


        return prompts



    # ========================================================
    # Metadata Creation
    # ========================================================


    def create_metadata(
        self,
        request: MusicPromptRequest,
        prompt: str,
    ) -> Dict[str, Any]:
        """
        Create prompt metadata.
        """

        return {

            "scene_description":
                request.scene_description,


            "mood":
                request.mood,


            "genre":
                request.genre,


            "duration":
                request.duration,


            "instruments":
                request.instruments,


            "generated_prompt":
                prompt,

        }



    # ========================================================
    # Configuration
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return builder configuration.
        """

        return {

            "cinematic":
                self.config.cinematic,


            "documentary":
                self.config.documentary,


            "emotional":
                self.config.emotional,


            "detail_level":
                self.config.detail_level,

        }



    # ========================================================
    # Diagnostics
    # ========================================================


    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return builder health status.
        """

        return {

            "service":
                "MusicPromptBuilder",


            "status":
                "healthy",


            "detail_level":
                self.config.detail_level,

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
                "AI Music Prompt Builder",


            "purpose":
                "Convert scenes into cinematic music prompts",


            "pipeline_stage":
                "AI Prompt Preparation",

        }



    # ========================================================
    # Prompt Validation
    # ========================================================


    def validate_prompt(
        self,
        prompt: str,
    ) -> bool:
        """
        Validate generated music prompt.
        """

        if not prompt:

            return False


        if len(prompt.strip()) < 30:

            return False


        return True
