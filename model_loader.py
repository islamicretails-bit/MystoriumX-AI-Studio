# ============================================================
# MystoriumX AI Studio
# Machine Learning Layer - Model Loader
#
# File:
# app/infrastructure/ml/model_loader.py
#
# Responsibility:
# Central AI model loading and resource management.
#
# Features:
# - PyTorch device detection
# - HuggingFace model loading
# - Model caching
# - Memory management
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from typing import Any, Dict, Optional


import logging


import torch



from transformers import (

    AutoProcessor,

    AutoModel,

)



from app.core.exceptions import (

    ModelLoadingError

)



logger = logging.getLogger(

    "MystoriumX.ModelLoader"

)



# ============================================================
# Model Loader
# ============================================================

class ModelLoader:
    """
    Production AI model manager.

    Handles:

    - Loading models
    - Device allocation
    - Cache management
    - Resource cleanup

    """



    def __init__(
        self
    ) -> None:


        self.device = self._detect_device()


        self.models: Dict[str, Any] = {}


        self.processors: Dict[str, Any] = {}



        logger.info(

            f"AI Device: {self.device}"

        )



    # ========================================================
    # Detect Device
    # ========================================================

    def _detect_device(
        self
    ) -> str:

        """
        Detect available hardware.
        """


        if torch.cuda.is_available():

            return "cuda"



        if hasattr(

            torch.backends,

            "mps"

        ) and torch.backends.mps.is_available():

            return "mps"



        return "cpu"



    # ========================================================
    # Load HuggingFace Model
    # ========================================================

    def load_transformer_model(
        self,
        model_name: str
    ) -> Any:

        """
        Load HuggingFace transformer model.
        """


        if model_name in self.models:


            logger.info(

                f"Using cached model: {model_name}"

            )


            return self.models[model_name]



        try:


            logger.info(

                f"Loading model: {model_name}"

            )


            processor = AutoProcessor.from_pretrained(

                model_name

            )


            model = AutoModel.from_pretrained(

                model_name

            )


            model.to(

                self.device

            )


            model.eval()



            self.models[model_name] = model


            self.processors[model_name] = processor



            logger.info(

                "Model loaded successfully"

            )


            return model



        except Exception as error:


            logger.exception(

                "Model loading failed"

            )


            raise ModelLoadingError(

                str(error),

                "MODEL_LOAD_FAILED"

            )



    # ========================================================
    # Get Processor
    # ========================================================

    def get_processor(
        self,
        model_name: str
    ) -> Optional[Any]:

        """
        Return model processor.
        """


        return self.processors.get(

            model_name

        )



    # ========================================================
    # Get Model
    # ========================================================

    def get_model(
        self,
        model_name: str
    ) -> Optional[Any]:

        """
        Return loaded model.
        """


        return self.models.get(

            model_name

        )



    # ========================================================
    # Check Model Loaded
    # ========================================================

    def is_loaded(
        self,
        model_name: str
    ) -> bool:

        """
        Check model availability.
        """


        return (

            model_name

            in

            self.models

        )



    # ========================================================
    # Remove Model
    # ========================================================

    def unload_model(
        self,
        model_name: str
    ) -> bool:

        """
        Remove model from memory.
        """


        if model_name not in self.models:

            return False



        del self.models[model_name]


        if model_name in self.processors:

            del self.processors[model_name]



        self.clear_memory()



        logger.info(

            f"Model unloaded: {model_name}"

        )


        return True



    # ========================================================
    # Clear Memory
    # ========================================================

    def clear_memory(
        self
    ) -> None:

        """
        Release GPU memory.
        """


        if torch.cuda.is_available():

            torch.cuda.empty_cache()



    # ========================================================
    # System Information
    # ========================================================

    def get_system_info(
        self
    ) -> dict:

        """
        Return AI environment details.
        """


        return {


            "device":

                self.device,


            "cuda_available":

                torch.cuda.is_available(),


            "loaded_models":

                list(

                    self.models.keys()

                )

        }



# ============================================================
# Global Instance
# ============================================================

model_loader = ModelLoader()
