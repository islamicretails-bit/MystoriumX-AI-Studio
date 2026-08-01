# ============================================================
# MystoriumX AI Studio
# Computer Vision Layer - OpenCV Scene Detector
#
# File:
# app/infrastructure/cv/opencv_detector.py
#
# Responsibility:
# Video scene detection and visual timeline analysis.
#
# Technology:
# - OpenCV
# - Computer Vision
#
# ============================================================


from __future__ import annotations


from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import logging


import cv2



logger = logging.getLogger(
    "MystoriumX.OpenCVDetector"
)



# ============================================================
# Scene Boundary Model
# ============================================================

@dataclass
class SceneBoundary:
    """
    Represents detected video scene boundary.
    """

    start_frame: int

    end_frame: int

    start_time: float

    end_time: float

    confidence: float



# ============================================================
# OpenCV Detector
# ============================================================

class OpenCVSceneDetector:
    """
    OpenCV based documentary scene detector.

    Features:

    - Video loading
    - Frame sampling
    - Scene change detection
    - Timeline extraction

    Future:

    - Deep learning vision models
    - CLIP embeddings
    - Object detection
    - Emotion recognition

    """



    def __init__(
        self,
        threshold: float = 35.0,
        sample_rate: int = 5
    ) -> None:


        self.threshold = threshold

        self.sample_rate = sample_rate


        logger.info(
            "OpenCV Scene Detector initialized"
        )



    # ========================================================
    # Main Detection Method
    # ========================================================

    def detect_scenes(
        self,
        video_path: Path
    ) -> List[SceneBoundary]:

        """
        Detect scene changes from video.

        Args:

            video_path:
                Input video file.

        Returns:

            List of scene boundaries.

        """


        self._validate_video(
            video_path
        )


        capture = cv2.VideoCapture(
            str(video_path)
        )


        if not capture.isOpened():

            raise RuntimeError(
                "Unable to open video."
            )



        fps = capture.get(
            cv2.CAP_PROP_FPS
        )


        total_frames = int(
            capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )



        scenes = []


        previous_frame = None


        start_frame = 0


        current_frame = 0



        try:


            while True:


                success, frame = (
                    capture.read()
                )


                if not success:

                    break



                if current_frame % self.sample_rate != 0:

                    current_frame += 1

                    continue



                gray = cv2.cvtColor(

                    frame,

                    cv2.COLOR_BGR2GRAY

                )



                if previous_frame is not None:


                    difference = (
                        self._calculate_difference(

                            previous_frame,

                            gray

                        )
                    )



                    if difference > self.threshold:


                        scenes.append(

                            SceneBoundary(

                                start_frame=start_frame,

                                end_frame=current_frame,

                                start_time=(
                                    start_frame / fps
                                ),

                                end_time=(
                                    current_frame / fps
                                ),

                                confidence=min(

                                    difference / 100,

                                    1.0

                                )

                            )

                        )


                        start_frame = current_frame



                previous_frame = gray


                current_frame += 1



            if start_frame < total_frames:


                scenes.append(

                    SceneBoundary(

                        start_frame=start_frame,

                        end_frame=total_frames,

                        start_time=(
                            start_frame / fps
                        ),

                        end_time=(
                            total_frames / fps
                        ),

                        confidence=1.0

                    )

                )



            logger.info(

                f"Detected {len(scenes)} scenes"

            )


            return scenes



        finally:


            capture.release()



    # ========================================================
    # Frame Difference
    # ========================================================

    def _calculate_difference(
        self,
        frame_a,
        frame_b
    ) -> float:

        """
        Calculate visual difference.
        """


        difference = cv2.absdiff(

            frame_a,

            frame_b

        )


        score = (

            difference.mean()

        )


        return float(
            score
        )



    # ========================================================
    # Validation
    # ========================================================

    def _validate_video(
        self,
        video_path: Path
    ) -> None:

        """
        Validate video file.
        """


        if not video_path.exists():

            raise FileNotFoundError(

                f"Video not found: {video_path}"

            )


        supported = [

            ".mp4",

            ".mov",

            ".avi",

            ".mkv"

        ]


        if video_path.suffix.lower() not in supported:

            raise ValueError(

                "Unsupported video format"

            )



    # ========================================================
    # Metadata Export
    # ========================================================

    def scenes_to_dict(
        self,
        scenes: List[SceneBoundary]
    ) -> List[Dict[str, Any]]:

        """
        Convert scenes into JSON format.
        """


        return [

            {

                "start_frame":
                    scene.start_frame,

                "end_frame":
                    scene.end_frame,

                "start_time":
                    scene.start_time,

                "end_time":
                    scene.end_time,

                "confidence":
                    scene.confidence

            }

            for scene in scenes

        ]
