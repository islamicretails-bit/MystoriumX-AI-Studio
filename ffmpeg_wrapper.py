# ============================================================
# MystoriumX AI Studio
# DSP Layer - FFmpeg Wrapper
#
# File:
# app/infrastructure/dsp/ffmpeg_wrapper.py
#
# Responsibility:
# Professional media processing layer.
#
# Features:
# - Video information extraction
# - Audio extraction
# - Format conversion
# - Media rendering pipeline
#
# Technology:
# - FFmpeg
# - FFprobe
#
# ============================================================


from __future__ import annotations


from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
import logging
import subprocess
import json



logger = logging.getLogger(
    "MystoriumX.FFmpegWrapper"
)



# ============================================================
# Media Information Model
# ============================================================

@dataclass
class MediaInfo:
    """
    Stores media metadata.
    """

    duration: float

    width: Optional[int]

    height: Optional[int]

    fps: Optional[float]

    audio_codec: Optional[str]

    video_codec: Optional[str]



# ============================================================
# FFmpeg Wrapper
# ============================================================

class FFmpegWrapper:
    """
    FFmpeg media processing manager.

    Handles:

    - Video analysis
    - Audio extraction
    - Conversion
    - Rendering preparation

    """



    def __init__(
        self,
        ffmpeg_binary: str = "ffmpeg",
        ffprobe_binary: str = "ffprobe"
    ) -> None:


        self.ffmpeg = ffmpeg_binary

        self.ffprobe = ffprobe_binary


        logger.info(
            "FFmpeg Wrapper initialized"
        )



    # ========================================================
    # Get Media Information
    # ========================================================

    def get_media_info(
        self,
        media_file: Path
    ) -> MediaInfo:

        """
        Extract media metadata using ffprobe.
        """


        self._validate_file(
            media_file
        )


        command = [

            self.ffprobe,

            "-v",
            "quiet",

            "-print_format",
            "json",

            "-show_format",

            "-show_streams",

            str(media_file)

        ]


        try:


            result = subprocess.run(

                command,

                capture_output=True,

                text=True,

                check=True

            )


            data = json.loads(

                result.stdout

            )


            duration = float(

                data.get(

                    "format",

                    {}

                )
                .get(

                    "duration",

                    0

                )

            )


            width = None

            height = None

            fps = None

            audio_codec = None

            video_codec = None



            for stream in data.get(

                "streams",

                []

            ):


                if stream.get(

                    "codec_type"

                ) == "video":


                    width = stream.get(
                        "width"
                    )


                    height = stream.get(
                        "height"
                    )


                    video_codec = stream.get(
                        "codec_name"
                    )


                    fps = self._parse_fps(

                        stream.get(

                            "r_frame_rate"

                        )

                    )



                if stream.get(

                    "codec_type"

                ) == "audio":


                    audio_codec = stream.get(

                        "codec_name"

                    )



            return MediaInfo(

                duration=duration,

                width=width,

                height=height,

                fps=fps,

                audio_codec=audio_codec,

                video_codec=video_codec

            )



        except Exception as error:


            logger.exception(

                "Media analysis failed"

            )


            raise error



    # ========================================================
    # Extract Audio
    # ========================================================

    def extract_audio(
        self,
        video_file: Path,
        output_audio: Path
    ) -> Path:

        """
        Extract narration or soundtrack audio.
        """


        self._validate_file(

            video_file

        )


        command = [

            self.ffmpeg,

            "-y",

            "-i",

            str(video_file),

            "-vn",

            "-acodec",

            "pcm_s16le",

            str(output_audio)

        ]


        self._run_command(

            command

        )


        return output_audio



    # ========================================================
    # Convert Audio Format
    # ========================================================

    def convert_audio(
        self,
        input_file: Path,
        output_file: Path
    ) -> Path:

        """
        Convert audio between formats.
        """


        self._validate_file(

            input_file

        )


        command = [

            self.ffmpeg,

            "-y",

            "-i",

            str(input_file),

            str(output_file)

        ]


        self._run_command(

            command

        )


        return output_file



    # ========================================================
    # Render Final Media
    # ========================================================

    def merge_audio_video(
        self,
        video_file: Path,
        audio_file: Path,
        output_file: Path
    ) -> Path:

        """
        Combine video with final soundtrack.
        """


        command = [

            self.ffmpeg,

            "-y",

            "-i",

            str(video_file),

            "-i",

            str(audio_file),

            "-map",

            "0:v:0",

            "-map",

            "1:a:0",

            "-c:v",

            "copy",

            "-shortest",

            str(output_file)

        ]


        self._run_command(

            command

        )


        return output_file



    # ========================================================
    # Execute Command
    # ========================================================

    def _run_command(
        self,
        command: list[str]
    ) -> None:

        """
        Execute FFmpeg command safely.
        """


        try:


            subprocess.run(

                command,

                check=True,

                capture_output=True,

                text=True

            )


            logger.info(

                "FFmpeg command completed"

            )


        except subprocess.CalledProcessError as error:


            logger.error(

                error.stderr

            )


            raise RuntimeError(

                "FFmpeg execution failed"

            )



    # ========================================================
    # FPS Parser
    # ========================================================

    def _parse_fps(
        self,
        value: Optional[str]
    ) -> Optional[float]:

        """
        Convert FFmpeg FPS string.
        """


        if not value:

            return None



        try:


            numerator, denominator = value.split("/")


            return round(

                int(numerator)

                /

                int(denominator),

                2

            )


        except Exception:


            return None



    # ========================================================
    # Validation
    # ========================================================

    def _validate_file(
        self,
        file_path: Path
    ) -> None:

        """
        Validate input file.
        """


        if not file_path.exists():

            raise FileNotFoundError(

                f"File not found: {file_path}"

            )
