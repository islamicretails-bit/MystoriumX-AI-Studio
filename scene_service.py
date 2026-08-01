# ============================================================
# MystoriumX AI Studio
# Service Layer - Scene Analysis Service
#
# File:
# app/services/scene_service.py
#
# Responsibility:
# Manage documentary video scene analysis workflow.
#
# Flow:
#
# Video
#   |
#   ↓
# Computer Vision Detector
#   |
#   ↓
# Scene Processing
#   |
#   ↓
# Scene Entities
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path

from typing import List, Dict, Any

from uuid import uuid4

import logging



from app.domain.entities import SceneEntity

from app.domain.enums import SceneMood

from app.core.exceptions import SceneDetectionError

from app.infrastructure.cv.opencv_detector import OpenCVDetector



logger = logging.getLogger(
    "MystoriumX.SceneService"
)



# ============================================================
# Scene Service
# ============================================================

class SceneService:
    """
    Handles video scene understanding.

    Responsibilities:

    - Detect scenes
    - Analyze intensity
    - Assign cinematic mood
    - Create SceneEntity objects

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
        Analyze uploaded documentary video.
        """


        if not video_path.exists():

            raise SceneDetectionError(

                "Video file not found",

                "VIDEO_NOT_FOUND"

            )


        try:

            logger.info(
                f"Starting scene analysis: {video_path}"
            )


            detected_scenes = (

                self.detector.detect_scenes(

                    video_path

                )

            )


            scenes = (

                self._build_scene_entities(

                    detected_scenes

                )

            )


            logger.info(

                f"{len(scenes)} scenes created"

            )


            return scenes



        except Exception as error:


            logger.exception(

                "Scene processing failed"

            )


            raise SceneDetectionError(

                str(error),

                "SCENE_PROCESSING_FAILED"

            )



    # ========================================================
    # Build Scene Entities
    # ========================================================

    def _build_scene_entities(
        self,
        scenes: List[Dict[str, Any]]
    ) -> List[SceneEntity]:

        """
        Convert detector output into domain entities.
        """


        result = []



        for scene in scenes:


            start = float(

                scene.get(

                    "start_time",

                    0

                )

            )


            end = float(

                scene.get(

                    "end_time",

                    0

                )

            )


            intensity = float(

                scene.get(

                    "intensity",

                    0

                )

            )


            entity = SceneEntity(

                scene_id=(

                    f"scene_"

                    f"{uuid4().hex[:8]}"

                ),

                start_time=start,

                end_time=end,

                duration=max(

                    end - start,

                    0

                ),

                confidence=float(

                    scene.get(

                        "confidence",

                        0

                    )

                ),

                mood=(

                    self._detect_mood(

                        scene

                    )

                ).value,

                intensity=intensity,

                description=scene.get(

                    "description"

                )

            )


            result.append(

                entity

            )



        return result



    # ========================================================
    # Detect Cinematic Mood
    # ========================================================

    def _detect_mood(
        self,
        scene: Dict[str, Any]
    ) -> SceneMood:

        """
        Determine scene emotion.
        """


        mood = scene.get(

            "mood"

        )



        if mood:


            try:

                return SceneMood(

                    mood.lower()

                )

            except ValueError:

                pass



        intensity = float(

            scene.get(

                "intensity",

                0

            )

        )



        if intensity >= 8:

            return SceneMood.ACTION



        if intensity >= 5:

            return SceneMood.TENSE



        return SceneMood.MYSTERIOUS



    # ========================================================
    # Scene Summary
    # ========================================================

    def generate_summary(
        self,
        scenes: List[SceneEntity]
    ) -> Dict[str, Any]:

        """
        Create scene analytics.
        """


        if not scenes:

            return {

                "total_scenes": 0,

                "total_duration": 0,

                "average_intensity": 0

            }



        return {


            "total_scenes":

                len(scenes),


            "total_duration":

                round(

                    sum(

                        scene.duration

                        for scene in scenes

                    ),

                    2

                ),


            "average_intensity":

                round(

                    sum(

                        scene.intensity

                        for scene in scenes

                    )

                    /

                    len(scenes),

                    2

                )

        }



# ============================================================
# Global Service Instance
# ============================================================

scene_service = SceneService()
