"""
Reporly — File Reader
Reads CSV/Excel uploads into pandas DataFrame with validation.
"""
import io
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class FileReadError(Exception):
    """Raised when file cannot be read."""
    pass


def read_uploaded_file(
    uploaded_file,
    max_size_mb: int = 10,
    max_rows: int = 100_000,
    max_columns: int = 50,
) -> pd.DataFrame:
    """
    Read uploaded file (Streamlit UploadedFile or file-like) into DataFrame.

    Args:
        uploaded_file: Streamlit UploadedFile or file-like object
        max_size_mb: Maximum file size in MB
        max_rows: Maximum rows to read
        max_columns: Maximum columns allowed

    Returns:
        Cleaned pandas DataFrame

    Raises:
        FileReadError: On validation failure or read error
    """
    filename = getattr(uploaded_file, "name", "unknown")
    file_size = getattr(uploaded_file, "size", 0)

    # Validate size
    if file_size > max_size_mb * 1024 * 1024:
        raise FileReadError(
            f"File too large: {file_size / 1024 / 1024:.1f}MB "
            f"(max: {max_size_mb}MB)"
        )

    # Read based on extension
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    try:
        if ext == "csv":
            df = _read_csv(uploaded_file)
        elif ext in ("xlsx", "xls"):
            df = _read_excel(uploaded_file)
        elif ext == "tsv":
            df = _read_csv(uploaded_file, sep="\t")
        else:
            raise FileReadError(
                f"Unsupported format: .{ext}. Supported: .csv, .xlsx, .xls, .tsv"
            )
    except FileReadError:
        raise
    except Exception as e:
        raise FileReadError(f"Failed to read file: {str(e)}")

    # Validate dimensions
    if len(df) == 0:
        raise FileReadError("File is empty (0 rows)")
    if len(df.columns) > max_columns:
        raise FileReadError(
            f"Too many columns: {len(df.columns)} (max: {max_columns})"
        )
    if len(df) > max_rows:
        logger.warning("File has %d rows, truncating to %d", len(df), max_rows)
        df = df.head(max_rows)

    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]

    # Handle duplicate column names
    seen = {}
    new_cols = []
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
            logger.warning("Duplicate column '%s' renamed to '%s_%d'", col, col, seen[col])
        else:
            seen[col] = 0
            new_cols.append(col)
    df.columns = new_cols

    # Drop all-empty columns
    empty_cols = [c for c in df.columns if df[c].isna().all()]
    if empty_cols:
        logger.warning("Dropping %d all-empty columns: %s", len(empty_cols), empty_cols)
        df = df.drop(columns=empty_cols)

    # Validate header row (check if first row looks like data, not headers)
    unnamed_count = sum(1 for c in df.columns if c.startswith("Unnamed"))
    if unnamed_count > len(df.columns) * 0.5:
        logger.warning("Many unnamed columns (%d/%d) — file may be missing headers",
                        unnamed_count, len(df.columns))

    logger.info(
        "File read OK: %s (%d rows x %d cols)",
        filename, len(df), len(df.columns),
    )
    return df


# ---------------------------------------------------------------------------
# Internal readers
# ---------------------------------------------------------------------------

def _read_csv(uploaded_file, sep: str = ",") -> pd.DataFrame:
    """Read CSV with encoding detection."""
    content = uploaded_file.read()
    uploaded_file.seek(0)  # Reset for potential re-read

    # Try UTF-8 first, then latin-1 as fallback
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            return pd.read_csv(
                io.BytesIO(content),
                sep=sep,
                encoding=encoding,
                on_bad_lines="skip",
            )
        except UnicodeDecodeError:
            continue

    raise FileReadError("Could not decode file with any supported encoding")


def _read_excel(uploaded_file) -> pd.DataFrame:
    """Read Excel file (first sheet)."""
    return pd.read_excel(uploaded_file, engine="openpyxl")
