# ============================================================
# MystoriumX AI Studio
# Machine Learning Layer - Cinematic Prompt Enhancer
#
# File:
# app/infrastructure/ml/prompt_enhancer.py
#
# Responsibility:
# Convert simple user ideas into professional
# cinematic AI music prompts.
#
# Features:
# - Documentary style enhancement
# - Emotion mapping
# - Scene context analysis
# - MusicGen optimized prompts
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from typing import Dict, Optional


import logging



logger = logging.getLogger(

    "MystoriumX.PromptEnhancer"

)



# ============================================================
# Prompt Enhancer
# ============================================================

class PromptEnhancer:
    """
    AI cinematic prompt optimization engine.

    Converts:

    Simple Prompt:
        "dark mystery music"

    Into:

        "A dark cinematic documentary score,
        deep atmospheric textures,
        slow orchestral tension,
        emotional storytelling..."

    """



    def __init__(
        self
    ) -> None:


        self.genre_styles = {

            "mystery":

                "dark cinematic mystery, atmospheric tension, investigative documentary",

            "history":

                "ancient cinematic orchestra, epic historical documentary",

            "horror":

                "dark ambient horror score, psychological tension",

            "space":

                "deep futuristic ambient, cosmic cinematic atmosphere",

            "nature":

                "emotional organic documentary soundtrack",

            "war":

                "powerful orchestral battle score, dramatic percussion"

        }



        self.emotion_styles = {

            "sad":

                "emotional piano, melancholic strings, deep feeling",

            "epic":

                "massive orchestra, powerful drums, heroic atmosphere",

            "tense":

                "slow building suspense, dark textures, rising intensity",

            "hopeful":

                "warm cinematic harmony, inspirational atmosphere",

            "mysterious":

                "shadowy ambience, mysterious sound design"

        }



        logger.info(

            "Prompt Enhancer initialized"

        )



    # ========================================================
    # Enhance Prompt
    # ========================================================

    def enhance_prompt(
        self,
        prompt: str,
        context: Optional[Dict] = None
    ) -> str:

        """
        Generate professional cinematic prompt.
        """


        context = context or {}



        original = prompt.strip()



        style = self._detect_style(

            original,

            context

        )



        emotion = self._detect_emotion(

            original,

            context

        )



        intensity = context.get(

            "intensity",

            5

        )



        enhanced_prompt = (

            f"{style}. "

            f"{emotion}. "

            f"Cinematic documentary soundtrack, "

            f"professional film score, "

            f"high quality orchestral arrangement, "

            f"immersive atmosphere, "

            f"intensity level {intensity}/10. "

            f"Original concept: {original}"

        )



        logger.info(

            "Prompt enhanced successfully"

        )



        return enhanced_prompt



    # ========================================================
    # Detect Style
    # ========================================================

    def _detect_style(
        self,
        prompt: str,
        context: Dict
    ) -> str:

        """
        Detect cinematic genre.
        """


        selected_style = context.get(

            "style"

        )



        if selected_style in self.genre_styles:


            return self.genre_styles[selected_style]



        text = prompt.lower()



        for key, value in self.genre_styles.items():


            if key in text:

                return value



        return (

            "cinematic documentary orchestral score"

        )



    # ========================================================
    # Detect Emotion
    # ========================================================

    def _detect_emotion(
        self,
        prompt: str,
        context: Dict
    ) -> str:

        """
        Detect emotional direction.
        """


        selected = context.get(

            "emotion"

        )



        if selected in self.emotion_styles:


            return self.emotion_styles[selected]



        text = prompt.lower()



        for key, value in self.emotion_styles.items():


            if key in text:

                return value



        return (

            "deep emotional cinematic atmosphere"

        )



    # ========================================================
    # MusicGen Format
    # ========================================================

    def create_musicgen_prompt(
        self,
        enhanced_prompt: str
    ) -> str:

        """
        Prepare final MusicGen compatible prompt.
        """


        return (

            "Instrumental only. "

            "No vocals. "

            "Hollywood documentary film score. "

            +

            enhanced_prompt

        )



    # ========================================================
    # Prompt Analysis
    # ========================================================

    def analyze_prompt(
        self,
        prompt: str
    ) -> Dict:

        """
        Return prompt intelligence data.
        """


        return {


            "length":

                len(prompt),


            "words":

                len(

                    prompt.split()

                ),


            "cinematic_ready":

                len(prompt.split()) > 5

        }



# ============================================================
# Global Instance
# ============================================================

prompt_enhancer = PromptEnhancer()
