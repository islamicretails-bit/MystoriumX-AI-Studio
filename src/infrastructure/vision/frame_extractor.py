"""
MystoriumX AI Studio

Video Frame Extraction Engine

Responsible for:
- Extracting frames from videos
- Creating keyframes
- Preparing images for AI analysis

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging

from dataclasses import dataclass
from pathlib import Path

from typing import Any, Dict, List, Optional, Protocol



# ============================================================
# Exceptions
# ============================================================


class FrameExtractionError(Exception):
    """
    Base frame extraction exception.
    """



class VideoProcessingError(FrameExtractionError):
    """
    Raised when video processing fails.
    """



# ============================================================
# Video Backend Contract
# ============================================================


class VideoBackendProtocol(Protocol):
    """
    Contract for video processing backend.

    Implementations:
    - FFmpeg wrapper
    - OpenCV backend
    """

    def extract_frames(
        self,
        video_file: Path,
        output_directory: Path,
        fps: int,
    ) -> Path:
        ...



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class FrameExtractorConfig:
    """
    Frame extraction settings.
    """

    fps: int = 1

    image_format: str = "jpg"

    max_frames: int = 500

    quality: int = 95



# ============================================================
# Frame Extractor
# ============================================================


class FrameExtractor:
    """
    Production video frame extractor.

    Converts videos into AI-ready
    image sequences.
    """

    def __init__(
        self,
        backend: VideoBackendProtocol,
        config: Optional[
            FrameExtractorConfig
        ] = None,

        logger: Optional[
            logging.Logger
        ] = None,

    ) -> None:


        self.backend = backend


        self.config = (

            config

            if config

            else FrameExtractorConfig()

        )


        self.logger = (

            logger

            if logger

            else logging.getLogger(
                self.__class__.__name__
            )

        )



    # ========================================================
    # Public API
    # ========================================================


    def extract(
        self,
        video_file: Path,
        output_directory: Path,
    ) -> Path:
        """
        Extract frames from video.
        """

        self._validate_video(
            video_file
        )


        self.logger.info(
            "Starting frame extraction"
        )


        try:

            output_directory.mkdir(
                parents=True,
                exist_ok=True
            )


            result = (

                self.backend.extract_frames(
                    video_file,
                    output_directory,
                    self.config.fps,
                )

            )


            self.logger.info(
                "Frame extraction completed"
            )


            return result


        except Exception as exc:

            self.logger.exception(
                "Frame extraction failed"
            )


            raise VideoProcessingError(
                f"Unable to extract frames: {exc}"
            ) from exc
              # ========================================================
    # Frame Listing
    # ========================================================


    def list_frames(
        self,
        directory: Path,
    ) -> List[Path]:
        """
        Return extracted frame files.
        """

        if not directory.exists():

            raise FrameExtractionError(
                "Frame directory does not exist"
            )


        frames = sorted(

            [

                file

                for file in directory.iterdir()

                if file.is_file()

                and file.suffix.lower()

                in {

                    ".jpg",

                    ".jpeg",

                    ".png",

                }

            ]

        )


        if len(frames) > self.config.max_frames:

            frames = frames[
                :self.config.max_frames
            ]


        return frames



    # ========================================================
    # Frame Metadata
    # ========================================================


    def create_frame_metadata(
        self,
        frames: List[Path],
    ) -> List[Dict[str, Any]]:
        """
        Create metadata for extracted frames.
        """

        metadata: List[
            Dict[str, Any]
        ] = []


        for index, frame in enumerate(
            frames,
            start=1
        ):

            metadata.append(

                {

                    "frame_id":
                        index,


                    "file":
                        str(frame),


                    "format":
                        frame.suffix.lower(),


                    "size":
                        frame.stat().st_size,

                }

            )


        return metadata



    # ========================================================
    # Keyframe Selection
    # ========================================================


    def select_keyframes(
        self,
        frames: List[Path],
        interval: int = 10,
    ) -> List[Path]:
        """
        Select important frames
        for AI scene analysis.
        """

        if interval <= 0:

            raise FrameExtractionError(
                "Interval must be positive"
            )


        return [

            frame

            for index, frame
            in enumerate(frames)

            if index % interval == 0

        ]



    # ========================================================
    # Frame Validation
    # ========================================================


    def validate_frames(
        self,
        frames: List[Path],
    ) -> bool:
        """
        Validate extracted frames.
        """

        if not frames:

            return False


        for frame in frames:

            if not frame.exists():

                return False


            if frame.stat().st_size <= 0:

                return False


        return True



    # ========================================================
    # Extraction Profiles
    # ========================================================


    def apply_profile(
        self,
        profile: str = "documentary",
    ) -> None:
        """
        Apply extraction profile.

        Profiles:
        - documentary
        - fast_analysis
        - high_quality
        """

        profiles = {


            "documentary": {

                "fps": 1,

                "max_frames": 500,

            },


            "fast_analysis": {

                "fps": 0.5,

                "max_frames": 200,

            },


            "high_quality": {

                "fps": 2,

                "max_frames": 1000,

            },

        }


        if profile not in profiles:

            raise FrameExtractionError(

                f"Unknown profile: {profile}"

            )


        selected = profiles[profile]


        self.config.fps = (
            selected["fps"]
        )


        self.config.max_frames = (
            selected["max_frames"]
        )


        self.logger.info(
            f"Applied frame profile: {profile}"
        )
          # ========================================================
    # Frame Timeline Mapping
    # ========================================================


    def create_timeline_map(
        self,
        frames: List[Path],
        fps: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Map frames with video timeline.
        """

        frame_rate = (

            fps

            if fps

            else self.config.fps

        )


        if frame_rate <= 0:

            raise FrameExtractionError(
                "FPS must be greater than zero"
            )


        timeline: List[
            Dict[str, Any]
        ] = []


        for index, frame in enumerate(
            frames
        ):

            timeline.append(

                {

                    "frame":
                        str(frame),


                    "frame_number":
                        index + 1,


                    "timestamp":
                        round(
                            index / frame_rate,
                            3
                        ),

                }

            )


        return timeline



    # ========================================================
    # Frame Summary
    # ========================================================


    def create_summary(
        self,
        frames: List[Path],
    ) -> Dict[str, Any]:
        """
        Generate frame extraction summary.
        """

        total_size = 0


        for frame in frames:

            if frame.exists():

                total_size += (
                    frame.stat()
                    .st_size
                )


        return {

            "total_frames":
                len(frames),


            "total_size_bytes":
                total_size,


            "format":
                self.config.image_format,


            "fps":
                self.config.fps,

        }



    # ========================================================
    # Configuration Access
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return extractor configuration.
        """

        return {

            "fps":
                self.config.fps,


            "image_format":
                self.config.image_format,


            "max_frames":
                self.config.max_frames,


            "quality":
                self.config.quality,

        }



    # ========================================================
    # Diagnostics
    # ========================================================


    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return extractor health status.
        """

        return {

            "service":
                "FrameExtractor",


            "status":
                "healthy",


            "backend":
                self.backend.__class__.__name__,


            "fps":
                self.config.fps,

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
                "Video Frame Extraction Engine",


            "purpose":
                "Prepare video frames for AI scene analysis",


            "pipeline_stage":
                "Vision Processing",

        }



    # ========================================================
    # Supported Video Formats
    # ========================================================


    def is_supported_video(
        self,
        video_file: Path,
    ) -> bool:
        """
        Check supported video formats.
        """

        supported_formats = {

            ".mp4",

            ".mov",

            ".mkv",

            ".avi",

            ".webm",

        }


        return (

            video_file.suffix.lower()

            in

            supported_formats

        )
