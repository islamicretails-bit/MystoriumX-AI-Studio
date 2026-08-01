"""
MystoriumX AI Studio
Model: Project
Part 1/3
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from models.audio import AudioAsset
from models.scene import SceneStatus


class ProjectStatus(str, Enum):
    CREATED = "created"
    UPLOADED = "uploaded"
    ANALYZING = "analyzing"
    SCENE_DETECTION = "scene_detection"
    PROMPT_GENERATION = "prompt_generation"
    MUSIC_GENERATION = "music_generation"
    AUDIO_PROCESSING = "audio_processing"
    MASTERING = "mastering"
    EXPORTING = "exporting"
    COMPLETED = "completed"
    FAILED = "failed"


class ExportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(slots=True)
class ProjectMetadata:
    project_id: str
    project_name: str
    created_at: datetime
    updated_at: datetime
    author: Optional[str] = None
    description: Optional[str] = None
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "author": self.author,
            "description": self.description,
            "version": self.version,
        }


@dataclass(slots=True)
class ProjectPaths:
    root: Path
    upload_dir: Path
    frames_dir: Path
    scenes_dir: Path
    prompts_dir: Path
    music_dir: Path
    audio_dir: Path
    waveform_dir: Path
    export_dir: Path
    logs_dir: Path

    def to_dict(self) -> Dict[str, str]:
        return {
            "root": str(self.root),
            "upload_dir": str(self.upload_dir),
            "frames_dir": str(self.frames_dir),
            "scenes_dir": str(self.scenes_dir),
            "prompts_dir": str(self.prompts_dir),
            "music_dir": str(self.music_dir),
            "audio_dir": str(self.audio_dir),
            "waveform_dir": str(self.waveform_dir),
            "export_dir": str(self.export_dir),
            "logs_dir": str(self.logs_dir),
        }


@dataclass(slots=True)
class ProjectStatistics:
    total_scenes: int = 0
    processed_scenes: int = 0
    failed_scenes: int = 0
    generated_tracks: int = 0
    exported_files: int = 0
    total_duration_seconds: float = 0.0
    processing_time_seconds: float = 0.0

    @property
    def progress_percentage(self) -> float:
        if self.total_scenes == 0:
            return 0.0
        return round(
            (self.processed_scenes / self.total_scenes) * 100,
            2,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_scenes": self.total_scenes,
            "processed_scenes": self.processed_scenes,
            "failed_scenes": self.failed_scenes,
            "generated_tracks": self.generated_tracks,
            "exported_files": self.exported_files,
            "total_duration_seconds": self.total_duration_seconds,
            "processing_time_seconds": self.processing_time_seconds,
            "progress_percentage": self.progress_percentage,
        }
      """
MystoriumX AI Studio
Model: Project
Part 2/3
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from models.audio import AudioAsset
from models.scene import SceneModel


@dataclass(slots=True)
class ExportArtifact:
    file_name: str
    file_path: str
    mime_type: str
    size_bytes: int
    created_at: datetime
    checksum: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_name": self.file_name,
            "file_path": self.file_path,
            "mime_type": self.mime_type,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at.isoformat(),
            "checksum": self.checksum,
        }


@dataclass(slots=True)
class ProjectConfiguration:
    target_sample_rate: int = 48000
    target_bit_depth: int = 24
    target_lufs: float = -14.0
    enable_mastering: bool = True
    enable_waveform: bool = True
    enable_scene_analysis: bool = True
    enable_prompt_enhancement: bool = True
    enable_music_generation: bool = True
    enable_export: bool = True
    output_format: str = "wav"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_sample_rate": self.target_sample_rate,
            "target_bit_depth": self.target_bit_depth,
            "target_lufs": self.target_lufs,
            "enable_mastering": self.enable_mastering,
            "enable_waveform": self.enable_waveform,
            "enable_scene_analysis": self.enable_scene_analysis,
            "enable_prompt_enhancement": self.enable_prompt_enhancement,
            "enable_music_generation": self.enable_music_generation,
            "enable_export": self.enable_export,
            "output_format": self.output_format,
        }


@dataclass(slots=True)
class ProjectModel:
    metadata: ProjectMetadata
    paths: ProjectPaths
    configuration: ProjectConfiguration = field(
        default_factory=ProjectConfiguration
    )
    statistics: ProjectStatistics = field(
        default_factory=ProjectStatistics
    )

    scenes: List[SceneModel] = field(default_factory=list)
    audio_assets: List[AudioAsset] = field(default_factory=list)
    exports: List[ExportArtifact] = field(default_factory=list)

    status: ProjectStatus = ProjectStatus.CREATED
    export_status: ExportStatus = ExportStatus.PENDING

    active_scene_id: Optional[str] = None
    active_audio_id: Optional[str] = None

    error_message: Optional[str] = None

    tags: List[str] = field(default_factory=list)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_scene(self, scene: SceneModel) -> None:
        self.scenes.append(scene)
        self.statistics.total_scenes = len(self.scenes)
        self.updated_at = datetime.utcnow()

    def add_audio(self, asset: AudioAsset) -> None:
        self.audio_assets.append(asset)
        self.updated_at = datetime.utcnow()

    def add_export(self, artifact: ExportArtifact) -> None:
        self.exports.append(artifact)
        self.statistics.exported_files = len(self.exports)
        self.updated_at = datetime.utcnow()
      """
MystoriumX AI Studio
Model: Project
Part 3/3
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from models.audio import AudioAsset
from models.scene import SceneModel


class ProjectModel(ProjectModel):
    @property
    def total_audio_assets(self) -> int:
        return len(self.audio_assets)

    @property
    def total_exports(self) -> int:
        return len(self.exports)

    @property
    def is_completed(self) -> bool:
        return self.status == ProjectStatus.COMPLETED

    @property
    def has_failed(self) -> bool:
        return self.status == ProjectStatus.FAILED

    def get_scene(self, scene_id: str) -> Optional[SceneModel]:
        return next(
            (scene for scene in self.scenes if scene.scene_id == scene_id),
            None,
        )

    def get_audio_asset(self, asset_id: str) -> Optional[AudioAsset]:
        return next(
            (
                asset
                for asset in self.audio_assets
                if asset.asset_id == asset_id
            ),
            None,
        )

    def mark_completed(self) -> None:
        self.status = ProjectStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def mark_failed(self, message: str) -> None:
        self.status = ProjectStatus.FAILED
        self.error_message = message
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "paths": self.paths.to_dict(),
            "configuration": self.configuration.to_dict(),
            "statistics": self.statistics.to_dict(),
            "status": self.status.value,
            "export_status": self.export_status.value,
            "active_scene_id": self.active_scene_id,
            "active_audio_id": self.active_audio_id,
            "error_message": self.error_message,
            "tags": self.tags,
            "updated_at": self.updated_at.isoformat(),
            "scenes": [
                scene.to_dict()
                for scene in self.scenes
            ],
            "audio_assets": [
                asset.to_dict()
                for asset in self.audio_assets
            ],
            "exports": [
                export.to_dict()
                for export in self.exports
            ],
        }
