# ============================================================
# MystoriumX AI Studio
# UI Component - Audio Player
#
# File:
# app/ui/components/audio_player.py
#
# Responsibility:
# Professional Streamlit audio playback component.
#
# Features:
# - Audio preview
# - Metadata display
# - Download support
# - Multiple format handling
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from pathlib import Path

from typing import Dict, Any, Optional


import logging



import streamlit as st



logger = logging.getLogger(

    "MystoriumX.AudioPlayer"

)



# ============================================================
# Audio Player Component
# ============================================================

class AudioPlayer:
    """
    Streamlit audio playback component.

    Used for:

    - Generated music preview
    - Mastered soundtrack review
    - Final export listening

    """



    def __init__(

        self

    ) -> None:


        logger.info(

            "Audio Player initialized"

        )



    # ========================================================
    # Render Audio Player
    # ========================================================

    def render(

        self,

        audio_file: Path,

        title: str = "Generated Soundtrack"

    ) -> None:

        """
        Display audio player.
        """


        if not audio_file.exists():


            st.warning(

                "Audio file not available"

            )


            return



        try:


            st.subheader(

                f"🎵 {title}"

            )



            with open(

                audio_file,

                "rb"

            ) as file:


                audio_bytes = file.read()



            st.audio(

                audio_bytes

            )



            self._download_button(

                audio_bytes,

                audio_file.name

            )



            logger.info(

                f"Playing audio: {audio_file}"

            )



        except Exception as error:


            logger.exception(

                "Audio player failed"

            )


            st.error(

                str(error)

            )



    # ========================================================
    # Download Button
    # ========================================================

    def _download_button(

        self,

        audio_bytes: bytes,

        filename: str

    ) -> None:

        """
        Create download button.
        """


        st.download_button(

            label="⬇️ Download Audio",

            data=audio_bytes,

            file_name=filename,

            mime=self._detect_mime(

                filename

            )

        )



    # ========================================================
    # Detect MIME
    # ========================================================

    def _detect_mime(

        self,

        filename: str

    ) -> str:

        """
        Detect audio MIME type.
        """


        extension = (

            Path(filename)

            .suffix

            .lower()

        )



        mime_types = {


            ".wav":

                "audio/wav",


            ".mp3":

                "audio/mpeg",


            ".m4a":

                "audio/mp4",


            ".ogg":

                "audio/ogg"

        }



        return mime_types.get(

            extension,

            "audio/wav"

        )



    # ========================================================
    # Audio Information Card
    # ========================================================

    def show_metadata(

        self,

        metadata: Dict[str, Any]

    ) -> None:

        """
        Display audio analytics.
        """


        st.markdown(

            "### 🎧 Audio Analytics"

        )



        columns = st.columns(

            3

        )



        items = list(

            metadata.items()

        )



        for index, item in enumerate(items):


            key, value = item



            columns[

                index % 3

            ].metric(

                key.replace(

                    "_",

                    " "

                ).title(),

                value

            )



    # ========================================================
    # Compare Audio Versions
    # ========================================================

    def compare(

        self,

        original: Optional[Path],

        mastered: Optional[Path]

    ) -> None:

        """
        Compare original and mastered audio.
        """


        st.subheader(

            "🎚️ Audio Comparison"

        )



        col1, col2 = st.columns(

            2

        )



        with col1:


            st.write(

                "Original Audio"

            )


            if original and original.exists():


                st.audio(

                    str(original)

                )



        with col2:


            st.write(

                "Mastered Audio"

            )


            if mastered and mastered.exists():


                st.audio(

                    str(mastered)

                )



# ============================================================
# Global Instance
# ============================================================

audio_player = AudioPlayer()
