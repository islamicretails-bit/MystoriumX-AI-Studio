# ============================================================
# MystoriumX AI Studio
# Service Layer - AI Prompt Enhancement Service
#
# File:
# app/services/prompt_service.py
#
# Responsibility:
# Converts basic user ideas into professional
# cinematic AI music generation prompts.
# ============================================================


from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import logging


logger = logging.getLogger(
    "MystoriumX.PromptService"
)



# ============================================================
# Prompt Result Model
# ============================================================

@dataclass
class EnhancedPrompt:
    """
    Stores enhanced cinematic prompt data.
    """

    original_prompt: str

    enhanced_prompt: str

    mood: str

    genre: str

    instruments: List[str]

    intensity: int



# ============================================================
# Prompt Service
# ============================================================

class PromptService:
    """
    AI Prompt Enhancement Engine.

    Responsibilities:

    - Expand simple ideas
    - Add cinematic language
    - Select musical direction
    - Prepare MusicGen compatible prompts

    Future integrations:

    - LLM API
    - Local Llama models
    - HuggingFace Transformers
    """



    def __init__(
        self
    ) -> None:

        logger.info(
            "PromptService initialized"
        )



    # ========================================================
    # Main Prompt Enhancement
    # ========================================================

    def enhance_prompt(
        self,
        user_prompt: str,
        style: str = "Hollywood Documentary",
        intensity: int = 7
    ) -> EnhancedPrompt:

        """
        Convert user description into
        cinematic music prompt.

        Args:

            user_prompt:
                User creative idea.

            style:
                Documentary music style.

            intensity:
                Emotional intensity level.

        Returns:

            EnhancedPrompt object.
        """


        if not user_prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )



        mood = (
            self._detect_mood(
                user_prompt
            )
        )


        genre = (
            self._select_genre(
                style
            )
        )


        instruments = (
            self._select_instruments(
                mood
            )
        )


        enhanced = (
            self._build_cinematic_prompt(

                user_prompt,

                mood,

                genre,

                instruments,

                intensity

            )
        )


        return EnhancedPrompt(

            original_prompt=user_prompt,

            enhanced_prompt=enhanced,

            mood=mood,

            genre=genre,

            instruments=instruments,

            intensity=intensity

        )



    # ========================================================
    # Mood Detection
    # ========================================================

    def _detect_mood(
        self,
        prompt: str
    ) -> str:

        """
        Basic mood classification.

        Future:
        Transformer emotion model.
        """


        keywords = {

            "dark":
                "dark mysterious",

            "mystery":
                "mysterious suspense",

            "sad":
                "emotional dramatic",

            "epic":
                "heroic powerful",

            "ancient":
                "ancient historical",

            "space":
                "cosmic futuristic"

        }


        text = prompt.lower()


        for key, value in keywords.items():

            if key in text:

                return value



        return "cinematic emotional"



    # ========================================================
    # Genre Selection
    # ========================================================

    def _select_genre(
        self,
        style: str
    ) -> str:

        """
        Select soundtrack genre.
        """


        mapping = {

            "Hollywood Documentary":
                "cinematic orchestral documentary",

            "Dark Mystery":
                "dark ambient thriller",

            "Epic Historical":
                "epic orchestral score",

            "Nature Documentary":
                "organic atmospheric cinematic",

            "Sci-Fi Atmosphere":
                "futuristic electronic cinematic"

        }


        return mapping.get(

            style,

            "cinematic documentary"

        )



    # ========================================================
    # Instrument Selection
    # ========================================================

    def _select_instruments(
        self,
        mood: str
    ) -> List[str]:

        """
        Choose instruments based on mood.
        """


        if "dark" in mood:

            return [

                "deep cello",

                "low strings",

                "dark atmospheric pads",

                "cinematic percussion"

            ]


        if "epic" in mood:

            return [

                "full orchestra",

                "brass",

                "powerful drums",

                "choir"

            ]



        return [

            "piano",

            "strings",

            "ambient textures",

            "soft percussion"

        ]



    # ========================================================
    # Cinematic Prompt Builder
    # ========================================================

    def _build_cinematic_prompt(
        self,
        original: str,
        mood: str,
        genre: str,
        instruments: List[str],
        intensity: int
    ) -> str:

        """
        Creates final professional prompt.
        """


        instrument_text = ", ".join(
            instruments
        )


        return (

            f"{genre} soundtrack, "

            f"{mood} atmosphere, "

            f"based on: {original}. "

            f"Featuring {instrument_text}. "

            f"Emotional intensity level {intensity}/10. "

            "Professional Hollywood documentary "

            "music composition with cinematic "

            "storytelling, dynamic progression, "

            "and immersive sound design."

        )



    # ========================================================
    # Export Dictionary
    # ========================================================

    def to_dict(
        self,
        prompt: EnhancedPrompt
    ) -> Dict:

        """
        Convert enhanced prompt into
        serializable format.
        """


        return {

            "original":
                prompt.original_prompt,

            "enhanced":
                prompt.enhanced_prompt,

            "mood":
                prompt.mood,

            "genre":
                prompt.genre,

            "instruments":
                prompt.instruments,

            "intensity":
                prompt.intensity

        }
