"""
MystoriumX AI Studio - Core Interface & Styling Architecture (Part 1)

This module initializes the application layout, global session state, system hardware
telemetry, and Hollywood-grade dark glassmorphism theme styling for MystoriumX AI Studio.

Author: Senior Python Software Architect
Platform: Streamlit (Python 3.11)
"""

import datetime
import pathlib
import platform
from typing import Any, Dict

import streamlit as st

# =============================================================================
# Global Constants & Application Metadata
# =============================================================================
APP_NAME: str = "MystoriumX AI Studio"
APP_VERSION: str = "1.0.0-PROD"
APP_AUTHOR: str = "MystoriumX Engineering"
APP_COPYRIGHT: str = f"© {datetime.datetime.now().year} MystoriumX AI. All Rights Reserved."
APP_LICENSE: str = "MIT"
APP_WEBSITE: str = "https://github.com/modrenshoppinghub/MystoriumX-AI-Studio"
APP_GITHUB: str = "https://github.com/modrenshoppinghub/MystoriumX-AI-Studio"

# Design System Palette (Dark Glassmorphism)
COLOR_BG_PRIMARY: str = "#090a0f"
COLOR_BG_SECONDARY: str = "#12151e"
COLOR_CARD_BG: str = "rgba(22, 27, 38, 0.7)"
COLOR_ACCENT_PRIMARY: str = "#7928ca"
COLOR_ACCENT_SECONDARY: str = "#ff4b4b"
COLOR_ACCENT_GRADIENT: str = "linear-gradient(135deg, #ff4b4b 0%, #7928ca 100%)"
COLOR_TEXT_PRIMARY: str = "#f1f5f9"
COLOR_TEXT_SECONDARY: str = "#94a3b8"
COLOR_BORDER: str = "rgba(255, 255, 255, 0.08)"
COLOR_SUCCESS: str = "#10b981"
COLOR_WARNING: str = "#f59e0b"
COLOR_ERROR: str = "#ef4444"

# =============================================================================
# Page Configuration
# =============================================================================
st.set_page_config(
    page_title=f"{APP_NAME} | Hollywood AI Audio Suite",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# Custom CSS (Dark Glassmorphism, RunwayML / Midjourney Aesthetics)
# =============================================================================
CUSTOM_CSS: str = f"""
<style>
    /* Global Reset & Core Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: {COLOR_TEXT_PRIMARY};
    }}

    .stApp {{
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, {COLOR_BG_PRIMARY} 60%);
        background-attachment: fixed;
    }}

    /* Main Container Padding */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    /* Hide Streamlit Default Headers & Footers */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {{
        background-color: rgba(13, 15, 22, 0.85) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid {COLOR_BORDER};
    }}

    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLOR_TEXT_PRIMARY} !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}

    /* Gradient Hero Title Class */
    .hero-title {{
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: {COLOR_ACCENT_GRADIENT};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
    }}

    .hero-subtitle {{
        font-size: 1.15rem;
        color: {COLOR_TEXT_SECONDARY};
        margin-bottom: 2rem;
        font-weight: 400;
    }}

    /* Glassmorphic Rounded Cards */
    .glass-card {{
        background: {COLOR_CARD_BG};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {COLOR_BORDER};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .glass-card:hover {{
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }}

    /* Metric Badges & Status */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .status-badge-active {{
        background: rgba(16, 185, 129, 0.15);
        color: {COLOR_SUCCESS};
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .status-badge-idle {{
        background: rgba(148, 163, 184, 0.15);
        color: {COLOR_TEXT_SECONDARY};
        border: 1px solid rgba(148, 163, 184, 0.3);
    }}

    /* Button Animations & Gradient */
    .stButton>button {{
        background: {COLOR_ACCENT_GRADIENT} !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.75rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(121, 40, 202, 0.3) !important;
        width: 100%;
    }}

    .stButton>button:hover {{
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(255, 75, 75, 0.45) !important;
    }}

    .stButton>button:active {{
        transform: translateY(0);
    }}

    /* Drag and Drop File Uploader Styling */
    [data-testid="stFileUploadDropzone"] {{
        background: rgba(18, 21, 30, 0.6) !important;
        border: 2px dashed rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        transition: border-color 0.3s ease !important;
    }}

    [data-testid="stFileUploadDropzone"]:hover {{
        border-color: {COLOR_ACCENT_PRIMARY} !important;
    }}

    /* Input Controls (Selectbox, Slider, Textarea) */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: rgba(18, 21, 30, 0.8) !important;
        color: {COLOR_TEXT_PRIMARY} !important;
        border: 1px solid {COLOR_BORDER} !important;
        border-radius: 8px !important;
    }}

    .stSelectbox>div>div {{
        background-color: rgba(18, 21, 30, 0.8) !important;
        color: {COLOR_TEXT_PRIMARY} !important;
        border: 1px solid {COLOR_BORDER} !important;
        border-radius: 8px !important;
    }}

    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {COLOR_BG_PRIMARY};
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.15);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}

    /* Code & Monospace Formatting */
    code, pre, .stCodeBlock {{
        font-family: 'JetBrains Mono', monospace !important;
        background-color: rgba(10, 12, 18, 0.9) !important;
        border-radius: 6px !important;
    }}

    /* Sidebar Branding Header */
    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding-bottom: 1.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid {COLOR_BORDER};
    }}

    .sidebar-brand-icon {{
        font-size: 2rem;
    }}

    .sidebar-brand-text {{
        font-size: 1.2rem;
        font-weight: 700;
        background: {COLOR_ACCENT_GRADIENT};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =============================================================================
# Helper & Utility Functions
# =============================================================================
def get_system_information() -> Dict[str, Any]:
    """Inspects host environment and extracts system architecture metadata.

    Returns:
        Dict[str, Any]: Key hardware and platform specifications.
    """
    return {
        "operating_system": f"{platform.system()} {platform.release()}",
        "python_version": platform.python_version(),
        "processor": platform.processor() or "Generic X86/ARM Processor",
        "machine": platform.machine(),
        "architecture": platform.architecture()[0],
        "gpu_available": False,  # Managed dynamically in engine module
        "memory_capacity": "Host Default (32GB Scalable)",
        "cuda_version": "N/A (CPU Mode / Deferred Check)"
    }


def get_application_metadata() -> Dict[str, str]:
    """Retrieves high-level metadata regarding the MystoriumX AI Studio platform.

    Returns:
        Dict[str, str]: Application identification and meta-attributes.
    """
    return {
        "application_name": APP_NAME,
        "version": APP_VERSION,
        "author": APP_AUTHOR,
        "copyright": APP_COPYRIGHT,
        "license": APP_LICENSE,
        "website": APP_WEBSITE,
        "github": APP_GITHUB
    }


def initialize_session_state() -> None:
    """Initializes global Streamlit session state variables required for cross-tab
    state persistence and workflow orchestration.
    """
    default_state: Dict[str, Any] = {
        "uploaded_video": None,
        "uploaded_script": None,
        "uploaded_audio": None,
        "generated_audio": None,
        "results": None,
        "logs": [],
        "pipeline_running": False,
        "current_project": "Untitled_Cinematic_Score",
        "system_info": get_system_information(),
        "progress": 0.0,
        "status": "Idle",
        "scene_data": [],
        "enhanced_prompt": "",
        "mastering_preset": "cinematic",
        "audio_format": "wav",
        "sample_rate": 48000
    }

    for key, val in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = val


# =============================================================================
# Sidebar View Component
# =============================================================================
def render_sidebar() -> None:
    """Renders the global sidebar consisting of platform telemetry,
    system architecture info, and application metadata.
    """
    with st.sidebar:
        # Branding Header
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <span class="sidebar-brand-icon">🎬</span>
                <div>
                    <div class="sidebar-brand-text">{APP_NAME}</div>
                    <div style="font-size: 0.75rem; color: {COLOR_TEXT_SECONDARY};">v{APP_VERSION}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Engine Status Indicator
        is_running = st.session_state.get("pipeline_running", False)
        badge_class = "status-badge-active" if is_running else "status-badge-idle"
        badge_text = "PROCESSING" if is_running else "ENGINE READY"

        st.markdown(
            f"""
            <div style="margin-bottom: 1.5rem;">
                <div style="font-size: 0.75rem; color: {COLOR_TEXT_SECONDARY}; margin-bottom: 0.35rem;">SYSTEM STATUS</div>
                <span class="status-badge {badge_class}">● {badge_text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Hardware Information Panel
        st.subheader("💻 System Architecture")
        sys_info = st.session_state.get("system_info", get_system_information())

        st.markdown(
            f"""
            <div style="font-size: 0.85rem; line-height: 1.6; color: {COLOR_TEXT_SECONDARY}; margin-bottom: 1rem;">
                <div><strong style="color: {COLOR_TEXT_PRIMARY};">OS:</strong> {sys_info['operating_system']}</div>
                <div><strong style="color: {COLOR_TEXT_PRIMARY};">Python:</strong> {sys_info['python_version']}</div>
                <div><strong style="color: {COLOR_TEXT_PRIMARY};">Arch:</strong> {sys_info['machine']} ({sys_info['architecture']})</div>
                <div><strong style="color: {COLOR_TEXT_PRIMARY};">Acceleration:</strong> {'CUDA' if sys_info['gpu_available'] else 'CPU Native'}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Active Project Metadata
        st.subheader("📁 Project Session")
        st.text_input(
            "Project Name",
            value=st.session_state.get("current_project", "Untitled_Score"),
            key="current_project_input"
        )

        st.markdown("---")

        # Application About Section
        st.subheader("ℹ️ About Platform")
        meta = get_application_metadata()
        st.markdown(
            f"""
            <div style="font-size: 0.8rem; color: {COLOR_TEXT_SECONDARY}; line-height: 1.5;">
                <div><strong>Author:</strong> {meta['author']}</div>
                <div><strong>License:</strong> {meta['license']}</div>
                <div><strong>Website:</strong> <a href="{meta['website']}" target="_blank" style="color: {COLOR_ACCENT_PRIMARY};">{meta['website']}</a></div>
                <div style="margin-top: 0.75rem; font-size: 0.75rem; color: #64748b;">{meta['copyright']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =============================================================================
# Execution Entry Point (Part 1 Initialization)
# =============================================================================
initialize_session_state()
render_sidebar()
