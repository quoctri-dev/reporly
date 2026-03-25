"""
Reporly — Basic Session Analytics
Tracks report generation stats within Streamlit session state.
"""
import streamlit as st
from datetime import datetime


def _ensure_state():
    """Initialize analytics in session state if not present."""
    if "analytics" not in st.session_state:
        st.session_state.analytics = {
            "reports_generated": 0,
            "formats_used": {},
            "templates_used": {},
            "total_rows_processed": 0,
            "session_start": datetime.now().isoformat(),
        }


def track_report(export_format: str, template_name: str, rows: int, file_size_kb: float):
    """Track a report generation event."""
    _ensure_state()
    stats = st.session_state.analytics
    stats["reports_generated"] += 1
    stats["formats_used"][export_format] = stats["formats_used"].get(export_format, 0) + 1
    stats["templates_used"][template_name] = stats["templates_used"].get(template_name, 0) + 1
    stats["total_rows_processed"] += rows


def get_session_stats() -> dict:
    """Get current session statistics."""
    _ensure_state()
    return st.session_state.analytics


def render_sidebar_stats():
    """Render analytics summary in sidebar."""
    stats = get_session_stats()
    if stats["reports_generated"] > 0:
        st.sidebar.divider()
        st.sidebar.caption(f"Session: {stats['reports_generated']} reports generated")
