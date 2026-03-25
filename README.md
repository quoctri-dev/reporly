# Reporly — AI Report Generator

> Upload any data → AI understands it → Professional report in 2 minutes

## What It Does

Reporly turns raw CSV/Excel data into professional reports with AI-powered insights.

- Upload CSV, Excel, or TSV files (max 10MB)
- AI automatically detects patterns, trends, and anomalies
- Download reports as PDF, PowerPoint, or Word
- 3 built-in templates: Minimal, Corporate, Modern
- Dark dashboard UI with interactive exploration

## Quick Start

```bash
# 1. Clone
git clone https://github.com/quoctri-dev/reporly.git
cd reporly

# 2. Setup
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env → add your LLM_API_KEY (get free: https://aistudio.google.com/apikey)

# 4. Run
streamlit run app.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_API_KEY` | — | **Required.** API key for AI provider |
| `LLM_MODEL` | `gemini/gemini-2.0-flash` | Any [LiteLLM model string](https://docs.litellm.ai/docs/providers) |
| `MAX_INSIGHTS` | `5` | Number of AI insights to generate |
| `MAX_CHARTS` | `5` | Number of charts to generate |
| `MAX_FILE_SIZE_MB` | `10` | Max upload file size |

**Swap AI provider:** change `LLM_MODEL` + `LLM_API_KEY` in `.env`. No code changes needed.

| Provider | Model String | Key Source |
|----------|-------------|------------|
| Google Gemini | `gemini/gemini-2.0-flash` | [AI Studio](https://aistudio.google.com/apikey) |
| Anthropic Claude | `claude-sonnet-4-6` | [Console](https://console.anthropic.com) |
| Groq (free) | `groq/llama-3.1-70b` | [Console](https://console.groq.com) |

## Features

- **AI Analysis** — LLM-powered pattern detection with structured insights
- **Smart Charts** — Auto-generated matplotlib visualizations based on AI suggestions
- **3 Export Formats** — PDF (ReportLab), PowerPoint (python-pptx), Word (python-docx)
- **3 Templates** — Minimal (clean), Corporate (formal navy), Modern (bold gradient)
- **Self-Healing** — Graceful degradation: LLM fails → fallback to raw stats, no crash
- **Dashboard UI** — Dark theme, 4 tabs, glassmorphism cards, Google Fonts
- **Swappable AI** — Change provider in `.env`, architecture stays the same
- **Encoding Detection** — Auto-handles UTF-8, Latin-1, CP1252

## Architecture

```
app.py                  ← Streamlit wiring (dashboard layout, tabs)
  │
src/config.py           ← All settings from .env
src/providers/          ← LLM adapter (LiteLLM, swap-ready)
src/core/               ← Business logic (detector, analyzer, models, health)
src/charts/             ← Chart generation (matplotlib)
src/io/                 ← File reader + PDF/PPTX/DOCX exporters
src/templates/          ← 3 built-in report styles
src/ui/                 ← Custom CSS + tab renderers
```

Dependency direction: `config → providers → core → charts → io → ui → app`

Each module < 300 lines. Clean separation of concerns.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit 1.55, custom CSS |
| AI | LiteLLM (Gemini, Claude, Groq, etc.) |
| Charts | matplotlib, Plotly |
| PDF Export | ReportLab |
| PPTX Export | python-pptx |
| DOCX Export | python-docx |
| Data | pandas, openpyxl |
| Runtime | Python 3.13 |

## License

MIT
