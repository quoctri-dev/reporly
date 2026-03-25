"""
Reporly — Data models (Layer 0: depends on NOTHING)
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ColumnInfo:
    """Metadata about a single column."""
    name: str
    dtype: str           # numeric, categorical, datetime, text
    null_count: int
    null_pct: float
    unique_count: int
    sample_values: list = field(default_factory=list)
    stats: dict = field(default_factory=dict)  # mean, median, min, max (numeric only)


@dataclass
class DataProfile:
    """Complete profile of uploaded dataset."""
    filename: str
    rows: int
    columns: int
    column_info: list[ColumnInfo] = field(default_factory=list)
    basic_stats: dict = field(default_factory=dict)  # summary statistics
    warnings: list[str] = field(default_factory=list)  # data quality warnings


@dataclass
class Insight:
    """A single AI-generated insight about the data."""
    title: str
    description: str
    importance: str      # high, medium, low
    chart_type: str      # bar, line, scatter, pie, heatmap, none
    columns_involved: list[str] = field(default_factory=list)


@dataclass
class Report:
    """Complete report ready for export."""
    title: str
    data_profile: DataProfile
    insights: list[Insight] = field(default_factory=list)
    charts: list[bytes] = field(default_factory=list)  # PNG images
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)
