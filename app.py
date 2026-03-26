"""
Reporly — AI Report Generator (Phase 2 Dashboard UI)
Upload data -> AI analyzes -> Professional report (PDF / PPTX / DOCX)

Wiring layer: imports all modules, no business logic here.
UI: Dashboard layout — sidebar settings + main area with 4 tabs.
"""
import streamlit as st

# Must be first Streamlit call
st.set_page_config(
    page_title="NoVa — AI Report Generator",
    page_icon=":material/analytics:",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from src.config import load_config, validate_config
from src.core.detector import detect_data
from src.io.reader import read_uploaded_file, FileReadError
from src.io.exporter import export_pdf
from src.io.pptx_exporter import export_pptx
from src.io.docx_exporter import export_docx
from src.core.analytics import render_sidebar_stats
from src.ui.styles import inject_custom_css, welcome_step_card
from src.ui.tabs import tab_data, tab_insights, tab_charts, tab_export

# ---------------------------------------------------------------------------
# Config + CSS
# ---------------------------------------------------------------------------
config = load_config()
inject_custom_css()

EXPORT_FN_MAP = {"PDF": export_pdf, "PPTX": export_pptx, "DOCX": export_docx}
EXPORT_KEYS = list(EXPORT_FN_MAP.keys())


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
def _init_state():
    """Initialize session state with defaults."""
    for key, default in [
        ("df", None), ("profile", None), ("insights", []), ("charts", []),
        ("report_bytes", None), ("analysis_done", False), ("filename", ""),
    ]:
        st.session_state.setdefault(key, default)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def _render_sidebar() -> tuple:
    """Render sidebar. Returns (export_format, max_insights, max_charts)."""
    with st.sidebar:
        st.markdown(
            '<span class="rp-hero-badge">'
            '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            'background:#f43f5e;animation:dot 2s ease infinite;margin-right:6px;'
            'vertical-align:middle;"></span>NoVa</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"v{config.app_version}")
        st.divider()

        st.markdown("##### :material/tune: Settings")
        export_format = st.selectbox(
            "Export Format", options=EXPORT_KEYS, index=0,
            help="PDF, PPTX (PowerPoint), or DOCX (Word)",
        )
        st.divider()

        st.markdown("##### :material/settings: Analysis")
        max_insights = st.slider("Max Insights", 1, 10, config.max_insights)
        max_charts = st.slider("Max Charts", 1, 10, config.max_charts)

        st.divider()
        render_sidebar_stats()

    return export_format, max_insights, max_charts


# ---------------------------------------------------------------------------
# Welcome screen
# ---------------------------------------------------------------------------
def _show_welcome():
    """Welcome screen when no file uploaded."""
    st.markdown("")
    _, col_main, _ = st.columns([1, 3, 1])
    with col_main:
        st.markdown(
            '<div style="text-align:center; margin-bottom:8px;">'
            '<span class="rp-hero-badge">'
            '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            'background:#f43f5e;animation:dot 2s ease infinite;margin-right:6px;'
            'vertical-align:middle;"></span>NoVa</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<h1 style="text-align:center; font-size:3rem !important; margin-bottom:4px;">'
            'AI Report Generator</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="text-align:center; color:#8a8580; font-size:16px; margin-bottom:12px;">'
            'Upload &rarr; Analyze &rarr; Export</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="text-align:center; margin-bottom:32px;">'
            '<span class="rp-badge" style="background:rgba(244,63,94,.1);color:#f43f5e;'
            'font-size:12px;padding:4px 12px;margin:0 4px;">CSV</span>'
            '<span class="rp-badge" style="background:rgba(244,63,94,.1);color:#f43f5e;'
            'font-size:12px;padding:4px 12px;margin:0 4px;">XLSX</span>'
            '<span class="rp-badge" style="background:rgba(244,63,94,.1);color:#f43f5e;'
            'font-size:12px;padding:4px 12px;margin:0 4px;">TSV</span>'
            '<span style="color:#4c4945;margin:0 8px;">&rarr;</span>'
            '<span class="rp-badge" style="background:rgba(139,92,246,.1);color:#8b5cf6;'
            'font-size:12px;padding:4px 12px;margin:0 4px;">PDF</span>'
            '<span class="rp-badge" style="background:rgba(139,92,246,.1);color:#8b5cf6;'
            'font-size:12px;padding:4px 12px;margin:0 4px;">PPTX</span>'
            '<span class="rp-badge" style="background:rgba(139,92,246,.1);color:#8b5cf6;'
            'font-size:12px;padding:4px 12px;margin:0 4px;">DOCX</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    c1, c2, c3 = st.columns(3)
    # NOTE: HTML cards need actual glyphs, not :material/ shortcodes
    _icon_css = (
        '<link href="https://fonts.googleapis.com/css2?family='
        'Material+Symbols+Rounded:opsz,wght,FILL@24,400,1" rel="stylesheet">'
    )
    st.markdown(_icon_css, unsafe_allow_html=True)
    _ms = '<span class="material-symbols-rounded" style="font-size:32px;color:#f43f5e;">'
    with c1:
        welcome_step_card(f"{_ms}upload_file</span>", "Upload", "CSV, Excel, or TSV")
    with c2:
        welcome_step_card(f"{_ms}psychology</span>", "AI Analyze", "Insights, trends & charts")
    with c3:
        welcome_step_card(f"{_ms}download</span>", "Download", "PDF, PPTX, or DOCX")



# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------
def _process_upload(uploaded_file):
    """Read and profile uploaded file into session_state."""
    try:
        df = read_uploaded_file(
            uploaded_file,
            max_size_mb=config.max_file_size_mb,
            max_rows=config.max_rows,
            max_columns=config.max_columns,
        )
    except FileReadError as e:
        st.error(f":material/error: Could not read file: {e}")
        return

    profile = detect_data(df, filename=uploaded_file.name)
    st.session_state.df = df
    st.session_state.profile = profile
    st.session_state.filename = uploaded_file.name
    st.session_state.insights = []
    st.session_state.charts = []
    st.session_state.report_bytes = None
    st.session_state.analysis_done = False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    """Dashboard main flow."""
    _init_state()

    config_errors = validate_config(config)
    if config_errors:
        st.error(":material/error: Configuration issues")
        for err in config_errors:
            st.warning(err)
        st.info("Set up your `.env` file — see `.env.example` for instructions.")
        st.stop()

    export_format, max_insights, max_charts = _render_sidebar()
    template_key = "nova"

    # Header
    st.title("NoVa")
    st.caption("Upload your data  ·  AI analyzes it  ·  Download a professional report")

    # File upload
    uploaded_file = st.file_uploader(
        "Drop your data file here",
        type=["csv", "xlsx", "xls", "tsv"],
        help=f"Max {config.max_file_size_mb}MB. Supports CSV, Excel, TSV",
        label_visibility="collapsed",
    )

    if not uploaded_file:
        st.session_state.df = None
        _show_welcome()
        return

    # Process new file
    if st.session_state.filename != uploaded_file.name or st.session_state.df is None:
        with st.spinner("Reading file..."):
            _process_upload(uploaded_file)
        if st.session_state.df is None:
            return
        st.success(f"✅ {uploaded_file.name} loaded")
        uc1, uc2, uc3 = st.columns(3)
        uc1.metric("Rows", f"{len(st.session_state.df):,}")
        uc2.metric("Columns", str(len(st.session_state.df.columns)))
        uc3.metric("Size", f"{uploaded_file.size / 1024:.0f} KB")

    # Dashboard tabs
    t_data, t_insights, t_charts, t_export = st.tabs([
        ":material/table_view:  Data",
        ":material/lightbulb:  Insights",
        ":material/bar_chart:  Charts",
        ":material/download:  Export",
    ])

    with t_data:
        tab_data()
    with t_insights:
        tab_insights(max_insights)
    with t_charts:
        tab_charts(max_charts)
    with t_export:
        tab_export(export_format, template_key, EXPORT_FN_MAP)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
else:
    main()
