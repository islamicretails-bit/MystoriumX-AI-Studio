# ============================================================
# MystoriumX AI Studio
# Machine Learning Layer - MusicGen Provider
#
# File:
# app/infrastructure/ml/musicgen_provider.py
#
# Responsibility:
# AI cinematic music generation engine.
#
# Features:
# - MusicGen model integration
# - Prompt based soundtrack generation
# - Audio export
# - Model resource handling
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path

from typing import Optional


import logging



import torch

import torchaudio



from app.core.exceptions import (

    MusicGenerationError

)



from app.infrastructure.ml.model_loader import (

    model_loader

)



logger = logging.getLogger(

    "MystoriumX.MusicGen"

)



# ============================================================
# MusicGen Provider
# ============================================================

class MusicGenProvider:
    """
    AI music generation provider.

    Responsible for:

    Prompt
       |
       ↓
    MusicGen Model
       |
       ↓
    Generated Audio

    """



    def __init__(
        self,
        model_name: str =
        "facebook/musicgen-medium"
    ) -> None:


        self.model_name = model_name


        self.model = None


        self.processor = None



        logger.info(

            "MusicGen Provider initialized"

        )



    # ========================================================
    # Load Model
    # ========================================================

    def load(
        self
    ) -> None:

        """
        Load MusicGen model.
        """


        try:


            self.model = (

                model_loader
                .load_transformer_model(

                    self.model_name

                )

            )


            self.processor = (

                model_loader
                .get_processor(

                    self.model_name

                )

            )


            logger.info(

                "MusicGen model loaded"

            )



        except Exception as error:


            raise MusicGenerationError(

                str(error),

                "MUSICGEN_LOAD_FAILED"

            )



    # ========================================================
    # Generate Music
    # ========================================================

    def generate(
        self,
        prompt: str,
        duration_seconds: int,
        output_path: Path
    ) -> Path:

        """
        Generate cinematic soundtrack.

        Note:
        Requires MusicGen compatible model.
        """


        if self.model is None:


            self.load()



        try:


            logger.info(

                "Generating music..."

            )



            inputs = self.processor(

                text=[prompt],

                padding=True,

                return_tensors="pt"

            )



            inputs = {


                key:

                value.to(

                    model_loader.device

                )

                for key, value in inputs.items()

            }



            with torch.no_grad():


                audio_values = (

                    self.model.generate(

                        **inputs,

                        max_new_tokens=

                        duration_seconds * 50

                    )

                )



            waveform = (

                audio_values[0]

                .cpu()

            )



            sample_rate = (

                32000

            )



            torchaudio.save(

                str(output_path),

                waveform,

                sample_rate

            )



            logger.info(

                f"Music exported: {output_path}"

            )



            return output_path



        except Exception as error:


            logger.exception(

                "Music generation failed"

            )


            raise MusicGenerationError(

                str(error),

                "MUSIC_GENERATION_FAILED"

            )



    # ========================================================
    # Check Status
    # ========================================================

    def is_ready(
        self
    ) -> bool:

        """
        Check provider availability.
        """


        return (

            self.model is not None

        )



    # ========================================================
    # Release Model
    # ========================================================

    def unload(
        self
    ) -> None:

        """
        Release model resources.
        """


        self.model = None


        self.processor = None



        model_loader.clear_memory()



        logger.info(

            "MusicGen resources released"

        )



# ============================================================
# Global Instance
# ============================================================

musicgen_provider = MusicGenProvider()
