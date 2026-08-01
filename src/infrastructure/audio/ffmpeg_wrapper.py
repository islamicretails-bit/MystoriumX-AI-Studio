"""
MystoriumX AI Studio

FFmpeg Wrapper Engine

Responsible for:
- FFmpeg command execution
- Audio/video conversion
- Media information extraction
- Format processing

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import json
import logging
import subprocess

from dataclasses import dataclass
from pathlib import Path

from typing import Any, Dict, List, Optional



# ============================================================
# Exceptions
# ============================================================


class FFmpegError(Exception):
    """
    Base FFmpeg exception.
    """



class FFmpegExecutionError(FFmpegError):
    """
    Raised when FFmpeg command fails.
    """



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class FFmpegConfig:
    """
    FFmpeg execution configuration.
    """

    executable: str = "ffmpeg"

    probe_executable: str = "ffprobe"

    timeout: int = 300

    overwrite: bool = True



# ============================================================
# FFmpeg Wrapper
# ============================================================


class FFmpegWrapper:
    """
    Production FFmpeg interface.

    Provides:
    - Conversion
    - Extraction
    - Media analysis
    """

    def __init__(
        self,
        config: Optional[
            FFmpegConfig
        ] = None,

        logger: Optional[
            logging.Logger
        ] = None,
    ) -> None:


        self.config = (

            config

            if config

            else FFmpegConfig()

        )


        self.logger = (

            logger

            if logger

            else logging.getLogger(
                self.__class__.__name__
            )

        )



    # ========================================================
    # Command Runner
    # ========================================================


    def run(
        self,
        command: List[str],
    ) -> str:
        """
        Execute FFmpeg command.
        """

        self.logger.info(
            "Executing FFmpeg command"
        )


        try:

            result = subprocess.run(

                command,

                capture_output=True,

                text=True,

                timeout=self.config.timeout,

            )


            if result.returncode != 0:

                raise FFmpegExecutionError(

                    result.stderr

                )


            return result.stdout


        except subprocess.TimeoutExpired as exc:

            raise FFmpegExecutionError(

                "FFmpeg execution timeout"

            ) from exc



    # ========================================================
    # Audio Conversion
    # ========================================================


    def convert_audio(
        self,
        input_file: Path,
        output_file: Path,
        codec: str = "pcm_s16le",
    ) -> Path:
        """
        Convert audio format.
        """

        self._validate_file(
            input_file
        )


        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        command = [

            self.config.executable,

            "-y"
            if self.config.overwrite
            else "-n",

            "-i",

            str(input_file),

            "-codec:a",

            codec,

            str(output_file),

        ]


        self.run(
            command
        )


        return output_file
          # ========================================================
    # Video Frame Extraction
    # ========================================================


    def extract_frames(
        self,
        video_file: Path,
        output_directory: Path,
        fps: int = 1,
    ) -> Path:
        """
        Extract video frames for scene analysis.
        """

        self._validate_file(
            video_file
        )


        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )


        output_pattern = (

            output_directory
            /
            "frame_%06d.jpg"

        )


        command = [

            self.config.executable,

            "-y"
            if self.config.overwrite
            else "-n",

            "-i",

            str(video_file),

            "-vf",

            f"fps={fps}",

            str(output_pattern),

        ]


        self.run(
            command
        )


        return output_directory



    # ========================================================
    # Media Information
    # ========================================================


    def get_media_info(
        self,
        media_file: Path,
    ) -> Dict[str, Any]:
        """
        Extract media information using ffprobe.
        """

        self._validate_file(
            media_file
        )


        command = [

            self.config.probe_executable,

            "-v",

            "quiet",

            "-print_format",

            "json",

            "-show_format",

            "-show_streams",

            str(media_file),

        ]


        try:

            result = self.run_probe(
                command
            )


            return json.loads(
                result
            )


        except json.JSONDecodeError as exc:

            raise FFmpegExecutionError(

                "Invalid ffprobe response"

            ) from exc



    # ========================================================
    # FFprobe Runner
    # ========================================================


    def run_probe(
        self,
        command: List[str],
    ) -> str:
        """
        Execute ffprobe command.
        """

        try:

            result = subprocess.run(

                command,

                capture_output=True,

                text=True,

                timeout=self.config.timeout,

            )


            if result.returncode != 0:

                raise FFmpegExecutionError(

                    result.stderr

                )


            return result.stdout



        except subprocess.TimeoutExpired as exc:

            raise FFmpegExecutionError(

                "FFprobe execution timeout"

            ) from exc



    # ========================================================
    # Duration Extraction
    # ========================================================


    def get_duration(
        self,
        media_file: Path,
    ) -> float:
        """
        Return media duration in seconds.
        """

        info = self.get_media_info(
            media_file
        )


        try:

            duration = (

                info
                .get(
                    "format",
                    {}
                )
                .get(
                    "duration",
                    0
                )

            )


            return float(
                duration
            )


        except (
            TypeError,
            ValueError,
        ) as exc:

            raise FFmpegExecutionError(

                "Unable to read duration"

            ) from exc



    # ========================================================
    # Audio Stream Information
    # ========================================================


    def get_audio_stream(
        self,
        media_file: Path,
    ) -> Dict[str, Any]:
        """
        Return first audio stream details.
        """

        info = self.get_media_info(
            media_file
        )


        streams = info.get(
            "streams",
            []
        )


        for stream in streams:

            if stream.get(
                "codec_type"
            ) == "audio":

                return stream



        return {}
          # ========================================================
    # Audio Extraction From Video
    # ========================================================


    def extract_audio(
        self,
        video_file: Path,
        output_file: Path,
        codec: str = "pcm_s16le",
    ) -> Path:
        """
        Extract audio track from video.
        """

        self._validate_file(
            video_file
        )


        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        command = [

            self.config.executable,

            "-y"
            if self.config.overwrite
            else "-n",

            "-i",

            str(video_file),

            "-vn",

            "-codec:a",

            codec,

            str(output_file),

        ]


        self.run(
            command
        )


        return output_file



    # ========================================================
    # Thumbnail Generation
    # ========================================================


    def create_thumbnail(
        self,
        video_file: Path,
        output_file: Path,
        timestamp: str = "00:00:01",
    ) -> Path:
        """
        Generate video thumbnail.
        """

        self._validate_file(
            video_file
        )


        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        command = [

            self.config.executable,

            "-y"
            if self.config.overwrite
            else "-n",

            "-ss",

            timestamp,

            "-i",

            str(video_file),

            "-frames:v",

            "1",

            str(output_file),

        ]


        self.run(
            command
        )


        return output_file



    # ========================================================
    # File Validation
    # ========================================================


    def _validate_file(
        self,
        file_path: Path,
    ) -> None:
        """
        Validate input media file.
        """

        if not file_path.exists():

            raise FFmpegError(
                f"File not found: {file_path}"
            )


        if not file_path.is_file():

            raise FFmpegError(
                "Path is not a file"
            )


        if file_path.stat().st_size <= 0:

            raise FFmpegError(
                "File is empty"
            )



    # ========================================================
    # Configuration
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return FFmpeg configuration.
        """

        return {

            "ffmpeg":
                self.config.executable,


            "ffprobe":
                self.config.probe_executable,


            "timeout":
                self.config.timeout,


            "overwrite":
                self.config.overwrite,

        }



    # ========================================================
    # Diagnostics
    # ========================================================


    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return wrapper health status.
        """

        return {

            "service":
                "FFmpegWrapper",


            "status":
                "healthy",


            "ffmpeg":
                self.config.executable,


            "ffprobe":
                self.config.probe_executable,

        }



    # ========================================================
    # Supported Formats
    # ========================================================


    def is_supported_media(
        self,
        file_path: Path,
    ) -> bool:
        """
        Check supported media formats.
        """

        supported = {

            ".mp4",

            ".mov",

            ".mkv",

            ".avi",

            ".wav",

            ".mp3",

            ".flac",

        }


        return (

            file_path.suffix.lower()

            in

            supported

        )
