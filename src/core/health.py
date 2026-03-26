"""
Reporly — Self-Healing & Error Classification
Validates setup, classifies errors, and provides user-friendly messages.
"""
import os
import sys
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class ErrorCategory(Enum):
    DATA_ERROR = "data"
    LLM_ERROR = "llm"
    EXPORT_ERROR = "export"
    CONFIG_ERROR = "config"
    UNKNOWN = "unknown"


@dataclass
class ErrorInfo:
    category: ErrorCategory
    message: str
    suggestion: str
    original: Exception | None = None


# ---------------------------------------------------------------------------
# Setup validation
# ---------------------------------------------------------------------------

def validate_setup() -> list[str]:
    """
    Run 5-layer health check. Returns list of warnings (empty = all OK).
    """
    warnings = []

    # 1. Python version
    if sys.version_info < (3, 9):
        warnings.append(
            f"Python {sys.version_info.major}.{sys.version_info.minor} detected. "
            "Reporly requires Python 3.9+."
        )

    # 2. Required packages
    required = ["streamlit", "pandas", "litellm", "reportlab", "pptx", "docx"]
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            warnings.append(f"Package '{pkg}' not installed. Run: pip install -r requirements.txt")

    # 3. .env + API key
    env_path = Path(".env")
    if not env_path.exists():
        warnings.append("No .env file found. Copy .env.example to .env and set your API key.")
    api_key = os.getenv("LLM_API_KEY", os.getenv("GOOGLE_AI_API_KEY", ""))
    if not api_key:
        warnings.append("LLM_API_KEY not set. AI analysis will not work.")

    # 4. LLM reachability (quick check — skip if no key)
    if api_key:
        try:
            from litellm import completion
            model = os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash")
            completion(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5,
                api_key=api_key,
            )
        except Exception as e:
            warnings.append(f"LLM API not reachable: {str(e)[:100]}")

    # 5. Write permission
    try:
        test_path = Path("/tmp/reporly_health_check")
        test_path.write_text("ok")
        test_path.unlink()
    except Exception:
        warnings.append("No write permission for temp directory.")

    return warnings


# ---------------------------------------------------------------------------
# Error classification
# ---------------------------------------------------------------------------

def classify_error(exc: Exception) -> ErrorInfo:
    """Classify an exception into a user-friendly ErrorInfo."""
    exc_str = str(exc).lower()
    exc_type = type(exc).__name__

    # Data errors
    if exc_type in ("FileReadError", "ParserError", "EmptyDataError"):
        return ErrorInfo(
            category=ErrorCategory.DATA_ERROR,
            message="There was a problem reading your data file.",
            suggestion="Check that the file is a valid CSV or Excel file, and try re-saving it as UTF-8 CSV.",
            original=exc,
        )
    if "encoding" in exc_str or "codec" in exc_str or "decode" in exc_str:
        return ErrorInfo(
            category=ErrorCategory.DATA_ERROR,
            message="File encoding issue detected.",
            suggestion="Try re-saving the file as UTF-8 encoded CSV.",
            original=exc,
        )

    # LLM errors
    if any(k in exc_str for k in ("api", "rate limit", "quota", "authentication", "401", "403", "429")):
        return ErrorInfo(
            category=ErrorCategory.LLM_ERROR,
            message="AI service error — the analysis could not be completed.",
            suggestion="Check your API key in .env, or try again in a few minutes if rate-limited.",
            original=exc,
        )
    if any(k in exc_str for k in ("timeout", "connection", "unreachable")):
        return ErrorInfo(
            category=ErrorCategory.LLM_ERROR,
            message="Could not reach the AI service.",
            suggestion="Check your internet connection and try again.",
            original=exc,
        )

    # Export errors
    if any(k in exc_str for k in ("reportlab", "pptx", "docx", "pdf", "export")):
        return ErrorInfo(
            category=ErrorCategory.EXPORT_ERROR,
            message="Report export failed.",
            suggestion="Try a different export format, or check that all dependencies are installed.",
            original=exc,
        )

    # Config errors
    if any(k in exc_str for k in ("env", "config", "key not set", "missing")):
        return ErrorInfo(
            category=ErrorCategory.CONFIG_ERROR,
            message="Configuration error.",
            suggestion="Check your .env file and ensure all required values are set.",
            original=exc,
        )

    # Unknown
    return ErrorInfo(
        category=ErrorCategory.UNKNOWN,
        message=f"An unexpected error occurred: {exc_type}",
        suggestion="Please try again. If the problem persists, check the logs.",
        original=exc,
    )


def get_user_message(error_info: ErrorInfo) -> str:
    """Format ErrorInfo into a single user-friendly message."""
    return f"❌ {error_info.message}\n\n💡 **Try:** {error_info.suggestion}"
