"""
Reporly — Report Templates (3 built-in styles)
Each template defines colors, fonts, and sizing for consistent report output.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    """Report style template — used by all exporters (PDF, PPTX, DOCX)."""
    name: str
    primary_color: str
    secondary_color: str
    accent_color: str
    font_heading: str
    font_body: str
    font_size_title: int
    font_size_heading: int
    font_size_body: int
    font_size_caption: int
    header_style: str       # "clean", "boxed", "gradient"
    table_style: str        # "minimal", "bordered", "striped"


MINIMAL = Template(
    name="minimal",
    primary_color="#374151",
    secondary_color="#6B7280",
    accent_color="#2563EB",
    font_heading="Helvetica",
    font_body="Helvetica",
    font_size_title=22,
    font_size_heading=14,
    font_size_body=10,
    font_size_caption=8,
    header_style="clean",
    table_style="minimal",
)

CORPORATE = Template(
    name="corporate",
    primary_color="#1E3A5F",
    secondary_color="#2C5F8A",
    accent_color="#B8860B",
    font_heading="Times-Roman",
    font_body="Times-Roman",
    font_size_title=24,
    font_size_heading=14,
    font_size_body=10,
    font_size_caption=8,
    header_style="boxed",
    table_style="bordered",
)

MODERN = Template(
    name="modern",
    primary_color="#6366F1",
    secondary_color="#8B5CF6",
    accent_color="#EC4899",
    font_heading="Helvetica",
    font_body="Helvetica",
    font_size_title=24,
    font_size_heading=14,
    font_size_body=10,
    font_size_caption=8,
    header_style="gradient",
    table_style="striped",
)

TEMPLATES = {
    "minimal": MINIMAL,
    "corporate": CORPORATE,
    "modern": MODERN,
}
