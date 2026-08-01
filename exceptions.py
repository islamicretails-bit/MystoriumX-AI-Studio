# ============================================================
# MystoriumX AI Studio
# Core Layer - Custom Exception System
#
# File:
# app/core/exceptions.py
#
# Responsibility:
# Centralized application error handling.
#
# Features:
# - AI pipeline exceptions
# - Media processing errors
# - Storage errors
# - Validation errors
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from typing import Optional


import logging



logger = logging.getLogger(
    "MystoriumX.Exceptions"
)



# ============================================================
# Base Application Exception
# ============================================================

class MystoriumXException(Exception):
    """
    Base exception for all application errors.
    """



    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None
    ) -> None:


        self.message = message

        self.error_code = error_code


        super().__init__(

            message

        )



# ============================================================
# Configuration Errors
# ============================================================

class ConfigurationError(
    MystoriumXException
):
    """
    Raised when application configuration fails.
    """



# ============================================================
# File Errors
# ============================================================

class FileProcessingError(
    MystoriumXException
):
    """
    Raised when file handling fails.
    """



# ============================================================
# Upload Errors
# ============================================================

class UploadError(
    MystoriumXException
):
    """
    Raised during user upload processing.
    """



# ============================================================
# Video Processing Errors
# ============================================================

class VideoProcessingError(
    MystoriumXException
):
    """
    Raised when video analysis fails.
    """



# ============================================================
# Scene Detection Errors
# ============================================================

class SceneDetectionError(
    MystoriumXException
):
    """
    Raised when computer vision scene analysis fails.
    """



# ============================================================
# Audio Processing Errors
# ============================================================

class AudioProcessingError(
    MystoriumXException
):
    """
    Raised when audio DSP operations fail.
    """



# ============================================================
# Music Generation Errors
# ============================================================

class MusicGenerationError(
    MystoriumXException
):
    """
    Raised when AI music generation fails.
    """



# ============================================================
# Model Errors
# ============================================================

class ModelLoadingError(
    MystoriumXException
):
    """
    Raised when AI model loading fails.
    """



# ============================================================
# Export Errors
# ============================================================

class ExportError(
    MystoriumXException
):
    """
    Raised when final export fails.
    """



# ============================================================
# Storage Errors
# ============================================================

class StorageError(
    MystoriumXException
):
    """
    Raised when project storage fails.
    """



# ============================================================
# Security Errors
# ============================================================

class SecurityViolationError(
    MystoriumXException
):
    """
    Raised when unsafe operation detected.
    """



# ============================================================
# Exception Handler Utility
# ============================================================

class ExceptionHandler:
    """
    Central exception logging helper.

    Converts errors into
    production readable format.

    """



    @staticmethod
    def handle(
        error: Exception
    ) -> dict:

        """
        Convert exception into response format.
        """


        logger.exception(

            str(error)

        )



        if isinstance(

            error,

            MystoriumXException

        ):


            return {


                "success":

                    False,


                "error":

                    error.message,


                "code":

                    error.error_code

            }



        return {


            "success":

                False,


            "error":

                "Internal application error",


            "code":

                "UNKNOWN_ERROR"

        }



    @staticmethod
    def raise_error(
        error_type,
        message: str,
        code: str
    ) -> None:

        """
        Raise formatted application error.
        """


        raise error_type(

            message,

            code

        )



# ============================================================
# Global Exception Handler
# ============================================================

exception_handler = ExceptionHandler()
