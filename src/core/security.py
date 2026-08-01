"""
MystoriumX AI Studio
Core Security

File:
src/core/security.py

Part 1/3
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import mimetypes
import os
import re
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterable

from src.core.config import get_config
from src.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


# ==============================================================================
# Constants
# ==============================================================================

_INVALID_FILENAME_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"[^A-Za-z0-9._-]+"
)

_RESERVED_WINDOWS_NAMES: Final[set[str]] = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


# ==============================================================================
# Security Configuration
# ==============================================================================


@dataclass(slots=True, frozen=True)
class SecurityPolicy:
    """
    Runtime security policy.
    """

    max_filename_length: int
    sanitize_filenames: bool
    verify_ssl: bool
    allowed_protocols: tuple[str, ...]

    @classmethod
    def load(cls) -> "SecurityPolicy":
        config = get_config()

        return cls(
            max_filename_length=(
                config.security.maximum_filename_length
            ),
            sanitize_filenames=(
                config.security.sanitize_filenames
            ),
            verify_ssl=config.security.verify_ssl,
            allowed_protocols=tuple(
                config.security.allowed_protocols
            ),
        )


_POLICY = SecurityPolicy.load()


# ==============================================================================
# Path Validation
# ==============================================================================


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename while preserving its extension.
    """

    filename = filename.strip()

    if not filename:
        raise ValidationError("Filename cannot be empty.")

    cleaned = _INVALID_FILENAME_PATTERN.sub("_", filename)

    cleaned = cleaned.strip("._")

    if len(cleaned) > _POLICY.max_filename_length:
        stem, suffix = os.path.splitext(cleaned)

        max_stem = (
            _POLICY.max_filename_length - len(suffix)
        )

        cleaned = stem[:max_stem] + suffix

    stem = Path(cleaned).stem.upper()

    if stem in _RESERVED_WINDOWS_NAMES:
        cleaned = f"safe_{cleaned}"

    if not cleaned:
        raise ValidationError("Invalid filename.")

    return cleaned


def validate_extension(
    path: str | Path,
    allowed_extensions: Iterable[str],
) -> None:
    """
    Validate a file extension.
    """

    suffix = Path(path).suffix.lower()

    allowed = {
        ext.lower()
        for ext in allowed_extensions
    }

    if suffix not in allowed:
        raise ValidationError(
            f"Unsupported file extension: {suffix}"
        )


def ensure_safe_path(path: Path) -> Path:
    """
    Resolve and validate a filesystem path.
    """

    resolved = path.expanduser().resolve()

    if ".." in resolved.parts:
        raise ValidationError(
            "Directory traversal detected."
        )

    return resolved


# ==============================================================================
# MIME Validation
# ==============================================================================


def guess_mime_type(path: str | Path) -> str:
    """
    Guess MIME type using Python's mimetypes database.
    """

    mime, _ = mimetypes.guess_type(str(path))

    return mime or "application/octet-stream"


def is_video_file(path: str | Path) -> bool:
    """
    Return True if the file appears to be a video.
    """

    return guess_mime_type(path).startswith("video/")


def is_audio_file(path: str | Path) -> bool:
    """
    Return True if the file appears to be audio.
    """

    return guess_mime_type(path).startswith("audio/")
  # ==============================================================================
# Hash Utilities
# ==============================================================================


def sha256_file(file_path: Path) -> str:
    """
    Calculate SHA-256 checksum of a file.
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


def sha256_text(text: str) -> str:
    """
    Calculate SHA-256 hash of text.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def generate_secure_token(
    length: int = 32,
) -> str:
    """
    Generate a cryptographically secure token.
    """

    if length < 16:
        raise ValidationError(
            "Token length must be at least 16."
        )

    return secrets.token_hex(length)


def generate_secret_key(
    length: int = 64,
) -> str:
    """
    Generate a secure secret key.
    """

    return secrets.token_urlsafe(length)


# ==============================================================================
# HMAC Utilities
# ==============================================================================


def create_signature(
    message: str,
    secret: str,
) -> str:
    """
    Create HMAC-SHA256 signature.
    """

    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_signature(
    message: str,
    signature: str,
    secret: str,
) -> bool:
    """
    Verify HMAC signature.
    """

    expected = create_signature(
        message,
        secret,
    )

    return hmac.compare_digest(
        expected,
        signature,
    )


# ==============================================================================
# Environment Validation
# ==============================================================================


def verify_protocol(
    protocol: str,
) -> bool:
    """
    Verify that a protocol is allowed.
    """

    return (
        protocol.lower()
        in _POLICY.allowed_protocols
    )


def require_environment(
    variable_name: str,
) -> str:
    """
    Read a required environment variable.
    """

    value = os.getenv(variable_name)

    if not value:
        raise ValidationError(
            f"Missing environment variable: {variable_name}"
        )

    return value


def file_exists(
    path: Path,
) -> bool:
    """
    Safely determine whether a file exists.
    """

    try:
        return ensure_safe_path(path).exists()
    except Exception:
        logger.exception(
            "File existence check failed."
        )
        return False
      # ==============================================================================
# Security Helpers
# ==============================================================================


def validate_upload(
    file_path: Path,
    allowed_extensions: Iterable[str],
) -> Path:
    """
    Validate an uploaded file.
    """

    file_path = ensure_safe_path(file_path)

    if not file_path.exists():
        raise ValidationError(
            f"File does not exist: {file_path}"
        )

    validate_extension(
        file_path,
        allowed_extensions,
    )

    return file_path


def sanitize_upload_name(
    filename: str,
) -> str:
    """
    Sanitize an uploaded filename.
    """

    return sanitize_filename(filename)


def secure_compare(
    value1: str,
    value2: str,
) -> bool:
    """
    Constant-time string comparison.
    """

    return hmac.compare_digest(
        value1,
        value2,
    )


__all__ = [
    "SecurityPolicy",
    "sanitize_filename",
    "sanitize_upload_name",
    "validate_extension",
    "validate_upload",
    "ensure_safe_path",
    "guess_mime_type",
    "is_video_file",
    "is_audio_file",
    "sha256_file",
    "sha256_text",
    "generate_secure_token",
    "generate_secret_key",
    "create_signature",
    "verify_signature",
    "verify_protocol",
    "require_environment",
    "file_exists",
    "secure_compare",
]
