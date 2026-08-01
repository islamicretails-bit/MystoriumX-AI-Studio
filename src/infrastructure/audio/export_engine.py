"""
MystoriumX AI Studio

Production Export Engine

Responsible for:
- Exporting mastered audio
- Managing production outputs
- Creating final delivery packages

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging
import shutil

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# Exceptions
# ============================================================

class ExportEngineError(Exception):
    """
    Base export engine exception.
    """


class ExportError(ExportEngineError):
    """
    Raised when export fails.
    """


# ============================================================
# Configuration
# ============================================================

@dataclass(slots=True)
class ExportConfig:
    """
    Export configuration.
    """

    export_directory: Path

    overwrite_existing: bool = True

    create_project_folder: bool = True

    export_format: str = "wav"



# ============================================================
# Export Result
# ============================================================

@dataclass(slots=True)
class ExportResult:
    """
    Export result.
    """

    output_file: Path

    format: str

    success: bool

    metadata: Dict[str, Any]


# ============================================================
# Export Engine
# ============================================================

class ExportEngine:
    """
    Production export engine.
    """

    def __init__(
        self,
        config: ExportConfig,
        logger: Optional[logging.Logger] = None,
    ) -> None:

        self.config = config

        self.logger = (
            logger
            if logger
            else logging.getLogger(
                self.__class__.__name__
            )
        )

        self.export_directory = (
            self.config.export_directory
        )

        self.export_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._history: List[
            ExportResult
        ] = []

    # ========================================================
    # Export Audio
    # ========================================================

    def export(
        self,
        source_file: Path,
        output_name: Optional[str] = None,
    ) -> ExportResult:
        """
        Export processed audio.
        """

        self._validate_source(
            source_file
        )

        output_path = self._build_output_path(
            source_file,
            output_name,
        )

        shutil.copy2(
            source_file,
            output_path,
        )

        result = ExportResult(

            output_file=output_path,

            format=self.config.export_format,

            success=True,

            metadata=self._create_metadata(
                output_path
            ),

        )

        self._history.append(
            result
        )

        self.logger.info(
            "Export completed: %s",
            output_path,
        )

        return result
          # ========================================================
    # Build Output Path
    # ========================================================

    def _build_output_path(
        self,
        source_file: Path,
        output_name: Optional[str],
    ) -> Path:
        """
        Build final export path.
        """

        file_name = (

            output_name

            if output_name

            else source_file.stem

        )


        extension = (
            self.config.export_format.lower()
        )


        output_path = (

            self.export_directory

            /

            f"{file_name}.{extension}"

        )


        if (

            output_path.exists()

            and

            not self.config.overwrite_existing

        ):

            raise ExportError(

                f"Export already exists: {output_path}"

            )


        return output_path



    # ========================================================
    # Validate Source File
    # ========================================================

    def _validate_source(
        self,
        source_file: Path,
    ) -> None:
        """
        Validate source audio file.
        """

        if not source_file.exists():

            raise ExportError(

                f"Source file not found: {source_file}"

            )


        if not source_file.is_file():

            raise ExportError(

                "Source path is not a file."

            )


        if source_file.stat().st_size <= 0:

            raise ExportError(

                "Source file is empty."

            )



    # ========================================================
    # Export Multiple Files
    # ========================================================

    def export_multiple(
        self,
        files: List[Path],
    ) -> List[ExportResult]:
        """
        Export multiple audio files.
        """

        results: List[
            ExportResult
        ] = []


        for audio_file in files:

            results.append(

                self.export(
                    audio_file
                )

            )


        return results



    # ========================================================
    # Create Project Package
    # ========================================================

    def create_project_package(
        self,
        project_name: str,
    ) -> Path:
        """
        Create project export folder.
        """

        project_directory = (

            self.export_directory

            /

            project_name

        )


        project_directory.mkdir(

            parents=True,

            exist_ok=True,

        )


        self.logger.info(

            "Created project package: %s",

            project_directory,

        )


        return project_directory



    # ========================================================
    # Export History
    # ========================================================

    def get_history(
        self,
    ) -> List[ExportResult]:
        """
        Return export history.
        """

        return list(
            self._history
        )



    # ========================================================
    # Clear History
    # ========================================================

    def clear_history(
        self,
    ) -> None:
        """
        Clear export history.
        """

        self._history.clear()

        self.logger.info(
            "Export history cleared."
        )
          # ========================================================
    # Create Metadata
    # ========================================================

    def _create_metadata(
        self,
        output_file: Path,
    ) -> Dict[str, Any]:
        """
        Create export metadata.
        """

        file_stat = output_file.stat()

        return {
            "filename": output_file.name,
            "path": str(output_file),
            "format": output_file.suffix.lstrip("."),
            "size_bytes": file_stat.st_size,
            "created_timestamp": file_stat.st_ctime,
            "modified_timestamp": file_stat.st_mtime,
        }

    # ========================================================
    # Export Statistics
    # ========================================================

    def get_statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Return export statistics.
        """

        total_size = sum(
            result.output_file.stat().st_size
            for result in self._history
            if result.output_file.exists()
        )

        return {
            "total_exports": len(self._history),
            "total_size_bytes": total_size,
            "export_directory": str(
                self.export_directory
            ),
            "default_format": self.config.export_format,
        }

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
            "export_directory": str(
                self.config.export_directory
            ),
            "overwrite_existing": (
                self.config.overwrite_existing
            ),
            "create_project_folder": (
                self.config.create_project_folder
            ),
            "export_format": (
                self.config.export_format
            ),
        }

    # ========================================================
    # Health Check
    # ========================================================

    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return export engine health.
        """

        return {
            "service": "ExportEngine",
            "status": "healthy",
            "export_directory_exists": (
                self.export_directory.exists()
            ),
            "history_entries": len(
                self._history
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
            "service": "Production Export Engine",
            "purpose": (
                "Export mastered audio and "
                "manage production deliverables"
            ),
            "pipeline_stage": "Final Export",
        }

    # ========================================================
    # Cleanup
    # ========================================================

    def cleanup_empty_exports(
        self,
    ) -> int:
        """
        Remove empty files from export directory.

        Returns:
            Number of deleted files.
        """

        removed = 0

        for file_path in self.export_directory.glob("*"):

            if (
                file_path.is_file()
                and file_path.stat().st_size == 0
            ):
                file_path.unlink()
                removed += 1

        if removed:

            self.logger.info(
                "Removed %d empty export file(s).",
                removed,
            )

        return removed
