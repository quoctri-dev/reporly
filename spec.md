# Reporly Phase 1 — MVP Spec (SDD)
> Last updated: 2026-03-25 | Status: BUILDING

---

## SP1. Requirements Summary
- **What:** Upload CSV/Excel → AI analyze → export PDF report đẹp
- **Why:** Gap thị trường: tools phân tích giỏi nhưng output xấu. Reporly = output chuyên nghiệp
- **Who:** SMBs, non-technical users cần reports nhanh

## SP2. Architecture Decisions
- **Pattern:** Modular monolith (Stage 2 từ đầu — dự án lâu dài)
- **AI:** Gemini (default, free quota) via LiteLLM → swap Claude/Groq qua .env
- **Charts:** plotly (preview) + matplotlib (PDF static)
- **PDF:** ReportLab (programmatic control)
- **Data:** pandas + openpyxl
- **UI:** Streamlit single-page
- **Mode:** Spec-Driven (long-term project)

## SP3. Data Models
```python
@dataclass
class DataProfile:
    filename: str
    rows: int
    columns: int
    column_info: list[ColumnInfo]  # name, dtype, nulls, unique
    basic_stats: dict              # mean, median, min, max per numeric col

@dataclass
class ColumnInfo:
    name: str
    dtype: str           # numeric, categorical, datetime, text
    null_count: int
    unique_count: int
    sample_values: list

@dataclass
class Insight:
    title: str
    description: str
    importance: str      # high, medium, low
    chart_suggestion: str  # bar, line, scatter, pie, heatmap

@dataclass
class Report:
    title: str
    data_profile: DataProfile
    insights: list[Insight]
    charts: list[bytes]    # PNG chart images
    generated_at: datetime
```

## SP4. Phase Plan
- **PD1 Foundation:** config + providers + core/detector (data profiling)
- **PD2 Enrichment:** core/analyzer (AI insights) + charts/generator
- **PD3 Expansion:** io/exporter (PDF generation)
- **PD4 Polish:** app.py (Streamlit UI) + integration test

## SP5. Testing Strategy
- Unit: detector (diverse CSV inputs), analyzer (mock LLM response)
- E2E: upload sample.csv → get PDF → verify file exists + size > 0
- Edge: empty file, 1 row, all-null column, mixed types

## SP6. Constraints
- 1 file upload max 10MB
- Max 50 columns, 100K rows
- PDF max 20 pages
- Mỗi file < 300 lines code
- Total < 10 core files (Stage 2 Cowork)

## SP7. Known Pitfalls
- LLM hallucinate insights không match data → validate insights against actual data
- Large files slow pandas → enforce row/col limits early
- matplotlib thread-safety trong Streamlit → use Agg backend
- ReportLab unicode Vietnamese → set font explicitly

## SP8. Swappable Components
| Component | .env Key | Default | Alternatives | Adapter? |
|-----------|----------|---------|-------------|----------|
| LLM | LLM_MODEL | gemini/gemini-2.0-flash | claude-sonnet-4-6, groq/llama-3.1-70b | LiteLLM router |
| LLM API Key | LLM_API_KEY | GOOGLE_AI_API_KEY value | ANTHROPIC_API_KEY, GROQ_API_KEY | LiteLLM handles |
| Chart lib | — | plotly+matplotlib | — | N/A (Phase 1 fixed) |
| PDF engine | — | ReportLab | — | N/A (Phase 1 fixed) |

## SP9. Self-Healing Strategy
- **Pre-run:** validate_setup() check: Python, packages, .env keys (LLM_MODEL, LLM_API_KEY)
- **Runtime:** LLM call retry 3x backoff → fallback provider if configured
- **Post-run:** verify PDF exists + size > 0
- **Graceful:** Chart fail → skip that chart, still generate report. LLM fail → show raw stats only.

## SP10. Module Contracts
| Module | Public Interface | Depends On |
|--------|-----------------|------------|
| config | get_config() → Config dataclass | .env only |
| providers | call_llm(prompt, model?) → str | config |
| core/detector | detect(df) → DataProfile | pandas (no provider) |
| core/analyzer | analyze(profile, df_sample) → list[Insight] | providers |
| charts | generate_charts(df, insights) → list[bytes] | plotly, matplotlib |
| io/reader | read_file(uploaded) → DataFrame | pandas, openpyxl |
| io/exporter | export_pdf(report) → bytes | ReportLab, charts |
| app | Streamlit UI — wiring | ALL modules |

Dependency direction: config ← providers ← core ← io ← app
