# ============================================================
# MystoriumX AI Studio
# Domain Layer - Core Entities
#
# File:
# app/domain/entities.py
#
# Responsibility:
# Business objects and core domain models.
#
# Clean Architecture:
# Domain layer contains no external dependencies.
#
# ============================================================


from __future__ import annotations


from dataclasses import dataclass, field

from pathlib import Path

from typing import List, Optional, Dict

from datetime import datetime



# ============================================================
# Project Entity
# ============================================================

@dataclass
class ProjectEntity:
    """
    Represents a documentary AI project.
    """


    project_id: str


    name: str


    created_at: datetime = field(

        default_factory=datetime.now

    )


    video_file: Optional[Path] = None


    script_file: Optional[Path] = None


    narration_file: Optional[Path] = None


    status: str = "created"


    metadata: Dict = field(

        default_factory=dict

    )



# ============================================================
# Scene Entity
# ============================================================

@dataclass
class SceneEntity:
    """
    Represents detected documentary scene.
    """


    scene_id: str


    start_time: float


    end_time: float


    duration: float


    confidence: float


    mood: Optional[str] = None


    intensity: float = 0.0


    description: Optional[str] = None



# ============================================================
# Audio Entity
# ============================================================

@dataclass
class AudioEntity:
    """
    Represents generated soundtrack.
    """


    audio_id: str


    file_path: Path


    duration: float


    sample_rate: int


    format: str


    loudness_lufs: Optional[float] = None


    mastered: bool = False



# ============================================================
# Music Prompt Entity
# ============================================================

@dataclass
class MusicPromptEntity:
    """
    Represents AI music generation prompt.
    """


    prompt_id: str


    original_prompt: str


    enhanced_prompt: Optional[str] = None


    cinematic_style: Optional[str] = None


    emotion: Optional[str] = None


    intensity_level: float = 0.0



# ============================================================
# Processing Job Entity
# ============================================================

@dataclass
class ProcessingJobEntity:
    """
    Represents AI pipeline execution job.
    """


    job_id: str


    project_id: str


    current_stage: str = "initialized"


    progress: float = 0.0


    completed: bool = False


    error_message: Optional[str] = None



# ============================================================
# Export Package Entity
# ============================================================

@dataclass
class ExportEntity:
    """
    Represents final exported package.
    """


    export_id: str


    project_id: str


    output_files: List[Path] = field(

        default_factory=list

    )


    export_format: str = "wav"


    created_at: datetime = field(

        default_factory=datetime.now

    )



# ============================================================
# Documentary Workflow Entity
# ============================================================

@dataclass
class DocumentaryWorkflow:
    """
    Complete documentary production state.

    Connects:

    Video
      ↓
    Scenes
      ↓
    Music
      ↓
    Export

    """


    project: ProjectEntity


    scenes: List[SceneEntity] = field(

        default_factory=list

    )


    audio: Optional[AudioEntity] = None


    prompt: Optional[MusicPromptEntity] = None


    job: Optional[ProcessingJobEntity] = None


    export: Optional[ExportEntity] = None
