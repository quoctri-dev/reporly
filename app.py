"""
Reporly — AI Report Generator
Upload data -> AI analyzes -> Professional report (PDF / PPTX / DOCX)

Streamlit app (wiring layer — imports all modules, no business logic here).
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# Must be first Streamlit call
st.set_page_config(
    page_title="Reporly — AI Report Generator",
    page_icon="📊",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Imports (all modules)
# ---------------------------------------------------------------------------
from src.config import load_config, validate_config
from src.providers import call_llm
from src.core.detector import detect_data
from src.core.analyzer import analyze_data
from src.core.models import Report
from src.charts import generate_charts
from src.io.reader import read_uploaded_file, FileReadError
from src.io.exporter import export_pdf
from src.io.pptx_exporter import export_pptx
from src.io.docx_exporter import export_docx
from src.templates import TEMPLATE_NAMES
from src.core.health import classify_error, get_user_message
from src.core.analytics import track_report, render_sidebar_stats


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
config = load_config()

# Export format metadata
EXPORT_FORMATS = {
    "PDF": {
        "ext": "pdf",
        "mime": "application/pdf",
        "fn": export_pdf,
    },
    "PPTX": {
        "ext": "pptx",
        "mime": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "fn": export_pptx,
    },
    "DOCX": {
        "ext": "docx",
        "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "fn": export_docx,
    },
}


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

def main():
    """Main app flow: upload -> analyze -> preview -> download."""

    # Header
    st.title("📊 Reporly")
    st.caption("Upload your data · AI analyzes it · Download a professional report")

    # --- Sidebar ---
    with st.sidebar:
        st.header("Settings")

        export_format = st.selectbox(
            "Export Format",
            options=list(EXPORT_FORMATS.keys()),
            index=0,
            help="Choose output format: PDF, PPTX (PowerPoint), or DOCX (Word)",
        )

        template_name = st.selectbox(
            "Report Template",
            options=[n.capitalize() for n in TEMPLATE_NAMES],
            index=0,
            help="Minimal: clean & simple · Corporate: formal & navy · Modern: bold & colorful",
        )
        template_key = template_name.lower()

        st.divider()
        st.subheader("Analysis")
        max_insights = st.slider("Max Insights", 1, 10, config.max_insights)
        max_charts = st.slider("Max Charts", 1, 10, config.max_charts)

        st.divider()
        st.caption(f"Reporly v{config.app_version}")

    render_sidebar_stats()
    st.divider()

    # Validate config
    config_errors = validate_config(config)
    if config_errors:
        st.error("Configuration issues:")
        for err in config_errors:
            st.warning(err)
        st.info("Set up your .env file — see .env.example for instructions.")
        st.stop()

    # Upload
    uploaded_file = st.file_uploader(
        "Upload your data file",
        type=["csv", "xlsx", "xls", "tsv"],
        help=f"Max {config.max_file_size_mb}MB. Supported: CSV, Excel, TSV",
    )

    if not uploaded_file:
        _show_welcome()
        return

    # Process pipeline
    _run_pipeline(uploaded_file, export_format, template_key, max_insights, max_charts)


def _show_welcome():
    """Welcome screen when no file uploaded."""
    st.markdown("### How it works")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("**1. Upload**")
        st.caption("Drop your CSV or Excel file")
    with cols[1]:
        st.markdown("**2. Analyze**")
        st.caption("AI detects patterns & insights")
    with cols[2]:
        st.markdown("**3. Download**")
        st.caption("Get a PDF, PPTX, or DOCX report")

    st.divider()
    st.markdown("**Supported templates:**")
    tcols = st.columns(3)
    tcols[0].markdown("**Minimal** — Clean & simple")
    tcols[1].markdown("**Corporate** — Formal & navy")
    tcols[2].markdown("**Modern** — Bold & colorful")


def _run_pipeline(uploaded_file, export_format: str, template_key: str,
                  max_insights: int, max_charts: int):
    """Execute the full analysis pipeline."""

    # Step 1: Read file
    with st.status("Reading file...", expanded=False) as status:
        try:
            df = read_uploaded_file(
                uploaded_file,
                max_size_mb=config.max_file_size_mb,
                max_rows=config.max_rows,
                max_columns=config.max_columns,
            )
            status.update(label=f"Loaded: {len(df):,} rows x {len(df.columns)} columns", state="complete")
        except FileReadError as e:
            st.error(f"Could not read file: {str(e)}")
            return

    # Show data preview
    with st.expander("Data Preview", expanded=False):
        st.dataframe(df.head(20))

    # Step 2: Detect & Profile
    with st.status("Profiling data...") as status:
        profile = detect_data(df, filename=uploaded_file.name)
        status.update(label="Data profiled", state="complete")

    # Show profile summary
    metric_cols = st.columns(4)
    metric_cols[0].metric("Rows", f"{profile.rows:,}")
    metric_cols[1].metric("Columns", str(profile.columns))
    metric_cols[2].metric("Numeric", str(profile.basic_stats.get("numeric_columns", 0)))
    metric_cols[3].metric("Missing", f"{profile.basic_stats.get('null_pct', 0)}%")

    if profile.warnings:
        with st.expander(f"{len(profile.warnings)} quality warnings"):
            for w in profile.warnings:
                st.warning(w)

    st.divider()

    # Step 3: AI Analysis
    report_title = st.text_input("Report title", value=f"Analysis: {uploaded_file.name}")

    if st.button("Generate Report", type="primary", use_container_width=True):
        _generate_report(df, profile, report_title, export_format, template_key,
                         max_insights, max_charts)


def _generate_report(df: pd.DataFrame, profile, title: str,
                     export_format: str, template_key: str,
                     max_insights: int, max_charts: int):
    """Generate insights, charts, and export to chosen format."""

    progress = st.progress(0, text="Starting analysis...")

    # AI Insights (with graceful degradation)
    insights = []
    progress.progress(10, text="AI analyzing your data...")
    try:
        with st.status("AI analyzing your data...") as status:
            sample_str = df.head(15).to_string(index=False)
            insights = analyze_data(
                profile=profile,
                data_sample_str=sample_str,
                call_llm_fn=call_llm,
                model=config.llm_model,
                api_key=config.llm_api_key,
                max_insights=max_insights,
                max_tokens=config.llm_max_tokens,
            )
            status.update(label=f"{len(insights)} insights found", state="complete")
    except Exception as e:
        err_info = classify_error(e)
        st.warning(get_user_message(err_info))
        st.info("Continuing with charts and raw data only (no AI insights).")

    progress.progress(40, text="Insights ready...")

    # Show insights
    if insights:
        st.markdown("### Key Insights")
        for i, ins in enumerate(insights, 1):
            importance_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(ins.importance, "⚪")
            st.markdown(f"**{i}. {ins.title}** {importance_emoji}")
            st.caption(ins.description)

    # Charts
    charts = []
    progress.progress(50, text="Generating charts...")
    try:
        with st.status("Generating charts...") as status:
            charts = generate_charts(
                df, insights,
                max_charts=max_charts,
                width=config.chart_width,
                height=config.chart_height,
            )
            status.update(label=f"{len(charts)} charts created", state="complete")
    except Exception as e:
        st.warning(f"Chart generation failed: {str(e)[:200]}. Report will be generated without charts.")

    progress.progress(70, text="Charts ready...")

    # Show chart previews
    if charts:
        st.markdown("### Charts")
        for chart_bytes in charts:
            st.image(chart_bytes)

    st.divider()

    # Build Report
    report = Report(
        title=title,
        data_profile=profile,
        insights=insights,
        charts=charts,
        generated_at=datetime.now(),
    )

    # Export to chosen format
    fmt = EXPORT_FORMATS[export_format]
    progress.progress(80, text=f"Building {export_format} report...")

    try:
        with st.status(f"Building {export_format} report...") as status:
            export_bytes = fmt["fn"](report, template_name=template_key, app_name=config.app_name)
            size_kb = len(export_bytes) / 1024
            status.update(label=f"{export_format} ready ({size_kb:.0f} KB)", state="complete")
    except Exception as e:
        err_info = classify_error(e)
        st.error(get_user_message(err_info))
        progress.progress(100, text="Export failed")
        return

    progress.progress(100, text="Done!")

    # Track analytics
    track_report(export_format, template_key, profile.rows, size_kb)

    # Download button
    base_name = profile.filename.rsplit(".", 1)[0]
    file_name = f"reporly_{base_name}_{datetime.now().strftime('%Y%m%d')}.{fmt['ext']}"

    st.download_button(
        label=f"Download {export_format} Report",
        data=export_bytes,
        file_name=file_name,
        mime=fmt["mime"],
        type="primary",
        use_container_width=True,
    )

    st.success("Report generated! Click above to download.")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
else:
    main()  # Streamlit runs directly
