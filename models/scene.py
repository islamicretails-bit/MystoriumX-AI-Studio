"""
MystoriumX AI Studio
Model: Scene
Part 1/3
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class SceneType(str, Enum):
    UNKNOWN = "unknown"
    INTRO = "intro"
    DIALOGUE = "dialogue"
    INTERVIEW = "interview"
    ACTION = "action"
    DRONE = "drone"
    BROLL = "broll"
    TIMELAPSE = "timelapse"
    ARCHIVE = "archive"
    CINEMATIC = "cinematic"
    OUTRO = "outro"


class SceneMood(str, Enum):
    UNKNOWN = "unknown"
    DARK = "dark"
    TENSE = "tense"
    MYSTERIOUS = "mysterious"
    EMOTIONAL = "emotional"
    EPIC = "epic"
    CALM = "calm"
    DRAMATIC = "dramatic"
    HOPEFUL = "hopeful"
    SUSPENSE = "suspense"


class SceneStatus(str, Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    READY = "ready"
    FAILED = "failed"


@dataclass(slots=True)
class Timestamp:
    start_seconds: float
    end_seconds: float

    @property
    def duration(self) -> float:
        return max(0.0, self.end_seconds - self.start_seconds)

    def to_dict(self) -> Dict[str, float]:
        return {
            "start_seconds": self.start_seconds,
            "end_seconds": self.end_seconds,
            "duration": self.duration,
        }


@dataclass(slots=True)
class SceneFrames:
    keyframe_path: Path
    thumbnail_path: Optional[Path] = None
    extracted_frames: List[Path] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "keyframe_path": str(self.keyframe_path),
            "thumbnail_path": (
                str(self.thumbnail_path)
                if self.thumbnail_path
                else None
            ),
            "extracted_frames": [
                str(frame)
                for frame in self.extracted_frames
            ],
        }


@dataclass(slots=True)
class VisualAnalysis:
    caption: str
    objects: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    emotions: List[str] = field(default_factory=list)
    colors: List[str] = field(default_factory=list)
    lighting: Optional[str] = None
    weather: Optional[str] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "caption": self.caption,
            "objects": self.objects,
            "locations": self.locations,
            "emotions": self.emotions,
            "colors": self.colors,
            "lighting": self.lighting,
            "weather": self.weather,
            "confidence": self.confidence,
        }


@dataclass(slots=True)
class ScenePrompt:
    original_prompt: str
    enhanced_prompt: str
    music_prompt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_prompt": self.original_prompt,
            "enhanced_prompt": self.enhanced_prompt,
            "music_prompt": self.music_prompt,
        }
