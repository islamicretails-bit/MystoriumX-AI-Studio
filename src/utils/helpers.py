"""
MystoriumX AI Studio
Utility Helpers

File:
src/utils/helpers.py

Part 1/3
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


# ==============================================================================
# Time Utilities
# ==============================================================================


def utc_now() -> datetime:
    """
    Return the current UTC datetime.
    """

    return datetime.utcnow()


def timestamp() -> float:
    """
    Return UNIX timestamp.
    """

    return time.time()


def generate_uuid() -> str:
    """
    Generate a UUID4 string.
    """

    return str(uuid.uuid4())


# ==============================================================================
# JSON Utilities
# ==============================================================================


def load_json(
    file_path: Path,
) -> Dict[str, Any]:
    """
    Load JSON from disk.
    """

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as stream:
        return json.load(stream)


def save_json(
    file_path: Path,
    data: Dict[str, Any],
    *,
    indent: int = 4,
) -> None:
    """
    Save JSON to disk.
    """

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with file_path.open(
        "w",
        encoding="utf-8",
    ) as stream:
        json.dump(
            data,
            stream,
            indent=indent,
            ensure_ascii=False,
        )


# ==============================================================================
# Dictionary Utilities
# ==============================================================================


def remove_none(
    mapping: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Remove keys with None values.
    """

    return {
        key: value
        for key, value in mapping.items()
        if value is not None
    }


def merge_dicts(
    *dictionaries: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Merge dictionaries.
    """

    merged: Dict[str, Any] = {}

    for dictionary in dictionaries:
        merged.update(dictionary)

    return merged


# ==============================================================================
# Timing Decorator
# ==============================================================================


def timed(
    function: F,
) -> F:
    """
    Log execution time.
    """

    @wraps(function)
    def wrapper(
        *args: Any,
        **kwargs: Any,
    ) -> Any:

        start = time.perf_counter()

        result = function(
            *args,
            **kwargs,
        )

        elapsed = time.perf_counter() - start

        logger.info(
            "%s executed in %.3f sec",
            function.__name__,
            elapsed,
        )

        return result

    return wrapper  # type: ignore[return-value]
# ==============================================================================
# String Utilities
# ==============================================================================


def human_readable_size(
    size_bytes: int,
) -> str:
    """
    Convert bytes to a human-readable string.
    """

    units = (
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    )

    size = float(size_bytes)

    for unit in units:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def format_duration(
    seconds: float,
) -> str:
    """
    Format seconds as HH:MM:SS.
    """

    total = int(seconds)

    hours, remainder = divmod(total, 3600)
    minutes, seconds = divmod(remainder, 60)

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )


# ==============================================================================
# Collection Utilities
# ==============================================================================


def chunked(
    values: Iterable[Any],
    chunk_size: int,
) -> list[list[Any]]:
    """
    Split an iterable into chunks.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero."
        )

    values = list(values)

    return [
        values[index:index + chunk_size]
        for index in range(
            0,
            len(values),
            chunk_size,
        )
    ]


def first_not_none(
    *values: Optional[Any],
) -> Optional[Any]:
    """
    Return the first non-None value.
    """

    for value in values:
        if value is not None:
            return value

    return None


# ==============================================================================
# Retry Decorator
# ==============================================================================


def retry(
    attempts: int = 3,
    delay: float = 1.0,
):
    """
    Retry a function when it raises an exception.
    """

    def decorator(function: F):

        @wraps(function)
        def wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> Any:

            last_exception: Exception | None = None

            for _ in range(attempts):

                try:
                    return function(
                        *args,
                        **kwargs,
                    )

                except Exception as exc:
                    last_exception = exc

                    logger.warning(
                        "Retrying %s after error: %s",
                        function.__name__,
                        exc,
                    )

                    time.sleep(delay)

            assert last_exception is not None

            raise last_exception

        return wrapper

    return decorator
# ==============================================================================
# Miscellaneous Utilities
# ==============================================================================


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """
    Clamp a value between the given limits.
    """

    return max(
        minimum,
        min(value, maximum),
    )


def safe_int(
    value: Any,
    default: int = 0,
) -> int:
    """
    Safely convert a value to int.
    """

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    """
    Safely convert a value to float.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ==============================================================================
# Module Exports
# ==============================================================================


__all__ = [
    "utc_now",
    "timestamp",
    "generate_uuid",
    "load_json",
    "save_json",
    "remove_none",
    "merge_dicts",
    "timed",
    "human_readable_size",
    "format_duration",
    "chunked",
    "first_not_none",
    "retry",
    "clamp",
    "safe_int",
    "safe_float",
]
