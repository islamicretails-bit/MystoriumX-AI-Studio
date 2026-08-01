# ============================================================
# MystoriumX AI Studio
# UI Component - Log Viewer
#
# File:
# app/ui/components/log_viewer.py
#
# Responsibility:
# Display application logs inside Streamlit.
#
# Features:
# - Real-time logs
# - Log levels
# - Debug monitoring
# - Pipeline event tracking
#
# Compatible:
# Python 3.11
#
# ============================================================


from __future__ import annotations


from typing import List, Dict


import logging


from datetime import datetime



import streamlit as st



logger = logging.getLogger(

    "MystoriumX.LogViewer"

)



# ============================================================
# Custom Log Handler
# ============================================================

class StreamlitLogHandler(logging.Handler):
    """
    Capture Python logs for Streamlit display.
    """



    def __init__(

        self

    ) -> None:


        super().__init__()


        self.logs: List[Dict[str, str]] = []



    def emit(

        self,

        record: logging.LogRecord

    ) -> None:

        """
        Store log records.
        """


        self.logs.append(

            {

                "time":

                    datetime.now()

                    .strftime(

                        "%H:%M:%S"

                    ),


                "level":

                    record.levelname,


                "message":

                    record.getMessage()

            }

        )



        # Keep memory controlled

        if len(self.logs) > 500:


            self.logs.pop(0)



# ============================================================
# Log Viewer
# ============================================================

class LogViewer:
    """
    Professional Streamlit log dashboard.

    Used for:

    - AI processing monitoring
    - Debugging
    - Error tracking

    """



    def __init__(

        self

    ) -> None:


        self.handler = StreamlitLogHandler()



        logger.info(

            "Log Viewer initialized"

        )



    # ========================================================
    # Attach Handler
    # ========================================================

    def attach(

        self

    ) -> None:

        """
        Attach handler to application logger.
        """


        root_logger = logging.getLogger()


        if self.handler not in root_logger.handlers:


            root_logger.addHandler(

                self.handler

            )


            root_logger.setLevel(

                logging.INFO

            )



    # ========================================================
    # Render Logs
    # ========================================================

    def render(

        self,

        title: str = "System Logs"

    ) -> None:

        """
        Display logs in Streamlit.
        """


        self.attach()



        st.subheader(

            f"📋 {title}"

        )



        if not self.handler.logs:


            st.info(

                "No logs available"

            )


            return



        for log in reversed(

            self.handler.logs

        ):



            level = log["level"]



            message = (

                f"{log['time']} "

                f"| {level} "

                f"| {log['message']}"

            )



            if level == "ERROR":


                st.error(

                    message

                )



            elif level == "WARNING":


                st.warning(

                    message

                )



            else:


                st.text(

                    message

                )



    # ========================================================
    # Clear Logs
    # ========================================================

    def clear(

        self

    ) -> None:

        """
        Remove stored logs.
        """


        self.handler.logs.clear()



    # ========================================================
    # Export Logs
    # ========================================================

    def export(

        self

    ) -> str:

        """
        Convert logs into text format.
        """


        output = []



        for log in self.handler.logs:


            output.append(

                (

                    f"{log['time']} "

                    f"{log['level']} "

                    f"{log['message']}"

                )

            )



        return "\n".join(

            output

        )



# ============================================================
# Global Instance
# ============================================================

log_viewer = LogViewer()
