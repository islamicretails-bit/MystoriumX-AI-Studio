"""
MystoriumX AI Studio

Cinematic Prompt Generation Service

Responsible for:
- AI music prompt generation
- Scene interpretation
- Documentary mood creation
- Cinematic storytelling prompts

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional



# ============================================================
# Exceptions
# ============================================================


class PromptServiceError(Exception):
    """
    Base prompt service exception.
    """



class PromptGenerationError(PromptServiceError):
    """
    Raised when prompt generation fails.
    """



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class PromptConfig:
    """
    Prompt generation configuration.
    """

    style: str = "cinematic documentary"

    genre: str = "orchestral"

    detail_level: str = "high"

    include_instruments: bool = True

    include_emotion: bool = True



# ============================================================
# Prompt Service
# ============================================================


class PromptService:
    """
    Production cinematic prompt generator.

    Converts documentary scene information
    into professional AI music prompts.
    """

    def __init__(
        self,
        config: Optional[PromptConfig] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:


        self.config = (

            config

            if config

            else PromptConfig()
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
        scenes: List[Dict[str, Any]],
    ) -> str:
        """
        Generate complete cinematic music prompt.

        Input:
            Scene analysis data

        Output:
            AI music generation prompt
        """

        self._validate_scenes(
            scenes
        )


        self.logger.info(
            "Generating cinematic music prompt"
        )


        try:

            context = (
                self._build_scene_context(
                    scenes
                )
            )


            emotion = (
                self._detect_overall_emotion(
                    scenes
                )
            )


            prompt = (
                self._create_prompt(
                    context,
                    emotion,
                )
            )


            self.logger.info(
                "Cinematic prompt generated successfully"
            )


            return prompt


        except Exception as exc:

            self.logger.exception(
                "Prompt generation failed"
            )


            raise PromptGenerationError(
                f"Unable to generate prompt: {exc}"
            ) from exc
              # ========================================================
    # Scene Context Builder
    # ========================================================


    def _build_scene_context(
        self,
        scenes: List[Dict[str, Any]],
    ) -> str:
        """
        Convert scene analysis into
        cinematic storytelling context.
        """

        context_parts: List[str] = []


        for scene in scenes:

            description = scene.get(
                "description",
                "unknown scene"
            )


            emotion = scene.get(
                "emotion",
                "neutral"
            )


            objects = scene.get(
                "objects",
                []
            )


            object_text = (
                ", ".join(objects)
                if objects
                else "visual elements"
            )


            context_parts.append(

                (
                    f"Scene shows {description}. "
                    f"Emotional atmosphere is {emotion}. "
                    f"Important elements: {object_text}."
                )

            )


        return " ".join(
            context_parts
        )



    # ========================================================
    # Emotion Analysis
    # ========================================================


    def _detect_overall_emotion(
        self,
        scenes: List[Dict[str, Any]],
    ) -> str:
        """
        Detect dominant emotional tone.
        """

        emotion_count: Dict[str, int] = {}


        for scene in scenes:

            emotion = scene.get(
                "emotion",
                "neutral"
            )


            emotion_count[emotion] = (
                emotion_count.get(
                    emotion,
                    0
                )
                + 1
            )


        if not emotion_count:

            return "neutral"


        return max(
            emotion_count,
            key=emotion_count.get
        )



    # ========================================================
    # Cinematic Prompt Builder
    # ========================================================


    def _create_prompt(
        self,
        context: str,
        emotion: str,
    ) -> str:
        """
        Build final AI music prompt.
        """

        prompt_parts: List[str] = []


        prompt_parts.append(

            f"{self.config.style} soundtrack"

        )


        prompt_parts.append(

            f"{self.config.genre} composition"

        )


        prompt_parts.append(

            f"Emotional tone: {emotion}"

        )


        prompt_parts.append(

            f"Story context: {context}"

        )



        if self.config.include_instruments:

            prompt_parts.append(

                (
                    "Use cinematic instruments including "
                    "orchestra, strings, piano, "
                    "deep percussion, atmospheric pads"
                )

            )



        if self.config.include_emotion:

            prompt_parts.append(

                (
                    "Create emotional progression, "
                    "tension, cinematic build-up, "
                    "and immersive storytelling"
                )

            )



        prompt_parts.append(

            (
                "Professional Hollywood documentary "
                "score, high quality production, "
                "powerful cinematic experience"
            )

        )


        return ". ".join(
            prompt_parts
        )



    # ========================================================
    # Style Enhancement
    # ========================================================


    def enhance_prompt(
        self,
        prompt: str,
        mood: Optional[str] = None,
        intensity: Optional[str] = None,
    ) -> str:
        """
        Add additional cinematic controls.
        """

        enhanced = prompt.strip()


        if mood:

            enhanced += (
                f". Overall mood: {mood}"
            )


        if intensity:

            enhanced += (
                f". Intensity level: {intensity}"
            )


        return enhanced
          # ========================================================
    # Genre Mapping
    # ========================================================


    def get_genre_profile(
        self,
        genre: str,
    ) -> Dict[str, Any]:
        """
        Return cinematic genre characteristics.
        """

        profiles: Dict[str, Dict[str, Any]] = {

            "mystery": {

                "instruments":
                    [
                        "dark strings",
                        "ambient pads",
                        "deep piano",
                    ],

                "tempo":
                    "slow",

                "emotion":
                    "suspense",
            },


            "historical": {

                "instruments":
                    [
                        "orchestra",
                        "choir",
                        "epic percussion",
                    ],

                "tempo":
                    "medium",

                "emotion":
                    "grand",
            },


            "emotional": {

                "instruments":
                    [
                        "piano",
                        "soft strings",
                        "ambient textures",
                    ],

                "tempo":
                    "slow",

                "emotion":
                    "deep emotional",
            },


            "action": {

                "instruments":
                    [
                        "heavy drums",
                        "brass",
                        "orchestra",
                    ],

                "tempo":
                    "fast",

                "emotion":
                    "intense",
            },
        }


        return profiles.get(
            genre.lower(),
            profiles["historical"]
        )



    # ========================================================
    # Documentary Prompt Templates
    # ========================================================


    def documentary_template(
        self,
        topic: str,
        tone: str,
    ) -> str:
        """
        Create documentary-specific prompt.
        """

        return (

            f"Create a cinematic documentary "
            f"soundtrack about {topic}. "

            f"The tone should be {tone}. "

            "Use professional film scoring "
            "techniques with emotional storytelling, "
            "orchestral layers, atmospheric sound "
            "design and dramatic progression."

        )



    def create_scene_prompt(
        self,
        scene: Dict[str, Any],
    ) -> str:
        """
        Generate prompt for individual scene.
        """

        description = scene.get(
            "description",
            "unknown"
        )


        emotion = scene.get(
            "emotion",
            "neutral"
        )


        return (

            "Cinematic documentary music for "
            f"a scene showing {description}. "

            f"Emotional direction: {emotion}. "

            "Include immersive atmosphere, "
            "professional orchestration, "
            "and Hollywood quality production."

        )



    # ========================================================
    # Validation
    # ========================================================


    def _validate_scenes(
        self,
        scenes: List[Dict[str, Any]],
    ) -> None:
        """
        Validate scene input.
        """

        if not scenes:

            raise PromptGenerationError(
                "Scene list cannot be empty"
            )


        if not isinstance(
            scenes,
            list
        ):

            raise PromptGenerationError(
                "Scenes must be a list"
            )



    # ========================================================
    # Metadata
    # ========================================================


    def build_metadata(
        self,
        prompt: str,
        scenes: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Create prompt generation metadata.
        """

        return {

            "service":
                "PromptService",


            "style":
                self.config.style,


            "genre":
                self.config.genre,


            "detail_level":
                self.config.detail_level,


            "scene_count":
                len(scenes),


            "prompt_length":
                len(prompt),

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
                "PromptService",


            "status":
                "healthy",


            "style":
                self.config.style,


            "genre":
                self.config.genre,

        }



    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return current configuration.
        """

        return {

            "style":
                self.config.style,


            "genre":
                self.config.genre,


            "detail_level":
                self.config.detail_level,


            "include_instruments":
                self.config.include_instruments,


            "include_emotion":
                self.config.include_emotion,

        }
      
