# ============================================================
# MystoriumX AI Studio
# Core Layer - Security Manager
#
# File:
# app/core/security.py
#
# Responsibility:
# Application security utilities.
#
# Features:
# - File validation
# - Safe filename handling
# - Upload protection
# - Extension checking
# - Size validation
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path

from typing import List

import logging

import re



logger = logging.getLogger(
    "MystoriumX.Security"
)



# ============================================================
# Security Manager
# ============================================================

class SecurityManager:
    """
    Application security controller.

    Protects:

    - User uploads
    - File paths
    - Media processing pipeline

    """



    def __init__(
        self,
        max_file_size_mb: int = 2048
    ) -> None:


        self.max_file_size = (

            max_file_size_mb

            *

            1024

            *

            1024

        )


        self.allowed_video_formats = [

            ".mp4",

            ".mov",

            ".avi",

            ".mkv"

        ]


        self.allowed_audio_formats = [

            ".wav",

            ".mp3",

            ".flac",

            ".m4a"

        ]


        self.allowed_script_formats = [

            ".txt",

            ".pdf",

            ".docx"

        ]



        logger.info(

            "Security Manager initialized"

        )



    # ========================================================
    # Validate File Exists
    # ========================================================

    def validate_file(
        self,
        file_path: Path
    ) -> bool:

        """
        Check file existence and size.
        """


        if not file_path.exists():

            raise FileNotFoundError(

                "File does not exist."

            )



        if file_path.stat().st_size > self.max_file_size:

            raise ValueError(

                "File size exceeds allowed limit."

            )



        return True



    # ========================================================
    # Validate Video
    # ========================================================

    def validate_video(
        self,
        file_path: Path
    ) -> bool:

        """
        Validate documentary video file.
        """


        self.validate_file(

            file_path

        )


        if file_path.suffix.lower() not in self.allowed_video_formats:


            raise ValueError(

                "Unsupported video format."

            )


        return True



    # ========================================================
    # Validate Audio
    # ========================================================

    def validate_audio(
        self,
        file_path: Path
    ) -> bool:

        """
        Validate narration/music file.
        """


        self.validate_file(

            file_path

        )


        if file_path.suffix.lower() not in self.allowed_audio_formats:


            raise ValueError(

                "Unsupported audio format."

            )


        return True



    # ========================================================
    # Validate Script
    # ========================================================

    def validate_script(
        self,
        file_path: Path
    ) -> bool:

        """
        Validate script document.
        """


        self.validate_file(

            file_path

        )


        if file_path.suffix.lower() not in self.allowed_script_formats:


            raise ValueError(

                "Unsupported script format."

            )


        return True



    # ========================================================
    # Safe Filename
    # ========================================================

    def sanitize_filename(
        self,
        filename: str
    ) -> str:

        """
        Remove unsafe characters.

        Example:

        My Video!!.mp4

        becomes:

        My_Video.mp4

        """


        cleaned = re.sub(

            r"[^a-zA-Z0-9._-]",

            "_",

            filename

        )


        return cleaned



    # ========================================================
    # Secure Path
    # ========================================================

    def secure_path(
        self,
        base_directory: Path,
        filename: str
    ) -> Path:

        """
        Create safe file path.

        Prevents:

        ../ path traversal attacks

        """


        safe_name = (

            self.sanitize_filename(

                filename

            )

        )


        final_path = (

            base_directory

            /

            safe_name

        ).resolve()



        base = (

            base_directory

            .resolve()

        )



        if not str(final_path).startswith(

            str(base)

        ):

            raise PermissionError(

                "Unsafe file path detected."

            )



        return final_path



    # ========================================================
    # Extension Check
    # ========================================================

    def is_supported_extension(
        self,
        filename: str,
        allowed: List[str]
    ) -> bool:

        """
        Check file extension.
        """


        return (

            Path(filename)

            .suffix

            .lower()

            in

            allowed

        )



    # ========================================================
    # Security Report
    # ========================================================

    def get_security_info(
        self
    ) -> dict:

        """
        Return security configuration.
        """


        return {


            "max_file_size_mb":

                self.max_file_size /

                (1024 * 1024),


            "video_formats":

                self.allowed_video_formats,


            "audio_formats":

                self.allowed_audio_formats,


            "script_formats":

                self.allowed_script_formats

        }



# ============================================================
# Global Security Instance
# ============================================================

security_manager = SecurityManager()
