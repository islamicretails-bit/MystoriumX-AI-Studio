# ============================================================
# MystoriumX AI Studio
# Service Layer - Export Service
#
# File:
# app/services/export_service.py
#
# Responsibility:
# Final cinematic audio export management.
#
# Supports:
# - WAV export
# - MP3 export
# - FLAC export
# - Project metadata export
#
# ============================================================


from __future__ import annotations


from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import logging
import shutil


logger = logging.getLogger(
    "MystoriumX.ExportService"
)



# ============================================================
# Export Configuration
# ============================================================

@dataclass
class ExportConfig:
    """
    Final export settings.
    """

    output_directory: Path

    format: str = "wav"

    project_name: str = "MystoriumX_Project"

    include_metadata: bool = True



# ============================================================
# Export Result
# ============================================================

@dataclass
class ExportResult:
    """
    Stores export operation result.
    """

    success: bool

    exported_files: List[Path] = field(
        default_factory=list
    )

    metadata_file: Optional[Path] = None

    error: Optional[str] = None



# ============================================================
# Export Service
# ============================================================

class ExportService:
    """
    Handles final soundtrack exporting.

    Pipeline:

    Mastered Audio
          |
          ↓
    Format Conversion
          |
          ↓
    Metadata Creation
          |
          ↓
    Final Project Package

    """



    def __init__(
        self
    ) -> None:


        logger.info(
            "Export Service initialized"
        )



    # ========================================================
    # Main Export Method
    # ========================================================

    def export_project(
        self,
        audio_file: Path,
        config: ExportConfig,
        metadata: Optional[Dict] = None
    ) -> ExportResult:

        """
        Export final documentary soundtrack.

        Args:

            audio_file:
                Mastered audio file.

            config:
                Export settings.

            metadata:
                Project information.

        """


        try:


            self._validate_input(
                audio_file
            )


            self._create_directory(
                config.output_directory
            )


            exported_files = []


            output_file = (
                self._export_audio(
                    audio_file,
                    config
                )
            )


            if output_file:

                exported_files.append(
                    output_file
                )



            metadata_file = None


            if config.include_metadata:

                metadata_file = (
                    self._save_metadata(
                        config,
                        metadata
                    )
                )



            return ExportResult(

                success=True,

                exported_files=
                    exported_files,

                metadata_file=
                    metadata_file

            )



        except Exception as error:


            logger.exception(
                "Export failed"
            )


            return ExportResult(

                success=False,

                error=str(error)

            )



    # ========================================================
    # Validation
    # ========================================================

    def _validate_input(
        self,
        audio_file: Path
    ) -> None:

        """
        Validate mastered audio.
        """


        if not audio_file.exists():

            raise FileNotFoundError(
                "Audio file does not exist."
            )



    # ========================================================
    # Directory Creation
    # ========================================================

    def _create_directory(
        self,
        directory: Path
    ) -> None:

        """
        Create export folder.
        """


        directory.mkdir(

            parents=True,

            exist_ok=True

        )



    # ========================================================
    # Audio Export
    # ========================================================

    def _export_audio(
        self,
        audio_file: Path,
        config: ExportConfig
    ) -> Optional[Path]:

        """
        Export final audio file.

        Future:

        - FFmpeg conversion
        - Bitrate control
        - Sample rate conversion

        """


        extension = (

            config.format.lower()

        )


        output_path = (

            config.output_directory

            /

            f"{config.project_name}.{extension}"

        )


        logger.info(
            f"Exporting audio: {output_path}"
        )


        # Temporary safe copy.
        # Real FFmpeg conversion
        # will be connected later.


        shutil.copy(

            audio_file,

            output_path

        )


        return output_path



    # ========================================================
    # Metadata Export
    # ========================================================

    def _save_metadata(
        self,
        config: ExportConfig,
        metadata: Optional[Dict]
    ) -> Path:

        """
        Save project metadata.
        """


        metadata_path = (

            config.output_directory

            /

            "project_metadata.txt"

        )


        content = (

            f"MystoriumX AI Studio\n"

            f"Project: {config.project_name}\n"

            f"Format: {config.format}\n\n"

            f"Metadata:\n"

            f"{metadata or {}}"

        )


        metadata_path.write_text(

            content,

            encoding="utf-8"

        )


        return metadata_path



    # ========================================================
    # Export Information
    # ========================================================

    def get_supported_formats(
        self
    ) -> List[str]:

        """
        Return supported formats.
        """


        return [

            "wav",

            "mp3",

            "flac"

        ]
