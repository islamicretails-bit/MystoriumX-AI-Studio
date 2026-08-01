# ============================================================
# MystoriumX AI Studio
# Schema Layer - User Input Schemas
#
# File:
# app/schemas/user_input.py
#
# Responsibility:
# Validate user requests coming from UI.
#
# Used by:
# - Streamlit Dashboard
# - Pipeline Orchestrator
# - AI Services
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path

from typing import Optional, Dict, List


from pydantic import BaseModel, Field



# ============================================================
# File Upload Input
# ============================================================

class FileUploadInput(BaseModel):
    """
    User uploaded media files.
    """


    video_file: Optional[Path] = None


    script_file: Optional[Path] = None


    narration_file: Optional[Path] = None



# ============================================================
# AI Prompt Input
# ============================================================

class PromptInput(BaseModel):
    """
    User cinematic music prompt.
    """


    prompt: str = Field(

        ...,

        min_length=5,

        max_length=1000,

        description="Music generation instruction"

    )


    style: Optional[str] = (

        "cinematic documentary"

    )


    emotion: Optional[str] = (

        "mysterious"

    )


    intensity: float = Field(

        default=5.0,

        ge=0.0,

        le=10.0

    )



# ============================================================
# Music Generation Input
# ============================================================

class MusicGenerationInput(BaseModel):
    """
    AI music generation parameters.
    """


    prompt: PromptInput


    duration_seconds: int = Field(

        default=60,

        ge=5,

        le=600

    )


    instrumental_only: bool = True


    cinematic: bool = True



# ============================================================
# Scene Analysis Input
# ============================================================

class SceneAnalysisInput(BaseModel):
    """
    Computer vision processing request.
    """


    video_path: Path


    detect_cuts: bool = True


    analyze_mood: bool = True


    extract_frames: bool = True



# ============================================================
# Mastering Input
# ============================================================

class MasteringInput(BaseModel):
    """
    Professional audio mastering settings.
    """


    audio_path: Path


    normalize_loudness: bool = True


    target_lufs: float = (

        -14.0

    )


    enable_compression: bool = True


    enable_limiting: bool = True



# ============================================================
# Export Input
# ============================================================

class ExportInput(BaseModel):
    """
    Final export request.
    """


    project_id: str


    output_format: str = (

        "wav"

    )


    include_metadata: bool = True


    include_analytics: bool = True



# ============================================================
# Complete AI Pipeline Request
# ============================================================

class PipelineRequest(BaseModel):
    """
    Complete documentary AI workflow request.

    Flow:

    Upload
      ↓
    Analysis
      ↓
    Music Generation
      ↓
    Mastering
      ↓
    Export

    """


    project_id: str


    files: FileUploadInput


    prompt: Optional[PromptInput] = None


    music: Optional[MusicGenerationInput] = None


    scene_analysis: Optional[SceneAnalysisInput] = None


    mastering: Optional[MasteringInput] = None


    export: Optional[ExportInput] = None


    options: Dict[str, bool] = Field(

        default_factory=lambda: {

            "auto_prompt": True,

            "scene_detection": True,

            "audio_mastering": True,

            "export": True

        }

    )



# ============================================================
# UI Session Input
# ============================================================

class UISessionInput(BaseModel):
    """
    Streamlit session configuration.
    """


    user_id: Optional[str] = None


    project_id: Optional[str] = None


    active_tab: str = (

        "dashboard"

    )


    preferences: Dict = Field(

        default_factory=dict

    )
