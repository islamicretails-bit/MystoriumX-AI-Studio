# ============================================================
# MystoriumX AI Studio
# UI Component - Upload Zone
#
# File:
# app/ui/components/upload_zone.py
#
# Responsibility:
# Professional Streamlit upload components.
#
# Features:
# - Video upload
# - Script upload
# - Narration upload
# - File validation
# - Temporary storage handling
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path

from typing import Optional, List


import tempfile

import logging



import streamlit as st



logger = logging.getLogger(

    "MystoriumX.UploadZone"

)



# ============================================================
# Upload Zone Component
# ============================================================

class UploadZone:
    """
    Reusable Streamlit upload component.

    Handles all project file uploads.
    """



    def __init__(

        self,

        storage_folder: str = "uploads"

    ) -> None:


        self.storage_folder = Path(

            storage_folder

        )


        self.storage_folder.mkdir(

            parents=True,

            exist_ok=True

        )


        logger.info(

            "Upload Zone initialized"

        )



    # ========================================================
    # Video Upload
    # ========================================================

    def video_upload(

        self

    ) -> Optional[Path]:

        """
        Upload documentary video file.
        """


        uploaded = st.file_uploader(

            "Upload Documentary Video",

            type=[

                "mp4",

                "mov",

                "mkv",

                "avi"

            ],

            key="video_upload"

        )



        if uploaded:


            return self._save_file(

                uploaded

            )



        return None



    # ========================================================
    # Script Upload
    # ========================================================

    def script_upload(

        self

    ) -> Optional[Path]:

        """
        Upload documentary script.
        """


        uploaded = st.file_uploader(

            "Upload Script / Story File",

            type=[

                "txt",

                "pdf",

                "docx"

            ],

            key="script_upload"

        )



        if uploaded:


            return self._save_file(

                uploaded

            )



        return None



    # ========================================================
    # Narration Upload
    # ========================================================

    def narration_upload(

        self

    ) -> Optional[Path]:

        """
        Upload voice narration.
        """


        uploaded = st.file_uploader(

            "Upload Narration / Voiceover",

            type=[

                "mp3",

                "wav",

                "m4a"

            ],

            key="narration_upload"

        )



        if uploaded:


            return self._save_file(

                uploaded

            )



        return None



    # ========================================================
    # Multiple Audio Upload
    # ========================================================

    def audio_files_upload(

        self

    ) -> List[Path]:

        """
        Upload multiple audio files.
        """


        files = st.file_uploader(

            "Upload Audio Files",

            type=[

                "wav",

                "mp3"

            ],

            accept_multiple_files=True,

            key="audio_files"

        )



        saved_files = []



        if files:


            for file in files:


                saved_files.append(

                    self._save_file(

                        file

                    )

                )



        return saved_files



    # ========================================================
    # Save Uploaded File
    # ========================================================

    def _save_file(

        self,

        uploaded_file

    ) -> Path:

        """
        Save uploaded file safely.
        """


        try:


            file_path = (

                self.storage_folder

                /

                uploaded_file.name

            )



            with open(

                file_path,

                "wb"

            ) as buffer:


                buffer.write(

                    uploaded_file.getbuffer()

                )



            logger.info(

                f"File uploaded: {file_path}"

            )



            return file_path



        except Exception as error:


            logger.exception(

                "Upload failed"

            )


            raise error



    # ========================================================
    # File Validation
    # ========================================================

    def validate_file(

        self,

        file_path: Path

    ) -> bool:

        """
        Check uploaded file validity.
        """


        if not file_path.exists():

            return False



        if file_path.stat().st_size == 0:

            return False



        return True



# ============================================================
# Global Instance
# ============================================================

upload_zone = UploadZone()
