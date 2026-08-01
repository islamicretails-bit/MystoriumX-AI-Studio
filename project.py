# ============================================================
# MystoriumX AI Studio
# Schema Layer - Project Schemas
#
# File:
# app/schemas/project.py
#
# Responsibility:
# Project data validation models.
#
# Used by:
# - Streamlit UI
# - Pipeline Services
# - API Layer
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from datetime import datetime

from pathlib import Path

from typing import Optional, Dict, List


from pydantic import BaseModel, Field



# ============================================================
# Project Creation Schema
# ============================================================

class ProjectCreateSchema(BaseModel):
    """
    User project creation request.
    """


    project_name: str = Field(

        ...,

        min_length=3,

        max_length=100,

        description="Documentary project name"

    )


    description: Optional[str] = Field(

        default=None,

        description="Project description"

    )



# ============================================================
# Project Upload Schema
# ============================================================

class ProjectUploadSchema(BaseModel):
    """
    Uploaded project files.
    """


    project_id: str


    video_path: Optional[Path] = None


    script_path: Optional[Path] = None


    narration_path: Optional[Path] = None



# ============================================================
# Project Configuration Schema
# ============================================================

class ProjectConfigSchema(BaseModel):
    """
    AI generation configuration.
    """


    project_id: str


    cinematic_style: str = (

        "documentary cinematic"

    )


    target_duration: Optional[int] = Field(

        default=None,

        description="Target soundtrack duration"

    )


    enable_scene_analysis: bool = True


    enable_music_generation: bool = True


    enable_mastering: bool = True



# ============================================================
# Project Status Schema
# ============================================================

class ProjectStatusSchema(BaseModel):
    """
    Current project processing state.
    """


    project_id: str


    status: str


    progress: float = Field(

        default=0.0,

        ge=0.0,

        le=100.0

    )


    current_stage: str


    message: Optional[str] = None



# ============================================================
# Project Result Schema
# ============================================================

class ProjectResultSchema(BaseModel):
    """
    Final project output information.
    """


    project_id: str


    completed: bool


    generated_files: List[str] = Field(

        default_factory=list

    )


    analytics: Dict = Field(

        default_factory=dict

    )


    created_at: datetime = Field(

        default_factory=datetime.now

    )



# ============================================================
# Complete Project Schema
# ============================================================

class ProjectSchema(BaseModel):
    """
    Complete project representation.
    """


    project_id: str


    project_name: str


    description: Optional[str] = None


    video_file: Optional[str] = None


    script_file: Optional[str] = None


    narration_file: Optional[str] = None


    status: str = "created"


    created_at: datetime = Field(

        default_factory=datetime.now

    )


    metadata: Dict = Field(

        default_factory=dict

    )
