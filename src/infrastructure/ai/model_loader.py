"""
MystoriumX AI Studio

AI Model Loader Engine

Responsible for:
- Loading AI models
- Managing model lifecycle
- Providing model instances
- Tracking model status

Architecture:
Clean Architecture
SOLID Principles

Python:
3.11+
"""

from __future__ import annotations

import logging

from dataclasses import dataclass, field

from pathlib import Path

from typing import Any, Dict, Optional, Protocol



# ============================================================
# Exceptions
# ============================================================


class ModelLoaderError(Exception):
    """
    Base model loader exception.
    """



class ModelLoadError(ModelLoaderError):
    """
    Raised when model loading fails.
    """



# ============================================================
# Model Backend Contract
# ============================================================


class ModelBackendProtocol(Protocol):
    """
    AI model backend contract.

    Implementations:
    - PyTorch
    - TensorFlow
    - Transformers
    - Local AI models
    """

    def load(
        self,
        model_path: Path,
        settings: Dict[str, Any],
    ) -> Any:
        ...



    def unload(
        self,
        model: Any,
    ) -> None:
        ...



# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class ModelLoaderConfig:
    """
    Model loading configuration.
    """

    models_directory: Path

    device: str = "auto"

    cache_enabled: bool = True

    preload: bool = False



# ============================================================
# Model Registry Entry
# ============================================================


@dataclass(slots=True)
class ModelEntry:
    """
    Loaded model information.
    """

    name: str

    path: Path

    instance: Optional[Any] = None

    loaded: bool = False

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Model Loader
# ============================================================


class ModelLoader:
    """
    Production AI model loader.

    Manages all AI models used by
    MystoriumX AI Studio.
    """

    def __init__(
        self,
        backend: ModelBackendProtocol,

        config: ModelLoaderConfig,

        logger: Optional[
            logging.Logger
        ] = None,

    ) -> None:


        self.backend = backend


        self.config = config


        self.logger = (

            logger

            if logger

            else logging.getLogger(
                self.__class__.__name__
            )

        )


        self.registry: Dict[
            str,
            ModelEntry
        ] = {}



    # ========================================================
    # Register Model
    # ========================================================


    def register(
        self,
        name: str,
        model_path: Path,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> None:
        """
        Register AI model.
        """

        if not name:

            raise ModelLoaderError(
                "Model name required"
            )


        self.registry[name] = ModelEntry(

            name=name,

            path=model_path,

            metadata=(
                metadata
                if metadata
                else {}
            ),

        )


        self.logger.info(
            f"Registered model: {name}"
        )
          # ========================================================
    # Load Model
    # ========================================================


    def load(
        self,
        name: str,
    ) -> Any:
        """
        Load registered AI model.
        """

        if name not in self.registry:

            raise ModelLoaderError(
                f"Model not registered: {name}"
            )


        entry = self.registry[name]


        if entry.loaded and entry.instance:

            return entry.instance



        if not entry.path.exists():

            raise ModelLoadError(
                f"Model file not found: {entry.path}"
            )



        self.logger.info(
            f"Loading model: {name}"
        )


        try:

            settings = (
                self._build_settings()
            )


            model = self.backend.load(

                entry.path,

                settings,

            )


            entry.instance = model


            entry.loaded = True


            self.registry[name] = entry



            self.logger.info(
                f"Model loaded: {name}"
            )


            return model



        except Exception as exc:

            self.logger.exception(
                "Model loading failed"
            )


            raise ModelLoadError(

                f"Unable to load model {name}: {exc}"

            ) from exc



    # ========================================================
    # Unload Model
    # ========================================================


    def unload(
        self,
        name: str,
    ) -> None:
        """
        Release model resources.
        """

        if name not in self.registry:

            raise ModelLoaderError(
                f"Unknown model: {name}"
            )


        entry = self.registry[name]


        if not entry.loaded:

            return



        try:

            self.backend.unload(
                entry.instance
            )


            entry.instance = None


            entry.loaded = False


            self.registry[name] = entry



            self.logger.info(
                f"Model unloaded: {name}"
            )



        except Exception as exc:

            raise ModelLoaderError(

                f"Unable to unload model: {exc}"

            ) from exc



    # ========================================================
    # Get Model
    # ========================================================


    def get_model(
        self,
        name: str,
    ) -> Any:
        """
        Return loaded model instance.
        """

        if name not in self.registry:

            raise ModelLoaderError(
                f"Model not registered: {name}"
            )


        entry = self.registry[name]


        if not entry.loaded:

            return self.load(
                name
            )


        return entry.instance



    # ========================================================
    # Settings Builder
    # ========================================================


    def _build_settings(
        self,
    ) -> Dict[str, Any]:
        """
        Build model loading settings.
        """

        return {

            "device":
                self.config.device,


            "cache":
                self.config.cache_enabled,


            "preload":
                self.config.preload,

        }



    # ========================================================
    # Model Validation
    ========================================================


    def validate_model(
        self,
        name: str,
    ) -> bool:
        """
        Validate registered model.
        """

        if name not in self.registry:

            return False


        entry = self.registry[name]


        return entry.path.exists()
          # ========================================================
    # Registry Information
    # ========================================================


    def list_models(
        self,
    ) -> Dict[str, Any]:
        """
        Return registered model information.
        """

        models = {}


        for name, entry in self.registry.items():

            models[name] = {

                "path":
                    str(entry.path),


                "loaded":
                    entry.loaded,


                "metadata":
                    entry.metadata,

            }


        return models



    # ========================================================
    # Loaded Models
    # ========================================================


    def get_loaded_models(
        self,
    ) -> list[str]:
        """
        Return currently loaded models.
        """

        return [

            name

            for name, entry
            in self.registry.items()

            if entry.loaded

        ]



    # ========================================================
    # Configuration
    ========================================================


    def get_configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return loader configuration.
        """

        return {

            "models_directory":
                str(
                    self.config.models_directory
                ),


            "device":
                self.config.device,


            "cache_enabled":
                self.config.cache_enabled,


            "preload":
                self.config.preload,

        }



    # ========================================================
    # Cleanup
    # ========================================================


    def unload_all(
        self,
    ) -> None:
        """
        Release all loaded models.
        """

        for name in list(
            self.registry.keys()
        ):

            if self.registry[name].loaded:

                self.unload(
                    name
                )



    # ========================================================
    # Diagnostics
    # ========================================================


    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Return model loader health.
        """

        return {

            "service":
                "ModelLoader",


            "status":
                "healthy",


            "registered_models":
                len(
                    self.registry
                ),


            "loaded_models":
                len(
                    self.get_loaded_models()
                ),

        }



    # ========================================================
    # Information
    # ========================================================


    def get_information(
        self,
    ) -> Dict[str, Any]:
        """
        Return service information.
        """

        return {

            "service":
                "AI Model Loader",


            "purpose":
                "Manage AI model lifecycle",


            "pipeline_stage":
                "AI Infrastructure",

        }



    # ========================================================
    # Auto Preload
    # ========================================================


    def preload_models(
        self,
    ) -> None:
        """
        Load all registered models
        when preload is enabled.
        """

        if not self.config.preload:

            return


        for name in self.registry:

            self.load(
                name
            )
