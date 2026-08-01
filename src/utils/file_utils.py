"""
MystoriumX AI Studio
Utility Module

File:
src/utils/file_utils.py

Part 1/3
"""

from __future__ import annotations

import hashlib
import logging
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from src.core.exceptions import FileProcessingError
from src.core.security import ensure_safe_path

logger = logging.getLogger(__name__)


# ==============================================================================
# File Metadata
# ==============================================================================


@dataclass(slots=True, frozen=True)
class FileMetadata:
    """
    File metadata container.
    """

    path: Path
    filename: str
    extension: str
    size_bytes: int
    created_at: datetime
    modified_at: datetime

    @classmethod
    def from_path(
        cls,
        file_path: Path,
    ) -> "FileMetadata":

        file_path = ensure_safe_path(file_path)

        if not file_path.exists():
            raise FileProcessingError(
                f"File not found: {file_path}"
            )

        stat = file_path.stat()

        return cls(
            path=file_path,
            filename=file_path.name,
            extension=file_path.suffix.lower(),
            size_bytes=stat.st_size,
            created_at=datetime.fromtimestamp(
                stat.st_ctime
            ),
            modified_at=datetime.fromtimestamp(
                stat.st_mtime
            ),
        )


# ==============================================================================
# Directory Utilities
# ==============================================================================


def ensure_directory(
    directory: Path,
) -> Path:
    """
    Ensure a directory exists.
    """

    directory = ensure_safe_path(directory)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def create_parent_directory(
    file_path: Path,
) -> None:
    """
    Create the parent directory for a file.
    """

    ensure_directory(file_path.parent)


def list_files(
    directory: Path,
    *,
    recursive: bool = False,
    extensions: Iterable[str] | None = None,
) -> list[Path]:
    """
    List files from a directory.
    """

    directory = ensure_safe_path(directory)

    if not directory.exists():
        return []

    iterator = (
        directory.rglob("*")
        if recursive
        else directory.glob("*")
    )

    files = [
        path
        for path in iterator
        if path.is_file()
    ]

    if extensions is None:
        return sorted(files)

    allowed = {
        ext.lower()
        for ext in extensions
    }

    return sorted(
        file
        for file in files
        if file.suffix.lower() in allowed
    )


# ==============================================================================
# File Operations
# ==============================================================================


def copy_file(
    source: Path,
    destination: Path,
) -> Path:
    """
    Copy a file preserving metadata.
    """

    source = ensure_safe_path(source)
    destination = ensure_safe_path(destination)

    if not source.exists():
        raise FileProcessingError(
            f"Source file not found: {source}"
        )

    create_parent_directory(destination)

    shutil.copy2(
        source,
        destination,
    )

    logger.info(
        "Copied '%s' -> '%s'",
        source,
        destination,
    )

    return destination


def move_file(
    source: Path,
    destination: Path,
) -> Path:
    """
    Move a file.
    """

    source = ensure_safe_path(source)
    destination = ensure_safe_path(destination)

    if not source.exists():
        raise FileProcessingError(
            f"Source file not found: {source}"
        )

    create_parent_directory(destination)

    shutil.move(
        str(source),
        str(destination),
    )

    logger.info(
        "Moved '%s' -> '%s'",
        source,
        destination,
    )

    return destination
  # ==============================================================================
# Delete Utilities
# ==============================================================================


def delete_file(
    file_path: Path,
    *,
    missing_ok: bool = True,
) -> None:
    """
    Delete a file.
    """

    file_path = ensure_safe_path(file_path)

    if not file_path.exists():

        if missing_ok:
            return

        raise FileProcessingError(
            f"File not found: {file_path}"
        )

    file_path.unlink()

    logger.info(
        "Deleted file: %s",
        file_path,
    )


def delete_directory(
    directory: Path,
    *,
    missing_ok: bool = True,
) -> None:
    """
    Delete a directory recursively.
    """

    directory = ensure_safe_path(directory)

    if not directory.exists():

        if missing_ok:
            return

        raise FileProcessingError(
            f"Directory not found: {directory}"
        )

    shutil.rmtree(directory)

    logger.info(
        "Deleted directory: %s",
        directory,
    )


# ==============================================================================
# Hash Utilities
# ==============================================================================


def calculate_sha256(
    file_path: Path,
) -> str:
    """
    Calculate SHA-256 checksum.
    """

    file_path = ensure_safe_path(file_path)

    digest = hashlib.sha256()

    with file_path.open("rb") as stream:

        while True:

            chunk = stream.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


# ==============================================================================
# File Information
# ==============================================================================


def file_size(
    file_path: Path,
) -> int:
    """
    Return file size in bytes.
    """

    file_path = ensure_safe_path(file_path)

    return file_path.stat().st_size


def file_exists(
    file_path: Path,
) -> bool:
    """
    Check if file exists.
    """

    return ensure_safe_path(file_path).exists()


def directory_exists(
    directory: Path,
) -> bool:
    """
    Check if directory exists.
    """

    return ensure_safe_path(directory).exists()


def file_extension(
    file_path: Path,
) -> str:
    """
    Return lowercase extension.
    """

    return ensure_safe_path(
        file_path
    ).suffix.lower()


def file_name(
    file_path: Path,
) -> str:
    """
    Return filename.
    """

    return ensure_safe_path(
        file_path
    ).name


def file_stem(
    file_path: Path,
) -> str:
    """
    Return filename without extension.
    """

    return ensure_safe_path(
        file_path
    ).stem
  # ==============================================================================
# Path Utilities
# ==============================================================================


def resolve_path(
    path: Path,
) -> Path:
    """
    Resolve and validate a filesystem path.
    """

    return ensure_safe_path(path)


def relative_path(
    path: Path,
    base: Path,
) -> Path:
    """
    Return a path relative to the given base directory.
    """

    path = ensure_safe_path(path)
    base = ensure_safe_path(base)

    return path.relative_to(base)


def touch_file(
    file_path: Path,
) -> Path:
    """
    Create an empty file if it does not already exist.
    """

    file_path = ensure_safe_path(file_path)

    create_parent_directory(file_path)

    file_path.touch(exist_ok=True)

    logger.info(
        "Created file: %s",
        file_path,
    )

    return file_path


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "FileMetadata",
    "ensure_directory",
    "create_parent_directory",
    "list_files",
    "copy_file",
    "move_file",
    "delete_file",
    "delete_directory",
    "calculate_sha256",
    "file_size",
    "file_exists",
    "directory_exists",
    "file_extension",
    "file_name",
    "file_stem",
    "resolve_path",
    "relative_path",
    "touch_file",
]
