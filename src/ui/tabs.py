"""
Reporly UI — Tab rendering functions.
Each tab is a self-contained function that reads/writes session_state.
No business logic here — only wiring + display.
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from src.config import load_config
from src.providers import call_llm
from src.core.analyzer import analyze_data
from src.core.models import Report
from src.charts import generate_charts
from src.core.health import classify_error, get_user_message
from src.core.analytics import track_report
from src.ui.styles import insight_card

config = load_config()

EXPORT_FORMATS = {
    "PDF": {"ext": "pdf", "mime": "application/pdf"},
    "PPTX": {
        "ext": "pptx",
        "mime": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    },
    "DOCX": {
        "ext": "docx",
        "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    },
}


# ---------------------------------------------------------------------------
# Tab: Data Overview
# ---------------------------------------------------------------------------
def tab_data():
    """Data overview — profile, quality, preview."""
    profile = st.session_state.profile
    df = st.session_state.df

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(":material/table_rows: Rows", f"{profile.rows:,}")
    m2.metric(":material/view_column: Columns", str(profile.columns))
    m3.metric(":material/calculate: Numeric", str(profile.basic_stats.get("numeric_columns", 0)))
    m4.metric(":material/report_problem: Missing", f"{profile.basic_stats.get('null_pct', 0)}%")

    st.markdown("")

    if profile.warnings:
        with st.expander(f":material/warning: {len(profile.warnings)} quality warnings", expanded=False):
            for w in profile.warnings:
                st.warning(w, icon=":material/info:")

    with st.expander(":material/table_view: Data Preview (first 30 rows)", expanded=True):
        st.dataframe(df.head(30), use_container_width=True, height=400)

    with st.expander(":material/list: Column Details", expanded=False):
        col_data = []
        for ci in profile.column_info:
            col_data.append({
                "Column": ci.name,
                "Type": ci.dtype,
                "Unique": ci.unique_count,
                "Null %": f"{ci.null_pct}%",
                "Sample": ", ".join(str(v) for v in ci.sample_values[:3]),
            })
        st.dataframe(pd.DataFrame(col_data), use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Tab: AI Insights
# ---------------------------------------------------------------------------
def tab_insights(max_insights: int):
    """AI Insights — generate and display insights."""
    profile = st.session_state.profile
    df = st.session_state.df

    if not st.session_state.analysis_done:
        st.markdown(
            '<p style="color:#888; text-align:center; padding:32px 0;">'
            ':material/psychology: Click below to generate AI insights from your data.</p>',
            unsafe_allow_html=True,
        )
        if st.button(":material/auto_awesome: Generate AI Insights", type="primary",
                      use_container_width=True):
            with st.status("Analyzing your data...", expanded=True) as status:
                try:
                    st.write("📊 Reading data profile...")
                    sample_str = df.head(15).to_string(index=False)
                    st.write("🤖 Sending to AI for analysis...")
                    insights = analyze_data(
                        profile=profile,
                        data_sample_str=sample_str,
                        call_llm_fn=call_llm,
                        model=config.llm_model,
                        api_key=config.llm_api_key,
                        max_insights=max_insights,
                        max_tokens=config.llm_max_tokens,
                    )
                    st.write("💡 Parsing insights...")
                    st.session_state.insights = insights
                    st.session_state.analysis_done = True
                    status.update(label="Analysis complete!", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    err_info = classify_error(e)
                    status.update(label="Analysis failed", state="error", expanded=False)
                    st.error(f"❌ {err_info.message}")
                    st.info(f"💡 Try: {err_info.suggestion}")
        return

    insights = st.session_state.insights
    if not insights:
        st.info(":material/info: No insights generated. Try with a different dataset.")
        return

    st.markdown(f"##### :material/lightbulb: {len(insights)} Insights Found")
    for i, ins in enumerate(insights, 1):
        insight_card(i, ins.title, ins.description, ins.importance)


# ---------------------------------------------------------------------------
# Tab: Charts
# ---------------------------------------------------------------------------
def tab_charts(max_charts: int):
    """Charts — generate and display charts."""
    df = st.session_state.df
    insights = st.session_state.insights

    if not st.session_state.analysis_done:
        st.markdown(
            '<div class="rp-insight-card" style="text-align:center;padding:32px;">'
            '<div class="rp-insight-title">No charts yet</div>'
            '<div class="rp-insight-desc">Generate AI insights first (Insights tab) '
            'to get smart chart suggestions.</div></div>',
            unsafe_allow_html=True,
        )
        return

    if not st.session_state.charts:
        if st.button(":material/bar_chart: Generate Charts", type="primary",
                      use_container_width=True):
            with st.status("Generating charts...", expanded=True) as status:
                try:
                    st.write("🎨 Creating visualizations...")
                    charts = generate_charts(
                        df, insights,
                        max_charts=max_charts,
                        width=config.chart_width,
                        height=config.chart_height,
                    )
                    st.write(f"✅ {len(charts)} charts generated!")
                    st.session_state.charts = charts
                    status.update(label="Charts ready!", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    status.update(label="Chart generation failed", state="error", expanded=False)
                    st.error(f"❌ Chart generation issue: {str(e)[:200]}")
                    st.info("💡 Try: Generate insights first, then retry charts.")
            return

    charts = st.session_state.charts
    st.markdown(f"##### :material/insert_chart: {len(charts)} Charts")

    for i in range(0, len(charts), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(charts):
                with col:
                    st.image(charts[idx], use_container_width=True)


# ---------------------------------------------------------------------------
# Tab: Export
# ---------------------------------------------------------------------------
def tab_export(export_format: str, template_key: str, export_fn_map: dict):
    """Export — template preview, generate, download."""
    insights = st.session_state.insights
    charts = st.session_state.charts

    report_title = st.text_input(
        ":material/title: Report Title",
        value=f"Analysis: {st.session_state.filename}",
    )

    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric(":material/lightbulb: Insights", str(len(insights)))
    col_s2.metric(":material/bar_chart: Charts", str(len(charts)))
    col_s3.metric(":material/description: Format", export_format)

    st.markdown("")

    if st.button(
        f":material/download: Generate & Download {export_format}",
        type="primary",
        use_container_width=True,
    ):
        _do_export(report_title, export_format, template_key, export_fn_map)


def _do_export(title: str, export_format: str, template_key: str, export_fn_map: dict):
    """Generate report and offer download."""
    profile = st.session_state.profile
    report = Report(
        title=title,
        data_profile=profile,
        insights=st.session_state.insights,
        charts=st.session_state.charts,
        generated_at=datetime.now(),
    )

    fmt = EXPORT_FORMATS[export_format]
    progress = st.progress(0, text=f"Building {export_format} report...")

    try:
        progress.progress(30, text="Assembling report content...")
        export_bytes = export_fn_map[export_format](
            report, template_name=template_key, app_name=config.app_name,
        )
        size_kb = len(export_bytes) / 1024
        progress.progress(100, text=f"Done! ({size_kb:.0f} KB)")

        track_report(export_format, template_key, profile.rows, size_kb)

        base_name = profile.filename.rsplit(".", 1)[0]
        file_name = f"reporly_{base_name}_{datetime.now().strftime('%Y%m%d')}.{fmt['ext']}"

        st.download_button(
            label=f":material/download: Download {export_format} ({size_kb:.0f} KB)",
            data=export_bytes,
            file_name=file_name,
            mime=fmt["mime"],
            type="primary",
            use_container_width=True,
        )
        st.toast(f"✅ {export_format} report ready — {size_kb:.0f} KB")
    except Exception as e:
        err_info = classify_error(e)
        st.error(f"❌ {err_info.message}")
        st.info(f"💡 Try: {err_info.suggestion}")
        progress.progress(100, text="Export failed")
