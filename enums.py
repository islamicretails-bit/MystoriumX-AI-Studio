# ============================================================
# MystoriumX AI Studio
# Domain Layer - Type Safe Enumerations
#
# File:
# app/domain/enums.py
#
# Responsibility:
# Centralized domain constants.
#
# Clean Architecture:
# No external dependencies.
#
# ============================================================


from __future__ import annotations


from enum import Enum



# ============================================================
# Project Status
# ============================================================

class ProjectStatus(Enum):
    """
    Documentary project lifecycle states.
    """


    CREATED = "created"


    UPLOADED = "uploaded"


    ANALYZING = "analyzing"


    MUSIC_GENERATING = "music_generating"


    MASTERING = "mastering"


    EXPORTING = "exporting"


    COMPLETED = "completed"


    FAILED = "failed"



# ============================================================
# Processing Pipeline Stages
# ============================================================

class ProcessingStage(Enum):
    """
    AI pipeline execution stages.
    """


    INITIALIZATION = "initialization"


    VIDEO_UPLOAD = "video_upload"


    SCRIPT_ANALYSIS = "script_analysis"


    VOICE_PROCESSING = "voice_processing"


    SCENE_DETECTION = "scene_detection"


    MOOD_ANALYSIS = "mood_analysis"


    PROMPT_GENERATION = "prompt_generation"


    MUSIC_GENERATION = "music_generation"


    AUDIO_MASTERING = "audio_mastering"


    AUDIO_ANALYTICS = "audio_analytics"


    FINAL_EXPORT = "final_export"



# ============================================================
# Scene Mood Types
# ============================================================

class SceneMood(Enum):
    """
    Cinematic scene emotions.
    """


    UNKNOWN = "unknown"


    DARK = "dark"


    MYSTERIOUS = "mysterious"


    TENSE = "tense"


    EPIC = "epic"


    EMOTIONAL = "emotional"


    HOPEFUL = "hopeful"


    SAD = "sad"


    HORROR = "horror"


    ACTION = "action"



# ============================================================
# Audio Formats
# ============================================================

class AudioFormat(Enum):
    """
    Supported soundtrack formats.
    """


    WAV = "wav"


    MP3 = "mp3"


    FLAC = "flac"


    AAC = "aac"



# ============================================================
# Video Formats
# ============================================================

class VideoFormat(Enum):
    """
    Supported documentary video formats.
    """


    MP4 = "mp4"


    MOV = "mov"


    MKV = "mkv"


    AVI = "avi"



# ============================================================
# AI Model Status
# ============================================================

class ModelStatus(Enum):
    """
    AI model loading states.
    """


    NOT_LOADED = "not_loaded"


    LOADING = "loading"


    READY = "ready"


    ERROR = "error"



# ============================================================
# Generation Status
# ============================================================

class GenerationStatus(Enum):
    """
    AI generation process states.
    """


    QUEUED = "queued"


    PROCESSING = "processing"


    GENERATED = "generated"


    FAILED = "failed"



# ============================================================
# Export Status
# ============================================================

class ExportStatus(Enum):
    """
    Final export states.
    """


    WAITING = "waiting"


    PROCESSING = "processing"


    SUCCESS = "success"


    FAILED = "failed"



# ============================================================
# User Input Types
# ============================================================

class InputType(Enum):
    """
    Supported user inputs.
    """


    VIDEO = "video"


    SCRIPT = "script"


    NARRATION = "narration"


    MUSIC_REFERENCE = "music_reference"
