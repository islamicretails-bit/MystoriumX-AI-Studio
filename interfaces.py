# ============================================================
# MystoriumX AI Studio
# Domain Layer - Abstract Interfaces
#
# File:
# app/domain/interfaces.py
#
# Responsibility:
# Define contracts between layers.
#
# Clean Architecture:
# Domain controls the rules.
# Infrastructure implements them.
#
# ============================================================


from __future__ import annotations


from abc import ABC, abstractmethod


from pathlib import Path

from typing import List, Dict, Any, Optional



# ============================================================
# Scene Analyzer Interface
# ============================================================

class SceneAnalyzerInterface(ABC):
    """
    Contract for computer vision scene analysis.
    """



    @abstractmethod
    def analyze_video(
        self,
        video_path: Path
    ) -> List[Any]:
        """
        Analyze video scenes.
        """

        pass



# ============================================================
# Audio Analyzer Interface
# ============================================================

class AudioAnalyzerInterface(ABC):
    """
    Contract for audio intelligence.
    """



    @abstractmethod
    def analyze_audio(
        self,
        audio_path: Path
    ) -> Dict[str, Any]:
        """
        Extract audio features.
        """

        pass



# ============================================================
# Music Generation Interface
# ============================================================

class MusicGeneratorInterface(ABC):
    """
    Contract for AI music providers.
    """



    @abstractmethod
    def generate_music(
        self,
        prompt: str,
        duration: int
    ) -> Path:
        """
        Generate cinematic soundtrack.
        """

        pass



# ============================================================
# Prompt Enhancement Interface
# ============================================================

class PromptEnhancerInterface(ABC):
    """
    Contract for AI prompt optimization.
    """



    @abstractmethod
    def enhance_prompt(
        self,
        prompt: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Improve music generation prompt.
        """

        pass



# ============================================================
# Audio Processing Interface
# ============================================================

class AudioProcessorInterface(ABC):
    """
    Contract for DSP processing.
    """



    @abstractmethod
    def process(
        self,
        audio_file: Path
    ) -> Path:
        """
        Process and enhance audio.
        """

        pass



# ============================================================
# Storage Interface
# ============================================================

class StorageInterface(ABC):
    """
    Contract for storage providers.
    """



    @abstractmethod
    def save_file(
        self,
        source: Path,
        destination: Path
    ) -> Path:
        """
        Save file.
        """

        pass



    @abstractmethod
    def delete_file(
        self,
        file_path: Path
    ) -> bool:
        """
        Delete file.
        """

        pass



# ============================================================
# Export Interface
# ============================================================

class ExportInterface(ABC):
    """
    Contract for final export system.
    """



    @abstractmethod
    def export(
        self,
        files: List[Path],
        output: Path
    ) -> Path:
        """
        Export final package.
        """

        pass



# ============================================================
# Model Provider Interface
# ============================================================

class ModelProviderInterface(ABC):
    """
    Contract for AI model loading.
    """



    @abstractmethod
    def load_model(
        self
    ) -> Any:
        """
        Load AI model.
        """

        pass



    @abstractmethod
    def unload_model(
        self
    ) -> None:
        """
        Release model resources.
        """

        pass



# ============================================================
# Pipeline Orchestrator Interface
# ============================================================

class PipelineInterface(ABC):
    """
    Contract for complete AI workflow.
    """



    @abstractmethod
    def execute(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Run complete pipeline.
        """

        pass
