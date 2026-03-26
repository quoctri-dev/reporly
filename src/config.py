"""
Reporly — Configuration (swap layer)
All external dependencies configured here. Swap = change .env, not code.
"""
import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (auto-find closest .env file)
load_dotenv()

# ---------------------------------------------------------------------------
# Config dataclass — single source of truth for all settings
# ---------------------------------------------------------------------------

@dataclass
class Config:
    """Application configuration. All values from .env or defaults."""

    # LLM Provider (swap via .env)
    llm_model: str = "gemini/gemini-2.0-flash"
    llm_api_key: str = ""
    llm_temperature: float = 0.3
    llm_max_tokens: int = 2000

    # Data limits
    max_file_size_mb: int = 10
    max_rows: int = 100_000
    max_columns: int = 50
    max_insights: int = 5

    # PDF settings
    pdf_max_pages: int = 20
    report_title: str = "Data Analysis Report"

    # Chart settings
    max_charts: int = 5
    chart_width: int = 800
    chart_height: int = 500

    # Export settings
    export_format: str = "pdf"          # pdf, pptx, docx
    template_name: str = "nova"

    # App settings
    app_name: str = "Reporly"
    app_version: str = "0.2.0"
    debug: bool = False


def load_config() -> Config:
    """Load config from environment variables with sensible defaults."""
    return Config(
        llm_model=os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash"),
        llm_api_key=os.getenv("LLM_API_KEY", os.getenv("GOOGLE_AI_API_KEY", "")),
        llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.3")),
        llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
        max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "10")),
        max_rows=int(os.getenv("MAX_ROWS", "100000")),
        max_columns=int(os.getenv("MAX_COLUMNS", "50")),
        max_insights=int(os.getenv("MAX_INSIGHTS", "5")),
        pdf_max_pages=int(os.getenv("PDF_MAX_PAGES", "20")),
        report_title=os.getenv("REPORT_TITLE", "Data Analysis Report"),
        max_charts=int(os.getenv("MAX_CHARTS", "5")),
        export_format=os.getenv("EXPORT_FORMAT", "pdf"),
        template_name=os.getenv("TEMPLATE_NAME", "nova"),
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_config(config: Config) -> list[str]:
    """Validate config, return list of errors (empty = OK)."""
    errors = []
    if not config.llm_api_key:
        errors.append(
            "LLM_API_KEY not set. "
            "Set LLM_API_KEY in .env or use GOOGLE_AI_API_KEY for Gemini."
        )
    if config.max_file_size_mb < 1:
        errors.append("MAX_FILE_SIZE_MB must be >= 1")
    if config.max_rows < 100:
        errors.append("MAX_ROWS must be >= 100")
    return errors
