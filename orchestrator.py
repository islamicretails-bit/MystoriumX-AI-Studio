# ============================================================
# MystoriumX AI Studio
# Service Layer - AI Pipeline Orchestrator
#
# File:
# app/services/orchestrator.py
#
# Responsibility:
# Central controller for complete AI documentary pipeline.
#
# Pipeline:
#
# Upload
#   |
#   ↓
# Scene Analysis
#   |
#   ↓
# Prompt Generation
#   |
#   ↓
# Music Generation
#   |
#   ↓
# Audio Mastering
#   |
#   ↓
# Export
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path

from typing import Dict, Any, Optional, Callable


import logging



from app.domain.enums import ProcessingStage



from app.schemas.user_input import PipelineRequest



from app.services.scene_service import scene_service

from app.services.prompt_service import prompt_service

from app.services.export_service import export_service



from app.infrastructure.ml.musicgen_provider import (

    musicgen_provider

)



from app.core.exceptions import (

    PipelineExecutionError

)



logger = logging.getLogger(

    "MystoriumX.Orchestrator"

)



# ============================================================
# Pipeline Orchestrator
# ============================================================

class PipelineOrchestrator:
    """
    Main AI workflow controller.

    Connects all production modules.

    """



    def __init__(

        self,

        progress_callback: Optional[
            Callable[[str, float], None]
        ] = None

    ) -> None:


        self.progress_callback = progress_callback



        logger.info(

            "Pipeline Orchestrator initialized"

        )



    # ========================================================
    # Execute Pipeline
    # ========================================================

    def execute(

        self,

        request: PipelineRequest

    ) -> Dict[str, Any]:

        """
        Execute complete documentary pipeline.

        """

        try:


            self._update_progress(

                ProcessingStage.INITIALIZATION,

                0.05

            )



            # ------------------------------------------------
            # Step 1
            # Scene Analysis
            # ------------------------------------------------


            scenes = []


            if request.scene_analysis:


                self._update_progress(

                    ProcessingStage.SCENE_DETECTION,

                    0.20

                )


                scenes = (

                    scene_service.analyze_video(

                        request.scene_analysis.video_path

                    )

                )



            # ------------------------------------------------
            # Step 2
            # Prompt Generation
            # ------------------------------------------------


            self._update_progress(

                ProcessingStage.PROMPT_GENERATION,

                0.35

            )


            user_prompt = (

                request.prompt.prompt

                if request.prompt

                else

                "cinematic documentary soundtrack"

            )


            final_prompt = (

                prompt_service.generate_prompt(

                    user_prompt,

                    scenes

                )

            )



            # ------------------------------------------------
            # Step 3
            # Music Generation
            # ------------------------------------------------


            self._update_progress(

                ProcessingStage.MUSIC_GENERATION,

                0.50

            )



            generated_audio = self._generate_music(

                final_prompt,

                request

            )



            # ------------------------------------------------
            # Step 4
            # Export
            # ------------------------------------------------


            self._update_progress(

                ProcessingStage.FINAL_EXPORT,

                0.85

            )



            export_result = (

                export_service.export_files(

                    request.project_id,

                    [

                        generated_audio

                    ]

                )

            )



            self._update_progress(

                ProcessingStage.FINAL_EXPORT,

                1.0

            )



            return {


                "success": True,


                "project_id":

                    request.project_id,


                "prompt":

                    final_prompt,


                "audio":

                    str(generated_audio),


                "export":

                    export_result


            }



        except Exception as error:


            logger.exception(

                "Pipeline failed"

            )


            raise PipelineExecutionError(

                str(error),

                "PIPELINE_FAILED"

            )



    # ========================================================
    # Generate Music
    # ========================================================

    def _generate_music(

        self,

        prompt: str,

        request: PipelineRequest

    ) -> Path:

        """
        Generate AI soundtrack.
        """


        output_directory = Path(

            "generated_audio"

        )


        output_directory.mkdir(

            exist_ok=True

        )



        output_file = (

            output_directory

            /

            f"{request.project_id}.wav"

        )



        duration = 60



        if request.music:


            duration = (

                request.music.duration_seconds

            )



        generated = (

            musicgen_provider.generate(

                prompt,

                duration,

                output_file

            )

        )



        return generated



    # ========================================================
    # Progress Update
    # ========================================================

    def _update_progress(

        self,

        stage: ProcessingStage,

        progress: float

    ) -> None:

        """
        Send progress updates.
        """


        logger.info(

            f"{stage.value}: {progress * 100}%"

        )



        if self.progress_callback:


            self.progress_callback(

                stage.value,

                progress

            )



# ============================================================
# Global Instance
# ============================================================

pipeline_orchestrator = PipelineOrchestrator()
