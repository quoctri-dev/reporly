"""
Reporly — AI Analysis Engine
Sends data profile to LLM, gets structured insights back.
Depends on: providers (LLM), models (dataclasses). NOT on pandas directly.
"""
import json
import logging
from .models import DataProfile, Insight

logger = logging.getLogger(__name__)


def analyze_data(
    profile: DataProfile,
    data_sample_str: str,
    call_llm_fn,
    model: str | None = None,
    api_key: str | None = None,
    max_insights: int = 5,
    max_tokens: int = 8000,
) -> list[Insight]:
    """
    Generate AI insights from data profile.

    Args:
        profile: DataProfile from detector
        data_sample_str: String representation of first N rows
        call_llm_fn: LLM calling function (dependency injection)
        model: LLM model string
        api_key: API key
        max_insights: Number of insights to generate
        max_tokens: Max LLM response tokens

    Returns:
        List of Insight objects
    """
    prompt = _build_analysis_prompt(profile, data_sample_str, max_insights)

    try:
        response = call_llm_fn(
            prompt=prompt,
            model=model,
            api_key=api_key,
            temperature=0.3,
            max_tokens=max_tokens,
        )
        logger.debug("LLM raw response:\n%s", response.content[:500])
        insights = _parse_insights(response.content)
        if not insights:
            logger.warning("LLM returned content but parsing yielded 0 insights — falling back")
            return _fallback_insights(profile)
        logger.info("AI analysis complete: %d insights generated", len(insights))
        return insights

    except Exception as e:
        logger.error("AI analysis failed: %s — returning fallback insights", str(e))
        return _fallback_insights(profile)


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def _build_analysis_prompt(
    profile: DataProfile, sample_str: str, max_insights: int
) -> str:
    """Build the analysis prompt for LLM."""

    # Column summary
    col_summary = "\n".join(
        f"  - {ci.name} ({ci.dtype}): {ci.unique_count} unique, "
        f"{ci.null_pct}% null"
        + (f", range [{ci.stats.get('min')}-{ci.stats.get('max')}]"
           if ci.stats else "")
        for ci in profile.column_info
    )

    # Warnings
    warn_str = "\n".join(f"  - {w}" for w in profile.warnings) if profile.warnings else "  None"

    return f"""You are a senior data analyst writing a business report. Analyze this dataset and provide exactly {max_insights} actionable insights.

DATASET:
- File: {profile.filename} ({profile.rows:,} rows, {profile.columns} columns)
- Numeric columns: {profile.basic_stats.get('numeric_columns', 0)}
- Categorical columns: {profile.basic_stats.get('categorical_columns', 0)}

COLUMNS:
{col_summary}

DATA QUALITY:
{warn_str}

SAMPLE DATA:
{sample_str}

RESPOND WITH ONLY A JSON ARRAY (no markdown, no text before/after):
[
  {{
    "title": "Concise insight title",
    "description": "2-3 sentences with SPECIFIC numbers from the data. State what it means for the business and what action to take.",
    "importance": "high|medium|low",
    "chart_type": "bar|line|scatter|pie|heatmap|none",
    "columns_involved": ["col1", "col2"]
  }}
]

INSIGHT RULES:
- Be SPECIFIC: "Email channel has highest ROI at 350%" not "Revenue varies across channels"
- Mention ACTUAL values, percentages, or comparisons from the data
- Include a recommended ACTION for each insight
- Chart type guide: bar (compare categories), line (trends over time), scatter (correlations between numerics), pie (proportions of a whole), heatmap (cross-tabulations)
- Order by business impact (most actionable first)
- columns_involved MUST be exact column names from the dataset"""


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def _parse_insights(response_text: str) -> list[Insight]:
    """Parse LLM response into Insight objects."""
    # Try to extract JSON from response
    text = response_text.strip()

    # Handle markdown code blocks
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    # Try full parse first (handles both array and object wrapper)
    data = None
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            data = parsed
        elif isinstance(parsed, dict):
            # Handle {"insights": [...]} wrapper
            for v in parsed.values():
                if isinstance(v, list):
                    data = v
                    break
    except json.JSONDecodeError:
        pass

    # Fallback: find JSON array in text
    if data is None:
        start = text.find("[")
        end = text.rfind("]") + 1
        if start == -1 or end == 0:
            logger.warning("No JSON array found in LLM response")
            return []
        try:
            data = json.loads(text[start:end])
        except json.JSONDecodeError as e:
            logger.warning("JSON parse failed: %s", str(e))
            return []

    insights = []
    for item in data:
        if not isinstance(item, dict):
            continue
        try:
            insights.append(Insight(
                title=str(item.get("title", "Untitled")),
                description=str(item.get("description", "")),
                importance=str(item.get("importance", "medium")),
                chart_type=str(item.get("chart_type", "none")),
                columns_involved=item.get("columns_involved", []),
            ))
        except Exception:
            continue

    return insights


# ---------------------------------------------------------------------------
# Fallback (graceful degradation — SP9)
# ---------------------------------------------------------------------------

def _fallback_insights(profile: DataProfile) -> list[Insight]:
    """Generate basic statistical insights when LLM fails."""
    insights = []

    # Null analysis
    total_nulls = profile.basic_stats.get("total_nulls", 0)
    if total_nulls > 0:
        insights.append(Insight(
            title="Missing Data Detected",
            description=(
                f"Dataset has {total_nulls:,} missing values "
                f"({profile.basic_stats.get('null_pct', 0)}% of all cells). "
                "Consider data cleaning before analysis."
            ),
            importance="high",
            chart_type="bar",
            columns_involved=[
                ci.name for ci in profile.column_info if ci.null_pct > 10
            ],
        ))

    # Numeric range insights
    for ci in profile.column_info:
        if ci.dtype == "numeric" and ci.stats:
            insights.append(Insight(
                title=f"{ci.name} Distribution",
                description=(
                    f"{ci.name} ranges from {ci.stats['min']} to {ci.stats['max']} "
                    f"(mean: {ci.stats['mean']}, median: {ci.stats['median']}). "
                    f"Std dev: {ci.stats.get('std', 'N/A')}."
                ),
                importance="medium",
                chart_type="bar",
                columns_involved=[ci.name],
            ))
            if len(insights) >= 5:
                break

    return insights[:5]
