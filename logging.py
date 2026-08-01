# ============================================================
# MystoriumX AI Studio
# Core Layer - Production Logging System
#
# File:
# app/core/logging.py
#
# Responsibility:
# Central application logging management.
#
# Features:
# - Console logging
# - File logging
# - Error tracking
# - Production log formatting
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


import logging

from pathlib import Path

from datetime import datetime

from typing import Optional



# ============================================================
# Log Configuration
# ============================================================

LOG_FORMAT = (

    "%(asctime)s | "

    "%(levelname)s | "

    "%(name)s | "

    "%(message)s"

)



DATE_FORMAT = (

    "%Y-%m-%d %H:%M:%S"

)



# ============================================================
# Logger Manager
# ============================================================

class LoggerManager:
    """
    Production logging controller.

    Provides:

    - Application logger setup
    - File logging
    - Console monitoring
    - Module logging support

    """



    def __init__(
        self,
        log_directory: str = "logs"
    ) -> None:


        self.log_directory = Path(

            log_directory

        )


        self.log_directory.mkdir(

            parents=True,

            exist_ok=True

        )


        self.log_file = (

            self.log_directory

            /

            self._generate_filename()

        )


        self._configured = False



    # ========================================================
    # Configure Logging
    # ========================================================

    def configure(
        self,
        level: int = logging.INFO
    ) -> None:

        """
        Configure global application logging.
        """


        if self._configured:

            return



        formatter = logging.Formatter(

            LOG_FORMAT,

            DATE_FORMAT

        )



        # Console Handler

        console_handler = (

            logging.StreamHandler()

        )


        console_handler.setFormatter(

            formatter

        )



        console_handler.setLevel(

            level

        )



        # File Handler

        file_handler = (

            logging.FileHandler(

                self.log_file,

                encoding="utf-8"

            )

        )


        file_handler.setFormatter(

            formatter

        )


        file_handler.setLevel(

            level

        )



        root_logger = logging.getLogger()



        root_logger.setLevel(

            level

        )



        root_logger.addHandler(

            console_handler

        )


        root_logger.addHandler(

            file_handler

        )



        self._configured = True



        logging.info(

            "MystoriumX logging system initialized"

        )



    # ========================================================
    # Create Module Logger
    # ========================================================

    def get_logger(
        self,
        name: str
    ) -> logging.Logger:

        """
        Return module logger.
        """


        return logging.getLogger(

            name

        )



    # ========================================================
    # Exception Logger
    # ========================================================

    def log_exception(
        self,
        logger: logging.Logger,
        error: Exception
    ) -> None:

        """
        Log application exceptions.
        """


        logger.exception(

            str(error)

        )



    # ========================================================
    # Generate Log Filename
    # ========================================================

    def _generate_filename(
        self
    ) -> str:

        """
        Generate unique log filename.
        """


        timestamp = (

            datetime.now()

            .strftime(

                "%Y%m%d_%H%M%S"

            )

        )


        return (

            f"mystoriumx_{timestamp}.log"

        )



# ============================================================
# Global Logger Instance
# ============================================================

logger_manager = LoggerManager()


logger_manager.configure()



# Application logger

app_logger = logger_manager.get_logger(

    "MystoriumX"

)
