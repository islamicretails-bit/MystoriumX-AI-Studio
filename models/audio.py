# File Name: models/audio.py
# Part 1/3

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class AudioFormat(str, Enum):
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    AAC = "aac"
    OGG = "ogg"


class AudioChannelMode(str, Enum):
    MONO = "mono"
    STEREO = "stereo"


class AudioStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class LoudnessMetrics:
    integrated_lufs: float
    loudness_range: float
    true_peak_dbtp: float
    sample_peak_dbfs: float
    rms_db: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "integrated_lufs": self.integrated_lufs,
            "loudness_range": self.loudness_range,
            "true_peak_dbtp": self.true_peak_dbtp,
            "sample_peak_dbfs": self.sample_peak_dbfs,
            "rms_db": self.rms_db,
        }


@dataclass(slots=True)
class EqualizerSettings:
    low_gain_db: float = 0.0
    mid_gain_db: float = 0.0
    high_gain_db: float = 0.0
    low_cut_hz: float = 20.0
    high_cut_hz: float = 20000.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "low_gain_db": self.low_gain_db,
            "mid_gain_db": self.mid_gain_db,
            "high_gain_db": self.high_gain_db,
            "low_cut_hz": self.low_cut_hz,
            "high_cut_hz": self.high_cut_hz,
        }


@dataclass(slots=True)
class CompressorSettings:
    threshold_db: float = -18.0
    ratio: float = 3.0
    attack_ms: float = 20.0
    release_ms: float = 150.0
    makeup_gain_db: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "threshold_db": self.threshold_db,
            "ratio": self.ratio,
            "attack_ms": self.attack_ms,
            "release_ms": self.release_ms,
            "makeup_gain_db": self.makeup_gain_db,
        }


@dataclass(slots=True)
class LimiterSettings:
    ceiling_db: float = -1.0
    release_ms: float = 100.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "ceiling_db": self.ceiling_db,
            "release_ms": self.release_ms,
        }


@dataclass(slots=True)
class MasteringProfile:
    target_lufs: float = -14.0
    normalize: bool = True
    equalizer: EqualizerSettings = field(default_factory=EqualizerSettings)
    compressor: CompressorSettings = field(default_factory=CompressorSettings)
    limiter: LimiterSettings = field(default_factory=LimiterSettings)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_lufs": self.target_lufs,
            "normalize": self.normalize,
            "equalizer": self.equalizer.to_dict(),
            "compressor": self.compressor.to_dict(),
            "limiter": self.limiter.to_dict(),
        }


@dataclass(slots=True)
class AudioMetadata:
    title: str
    created_at: datetime
    duration_seconds: float
    sample_rate: int
    bit_depth: int
    channels: AudioChannelMode
    format: AudioFormat
    codec: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "duration_seconds": self.duration_seconds,
            "sample_rate": self.sample_rate,
            "bit_depth": self.bit_depth,
            "channels": self.channels.value,
            "format": self.format.value,
            "codec": self.codec,
        }
      # File Name: models/audio.py
# Part 2/3

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class AudioAnalysis:
    tempo_bpm: float
    key: Optional[str]
    dynamic_range: float
    spectral_centroid: float
    zero_crossing_rate: float
    silence_ratio: float
    loudness: LoudnessMetrics

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tempo_bpm": self.tempo_bpm,
            "key": self.key,
            "dynamic_range": self.dynamic_range,
            "spectral_centroid": self.spectral_centroid,
            "zero_crossing_rate": self.zero_crossing_rate,
            "silence_ratio": self.silence_ratio,
            "loudness": self.loudness.to_dict(),
        }


@dataclass(slots=True)
class AudioEffects:
    reverb: bool = False
    stereo_widening: bool = False
    voice_ducking: bool = False
    deesser: bool = False
    denoise: bool = False
    limiter: bool = True

    def to_dict(self) -> Dict[str, bool]:
        return {
            "reverb": self.reverb,
            "stereo_widening": self.stereo_widening,
            "voice_ducking": self.voice_ducking,
            "deesser": self.deesser,
            "denoise": self.denoise,
            "limiter": self.limiter,
        }


@dataclass(slots=True)
class WaveformData:
    peaks: List[float]
    rms: List[float]
    image_path: Optional[Path] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "peaks": self.peaks,
            "rms": self.rms,
            "image_path": str(self.image_path) if self.image_path else None,
        }


@dataclass(slots=True)
class AudioAsset:
    asset_id: str
    source_file: Path
    output_file: Optional[Path]
    metadata: AudioMetadata
    analysis: Optional[AudioAnalysis] = None
    mastering: MasteringProfile = field(default_factory=MasteringProfile)
    effects: AudioEffects = field(default_factory=AudioEffects)
    waveform: Optional[WaveformData] = None
    tags: List[str] = field(default_factory=list)
    status: AudioStatus = AudioStatus.PENDING
    error_message: Optional[str] = None

    @property
    def is_processed(self) -> bool:
        return self.status == AudioStatus.COMPLETED

    @property
    def duration(self) -> float:
        return self.metadata.duration_seconds

    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "source_file": str(self.source_file),
            "output_file": str(self.output_file) if self.output_file else None,
            "metadata": self.metadata.to_dict(),
            "analysis": self.analysis.to_dict() if self.analysis else None,
            "mastering": self.mastering.to_dict(),
            "effects": self.effects.to_dict(),
            "waveform": self.waveform.to_dict() if self.waveform else None,
            "tags": self.tags,
            "status": self.status.value,
            "error_message": self.error_message,
        }
      # File Name: models/audio.py
# Part 3/3

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(slots=True)
class AudioBatch:
    project_id: str
    assets: List[AudioAsset] = field(default_factory=list)

    @property
    def completed(self) -> int:
        return sum(
            asset.status == AudioStatus.COMPLETED
            for asset in self.assets
        )

    @property
    def failed(self) -> int:
        return sum(
            asset.status == AudioStatus.FAILED
            for asset in self.assets
        )

    @property
    def processing(self) -> int:
        return sum(
            asset.status == AudioStatus.PROCESSING
            for asset in self.assets
        )

    def add(self, asset: AudioAsset) -> None:
        self.assets.append(asset)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "completed": self.completed,
            "failed": self.failed,
            "processing": self.processing,
            "total": len(self.assets),
            "assets": [
                asset.to_dict()
                for asset in self.assets
            ],
        }
