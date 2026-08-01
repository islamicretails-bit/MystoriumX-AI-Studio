# ============================================================
# MystoriumX AI Studio
# Storage Layer - Local Storage Manager
#
# File:
# app/storage/local_storage.py
#
# Responsibility:
# Manage project files, uploads, generated assets,
# temporary data and exported results.
#
# Features:
# - Project folder creation
# - File saving
# - File retrieval
# - Temporary storage
# - Export management
#
# ============================================================


from __future__ import annotations


from pathlib import Path
from typing import Optional, List
import shutil
import logging
import uuid



logger = logging.getLogger(
    "MystoriumX.LocalStorage"
)



# ============================================================
# Storage Manager
# ============================================================

class LocalStorage:
    """
    Local file storage management system.

    Directory Structure:

    storage/

        projects/

            project_id/

                uploads/

                processing/

                outputs/

                metadata/


    """



    def __init__(
        self,
        base_directory: str = "storage"
    ) -> None:


        self.base_path = Path(
            base_directory
        )


        self.projects_path = (
            self.base_path
            /
            "projects"
        )


        self.temp_path = (
            self.base_path
            /
            "temp"
        )


        self._initialize_storage()



        logger.info(
            "Local Storage initialized"
        )



    # ========================================================
    # Initialize Storage
    # ========================================================

    def _initialize_storage(
        self
    ) -> None:

        """
        Create required directories.
        """


        self.projects_path.mkdir(

            parents=True,

            exist_ok=True

        )


        self.temp_path.mkdir(

            parents=True,

            exist_ok=True

        )



    # ========================================================
    # Create Project
    # ========================================================

    def create_project(
        self,
        project_name: str
    ) -> str:

        """
        Create new project workspace.

        Returns:
            Unique project id.
        """


        project_id = (

            f"{project_name}_"

            f"{uuid.uuid4().hex[:8]}"

        )



        project_path = (

            self.projects_path

            /

            project_id

        )



        folders = [

            "uploads",

            "processing",

            "outputs",

            "metadata"

        ]


        for folder in folders:

            (

                project_path

                /

                folder

            ).mkdir(

                parents=True,

                exist_ok=True

            )



        logger.info(

            f"Project created: {project_id}"

        )


        return project_id



    # ========================================================
    # Get Project Path
    # ========================================================

    def get_project_path(
        self,
        project_id: str
    ) -> Path:

        """
        Return project directory.
        """


        path = (

            self.projects_path

            /

            project_id

        )


        if not path.exists():

            raise FileNotFoundError(

                "Project does not exist."

            )


        return path



    # ========================================================
    # Save Uploaded File
    # ========================================================

    def save_upload(
        self,
        project_id: str,
        file_path: Path
    ) -> Path:

        """
        Save uploaded media file.
        """


        project_path = (

            self.get_project_path(

                project_id

            )

        )


        upload_directory = (

            project_path

            /

            "uploads"

        )


        destination = (

            upload_directory

            /

            file_path.name

        )


        shutil.copy(

            file_path,

            destination

        )


        logger.info(

            f"File saved: {destination}"

        )


        return destination



    # ========================================================
    # Save Generated Output
    # ========================================================

    def save_output(
        self,
        project_id: str,
        output_file: Path
    ) -> Path:

        """
        Save final generated audio/video.
        """


        project_path = (

            self.get_project_path(

                project_id

            )

        )


        output_directory = (

            project_path

            /

            "outputs"

        )


        destination = (

            output_directory

            /

            output_file.name

        )


        shutil.copy(

            output_file,

            destination

        )


        return destination



    # ========================================================
    # Temporary File
    # ========================================================

    def create_temp_file(
        self,
        filename: str
    ) -> Path:

        """
        Create temporary workspace file.
        """


        temp_file = (

            self.temp_path

            /

            filename

        )


        return temp_file



    # ========================================================
    # List Project Files
    # ========================================================

    def list_project_files(
        self,
        project_id: str
    ) -> List[Path]:

        """
        Return all project files.
        """


        project_path = (

            self.get_project_path(

                project_id

            )

        )


        return [

            file

            for file in project_path.rglob("*")

            if file.is_file()

        ]



    # ========================================================
    # Delete Project
    # ========================================================

    def delete_project(
        self,
        project_id: str
    ) -> bool:

        """
        Remove complete project.
        """


        project_path = (

            self.projects_path

            /

            project_id

        )


        if not project_path.exists():

            return False



        shutil.rmtree(

            project_path

        )


        logger.info(

            f"Deleted project: {project_id}"

        )


        return True
