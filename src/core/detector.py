"""
Reporly — Data Detection & Profiling (no external provider dependency)
Analyzes uploaded DataFrame: column types, stats, quality warnings.
"""
import pandas as pd
import numpy as np
from .models import DataProfile, ColumnInfo


def detect_data(df: pd.DataFrame, filename: str = "uploaded_file") -> DataProfile:
    """
    Profile a DataFrame: detect types, compute stats, flag quality issues.

    Args:
        df: Input DataFrame
        filename: Original filename for the report

    Returns:
        DataProfile with complete metadata
    """
    column_info = [_analyze_column(df[col]) for col in df.columns]
    basic_stats = _compute_basic_stats(df)
    warnings = _detect_quality_issues(df, column_info)

    return DataProfile(
        filename=filename,
        rows=len(df),
        columns=len(df.columns),
        column_info=column_info,
        basic_stats=basic_stats,
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _classify_dtype(series: pd.Series) -> str:
    """Classify a pandas Series into our simplified types."""
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    # Try to detect datetime strings
    if series.dtype == object:
        sample = series.dropna().head(20)
        if len(sample) > 0:
            try:
                pd.to_datetime(sample)
                return "datetime"
            except (ValueError, TypeError):
                pass

        # Categorical vs text: low unique ratio = categorical
        unique_ratio = series.nunique() / max(len(series), 1)
        if unique_ratio < 0.3 or series.nunique() <= 20:
            return "categorical"
        return "text"

    return "text"


def _analyze_column(series: pd.Series) -> ColumnInfo:
    """Build ColumnInfo for a single column."""
    dtype = _classify_dtype(series)
    null_count = int(series.isna().sum())
    total = len(series)

    stats = {}
    if dtype == "numeric":
        clean = series.dropna()
        if len(clean) > 0:
            stats = {
                "mean": round(float(clean.mean()), 2),
                "median": round(float(clean.median()), 2),
                "min": round(float(clean.min()), 2),
                "max": round(float(clean.max()), 2),
                "std": round(float(clean.std()), 2) if len(clean) > 1 else 0,
            }

    sample = series.dropna().head(5).tolist()

    return ColumnInfo(
        name=series.name,
        dtype=dtype,
        null_count=null_count,
        null_pct=round(null_count / max(total, 1) * 100, 1),
        unique_count=int(series.nunique()),
        sample_values=sample,
        stats=stats,
    )


def _compute_basic_stats(df: pd.DataFrame) -> dict:
    """Compute dataset-level statistics."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = [
        c for c in df.columns if _classify_dtype(df[c]) == "categorical"
    ]

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "numeric_columns": len(numeric_cols),
        "categorical_columns": len(categorical_cols),
        "total_nulls": int(df.isna().sum().sum()),
        "null_pct": round(df.isna().sum().sum() / max(df.size, 1) * 100, 1),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
    }


def _detect_quality_issues(
    df: pd.DataFrame, column_info: list[ColumnInfo]
) -> list[str]:
    """Flag potential data quality issues."""
    warnings = []

    # High null columns
    for ci in column_info:
        if ci.null_pct > 50:
            warnings.append(f"Column '{ci.name}' has {ci.null_pct}% null values")

    # Duplicate rows
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        dup_pct = round(dup_count / len(df) * 100, 1)
        warnings.append(f"{dup_count} duplicate rows ({dup_pct}%)")

    # Single-value columns (no info)
    for ci in column_info:
        if ci.unique_count <= 1 and ci.null_count < len(df):
            warnings.append(f"Column '{ci.name}' has only 1 unique value — no info")

    return warnings
