# ============================================================
# MystoriumX AI Studio
# UI View - Main Dashboard Tab
#
# File:
# app/ui/views/main_tab.py
#
# Responsibility:
# Primary production dashboard for AI documentary workflow.
#
# Features:
# - Hero dashboard
# - Upload workspace
# - Project configuration
# - Pipeline execution
# - Progress integration
#
# Compatible:
# Python 3.11
# Streamlit Cloud
# ============================================================

from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any

import logging
import streamlit as st

# UI Components
from app.ui.components.upload_zone import upload_zone
from app.ui.components.progress_tracker import progress_tracker
from app.ui.components.audio_player import audio_player

# Services
from app.services.orchestrator import (
    MystoriumXOrchestrator,
    PipelineConfig,
)

logger = logging.getLogger("MystoriumX.MainTab")


# ============================================================
# Main Dashboard View
# ============================================================

class MainTab:
    """
    Primary AI Documentary Production Dashboard.

    Responsibilities:
    - Collect user inputs
    - Configure project
    - Trigger AI pipeline
    - Display processing status
    - Present generated soundtrack
    """

    def __init__(self) -> None:
        self.orchestrator = MystoriumXOrchestrator()
        logger.info("MainTab initialized")

    # ========================================================
    # Public Render Entry
    # ========================================================

    def render(self) -> None:
        """
        Render complete dashboard.
        """

        self._render_hero()
        self._render_workspace_header()

        st.divider()

        # These sections will be implemented in
        # Part 43.2 onwards.
        self._render_upload_section()

        st.divider()

        self._render_prompt_section()

        st.divider()

        self._render_configuration_section()

        st.divider()

        self._render_generate_section()

    # ========================================================
    # Hero Section
    # ========================================================

    def _render_hero(self) -> None:
        """
        Hollywood style dashboard hero.
        """

        st.markdown(
            """
            <div class="glass-card"
                 style="text-align:center; padding:2.5rem;">

                <div class="hero-title">
                    🎬 MystoriumX AI Studio
                </div>

                <div class="hero-subtitle">
                    Hollywood-Grade AI Documentary Audio Intelligence Platform
                </div>

                <div style="color:#94a3b8;
                            font-size:1rem;
                            max-width:760px;
                            margin:0 auto;">

                    Upload documentary footage, analyze scenes with
                    computer vision, generate cinematic AI music,
                    apply professional mastering, and export a
                    production-ready soundtrack.

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # Workspace Header
    # ========================================================

    def _render_workspace_header(self) -> None:
        """
        Dashboard overview cards.
        """

        st.markdown(
            """
            <div style="margin-bottom:1rem;">
                <h2 style="margin-bottom:0.25rem;">
                    🚀 Documentary Production Workspace
                </h2>
                <div style="color:#94a3b8;">
                    End-to-end AI soundtrack generation pipeline
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                """
                <div class="glass-card"
                     style="text-align:center;">

                    <div style="font-size:1.6rem;">🎥</div>
                    <div style="font-weight:700;">
                        Scene AI
                    </div>
                    <div style="color:#94a3b8;
                                font-size:0.85rem;">
                        Computer Vision
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="glass-card"
                     style="text-align:center;">

                    <div style="font-size:1.6rem;">🎼</div>
                    <div style="font-weight:700;">
                        MusicGen
                    </div>
                    <div style="color:#94a3b8;
                                font-size:0.85rem;">
                        AI Soundtrack
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                """
                <div class="glass-card"
                     style="text-align:center;">

                    <div style="font-size:1.6rem;">🎚️</div>
                    <div style="font-weight:700;">
                        Mastering
                    </div>
                    <div style="color:#94a3b8;
                                font-size:0.85rem;">
                        Cinema Ready
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                """
                <div class="glass-card"
                     style="text-align:center;">

                    <div style="font-size:1.6rem;">📦</div>
                    <div style="font-weight:700;">
                        Export
                    </div>
                    <div style="color:#94a3b8;
                                font-size:0.85rem;">
                        WAV / MP3 / FLAC
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    # ========================================================
    # Placeholders
    # ========================================================

    def _render_upload_section(self) -> None:
        st.info(
            "Upload workspace will be added in Part 43.2"
        )

    def _render_prompt_section(self) -> None:
        st.info(
            "AI Prompt workspace will be added in Part 43.3"
        )

    def _render_configuration_section(self) -> None:
        st.info(
            "Production configuration panel will be added in Part 43.3"
        )

    def _render_generate_section(self) -> None:
        st.info(
            "Pipeline execution controls will be added in Part 43.4"
        )


# ============================================================
# Factory Function
# ============================================================

def render_main_tab() -> None:
    """
    Render entry point for streamlit_app.py
    """

    MainTab().render()
  # ========================================================
# Upload Workspace
# ========================================================

def _render_upload_section(self) -> None:
    """
    Render upload workspace.
    """

    st.markdown("## 📁 Project Assets")

    st.caption(
        "Upload all required documentary assets before starting the AI pipeline."
    )

    left_column, right_column = st.columns(
        [2, 1],
        gap="large",
    )

    # ====================================================
    # LEFT SIDE
    # ====================================================

    with left_column:

        st.markdown("### 🎬 Upload Files")

        video_path = upload_zone.video_upload()

        if video_path is not None:

            st.success("✅ Documentary video uploaded")

            st.write(f"**File:** {video_path.name}")

            st.session_state["video_path"] = video_path

        st.markdown("---")

        script_path = upload_zone.script_upload()

        if script_path is not None:

            st.success("✅ Script uploaded")

            st.write(f"**File:** {script_path.name}")

            st.session_state["script_path"] = script_path

        st.markdown("---")

        narration_path = upload_zone.narration_upload()

        if narration_path is not None:

            st.success("✅ Narration uploaded")

            st.write(f"**File:** {narration_path.name}")

            st.session_state["narration_path"] = narration_path

    # ====================================================
    # RIGHT SIDE
    # ====================================================

    with right_column:

        st.markdown("### 📦 Upload Summary")

        video_ready = (
            st.session_state.get("video_path") is not None
        )

        script_ready = (
            st.session_state.get("script_path") is not None
        )

        narration_ready = (
            st.session_state.get("narration_path") is not None
        )

        st.metric(
            "Video",
            "Ready" if video_ready else "Missing",
        )

        st.metric(
            "Script",
            "Ready" if script_ready else "Missing",
        )

        st.metric(
            "Narration",
            "Ready" if narration_ready else "Missing",
        )
              st.markdown("---")

        st.markdown("### 📊 Project Status")

        uploaded_files = sum(
            [
                video_ready,
                script_ready,
                narration_ready,
            ]
        )

        progress = uploaded_files / 3

        st.progress(progress)

        st.write(
            f"Completion: **{uploaded_files}/3** files uploaded"
        )

        st.markdown("---")

        st.markdown("### ✅ Validation")

        validation_ok = True

        # ------------------------------------------
        # Video Validation
        # ------------------------------------------

        if video_ready:

            video_file = st.session_state["video_path"]

            if upload_zone.validate_file(video_file):

                st.success("🎥 Video validated")

            else:

                validation_ok = False

                st.error("❌ Invalid video file")

        else:

            validation_ok = False

            st.warning("Video not uploaded")

        # ------------------------------------------
        # Script Validation
        # ------------------------------------------

        if script_ready:

            script_file = st.session_state["script_path"]

            if upload_zone.validate_file(script_file):

                st.success("📄 Script validated")

            else:

                validation_ok = False

                st.error("❌ Invalid script file")

        else:

            validation_ok = False

            st.warning("Script not uploaded")

        # ------------------------------------------
        # Narration Validation
        # ------------------------------------------

        if narration_ready:

            narration_file = st.session_state["narration_path"]

            if upload_zone.validate_file(narration_file):

                st.success("🎤 Narration validated")

            else:

                validation_ok = False

                st.error("❌ Invalid narration file")

        else:

            validation_ok = False

            st.warning("Narration not uploaded")

        st.markdown("---")

        st.markdown("### 🚀 Pipeline Readiness")

        if validation_ok:

            st.success(
                "All required project assets are available."
            )

            st.session_state["pipeline_ready"] = True

        else:

            st.info(
                "Upload and validate all required assets to continue."
            )

            st.session_state["pipeline_ready"] = False

        st.markdown("---")

        with st.expander("📁 Uploaded Assets", expanded=False):

            if video_ready:

                st.write(
                    f"🎥 **Video:** {st.session_state['video_path'].name}"
                )

            if script_ready:

                st.write(
                    f"📄 **Script:** {st.session_state['script_path'].name}"
                )

            if narration_ready:

                st.write(
                    f"🎤 **Narration:** {st.session_state['narration_path'].name}"
                )

            if not any(
                [
                    video_ready,
                    script_ready,
                    narration_ready,
                ]
            ):

                st.caption(
                    "No project assets uploaded."
                )
              # ========================================================
# AI Prompt Workspace
# ========================================================

def _render_prompt_section(self) -> None:
    """
    Render AI prompt configuration workspace.
    """

    st.markdown("## 🤖 AI Prompt Workspace")

    st.caption(
        "Configure how MystoriumX AI generates the cinematic soundtrack."
    )

    left_column, right_column = st.columns(
        [2, 1],
        gap="large",
    )

    # ====================================================
    # LEFT PANEL
    # ====================================================

    with left_column:

        prompt = st.text_area(
            "🎬 Cinematic Music Prompt",
            placeholder=(
                "Example:\n\n"
                "Dark mysterious orchestral soundtrack with "
                "deep cinematic drones, emotional strings, "
                "epic percussion, suspense and tension."
            ),
            height=180,
            key="music_prompt",
        )

        st.session_state["music_prompt"] = prompt

        documentary_type = st.selectbox(
            "📺 Documentary Style",
            [
                "Historical Mystery",
                "Crime Documentary",
                "War Documentary",
                "Space Documentary",
                "Nature Documentary",
                "Ancient Civilizations",
                "True Story",
                "Horror Documentary",
                "Science Documentary",
                "Custom",
            ],
            key="documentary_style",
        )

        st.session_state[
            "documentary_style"
        ] = documentary_type

        cinematic_style = st.selectbox(
            "🎼 Cinematic Style",
            [
                "Hollywood",
                "Hans Zimmer",
                "Dark Ambient",
                "Epic Orchestra",
                "Hybrid Trailer",
                "Minimal Piano",
                "Emotional",
                "Mystery",
                "Suspense",
            ],
            key="cinematic_style",
        )

        st.session_state[
            "cinematic_style"
        ] = cinematic_style

    # ====================================================
    # RIGHT PANEL
    # ====================================================

    with right_column:

        st.markdown("### 🎭 Mood")

        mood = st.select_slider(
            "Scene Mood",
            options=[
                "Calm",
                "Hopeful",
                "Emotional",
                "Suspense",
                "Dark",
                "Terrifying",
            ],
            value="Suspense",
            key="scene_mood",
        )

        st.session_state["scene_mood"] = mood

        intensity = st.slider(
            "⚡ Intensity",
            min_value=1,
            max_value=10,
            value=7,
            key="music_intensity",
        )

        st.session_state[
            "music_intensity"
        ] = intensity

        duration = st.slider(
            "⏱ Target Duration (seconds)",
            min_value=30,
            max_value=600,
            value=180,
            step=30,
            key="target_duration",
        )

        st.session_state[
            "target_duration"
        ] = duration
              st.markdown("---")

        st.markdown("### ⚙️ AI Generation Settings")

        creativity = st.slider(
            "🎨 Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=0.75,
            step=0.05,
            key="creativity_level",
            help="Higher values create more creative music."
        )

        guidance_scale = st.slider(
            "🎼 Prompt Guidance",
            min_value=1.0,
            max_value=20.0,
            value=10.0,
            step=0.5,
            key="guidance_scale",
            help="Controls how strongly AI follows the prompt."
        )

        seed = st.number_input(
            "🎲 Random Seed",
            min_value=0,
            max_value=999999,
            value=42,
            step=1,
            key="generation_seed",
            help="Use the same seed for reproducible generations."
        )

        st.markdown("---")

        negative_prompt = st.text_area(
            "🚫 Negative Prompt",
            placeholder=(
                "Example:\n"
                "Low quality, noisy audio, distortion, clipping, "
                "vocals, speech, crowd noise."
            ),
            height=120,
            key="negative_prompt",
        )

        st.session_state["negative_prompt"] = negative_prompt

        st.markdown("---")

        st.markdown("### 🧠 AI Options")

        auto_scene_analysis = st.toggle(
            "Automatically Analyze Video Scenes",
            value=True,
            key="auto_scene_analysis",
        )

        auto_prompt_enhancement = st.toggle(
            "Automatically Enhance Prompt",
            value=True,
            key="auto_prompt_enhancement",
        )

        apply_mastering = st.toggle(
            "Apply Professional Audio Mastering",
            value=True,
            key="apply_mastering",
        )

        generate_waveform = st.toggle(
            "Generate Waveform & Analytics",
            value=True,
            key="generate_waveform",
        )

        st.session_state["auto_scene_analysis"] = auto_scene_analysis
        st.session_state["auto_prompt_enhancement"] = auto_prompt_enhancement
        st.session_state["apply_mastering"] = apply_mastering
        st.session_state["generate_waveform"] = generate_waveform

        st.markdown("---")

        st.markdown("### 📋 Prompt Preview")

        preview = f"""
Documentary Style : {documentary_type}

Cinematic Style : {cinematic_style}

Scene Mood : {mood}

Intensity : {intensity}/10

Target Duration : {duration} sec

Prompt:

{prompt if prompt else 'No custom prompt provided.'}

Negative Prompt:

{negative_prompt if negative_prompt else 'None'}
"""

        st.code(
            preview,
            language="text",
        )

        st.session_state["pipeline_config"] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "documentary_style": documentary_type,
            "cinematic_style": cinematic_style,
            "scene_mood": mood,
            "intensity": intensity,
            "duration": duration,
            "creativity": creativity,
            "guidance_scale": guidance_scale,
            "seed": seed,
            "auto_scene_analysis": auto_scene_analysis,
            "auto_prompt_enhancement": auto_prompt_enhancement,
            "apply_mastering": apply_mastering,
            "generate_waveform": generate_waveform,
        }
      # ========================================================
# Project Configuration Panel
# ========================================================

def _render_configuration_section(self) -> None:
    """
    Render project configuration panel.
    """

    st.markdown("## ⚙️ Project Configuration")

    st.caption(
        "Configure AI generation and export settings."
    )

    left_column, right_column = st.columns(
        [2, 1],
        gap="large",
    )

    # ====================================================
    # LEFT PANEL
    # ====================================================

    with left_column:

        project_name = st.text_input(
            "📁 Project Name",
            value="Untitled Documentary",
            key="project_name",
        )

        output_directory = st.text_input(
            "📂 Output Directory",
            value="output/",
            key="output_directory",
        )

        export_format = st.selectbox(
            "🎵 Export Format",
            [
                "WAV",
                "MP3",
                "FLAC",
            ],
            key="export_format",
        )

        sample_rate = st.selectbox(
            "🎧 Sample Rate",
            [
                44100,
                48000,
            ],
            index=1,
            key="sample_rate",
        )

        bit_depth = st.selectbox(
            "💿 Bit Depth",
            [
                16,
                24,
                32,
            ],
            index=1,
            key="bit_depth",
        )

    # ====================================================
    # RIGHT PANEL
    # ====================================================

    with right_column:

        st.markdown("### 🎛 Processing")

        normalize_audio = st.checkbox(
            "Normalize Audio",
            value=True,
            key="normalize_audio",
        )

        apply_limiting = st.checkbox(
            "True Peak Limiter",
            value=True,
            key="true_peak",
        )

        enable_logging = st.checkbox(
            "Detailed Logging",
            value=True,
            key="enable_logging",
        )

        keep_intermediate = st.checkbox(
            "Keep Temporary Files",
            value=False,
            key="keep_temp",
        )

    st.session_state["project_config"] = {
        "project_name": project_name,
        "output_directory": output_directory,
        "export_format": export_format,
        "sample_rate": sample_rate,
        "bit_depth": bit_depth,
        "normalize_audio": normalize_audio,
        "apply_limiting": apply_limiting,
        "enable_logging": enable_logging,
        "keep_intermediate": keep_intermediate,
    }
  # ========================================================
# Generate Pipeline Section
# ========================================================

def _render_generate_section(self) -> None:
    """
    Render AI pipeline execution controls.
    """

    st.markdown("## 🚀 Generate Cinematic Soundtrack")

    st.caption(
        "Start the complete MystoriumX AI production pipeline."
    )

    left_column, right_column = st.columns(
        [2, 1],
        gap="large",
    )

    # ====================================================
    # LEFT PANEL
    # ====================================================

    with left_column:

        generate = st.button(
            "🎬 Generate Soundtrack",
            type="primary",
            use_container_width=True,
        )

        if generate:

            if not st.session_state.get(
                "pipeline_ready",
                False,
            ):

                st.error(
                    "Please upload and validate all required project files."
                )

                return

            try:

                progress_tracker.create()

                progress_tracker.update(
                    "Initializing Project",
                    0.05,
                )

                config = PipelineConfig(
                    project_name=st.session_state[
                        "project_config"
                    ]["project_name"],
                    output_directory=Path(
                        st.session_state[
                            "project_config"
                        ]["output_directory"]
                    ),
                    export_format=st.session_state[
                        "project_config"
                    ]["export_format"],
                )

                progress_tracker.update(
                    "Loading AI Pipeline",
                    0.20,
                )

                result = self.orchestrator.run_pipeline(
                    config=config,
                    video_path=st.session_state[
                        "video_path"
                    ],
                    script_path=st.session_state[
                        "script_path"
                    ],
                    narration_path=st.session_state[
                        "narration_path"
                    ],
                    prompt=st.session_state[
                        "music_prompt"
                    ],
                )

                progress_tracker.update(
                    "Rendering Results",
                    0.90,
                )

                st.session_state[
                    "pipeline_result"
                ] = result

                progress_tracker.complete()

                st.success(
                    "🎉 AI Soundtrack Generated Successfully."
                )

            except Exception as error:

                logger.exception(error)

                progress_tracker.error(
                    str(error)
                )

                st.exception(error)

    # ====================================================
    # RIGHT PANEL
    # ====================================================

    with right_column:

        st.markdown("### 📋 Pipeline Status")

        st.metric(
            "Video",
            "Ready"
            if st.session_state.get(
                "video_path"
            )
            else "Missing",
        )

        st.metric(
            "Script",
            "Ready"
            if st.session_state.get(
                "script_path"
            )
            else "Missing",
        )

        st.metric(
            "Narration",
            "Ready"
            if st.session_state.get(
                "narration_path"
            )
            else "Missing",
        )

        st.metric(
            "AI Prompt",
            "Ready"
            if st.session_state.get(
                "music_prompt"
            )
            else "Default",
        )

    # ====================================================
    # Results Preview
    # ====================================================

    result = st.session_state.get(
        "pipeline_result"
    )

    if result is not None:

        st.divider()

        st.subheader(
            "🎵 Generated Soundtrack"
        )

        audio_path = getattr(
            result,
            "output_audio",
            None,
        )

        if audio_path is not None:

            audio_player.render(
                Path(audio_path)
            )

        metadata = getattr(
            result,
            "metadata",
            None,
        )

        if metadata:

            audio_player.show_metadata(
                metadata
            )

        st.success(
            "Pipeline finished successfully."
        )
      
