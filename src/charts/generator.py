"""
Reporly — Chart Generation
Creates charts from DataFrame + Insights. Outputs PNG bytes for PDF embedding.
Uses matplotlib (Agg backend for thread-safety in Streamlit).
"""
import io
import logging
import matplotlib
matplotlib.use("Agg")  # Thread-safe backend — MUST be before pyplot import
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

COLORS = [
    "#2563EB", "#7C3AED", "#059669", "#D97706", "#DC2626",
    "#0891B2", "#4F46E5", "#15803D", "#B45309", "#9333EA",
]

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#FAFAFA",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
})


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def generate_charts(
    df: pd.DataFrame,
    insights: list,
    max_charts: int = 5,
    width: int = 800,
    height: int = 500,
) -> list[bytes]:
    """
    Generate charts based on insights.

    Args:
        df: Source DataFrame
        insights: List of Insight objects (with chart_type + columns_involved)
        max_charts: Maximum number of charts
        width/height: Chart dimensions in pixels

    Returns:
        List of PNG bytes (one per chart)
    """
    charts = []
    dpi = 100
    fig_w, fig_h = width / dpi, height / dpi

    for insight in insights[:max_charts]:
        if insight.chart_type == "none":
            continue

        try:
            chart_bytes = _create_chart(
                df, insight.chart_type, insight.columns_involved,
                insight.title, fig_w, fig_h, dpi,
            )
            if chart_bytes:
                charts.append(chart_bytes)
                logger.info("Chart created: %s (%s)", insight.title, insight.chart_type)
        except Exception as e:
            logger.warning("Chart failed for '%s': %s — skipping", insight.title, e)
            continue

    # If no insights produced charts, generate defaults
    if not charts:
        charts = _generate_default_charts(df, max_charts, fig_w, fig_h, dpi)

    return charts


# ---------------------------------------------------------------------------
# Chart creation
# ---------------------------------------------------------------------------

def _create_chart(
    df: pd.DataFrame, chart_type: str, columns: list[str],
    title: str, fig_w: float, fig_h: float, dpi: int,
) -> bytes | None:
    """Create a single chart, return PNG bytes."""
    # Validate columns exist
    valid_cols = [c for c in columns if c in df.columns]
    if not valid_cols:
        return None

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)

    try:
        if chart_type == "bar":
            _draw_bar(df, valid_cols, ax)
        elif chart_type == "line":
            _draw_line(df, valid_cols, ax)
        elif chart_type == "scatter":
            _draw_scatter(df, valid_cols, ax)
        elif chart_type == "pie":
            _draw_pie(df, valid_cols, ax)
        elif chart_type == "heatmap":
            _draw_heatmap(df, valid_cols, ax)
        else:
            _draw_bar(df, valid_cols, ax)  # fallback

        ax.set_title(title, pad=15)
        fig.tight_layout()
        return _fig_to_bytes(fig)

    finally:
        plt.close(fig)


def _draw_bar(df: pd.DataFrame, cols: list[str], ax):
    """Bar chart: categorical distribution or numeric comparison."""
    col = cols[0]
    if df[col].dtype in ["object", "category"] or df[col].nunique() <= 15:
        counts = df[col].value_counts().head(10)
        bars = ax.barh(range(len(counts)), counts.values, color=COLORS[:len(counts)])
        ax.set_yticks(range(len(counts)))
        ax.set_yticklabels(counts.index, fontsize=9)
        ax.set_xlabel("Count")
        ax.invert_yaxis()
    else:
        ax.hist(df[col].dropna(), bins=20, color=COLORS[0], edgecolor="white")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")


def _draw_line(df: pd.DataFrame, cols: list[str], ax):
    """Line chart: trend over index or datetime."""
    for i, col in enumerate(cols[:3]):
        if pd.api.types.is_numeric_dtype(df[col]):
            ax.plot(df.index, df[col], color=COLORS[i % len(COLORS)], label=col, linewidth=1.5)
    ax.legend()
    ax.set_xlabel("Index")


def _draw_scatter(df: pd.DataFrame, cols: list[str], ax):
    """Scatter plot: relationship between 2 numeric columns."""
    if len(cols) >= 2:
        x, y = cols[0], cols[1]
        if pd.api.types.is_numeric_dtype(df[x]) and pd.api.types.is_numeric_dtype(df[y]):
            ax.scatter(df[x], df[y], alpha=0.5, color=COLORS[0], s=20)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            return
    # Fallback: histogram of first col
    _draw_bar(df, cols[:1], ax)


def _draw_pie(df: pd.DataFrame, cols: list[str], ax):
    """Pie chart: category proportions."""
    col = cols[0]
    counts = df[col].value_counts().head(8)
    if len(counts) > 0:
        ax.pie(
            counts.values, labels=counts.index, autopct="%1.1f%%",
            colors=COLORS[:len(counts)], startangle=90,
        )
        ax.axis("equal")


def _draw_heatmap(df: pd.DataFrame, cols: list[str], ax):
    """Correlation heatmap for numeric columns."""
    numeric = df[cols].select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        _draw_bar(df, cols[:1], ax)
        return

    corr = numeric.corr()
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(corr.columns, fontsize=8)
    plt.colorbar(im, ax=ax, shrink=0.8)


# ---------------------------------------------------------------------------
# Default charts (when AI insights don't produce charts)
# ---------------------------------------------------------------------------

def _generate_default_charts(
    df: pd.DataFrame, max_charts: int, fig_w: float, fig_h: float, dpi: int,
) -> list[bytes]:
    """Generate basic charts when no insight-driven charts were made."""
    charts = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Histogram of first numeric column
    if numeric_cols:
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.hist(df[numeric_cols[0]].dropna(), bins=20, color=COLORS[0], edgecolor="white")
        ax.set_title(f"Distribution of {numeric_cols[0]}", pad=15)
        ax.set_xlabel(numeric_cols[0])
        ax.set_ylabel("Frequency")
        fig.tight_layout()
        charts.append(_fig_to_bytes(fig))
        plt.close(fig)

    # Correlation heatmap if enough numeric cols
    if len(numeric_cols) >= 2 and len(charts) < max_charts:
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        _draw_heatmap(df, numeric_cols[:8], ax)
        ax.set_title("Correlation Matrix", pad=15)
        fig.tight_layout()
        charts.append(_fig_to_bytes(fig))
        plt.close(fig)

    return charts


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _fig_to_bytes(fig) -> bytes:
    """Convert matplotlib figure to PNG bytes."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    buf.seek(0)
    return buf.read()
