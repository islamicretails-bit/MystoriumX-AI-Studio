"""
MystoriumX AI Studio

Local Storage Manager

Responsible for:
- Managing project files
- Handling uploads
- Managing cache/temp/export folders

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


class StorageError(Exception):
    """
    Base storage exception.
    """



class FileOperationError(StorageError):
    """
    Raised when file operation fails.
    """



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class StorageConfig:
    """
    Storage configuration.
    """

    root_directory: Path

    uploads_directory: str = "uploads"

    temp_directory: str = "temp"

    cache_directory: str = "cache"

    exports_directory: str = "exports"



# ============================================================
# Local Storage
# ============================================================


class LocalStorage:
    """
    Production local storage manager.

    Handles all project file operations.
    """

    def __init__(
        self,
        config: StorageConfig,

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


        self._initialize_directories()



    # ========================================================
    # Initialize Storage
    # ========================================================


    def _initialize_directories(
        self,
    ) -> None:
        """
        Create required directories.
        """

        directories = [

            self.upload_path,

            self.temp_path,

            self.cache_path,

            self.export_path,

        ]


        for directory in directories:

            directory.mkdir(

                parents=True,

                exist_ok=True,

            )



    # ========================================================
    # Directory Properties
    # ========================================================


    @property
    def upload_path(
        self,
    ) -> Path:
        """
        Upload directory.
        """

        return (

            self.config.root_directory

            /

            self.config.uploads_directory

        )



    @property
    def temp_path(
        self,
    ) -> Path:
        """
        Temporary directory.
        """

        return (

            self.config.root_directory

            /

            self.config.temp_directory

        )



    @property
    def cache_path(
        self,
    ) -> Path:
        """
        Cache directory.
        """

        return (

            self.config.root_directory

            /

            self.config.cache_directory

        )



    @property
    def export_path(
        self,
    ) -> Path:
        """
        Export directory.
        """

        return (

            self.config.root_directory

            /

            self.config.exports_directory

        )
          # ========================================================
    # Save File
    # ========================================================

    def save_file(
        self,
        source: Path,
        destination_directory: Path,
        overwrite: bool = False,
    ) -> Path:
        """
        Save a file into the specified directory.
        """

        if not source.exists():

            raise FileOperationError(
                f"Source file does not exist: {source}"
            )

        destination_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            destination_directory / source.name
        )

        if destination.exists() and not overwrite:

            raise FileOperationError(
                f"File already exists: {destination}"
            )

        shutil.copy2(
            source,
            destination,
        )

        self.logger.info(
            "File saved: %s",
            destination,
        )

        return destination

    # ========================================================
    # Copy To Export
    # ========================================================

    def export_file(
        self,
        source: Path,
    ) -> Path:
        """
        Copy file to export directory.
        """

        return self.save_file(
            source=source,
            destination_directory=self.export_path,
            overwrite=True,
        )

    # ========================================================
    # Create Project Workspace
    # ========================================================

    def create_workspace(
        self,
        project_name: str,
    ) -> Path:
        """
        Create project workspace.
        """

        if not project_name.strip():

            raise StorageError(
                "Project name cannot be empty."
            )

        workspace = (
            self.config.root_directory
            / project_name
        )

        workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        for folder in (
            "uploads",
            "audio",
            "frames",
            "analysis",
            "exports",
            "logs",
        ):

            (
                workspace / folder
            ).mkdir(
                exist_ok=True
            )

        self.logger.info(
            "Workspace created: %s",
            workspace,
        )

        return workspace

    # ========================================================
    # Cache Operations
    # ========================================================

    def clear_cache(
        self,
    ) -> None:
        """
        Remove all cached files.
        """

        if not self.cache_path.exists():

            return

        for item in self.cache_path.iterdir():

            if item.is_dir():

                shutil.rmtree(
                    item,
                    ignore_errors=True,
                )

            else:

                item.unlink(
                    missing_ok=True
                )

        self.logger.info(
            "Cache cleared."
        )

    # ========================================================
    # Temporary Directory Cleanup
    # ========================================================

    def clear_temp(
        self,
    ) -> None:
        """
        Remove temporary files.
        """

        if not self.temp_path.exists():

            return

        for item in self.temp_path.iterdir():

            if item.is_dir():

                shutil.rmtree(
                    item,
                    ignore_errors=True,
                )

            else:

                item.unlink(
                    missing_ok=True
                )

        self.logger.info(
            "Temporary directory cleaned."
        )

    # ========================================================
    # Delete File
    # ========================================================

    def delete_file(
        self,
        file_path: Path,
    ) -> bool:
        """
        Delete a file.
        """

        if not file_path.exists():

            return False

        file_path.unlink(
            missing_ok=True
        )

        self.logger.info(
            "Deleted file: %s",
            file_path,
        )

        return True
          # ========================================================
    # File Metadata
    # ========================================================

    def get_file_metadata(
        self,
        file_path: Path,
    ) -> Dict[str, Any]:
        """
        Return file metadata.
        """

        if not file_path.exists():

            raise FileOperationError(
                f"File not found: {file_path}"
            )

        stat = file_path.stat()

        return {
            "name": file_path.name,
            "path": str(file_path),
            "suffix": file_path.suffix,
            "size_bytes": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "is_file": file_path.is_file(),
            "is_directory": file_path.is_dir(),
        }

    # ========================================================
    # Directory Size
    # ========================================================

    def get_directory_size(
        self,
        directory: Path,
    ) -> int:
        """
        Calculate directory size in bytes.
        """

        if not directory.exists():

            return 0

        total_size = 0

        for item in directory.rglob("*"):

            if item.is_file():

                total_size += item.stat().st_size

        return total_size

    # ========================================================
    # File Exists
    # ========================================================

    def file_exists(
        self,
        file_path: Path,
    ) -> bool:
        """
        Check whether a file exists.
        """

        return (
            file_path.exists()
            and file_path.is_file()
        )

    # ========================================================
    # Storage Statistics
    # ========================================================

    def get_storage_statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Return storage statistics.
        """

        return {

            "root_directory":
                str(
                    self.config.root_directory
                ),

            "uploads_size":
                self.get_directory_size(
                    self.upload_path
                ),

            "temp_size":
                self.get_directory_size(
                    self.temp_path
                ),

            "cache_size":
                self.get_directory_size(
                    self.cache_path
                ),

            "exports_size":
                self.get_directory_size(
                    self.export_path
                ),

        }

    # ========================================================
    # Configuration
    # ========================================================

    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return storage configuration.
        """

        return {

            "root_directory":
                str(
                    self.config.root_directory
                ),

            "uploads_directory":
                self.config.uploads_directory,

            "temp_directory":
                self.config.temp_directory,

            "cache_directory":
                self.config.cache_directory,

            "exports_directory":
                self.config.exports_directory,

        }

    # ========================================================
    # Health Check
    # ========================================================

    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return storage health status.
        """

        return {

            "service":
                "LocalStorage",

            "status":
                "healthy",

            "root_exists":
                self.config.root_directory.exists(),

            "uploads_exists":
                self.upload_path.exists(),

            "temp_exists":
                self.temp_path.exists(),

            "cache_exists":
                self.cache_path.exists(),

            "exports_exists":
                self.export_path.exists(),

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
                "Local Storage Manager",

            "purpose":
                "Manage uploads, cache, temporary files and exports",

            "pipeline_stage":
                "Storage Infrastructure",

        }
