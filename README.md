<p align="center">
  <h1 align="center">Reporly</h1>
  <p align="center"><strong>Turn raw data into professional reports with AI — in under 2 minutes.</strong></p>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AI-Gemini%20%7C%20Claude%20%7C%20Groq-orange" alt="AI Providers">
  <img src="https://img.shields.io/badge/export-PDF%20%7C%20PPTX%20%7C%20DOCX-green" alt="Export Formats">
  <img src="https://img.shields.io/github/license/quoctri-dev/reporly" alt="License">
</p>

---

## The Problem

You have CSV or Excel data. You need a professional report — with insights, charts, and clean formatting. Normally that means hours in Excel, then copy-pasting into PowerPoint or Word.

**Reporly does it in 3 steps:** upload your file → AI analyzes the data → download a ready-to-share report.

---

## Quick Start

```bash
git clone https://github.com/quoctri-dev/reporly.git
cd reporly

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Add your API key → get one free at https://aistudio.google.com/apikey

streamlit run app.py
```

Open `localhost:8501` → upload any CSV → get your report.

5 sample datasets included in `sample-data/` to try immediately.

---

## Features

### AI-Powered Analysis
Upload any tabular data and the AI detects patterns, trends, anomalies, and generates structured insights — no prompting required.

### 3 Export Formats
Download reports as **PDF** (ReportLab), **PowerPoint** (python-pptx), or **Word** (python-docx). Each format is purpose-built, not a simple conversion.

### 3 Report Templates

| Template | Style | Best For |
|----------|-------|----------|
| **Minimal** | Clean, light, spacious | Internal reviews, quick shares |
| **Corporate** | Navy headers, formal layout | Client presentations, board reports |
| **Modern** | Bold gradients, accent colors | Marketing reports, stakeholder decks |

### Smart Charts
AI suggests the right chart types based on your data structure. Charts are auto-generated and embedded in every export format.

### Self-Healing Pipeline
If the AI provider fails or returns unexpected output, Reporly falls back to statistical analysis automatically. No crashes, no blank reports.

### Swappable AI Provider
Switch between AI providers by changing one line in `.env` — no code changes:

```env
LLM_MODEL=gemini/gemini-2.0-flash    # Google (default, free tier available)
LLM_MODEL=claude-sonnet-4-6         # Anthropic
LLM_MODEL=groq/llama-3.1-70b         # Groq (free)
```

### Dashboard UI
Dark-themed interface with 4 interactive tabs — Data overview, AI Insights, Charts, and Export. Glassmorphism cards, Google Fonts, responsive layout.

### Encoding Detection
Auto-handles UTF-8, Latin-1, CP1252, and other common encodings. Messy CSVs from legacy systems just work.

---

## How It Works

```
Upload (CSV / Excel / TSV)
  → Reader (encoding detection, validation, size limits)
    → Detector (column types, distributions, anomalies)
      → Analyzer (AI-powered insights via LiteLLM)
        → Charts (matplotlib, auto-selected chart types)
          → Exporter (PDF / PPTX / DOCX with chosen template)
```

Each step runs independently. If any step fails, the pipeline continues with what it has — that's the self-healing design.

---

## Configuration

All settings live in `.env`. Copy `.env.example` to get started.

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_API_KEY` | — | **Required.** Your AI provider API key |
| `LLM_MODEL` | `gemini/gemini-2.0-flash` | Any [LiteLLM-compatible model](https://docs.litellm.ai/docs/providers) |
| `MAX_INSIGHTS` | `5` | Number of AI insights per report |
| `MAX_CHARTS` | `5` | Number of auto-generated charts |
| `MAX_FILE_SIZE_MB` | `10` | Upload size limit |

---

## Architecture

```
app.py                     ← Streamlit UI wiring (228 lines)
src/
├── config.py              ← Settings from .env (single source of truth)
├── providers/             ← LLM adapter (LiteLLM — swap-ready)
├── core/
│   ├── detector.py        ← Column type detection + data profiling
│   ├── analyzer.py        ← AI analysis orchestration
│   ├── models.py          ← Data models (dataclasses)
│   ├── health.py          ← Self-healing + error classification
│   └── analytics.py       ← Sidebar statistics
├── charts/
│   └── generator.py       ← Chart generation (matplotlib)
├── io/
│   ├── reader.py          ← File reader (CSV/Excel/TSV + encoding)
│   ├── exporter.py        ← PDF export (ReportLab)
│   ├── pptx_exporter.py   ← PowerPoint export
│   └── docx_exporter.py   ← Word export
├── templates/
│   └── styles.py          ← 3 report templates (dataclass-based)
└── ui/
    ├── styles.py          ← Custom CSS + glassmorphism components
    └── tabs.py            ← Tab renderers (Data/Insights/Charts/Export)
```

**Dependency direction:** `config → providers → core → charts → io → ui → app`

Every module stays under 300 lines. Clean separation — swap any layer without touching the others.

**Total:** ~2,900 lines across 18 modules.

---

## Sample Reports

Two pre-generated sample reports in [`portfolio/`](./portfolio/) show output quality:

- **E-commerce Sales Analysis** — revenue trends, top products, seasonal patterns
- **Marketing Campaign Performance** — ROI by channel, conversion analysis, recommendations

---

## Limitations

- **10MB upload limit** — designed for operational data, not big data pipelines
- **AI quality varies by provider** — Gemini Flash is fast but less nuanced than Claude for complex datasets
- **Charts are auto-generated** — matplotlib basics, not custom D3 visualizations
- **File upload only** — no direct database connections (CSV, Excel, TSV)
- **Single-user** — Streamlit session-based, not multi-tenant

---

## License

[MIT](LICENSE) — use it however you want.
