"""
Reporly — Report Template (NoVa default style)
Single template with NoVa brand colors for all report exports.
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


NOVA = Template(
    name="nova",
    primary_color="#f43f5e",      # NoVa rose
    secondary_color="#8b5cf6",    # NoVa purple
    accent_color="#fb923c",       # NoVa orange
    font_heading="Helvetica",
    font_body="Helvetica",
    font_size_title=22,
    font_size_heading=14,
    font_size_body=10,
    font_size_caption=8,
    header_style="clean",
    table_style="minimal",
)

TEMPLATES = {
    "nova": NOVA,
}
