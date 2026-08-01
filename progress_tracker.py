# ============================================================
# MystoriumX AI Studio
# UI Component - Progress Tracker
#
# File:
# app/ui/components/progress_tracker.py
#
# Responsibility:
# Display AI pipeline progress in Streamlit.
#
# Features:
# - Live progress bar
# - Processing stage display
# - Status updates
# - Pipeline tracking
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from typing import Dict, List


import logging


import streamlit as st



logger = logging.getLogger(

    "MystoriumX.ProgressTracker"

)



# ============================================================
# Progress Tracker
# ============================================================

class ProgressTracker:
    """
    Professional Streamlit progress controller.

    Used by:

    - Pipeline Orchestrator
    - AI Generation Workflow
    - Processing Dashboard

    """



    def __init__(

        self

    ) -> None:


        self.stages: List[str] = [

            "Initialization",

            "Scene Detection",

            "Prompt Generation",

            "Music Generation",

            "Audio Mastering",

            "Final Export"

        ]



        self.progress_value = 0.0


        self.current_stage = "Waiting"



        logger.info(

            "Progress Tracker initialized"

        )



    # ========================================================
    # Create UI
    # ========================================================

    def create(

        self

    ) -> Dict[str, object]:

        """
        Create Streamlit progress elements.
        """


        st.subheader(

            "🎬 AI Pipeline Progress"

        )



        status = st.empty()


        progress = st.progress(

            0

        )


        stage_box = st.empty()



        self.elements = {


            "status":

                status,


            "progress":

                progress,


            "stage":

                stage_box

        }



        return self.elements



    # ========================================================
    # Update Progress
    # ========================================================

    def update(

        self,

        stage: str,

        percentage: float

    ) -> None:

        """
        Update pipeline progress.
        """


        try:


            if not hasattr(

                self,

                "elements"

            ):

                self.create()



            percentage = max(

                0,

                min(

                    percentage,

                    1

                )

            )



            self.progress_value = percentage


            self.current_stage = stage



            self.elements["progress"].progress(

                percentage

            )



            self.elements["stage"].markdown(

                f"### Current Stage: {stage}"

            )



            self.elements["status"].info(

                f"Processing {percentage * 100:.0f}% complete"

            )



            logger.info(

                f"{stage}: {percentage}"

            )



        except Exception as error:


            logger.exception(

                "Progress update failed"

            )



    # ========================================================
    # Complete
    # ========================================================

    def complete(

        self

    ) -> None:

        """
        Mark pipeline completed.
        """


        self.update(

            "Completed",

            1.0

        )



        self.elements["status"].success(

            "AI Documentary Pipeline Completed Successfully"

        )



    # ========================================================
    # Error State
    # ========================================================

    def error(

        self,

        message: str

    ) -> None:

        """
        Display pipeline error.
        """


        if not hasattr(

            self,

            "elements"

        ):

            self.create()



        self.elements["status"].error(

            message

        )



        logger.error(

            message

        )



    # ========================================================
    # Reset
    # ========================================================

    def reset(

        self

    ) -> None:

        """
        Reset progress tracker.
        """


        self.progress_value = 0.0


        self.current_stage = "Waiting"



        if hasattr(

            self,

            "elements"

        ):


            self.elements["progress"].progress(

                0

            )


            self.elements["stage"].markdown(

                "### Current Stage: Waiting"

            )



# ============================================================
# Global Instance
# ============================================================

progress_tracker = ProgressTracker()
