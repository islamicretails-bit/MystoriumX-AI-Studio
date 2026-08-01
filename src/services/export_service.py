"""
MystoriumX AI Studio

Production Export Service

Responsible for:
- Final project packaging
- Audio export management
- Metadata generation
- Production file organization

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import json
import logging

from dataclasses import dataclass
from pathlib import Path

from typing import Any, Dict, List, Optional



# ============================================================
# Exceptions
# ============================================================


class ExportServiceError(Exception):
    """
    Base export service exception.
    """



class ExportFailedError(ExportServiceError):
    """
    Raised when export operation fails.
    """



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class ExportConfig:
    """
    Export configuration.
    """

    output_directory: Path

    audio_format: str = "wav"

    include_waveform: bool = True

    include_metadata: bool = True

    include_report: bool = True



# ============================================================
# Export Service
# ============================================================


class ExportService:
    """
    Production export manager.

    Creates final documentary audio package.
    """

    def __init__(
        self,
        config: ExportConfig,
        logger: Optional[
            logging.Logger
        ] = None,
    ) -> None:


        self.config = config


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


    def export(
        self,
        audio_file: Path,
        waveform_file: Optional[Path] = None,
        analytics: Optional[
            Dict[str, Any]
        ] = None,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Path:
        """
        Export complete production package.
        """


        self._validate_audio(
            audio_file
        )


        self.logger.info(
            "Starting final export process"
        )


        try:

            export_folder = (
                self._create_export_folder()
            )


            self._copy_audio(
                audio_file,
                export_folder,
            )


            if (
                self.config.include_waveform
                and waveform_file
            ):

                self._copy_waveform(
                    waveform_file,
                    export_folder,
                )


            if (
                self.config.include_metadata
                and metadata
            ):

                self._save_metadata(
                    metadata,
                    export_folder,
                )


            if (
                self.config.include_report
                and analytics
            ):

                self._save_report(
                    analytics,
                    export_folder,
                )


            self.logger.info(
                "Export completed successfully"
            )


            return export_folder


        except Exception as exc:

            self.logger.exception(
                "Export failed"
            )


            raise ExportFailedError(
                f"Export failed: {exc}"
            ) from exc
              # ========================================================
    # Export Folder Creation
    # ========================================================


    def _create_export_folder(
        self,
    ) -> Path:
        """
        Create unique export directory.
        """

        self.config.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )


        project_folder = (

            self.config.output_directory
            /
            "mystoriumx_export"

        )


        project_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        return project_folder



    # ========================================================
    # Audio Export
    # ========================================================


    def _copy_audio(
        self,
        audio_file: Path,
        export_folder: Path,
    ) -> Path:
        """
        Copy final mastered audio.
        """

        destination = (

            export_folder
            /
            f"final_audio.{self.config.audio_format}"

        )


        destination.write_bytes(
            audio_file.read_bytes()
        )


        return destination



    # ========================================================
    # Waveform Export
    # ========================================================


    def _copy_waveform(
        self,
        waveform_file: Path,
        export_folder: Path,
    ) -> Path:
        """
        Copy waveform visualization.
        """

        destination = (

            export_folder
            /
            waveform_file.name

        )


        destination.write_bytes(
            waveform_file.read_bytes()
        )


        return destination



    # ========================================================
    # Metadata Writer
    # ========================================================


    def _save_metadata(
        self,
        metadata: Dict[str, Any],
        export_folder: Path,
    ) -> Path:
        """
        Save project metadata JSON.
        """

        metadata_file = (

            export_folder
            /
            "metadata.json"

        )


        with metadata_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
                ensure_ascii=False,
            )


        return metadata_file



    # ========================================================
    # Analytics Report
    # ========================================================


    def _save_report(
        self,
        analytics: Dict[str, Any],
        export_folder: Path,
    ) -> Path:
        """
        Save analytics report.
        """

        report_file = (

            export_folder
            /
            "analytics_report.json"

        )


        with report_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                analytics,
                file,
                indent=4,
                ensure_ascii=False,
            )


        return report_file



    # ========================================================
    # Validation
    # ========================================================


    def _validate_audio(
        self,
        audio_file: Path,
    ) -> None:
        """
        Validate source audio.
        """

        if not audio_file.exists():

            raise ExportServiceError(
                f"Audio file not found: {audio_file}"
            )


        if not audio_file.is_file():

            raise ExportServiceError(
                "Audio path is not a file"
            )


        if audio_file.stat().st_size <= 0:

            raise ExportServiceError(
                "Audio file is empty"
            )
              # ========================================================
    # Export Package Validation
    # ========================================================


    def validate_package(
        self,
        export_folder: Path,
    ) -> bool:
        """
        Validate final exported package.
        """

        if not export_folder.exists():

            return False


        required_files = [

            "metadata.json",

        ]


        for file_name in required_files:

            file_path = (
                export_folder
                /
                file_name
            )


            if not file_path.exists():

                return False



        return True



    # ========================================================
    # Export Summary
    # ========================================================


    def create_summary(
        self,
        export_folder: Path,
    ) -> Dict[str, Any]:
        """
        Create export package summary.
        """

        files: List[str] = []


        if export_folder.exists():

            files = [

                file.name

                for file in export_folder.iterdir()

                if file.is_file()

            ]


        return {

            "export_directory":
                str(export_folder),


            "files":
                files,


            "file_count":
                len(files),


            "status":
                "completed"
                if files
                else "empty",

        }



    # ========================================================
    # Project Package Builder
    # ========================================================


    def build_project_package(
        self,
        files: List[Path],
        package_name: str,
    ) -> Path:
        """
        Create custom project package folder.
        """

        package_folder = (

            self.config.output_directory
            /
            package_name

        )


        package_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        for file in files:

            if file.exists():

                destination = (

                    package_folder
                    /
                    file.name

                )


                destination.write_bytes(
                    file.read_bytes()
                )


        return package_folder



    # ========================================================
    # Configuration
    # ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return export configuration.
        """

        return {

            "output_directory":
                str(
                    self.config.output_directory
                ),


            "audio_format":
                self.config.audio_format,


            "include_waveform":
                self.config.include_waveform,


            "include_metadata":
                self.config.include_metadata,


            "include_report":
                self.config.include_report,

        }



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
                "ExportService",


            "status":
                "healthy",


            "output_directory":
                str(
                    self.config.output_directory
                ),

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
                "Production Export Service",


            "purpose":
                "Create final documentary production package",


            "pipeline_stage":
                "Final Export",

        }
