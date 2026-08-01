"""
MystoriumX AI Studio

Scene Analysis Service

Responsible for:
- Documentary video scene analysis
- Scene metadata processing
- Vision pipeline integration
- Scene extraction

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol



# ============================================================
# Exceptions
# ============================================================


class SceneServiceError(Exception):
    """
    Base scene service exception.
    """



class SceneAnalysisError(SceneServiceError):
    """
    Raised when scene analysis fails.
    """



# ============================================================
# Scene Detector Contract
# ============================================================


class SceneDetectorProtocol(Protocol):
    """
    Contract for computer vision scene detectors.

    Implementations:
    - OpenCV detector
    - AI vision model
    - Frame analyzer
    """

    def detect(
        self,
        video_path: Path,
    ) -> List[Dict[str, Any]]:
        ...



# ============================================================
# Scene Data Model
# ============================================================


@dataclass(slots=True)
class SceneData:
    """
    Structured documentary scene information.
    """

    scene_id: int

    start_time: float

    end_time: float

    description: str

    emotion: str = "neutral"

    objects: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Scene Service
# ============================================================


class SceneService:
    """
    Production scene analysis service.

    Converts raw video into structured
    documentary scene information.
    """

    def __init__(
        self,
        detector: SceneDetectorProtocol,
        logger: Optional[logging.Logger] = None,
    ) -> None:


        self.detector = detector


        self.logger = logger or logging.getLogger(
            self.__class__.__name__
        )



    # ========================================================
    # Public API
    # ========================================================


    def analyze(
        self,
        video_path: Path,
    ) -> List[Dict[str, Any]]:
        """
        Analyze documentary video scenes.

        Returns:
            List of scene dictionaries
        """


        self._validate_video(
            video_path
        )


        self.logger.info(
            "Starting video scene analysis"
        )


        try:

            raw_scenes = self.detector.detect(
                video_path
            )


            scenes = (
                self._normalize_scenes(
                    raw_scenes
                )
            )


            if not scenes:

                raise SceneAnalysisError(
                    "No scenes detected"
                )


            self.logger.info(
                f"Detected {len(scenes)} scenes"
            )


            return scenes


        except Exception as exc:

            self.logger.exception(
                "Scene analysis failed"
            )


            raise SceneAnalysisError(
                f"Scene detection failed: {exc}"
            ) from exc
              # ========================================================
    # Scene Normalization
    # ========================================================


    def _normalize_scenes(
        self,
        raw_scenes: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Convert detector output into
        standardized scene format.
        """

        normalized: List[Dict[str, Any]] = []


        for index, scene in enumerate(
            raw_scenes,
            start=1
        ):

            normalized_scene = {

                "scene_id":
                    index,


                "start_time":
                    float(
                        scene.get(
                            "start_time",
                            0.0
                        )
                    ),


                "end_time":
                    float(
                        scene.get(
                            "end_time",
                            0.0
                        )
                    ),


                "description":
                    scene.get(
                        "description",
                        "Unknown documentary scene"
                    ),


                "emotion":
                    scene.get(
                        "emotion",
                        "neutral"
                    ),


                "objects":
                    scene.get(
                        "objects",
                        []
                    ),


                "metadata":
                    scene.get(
                        "metadata",
                        {}
                    ),
            }


            normalized.append(
                normalized_scene
            )


        return normalized



    # ========================================================
    # Scene Data Conversion
    # ========================================================


    def convert_to_scene_objects(
        self,
        scenes: List[Dict[str, Any]],
    ) -> List[SceneData]:
        """
        Convert dictionaries into
        strongly typed SceneData objects.
        """

        result: List[SceneData] = []


        for scene in scenes:

            result.append(

                SceneData(

                    scene_id=
                        scene["scene_id"],


                    start_time=
                        scene["start_time"],


                    end_time=
                        scene["end_time"],


                    description=
                        scene["description"],


                    emotion=
                        scene.get(
                            "emotion",
                            "neutral"
                        ),


                    objects=
                        scene.get(
                            "objects",
                            []
                        ),


                    metadata=
                        scene.get(
                            "metadata",
                            {}
                        ),
                )
            )


        return result



    # ========================================================
    # Scene Metadata Generation
    # ========================================================


    def build_scene_metadata(
        self,
        scene: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate AI-friendly scene metadata.

        Used by:
        - Prompt Service
        - Music Generation
        """

        duration = (

            scene.get(
                "end_time",
                0
            )

            -

            scene.get(
                "start_time",
                0
            )
        )


        return {

            "scene_id":
                scene.get(
                    "scene_id"
                ),


            "duration":
                duration,


            "description":
                scene.get(
                    "description"
                ),


            "emotion":
                scene.get(
                    "emotion",
                    "neutral"
                ),


            "visual_elements":
                scene.get(
                    "objects",
                    []
                ),


            "cinematic_context":
                self._generate_context(
                    scene
                ),
        }



    def _generate_context(
        self,
        scene: Dict[str, Any],
    ) -> str:
        """
        Create cinematic context description.
        """

        emotion = scene.get(
            "emotion",
            "neutral"
        )


        description = scene.get(
            "description",
            ""
        )


        return (
            f"A cinematic documentary scene "
            f"showing {description} "
            f"with {emotion} emotional tone."
        )



    # ========================================================
    # Validation
    # ========================================================


    def _validate_video(
        self,
        video_path: Path,
    ) -> None:
        """
        Validate uploaded video file.
        """

        if not video_path.exists():

            raise SceneAnalysisError(
                f"Video file not found: {video_path}"
            )


        if not video_path.is_file():

            raise SceneAnalysisError(
                "Video path is not a file"
            )
              # ========================================================
    # Scene Summary Generation
    # ========================================================


    def create_summary(
        self,
        scenes: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Create complete video scene summary.

        Used for:
        - AI prompt generation
        - Project reports
        - Analytics
        """

        total_duration = 0.0

        emotions: Dict[str, int] = {}

        objects: List[str] = []


        for scene in scenes:

            duration = (

                scene.get(
                    "end_time",
                    0
                )

                -

                scene.get(
                    "start_time",
                    0
                )
            )


            total_duration += duration


            emotion = scene.get(
                "emotion",
                "neutral"
            )


            emotions[emotion] = (
                emotions.get(
                    emotion,
                    0
                )
                + 1
            )


            objects.extend(

                scene.get(
                    "objects",
                    []
                )
            )


        return {

            "total_scenes":
                len(scenes),


            "total_duration":
                total_duration,


            "dominant_emotions":
                emotions,


            "detected_objects":
                list(
                    set(objects)
                ),
        }



    # ========================================================
    # Scene Filtering
    # ========================================================


    def filter_by_emotion(
        self,
        scenes: List[Dict[str, Any]],
        emotion: str,
    ) -> List[Dict[str, Any]]:
        """
        Filter scenes by emotional category.
        """

        return [

            scene

            for scene in scenes

            if scene.get(
                "emotion",
                ""
            ).lower()

            ==
            
            emotion.lower()
        ]



    def get_scene(
        self,
        scenes: List[Dict[str, Any]],
        scene_id: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve single scene by ID.
        """

        for scene in scenes:

            if scene.get(
                "scene_id"
            ) == scene_id:

                return scene


        return None



    # ========================================================
    # AI Prompt Preparation Data
    # ========================================================


    def prepare_prompt_context(
        self,
        scenes: List[Dict[str, Any]],
    ) -> str:
        """
        Prepare scene information
        for cinematic prompt generation.
        """

        context_parts: List[str] = []


        for scene in scenes:

            context_parts.append(

                (
                    f"Scene {scene.get('scene_id')}: "
                    f"{scene.get('description')} "
                    f"Emotion: "
                    f"{scene.get('emotion')}."
                )
            )


        return "\n".join(
            context_parts
        )



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
                "SceneService",


            "status":
                "healthy",


            "detector":
                self.detector.__class__.__name__,
        }



    # ========================================================
    # Configuration Information
    # ========================================================


    def get_information(
        self,
    ) -> Dict[str, Any]:
        """
        Return service information.
        """

        return {

            "service":
                "Scene Analysis Service",


            "purpose":
                "Documentary video scene understanding",


            "architecture":
                "Clean Architecture",


            "pipeline_stage":
                "Video Processing",

        }
