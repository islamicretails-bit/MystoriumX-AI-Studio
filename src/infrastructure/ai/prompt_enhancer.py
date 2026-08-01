"""
MystoriumX AI Studio

AI Prompt Enhancement Engine

Responsible for:
- Improving AI prompts
- Creating cinematic descriptions
- Preparing production-grade prompts

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging

from dataclasses import dataclass

from typing import Any, Dict, List, Optional, Protocol



# ============================================================
# Exceptions
# ============================================================


class PromptEnhancerError(Exception):
    """
    Base prompt enhancer exception.
    """



class PromptProcessingError(PromptEnhancerError):
    """
    Raised when prompt processing fails.
    """



# ============================================================
# AI Prompt Backend Contract
# ============================================================


class PromptBackendProtocol(Protocol):
    """
    AI prompt backend contract.

    Implementations:
    - LLM API
    - Local language model
    - Rule based engine
    """

    def enhance(
        self,
        prompt: str,
        settings: Dict[str, Any],
    ) -> str:
        ...



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class PromptEnhancerConfig:
    """
    Prompt enhancement configuration.
    """

    cinematic_style: bool = True

    documentary_style: bool = True

    emotional_depth: bool = True

    detail_level: str = "high"



# ============================================================
# Prompt Request
# ============================================================


@dataclass(slots=True)
class PromptRequest:
    """
    Prompt enhancement request.
    """

    text: str

    genre: str = "documentary"

    mood: str = "cinematic"

    keywords: List[str] = None



# ============================================================
# Prompt Enhancer
# ============================================================


class PromptEnhancer:
    """
    Production AI prompt enhancement service.

    Converts simple ideas into
    professional cinematic prompts.
    """

    def __init__(
        self,
        backend: PromptBackendProtocol,

        config: Optional[
            PromptEnhancerConfig
        ] = None,

        logger: Optional[
            logging.Logger
        ] = None,

    ) -> None:


        self.backend = backend


        self.config = (

            config

            if config

            else PromptEnhancerConfig()

        )


        self.logger = (

            logger

            if logger

            else logging.getLogger(
                self.__class__.__name__
            )

        )



    # ========================================================
    # Enhance Prompt
    # ========================================================


    def enhance(
        self,
        request: PromptRequest,
    ) -> str:
        """
        Enhance raw prompt.
        """

        self._validate_request(
            request
        )


        self.logger.info(
            "Enhancing AI prompt"
        )


        try:

            settings = (
                self._build_settings()
            )


            result = self.backend.enhance(

                request.text,

                  # ========================================================
    # Settings Builder
    # ========================================================


    def _build_settings(
        self,
    ) -> Dict[str, Any]:
        """
        Build prompt enhancement settings.
        """

        return {

            "cinematic_style":
                self.config.cinematic_style,


            "documentary_style":
                self.config.documentary_style,


            "emotional_depth":
                self.config.emotional_depth,


            "detail_level":
                self.config.detail_level,

        }



    # ========================================================
    # Request Validation
    # ========================================================


    def _validate_request(
        self,
        request: PromptRequest,
    ) -> None:
        """
        Validate prompt request.
        """

        if not request.text.strip():

            raise PromptEnhancerError(
                "Prompt text cannot be empty"
            )



    # ========================================================
    # Keyword Processing
    # ========================================================


    def process_keywords(
        self,
        keywords: Optional[
            List[str]
        ],
    ) -> str:
        """
        Convert keywords into prompt context.
        """

        if not keywords:

            return ""


        return ", ".join(

            [

                keyword.strip()

                for keyword in keywords

                if keyword.strip()

            ]

        )



    # ========================================================
    # Cinematic Template Builder
    ========================================================


    def create_cinematic_template(
        self,
        request: PromptRequest,
    ) -> str:
        """
        Create cinematic prompt structure.
        """

        keywords = (

            self.process_keywords(
                request.keywords
            )

        )


        return (

            f"{request.text}. "

            f"Style: {request.genre}. "

            f"Mood: {request.mood}. "

            f"Visual elements: {keywords}. "

            "Professional documentary "

            "cinematic storytelling, "

            "Hollywood production quality."

        )



    # ========================================================
    # Prompt Presets
    # ========================================================


    def get_preset(
        self,
        preset: str = "documentary",
    ) -> Dict[str, Any]:
        """
        Return prompt style presets.
        """

        presets = {


            "documentary": {

                "tone":
                    "educational cinematic",

                "detail":
                    "high",

                "emotion":
                    "deep",

            },


            "thriller": {

                "tone":
                    "dark suspense",

                "detail":
                    "very high",

                "emotion":
                    "intense",

            },


            "historical": {

                "tone":
                    "ancient epic",

                "detail":
                    "high",

                "emotion":
                    "dramatic",

            },


            "mystery": {

                "tone":
                    "investigative cinematic",

                "detail":
                    "very high",

                "emotion":
                    "suspense",

            },

        }


        if preset not in presets:

            raise PromptEnhancerError(

                f"Unknown prompt preset: {preset}"

            )


        return presets[preset]



    # ========================================================
    # Style Application
    ========================================================


    def apply_style(
        self,
        prompt: str,
        style: str,
    ) -> str:
        """
        Apply cinematic writing style.
        """

        styles = {


            "cinematic":

                "cinematic atmosphere, dramatic visuals",


            "documentary":

                "realistic documentary storytelling",


            "epic":

                "large scale epic Hollywood feeling",


            "dark":

                "dark mysterious emotional tone",

        }


        if style not in styles:

            raise PromptEnhancerError(

                f"Unknown style: {style}"

            )


        return (

            f"{prompt}. "

            f"{styles[style]}."

        )
  \    # ========================================================
    # Prompt Metadata
    # ========================================================


    def create_metadata(
        self,
        request: PromptRequest,
        enhanced_prompt: str,
    ) -> Dict[str, Any]:
        """
        Create prompt metadata.
        """

        return {

            "original_prompt":
                request.text,


            "enhanced_prompt":
                enhanced_prompt,


            "genre":
                request.genre,


            "mood":
                request.mood,


            "keywords":
                request.keywords
                if request.keywords
                else [],


            "engine":
                "MystoriumX Prompt Enhancer",

        }



    # ========================================================
    # Batch Enhancement
    # ========================================================


    def enhance_batch(
        self,
        requests: List[
            PromptRequest
        ],
    ) -> List[str]:
        """
        Enhance multiple prompts.
        """

        results: List[str] = []


        for request in requests:

            results.append(

                self.enhance(
                    request
                )

            )


        return results



    # ========================================================
    # Configuration
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return enhancer configuration.
        """

        return {

            "cinematic_style":
                self.config.cinematic_style,


            "documentary_style":
                self.config.documentary_style,


            "emotional_depth":
                self.config.emotional_depth,


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
        Return enhancer health status.
        """

        return {

            "service":
                "PromptEnhancer",


            "status":
                "healthy",


            "backend":
                self.backend.__class__.__name__,


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
                "AI Cinematic Prompt Enhancer",


            "purpose":
                "Transform simple ideas into production prompts",


            "pipeline_stage":
                "AI Prompt Processing",

        }



    # ========================================================
    # Quality Validation
    # ========================================================


    def validate_prompt(
        self,
        prompt: str,
    ) -> bool:
        """
        Validate generated prompt quality.
        """

        if not prompt:

            return False


        if len(prompt.strip()) < 20:

            return False


        return True
                settings,

            )


            return result



        except Exception as exc:

            self.logger.exception(
                "Prompt enhancement failed"
            )


            raise PromptProcessingError(

                f"Unable to enhance prompt: {exc}"

            ) from exc
