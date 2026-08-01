"""
MystoriumX AI Studio
Model: User Input

Enterprise Production Model
Python 3.11
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class InputSource(str, Enum):
    LOCAL = "local"
    URL = "url"
    YOUTUBE = "youtube"
    API = "api"


class ProcessingQuality(str, Enum):
    STANDARD = "standard"
    HIGH = "high"
    ULTRA = "ultra"
    CINEMATIC = "cinematic"


class MusicStyle(str, Enum):
    CINEMATIC = "cinematic"
    ORCHESTRAL = "orchestral"
    AMBIENT = "ambient"
    SUSPENSE = "suspense"
    DRAMATIC = "dramatic"
    EPIC = "epic"
    DOCUMENTARY = "documentary"
    MYSTERY = "mystery"
    HYBRID = "hybrid"


class ExportFormat(str, Enum):
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    AAC = "aac"
    OGG = "ogg"


@dataclass(slots=True)
class VideoInput:
    source: InputSource
    input_path: str
    original_filename: str
    file_size_bytes: int
    duration_seconds: float
    resolution: str
    frame_rate: float
    has_audio: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source.value,
            "input_path": self.input_path,
            "original_filename": self.original_filename,
            "file_size_bytes": self.file_size_bytes,
            "duration_seconds": self.duration_seconds,
            "resolution": self.resolution,
            "frame_rate": self.frame_rate,
            "has_audio": self.has_audio,
        }


@dataclass(slots=True)
class MusicGenerationSettings:
    style: MusicStyle = MusicStyle.DOCUMENTARY
    duration_seconds: Optional[float] = None
    cinematic_intensity: float = 0.8
    orchestral_amount: float = 0.8
    ambient_amount: float = 0.5
    percussion_amount: float = 0.6
    emotional_amount: float = 0.7
    generate_per_scene: bool = True
    seed: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "style": self.style.value,
            "duration_seconds": self.duration_seconds,
            "cinematic_intensity": self.cinematic_intensity,
            "orchestral_amount": self.orchestral_amount,
            "ambient_amount": self.ambient_amount,
            "percussion_amount": self.percussion_amount,
            "emotional_amount": self.emotional_amount,
            "generate_per_scene": self.generate_per_scene,
            "seed": self.seed,
        }


@dataclass(slots=True)
class AudioProcessingSettings:
    normalize_audio: bool = True
    target_lufs: float = -14.0
    apply_eq: bool = True
    apply_compression: bool = True
    apply_limiter: bool = True
    apply_voice_ducking: bool = True
    remove_noise: bool = True
    sample_rate: int = 48000
    bit_depth: int = 24

    def to_dict(self) -> Dict[str, Any]:
        return {
            "normalize_audio": self.normalize_audio,
            "target_lufs": self.target_lufs,
            "apply_eq": self.apply_eq,
            "apply_compression": self.apply_compression,
            "apply_limiter": self.apply_limiter,
            "apply_voice_ducking": self.apply_voice_ducking,
            "remove_noise": self.remove_noise,
            "sample_rate": self.sample_rate,
            "bit_depth": self.bit_depth,
        }


@dataclass(slots=True)
class ExportSettings:
    output_directory: Path
    output_format: ExportFormat = ExportFormat.WAV
    include_waveform: bool = True
    include_metadata: bool = True
    include_analytics: bool = True
    overwrite_existing: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "output_directory": str(self.output_directory),
            "output_format": self.output_format.value,
            "include_waveform": self.include_waveform,
            "include_metadata": self.include_metadata,
            "include_analytics": self.include_analytics,
            "overwrite_existing": self.overwrite_existing,
        }


@dataclass(slots=True)
class UserInputModel:
    project_name: str
    video: VideoInput
    quality: ProcessingQuality = ProcessingQuality.HIGH

    custom_prompt: Optional[str] = None

    language: str = "en"

    music: MusicGenerationSettings = field(
        default_factory=MusicGenerationSettings
    )

    audio: AudioProcessingSettings = field(
        default_factory=AudioProcessingSettings
    )

    export: ExportSettings = field(
        default_factory=lambda: ExportSettings(
            output_directory=Path("./exports")
        )
    )

    enable_scene_detection: bool = True
    enable_image_analysis: bool = True
    enable_prompt_enhancement: bool = True
    enable_music_generation: bool = True
    enable_mastering: bool = True
    enable_waveform_generation: bool = True
    enable_analytics: bool = True

    created_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "video": self.video.to_dict(),
            "quality": self.quality.value,
            "custom_prompt": self.custom_prompt,
            "language": self.language,
            "music": self.music.to_dict(),
            "audio": self.audio.to_dict(),
            "export": self.export.to_dict(),
            "enable_scene_detection": self.enable_scene_detection,
            "enable_image_analysis": self.enable_image_analysis,
            "enable_prompt_enhancement": self.enable_prompt_enhancement,
            "enable_music_generation": self.enable_music_generation,
            "enable_mastering": self.enable_mastering,
            "enable_waveform_generation": self.enable_waveform_generation,
            "enable_analytics": self.enable_analytics,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "tags": self.tags,
        }

    @property
    def processing_pipeline(self) -> List[str]:
        pipeline: List[str] = [
            "Video Upload",
        ]

        if self.enable_scene_detection:
            pipeline.append("Scene Detection")

        if self.enable_image_analysis:
            pipeline.append("Image Analysis")

        if self.enable_prompt_enhancement:
            pipeline.append("Prompt Enhancement")

        if self.enable_music_generation:
            pipeline.append("Music Generation")

        pipeline.append("Audio Processing")

        if self.enable_mastering:
            pipeline.append("Mastering")

        if self.enable_waveform_generation:
            pipeline.append("Waveform")

        if self.enable_analytics:
            pipeline.append("Analytics")

        pipeline.append("Export")

        return pipeline
