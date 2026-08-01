# ============================================================
# MystoriumX AI Studio
# Service Layer - Cinematic Prompt Service
#
# File:
# app/services/prompt_service.py
#
# Responsibility:
# Generate professional cinematic AI music prompts.
#
# Flow:
#
# Scene Analysis
#       +
# User Idea
#       |
#       ↓
# Prompt Enhancement
#       |
#       ↓
# MusicGen Prompt
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from typing import List, Dict, Any, Optional


import logging



from app.domain.entities import SceneEntity


from app.infrastructure.ml.prompt_enhancer import (

    PromptEnhancer

)



from app.core.exceptions import (

    MusicGenerationError

)



logger = logging.getLogger(

    "MystoriumX.PromptService"

)



# ============================================================
# Prompt Service
# ============================================================

class PromptService:
    """
    Controls cinematic prompt generation.

    Responsibilities:

    - Analyze scene information
    - Understand documentary mood
    - Enhance user prompts
    - Create MusicGen-ready prompts

    """



    def __init__(
        self,
        enhancer: Optional[PromptEnhancer] = None
    ) -> None:


        self.enhancer = (

            enhancer

            if enhancer

            else PromptEnhancer()

        )


        logger.info(

            "Prompt Service initialized"

        )



    # ========================================================
    # Generate Prompt
    # ========================================================

    def generate_prompt(
        self,
        user_prompt: str,
        scenes: List[SceneEntity]
    ) -> str:

        """
        Create final cinematic music prompt.
        """


        try:


            context = (

                self._build_scene_context(

                    scenes

                )

            )



            enhanced = (

                self.enhancer.enhance_prompt(

                    user_prompt,

                    context

                )

            )



            final_prompt = (

                self.enhancer.create_musicgen_prompt(

                    enhanced

                )

            )



            logger.info(

                "Cinematic prompt generated"

            )



            return final_prompt



        except Exception as error:


            logger.exception(

                "Prompt generation failed"

            )


            raise MusicGenerationError(

                str(error),

                "PROMPT_GENERATION_FAILED"

            )



    # ========================================================
    # Build Scene Context
    # ========================================================

    def _build_scene_context(
        self,
        scenes: List[SceneEntity]
    ) -> Dict[str, Any]:

        """
        Convert scene analysis into AI context.
        """


        if not scenes:


            return {


                "style":

                    "documentary",


                "emotion":

                    "mysterious",


                "intensity":

                    5

            }



        moods = [

            scene.mood

            for scene in scenes

            if scene.mood

        ]



        average_intensity = (

            sum(

                scene.intensity

                for scene in scenes

            )

            /

            len(scenes)

        )



        dominant_mood = (

            max(

                set(moods),

                key=moods.count

            )

            if moods

            else

            "mysterious"

        )



        return {


            "style":

                "cinematic documentary",


            "emotion":

                dominant_mood,


            "intensity":

                round(

                    average_intensity,

                    1

                )

        }



    # ========================================================
    # Generate Multiple Variations
    # ========================================================

    def generate_variations(
        self,
        prompt: str,
        scenes: List[SceneEntity],
        count: int = 3
    ) -> List[str]:

        """
        Generate multiple soundtrack ideas.
        """


        results = []



        for index in range(count):


            variation = self.generate_prompt(

                f"{prompt} variation {index + 1}",

                scenes

            )


            results.append(

                variation

            )



        return results



# ============================================================
# Global Instance
# ============================================================

prompt_service = PromptService()
