"""
MystoriumX AI Studio
Core Exceptions

File:
src/core/exceptions.py

Part 1/3
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
import traceback
import uuid


# ==============================================================================
# Base Exception
# ==============================================================================


@dataclass(slots=True)
class MystoriumXError(Exception):
    """
    Base exception for the MystoriumX AI Studio platform.
    """

    message: str
    details: Optional[str] = None
    error_code: str = "MX-0000"
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    exception_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exception_id": self.exception_id,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
        }


# ==============================================================================
# Configuration Exceptions
# ==============================================================================


class ConfigurationError(MystoriumXError):
    """
    Raised when application configuration is invalid.
    """

    def __init__(
        self,
        message: str,
        details: Optional[str] = None,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            details=details,
            error_code="CFG-1001",
            context=context,
        )


# ==============================================================================
# Validation Exceptions
# ==============================================================================


class ValidationError(MystoriumXError):
    """
    Raised when validation fails.
    """

    def __init__(
        self,
        message: str,
        field_name: Optional[str] = None,
        **context: Any,
    ) -> None:
        if field_name:
            context["field"] = field_name

        super().__init__(
            message=message,
            error_code="VAL-1002",
            context=context,
        )


# ==============================================================================
# File Exceptions
# ==============================================================================


class FileProcessingError(MystoriumXError):
    """
    Raised when a file cannot be processed.
    """

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        **context: Any,
    ) -> None:
        if file_path:
            context["file_path"] = file_path

        super().__init__(
            message=message,
            error_code="FIL-2001",
            context=context,
        )


class UnsupportedFileFormatError(FileProcessingError):
    """
    Raised when an unsupported file format is supplied.
    """

    def __init__(
        self,
        file_path: str,
        extension: str,
    ) -> None:
        super().__init__(
            message=f"Unsupported file format: {extension}",
            file_path=file_path,
            extension=extension,
        )


# ==============================================================================
# Video Exceptions
# ==============================================================================


class VideoProcessingError(MystoriumXError):
    """
    Raised when video processing fails.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            error_code="VID-3001",
            context=context,
        )


class FrameExtractionError(VideoProcessingError):
    """
    Raised when frame extraction fails.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            operation="frame_extraction",
            **context,
        )
# ==============================================================================
# Scene Exceptions
# ==============================================================================


class SceneDetectionError(MystoriumXError):
    """
    Raised when automatic scene detection fails.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            error_code="SCN-4001",
            context=context,
        )


class SceneAnalysisError(MystoriumXError):
    """
    Raised when scene analysis cannot be completed.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            error_code="SCN-4002",
            context=context,
        )


# ==============================================================================
# AI Exceptions
# ==============================================================================


class AIModelError(MystoriumXError):
    """
    Raised when an AI model fails.
    """

    def __init__(
        self,
        message: str,
        model_name: str | None = None,
        **context: Any,
    ) -> None:

        if model_name:
            context["model_name"] = model_name

        super().__init__(
            message=message,
            error_code="AI-5001",
            context=context,
        )


class PromptEnhancementError(AIModelError):
    """
    Raised when prompt enhancement fails.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            model_name="PromptEnhancer",
            **context,
        )


class MusicGenerationError(AIModelError):
    """
    Raised when music generation fails.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            model_name="MusicGenerator",
            **context,
        )


class ImageAnalysisError(AIModelError):
    """
    Raised when image analysis fails.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            model_name="ImageAnalyzer",
            **context,
        )


# ==============================================================================
# Audio Exceptions
# ==============================================================================


class AudioProcessingError(MystoriumXError):
    """
    Raised when audio processing fails.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            error_code="AUD-6001",
            context=context,
        )


class MasteringError(AudioProcessingError):
    """
    Raised when mastering fails.
    """

    pass


class WaveformGenerationError(AudioProcessingError):
    """
    Raised when waveform generation fails.
    """

    pass


class ExportError(MystoriumXError):
    """
    Raised when export fails.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            error_code="EXP-7001",
            context=context,
        )
# ==============================================================================
# Storage Exceptions
# ==============================================================================


class StorageError(MystoriumXError):
    """
    Raised when storage operations fail.
    """

    def __init__(
        self,
        message: str,
        **context: Any,
    ) -> None:
        super().__init__(
            message=message,
            error_code="STO-8001",
            context=context,
        )


class DatabaseError(StorageError):
    """
    Raised when database operations fail.
    """

    pass


class CacheError(StorageError):
    """
    Raised when cache operations fail.
    """

    pass


# ==============================================================================
# Utility Functions
# ==============================================================================


def exception_to_dict(exception: Exception) -> Dict[str, Any]:
    """
    Convert an exception into a serializable dictionary.
    """

    if isinstance(exception, MystoriumXError):
        payload = exception.to_dict()
    else:
        payload = {
            "exception_id": str(uuid.uuid4()),
            "error_code": "SYS-9999",
            "message": str(exception),
            "details": None,
            "context": {},
            "timestamp": datetime.utcnow().isoformat(),
        }

    payload["exception_type"] = exception.__class__.__name__
    payload["traceback"] = traceback.format_exc()

    return payload


def build_exception(
    message: str,
    *,
    error_code: str,
    **context: Any,
) -> MystoriumXError:
    """
    Create a generic MystoriumXError.
    """

    return MystoriumXError(
        message=message,
        error_code=error_code,
        context=context,
    )


__all__ = [
    "MystoriumXError",
    "ConfigurationError",
    "ValidationError",
    "FileProcessingError",
    "UnsupportedFileFormatError",
    "VideoProcessingError",
    "FrameExtractionError",
    "SceneDetectionError",
    "SceneAnalysisError",
    "AIModelError",
    "PromptEnhancementError",
    "MusicGenerationError",
    "ImageAnalysisError",
    "AudioProcessingError",
    "MasteringError",
    "WaveformGenerationError",
    "ExportError",
    "StorageError",
    "DatabaseError",
    "CacheError",
    "exception_to_dict",
    "build_exception",
]
