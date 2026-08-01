# ============================================================
# MystoriumX AI Studio
# Service Layer - Scene Analysis Service
#
# File:
# app/services/scene_service.py
#
# Responsibility:
# Coordinate video scene analysis workflow.
#
# Flow:
#
# Video
#   |
#   ↓
# OpenCV Detector
#   |
#   ↓
# Scene Entities
#   |
#   ↓
# Pipeline
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path

from typing import List, Dict, Any


import logging


import uuid



from app.domain.entities import (

    SceneEntity

)



from app.domain.enums import (

    SceneMood

)



from app.core.exceptions import (

    SceneDetectionError

)



from app.infrastructure.cv.opencv_detector import (

    OpenCVDetector

)



logger = logging.getLogger(

    "MystoriumX.SceneService"

)



# ============================================================
# Scene Service
# ============================================================

class SceneService:
    """
    Professional scene analysis service.

    Responsible for:

    - Video scene detection
    - Scene classification
    - Metadata generation
    - Domain entity creation

    """



    def __init__(
        self,
        detector: OpenCVDetector | None = None
    ) -> None:


        self.detector = (

            detector

            if detector

            else OpenCVDetector()

        )



        logger.info(

            "Scene Service initialized"

        )



    # ========================================================
    # Analyze Video
    # ========================================================

    def analyze_video(
        self,
        video_path: Path
    ) -> List[SceneEntity]:

        """
        Analyze documentary video.

        Returns:
            List of SceneEntity objects.
        """


        if not video_path.exists():

            raise SceneDetectionError(

                "Video file not found",

                "VIDEO_NOT_FOUND"

            )



        try:


            logger.info(

                f"Analyzing video: {video_path}"

            )



            raw_scenes = (

                self.detector
                .detect_scenes(

                    video_path

                )

            )



            scenes = (

                self._convert_to_entities(

                    raw_scenes

                )

            )



            logger.info(

                f"Detected {len(scenes)} scenes"

            )



            return scenes



        except SceneDetectionError:


            raise



        except Exception as error:


            logger.exception(

                "Scene analysis failed"

            )


            raise SceneDetectionError(

                str(error),

                "SCENE_ANALYSIS_FAILED"

            )



    # ========================================================
    # Convert Detector Output
    # ========================================================

    def _convert_to_entities(
        self,
        detected_scenes: List[Dict[str, Any]]
    ) -> List[SceneEntity]:

        """
        Convert CV output into domain objects.
        """


        scene_entities: List[SceneEntity] = []



        for index, scene in enumerate(

            detected_scenes

        ):



            start_time = float(

                scene.get(

                    "start_time",

                    0

                )

            )



            end_time = float(

                scene.get(

                    "end_time",

                    0

                )

            )



            duration = (

                end_time

                -

                start_time

            )



            mood = (

                self._detect_mood(

                    scene

                )

            )



            entity = SceneEntity(

                scene_id=(

                    f"scene_"

                    f"{uuid.uuid4().hex[:8]}"

                ),

                start_time=start_time,

                end_time=end_time,

                duration=max(

                    duration,

                    0

                ),

                confidence=float(

                    scene.get(

                        "confidence",

                        0.0

                    )

                ),

                mood=mood.value,

                intensity=float(

                    scene.get(

                        "intensity",

                        0.0

                    )

                ),

                description=scene.get(

                    "description"

                )

            )



            scene_entities.append(

                entity

            )



        return scene_entities



    # ========================================================
    # Mood Detection
    # ========================================================

    def _detect_mood(
        self,
        scene_data: Dict[str, Any]
    ) -> SceneMood:

        """
        Determine cinematic mood.

        Future:
        Can connect Vision Transformer model.
        """


        provided_mood = scene_data.get(

            "mood"

        )



        if provided_mood:


            try:

                return SceneMood(

                    provided_mood.lower()

                )


            except ValueError:


                pass



        intensity = float(

            scene_data.get(

                "intensity",

                0

            )

        )



        if intensity >= 8:


            return SceneMood.ACTION



        if intensity >= 5:


            return SceneMood.TENSE



        return SceneMood.UNKNOWN



    # ========================================================
    # Generate Scene Summary
    # ========================================================

    def create_summary(
        self,
        scenes: List[SceneEntity]
    ) -> Dict[str, Any]:

        """
        Generate scene analytics summary.
        """


        if not scenes:


            return {


                "total_scenes": 0,


                "average_intensity": 0

            }



        total_intensity = sum(

            scene.intensity

            for scene in scenes

        )



        return {


            "total_scenes":

                len(scenes),


            "total_duration":

                sum(

                    scene.duration

                    for scene in scenes

                ),


            "average_intensity":

                round(

                    total_intensity

                    /

                    len(scenes),

                    2

                )

        }



# ============================================================
# Global Instance
# ============================================================

scene_service = SceneService()
