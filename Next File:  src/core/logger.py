"""
MystoriumX AI Studio
Core Logger

File:
src/core/logger.py

Part 1/3
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from src.core.config import get_config


# ==============================================================================
# Configuration
# ==============================================================================


@dataclass(slots=True)
class LoggerConfiguration:
    """
    Logger configuration model.
    """

    name: str
    level: int
    log_file: Path
    enable_console: bool
    enable_file: bool
    max_bytes: int
    backup_count: int
    log_format: str


# ==============================================================================
# Formatter
# ==============================================================================


class ColoredFormatter(logging.Formatter):
    """
    ANSI colored formatter for console logging.
    """

    COLORS: Dict[int, str] = {
        logging.DEBUG: "\033[37m",
        logging.INFO: "\033[36m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[41m",
    }

    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)

        color = self.COLORS.get(record.levelno, self.RESET)

        return f"{color}{message}{self.RESET}"


# ==============================================================================
# Logger Manager
# ==============================================================================


class LoggerManager:
    """
    Enterprise logging manager.
    """

    def __init__(self) -> None:

        config = get_config()

        log_directory = config.directories.logs
        log_directory.mkdir(parents=True, exist_ok=True)

        logging_config = config.logging

        self.configuration = LoggerConfiguration(
            name=config.application.application_name,
            level=getattr(
                logging,
                logging_config.level.upper(),
                logging.INFO,
            ),
            log_file=log_directory / logging_config.log_filename,
            enable_console=logging_config.console_logging,
            enable_file=logging_config.file_logging,
            max_bytes=logging_config.max_file_size_mb * 1024 * 1024,
            backup_count=logging_config.backup_count,
            log_format=logging_config.log_format,
        )

        self._loggers: Dict[str, logging.Logger] = {}

    def get_logger(
        self,
        name: Optional[str] = None,
    ) -> logging.Logger:

        logger_name = (
            name
            if name
            else self.configuration.name
        )

        if logger_name in self._loggers:
            return self._loggers[logger_name]

        logger = logging.getLogger(logger_name)

        logger.setLevel(self.configuration.level)

        logger.propagate = False

        logger.handlers.clear()

        if self.configuration.enable_console:
            logger.addHandler(
                self._build_console_handler()
            )

        if self.configuration.enable_file:
            logger.addHandler(
                self._build_file_handler()
            )

        self._loggers[logger_name] = logger

        return logger

    def _build_console_handler(
        self,
    ) -> logging.Handler:

        handler = logging.StreamHandler(sys.stdout)

        formatter = ColoredFormatter(
            self.configuration.log_format
        )

        handler.setFormatter(formatter)

        handler.setLevel(self.configuration.level)

        return handler

    def _build_file_handler(
        self,
    ) -> logging.Handler:

        handler = logging.handlers.RotatingFileHandler(
            filename=self.configuration.log_file,
            maxBytes=self.configuration.max_bytes,
            backupCount=self.configuration.backup_count,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            self.configuration.log_format
        )

        handler.setFormatter(formatter)

        handler.setLevel(self.configuration.level)

        return handler
      # ==============================================================================
# Logger Utilities
# ==============================================================================


class LoggerManager(LoggerManager):
    """
    Extended logger manager utilities.
    """

    def set_level(self, level: int) -> None:
        """
        Update logging level for all managed loggers.
        """

        self.configuration.level = level

        for logger in self._loggers.values():
            logger.setLevel(level)

            for handler in logger.handlers:
                handler.setLevel(level)

    def add_file_handler(
        self,
        log_file: Path,
        level: Optional[int] = None,
    ) -> None:
        """
        Add an additional rotating file handler.
        """

        handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=self.configuration.max_bytes,
            backupCount=self.configuration.backup_count,
            encoding="utf-8",
        )

        handler.setFormatter(
            logging.Formatter(
                self.configuration.log_format
            )
        )

        handler.setLevel(
            level
            if level is not None
            else self.configuration.level
        )

        for logger in self._loggers.values():
            logger.addHandler(handler)

    def remove_handlers(self) -> None:
        """
        Remove every handler from all managed loggers.
        """

        for logger in self._loggers.values():

            handlers = logger.handlers[:]

            for handler in handlers:
                handler.close()
                logger.removeHandler(handler)

    def shutdown(self) -> None:
        """
        Gracefully shutdown logging.
        """

        self.remove_handlers()

        logging.shutdown()

    @property
    def logger_names(self) -> list[str]:
        """
        Return registered logger names.
        """

        return list(self._loggers.keys())

    def has_logger(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a logger exists.
        """

        return name in self._loggers

    def clear_cache(self) -> None:
        """
        Clear cached logger instances.
        """

        self.remove_handlers()

        self._loggers.clear()

    def reconfigure(self) -> None:
        """
        Reload configuration from RuntimeConfig.
        """

        config = get_config()

        self.configuration.level = getattr(
            logging,
            config.logging.level.upper(),
            logging.INFO,
        )

        self.configuration.enable_console = (
            config.logging.console_logging
        )

        self.configuration.enable_file = (
            config.logging.file_logging
        )

        self.configuration.max_bytes = (
            config.logging.max_file_size_mb
            * 1024
            * 1024
        )

        self.configuration.backup_count = (
            config.logging.backup_count
        )

        self.configuration.log_format = (
            config.logging.log_format
        )

        self.configuration.log_file = (
            config.directories.logs
            / config.logging.log_filename
        )

        self.clear_cache()
      # ==============================================================================
# Global Logger Instance
# ==============================================================================


_logger_manager = LoggerManager()


def get_logger(
    name: Optional[str] = None,
) -> logging.Logger:
    """
    Return a configured logger instance.
    """

    return _logger_manager.get_logger(name)


def set_log_level(level: int) -> None:
    """
    Set logging level for all loggers.
    """

    _logger_manager.set_level(level)


def reload_logger_configuration() -> None:
    """
    Reload logger configuration from RuntimeConfig.
    """

    _logger_manager.reconfigure()


def shutdown_logging() -> None:
    """
    Shutdown logging subsystem.
    """

    _logger_manager.shutdown()


# ==============================================================================
# Convenience Logger
# ==============================================================================

logger = get_logger("MystoriumX")


# ==============================================================================
# Module Exports
# ==============================================================================

__all__ = [
    "LoggerConfiguration",
    "ColoredFormatter",
    "LoggerManager",
    "get_logger",
    "set_log_level",
    "reload_logger_configuration",
    "shutdown_logging",
    "logger",
]
