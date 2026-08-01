"""
MystoriumX AI Studio
Upload Zone Component

File:
src/ui/components/upload_zone.py

Part 1/3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import streamlit as st

from src.core.constants import (
    SUPPORTED_VIDEO_EXTENSIONS,
)
from src.core.exceptions import ValidationError
from src.core.security import sanitize_filename
from src.ui.state import (
    SessionKeys,
    add_log,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Upload Models
# ==============================================================================


@dataclass(slots=True, frozen=True)
class UploadedFileInfo:
    """
    Uploaded file information.
    """

    name: str

    size: int

    extension: str

    mime_type: str


# ==============================================================================
# Upload Configuration
# ==============================================================================


@dataclass(slots=True, frozen=True)
class UploadConfig:
    """
    Upload component configuration.
    """

    label: str = (
        "Upload Documentary Video"
    )

    accepted_formats: tuple[str, ...] = (
        SUPPORTED_VIDEO_EXTENSIONS
    )

    max_size_mb: int = 2048


# ==============================================================================
# Upload Zone Component
# ==============================================================================


class UploadZone:
    """
    Streamlit upload component.
    """

    def __init__(
        self,
        config: UploadConfig | None = None,
    ) -> None:

        self.config = (
            config
            if config
            else UploadConfig()
        )


    def render(
        self,
    ) -> Optional[UploadedFileInfo]:
        """
        Render uploader UI.
        """

        uploaded_file = st.file_uploader(
            self.config.label,
            type=[
                ext.replace(".", "")
                for ext
                in self.config.accepted_formats
            ],
        )

        if uploaded_file is None:
            return None

        return self._process_upload(
            uploaded_file
        )


    def _process_upload(
        self,
        uploaded_file,
    ) -> UploadedFileInfo:
        """
        Process uploaded Streamlit file.
        """

        filename = sanitize_filename(
            uploaded_file.name
        )

        extension = Path(
            filename
        ).suffix.lower()

        if extension not in self.config.accepted_formats:
            raise ValidationError(
                f"Unsupported format: {extension}"
            )

        file_size = uploaded_file.size

        max_bytes = (
            self.config.max_size_mb
            * 1024
            * 1024
        )

        if file_size > max_bytes:
            raise ValidationError(
                "Uploaded file exceeds size limit."
            )

        info = UploadedFileInfo(
            name=filename,
            size=file_size,
            extension=extension,
            mime_type=uploaded_file.type,
        )

        st.session_state[
            SessionKeys.UPLOADED_FILE
        ] = info

        add_log(
            f"Uploaded file: {filename}"
        )

        logger.info(
            "Uploaded file accepted: %s",
            filename,
        )

        return info
      # ==============================================================================
# Upload Helper Methods
# ==============================================================================


def get_uploaded_file() -> Optional[UploadedFileInfo]:
    """
    Return current uploaded file information.
    """

    value = st.session_state.get(
        SessionKeys.UPLOADED_FILE
    )

    if isinstance(
        value,
        UploadedFileInfo,
    ):
        return value

    return None


def clear_uploaded_file() -> None:
    """
    Clear uploaded file state.
    """

    if SessionKeys.UPLOADED_FILE in st.session_state:

        del st.session_state[
            SessionKeys.UPLOADED_FILE
        ]

        add_log(
            "Uploaded file state cleared."
        )

        logger.info(
            "Upload state cleared."
        )


# ==============================================================================
# Upload UI Factory
# ==============================================================================


def render_upload_zone(
    config: UploadConfig | None = None,
) -> Optional[UploadedFileInfo]:
    """
    Render upload component.
    """

    component = UploadZone(
        config=config
    )

    return component.render()


# ==============================================================================
# Upload Validation
# ==============================================================================


def validate_uploaded_file(
    file_info: UploadedFileInfo,
) -> None:
    """
    Validate uploaded file information.
    """

    if not file_info.name:
        raise ValidationError(
            "Filename is empty."
        )

    if file_info.size <= 0:
        raise ValidationError(
            "Uploaded file is empty."
        )

    if not file_info.extension:
        raise ValidationError(
            "Missing file extension."
        )


def upload_summary(
    file_info: UploadedFileInfo,
) -> dict[str, str]:
    """
    Generate upload summary.
    """

    return {
        "name": file_info.name,
        "size": (
            f"{file_info.size / (1024 * 1024):.2f} MB"
        ),
        "format": file_info.extension,
        "mime": file_info.mime_type,
    }
  # ==============================================================================
# Upload Status UI
# ==============================================================================


def show_upload_status(
    file_info: Optional[UploadedFileInfo],
) -> None:
    """
    Display uploaded file status.
    """

    if file_info is None:

        st.info(
            "Please upload a documentary video file."
        )

        return

    summary = upload_summary(
        file_info
    )

    st.success(
        "Video uploaded successfully."
    )

    st.write(
        summary
    )


# ==============================================================================
# Default Component Instance
# ==============================================================================


_upload_zone = UploadZone()


def upload_video() -> Optional[UploadedFileInfo]:
    """
    Public upload entry point.
    """

    try:

        return _upload_zone.render()

    except Exception as exc:

        logger.exception(
            "Upload failed."
        )

        st.error(
            str(exc)
        )

        return None


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "UploadedFileInfo",
    "UploadConfig",
    "UploadZone",
    "render_upload_zone",
    "get_uploaded_file",
    "clear_uploaded_file",
    "validate_uploaded_file",
    "upload_summary",
    "show_upload_status",
    "upload_video",
]
