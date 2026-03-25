# Reporly — AI Report Generator

Upload your data, AI analyzes it, download a professional report (PDF, PPTX, or DOCX) in minutes.

## Features

- **Multi-format export**: PDF, PowerPoint (PPTX), Word (DOCX)
- **3 report templates**: Minimal, Corporate, Modern
- **AI-powered insights**: Automatic pattern detection and analysis
- **Smart charts**: Auto-generated visualizations based on your data
- **Encoding detection**: Handles UTF-8, Latin-1, CP1252 automatically
- **Self-healing**: Graceful error handling with user-friendly messages
- **Swap-ready AI**: Change LLM provider via `.env` — no code changes

## Quick Start

```bash
# 1. Clone
git clone <your-repo-url>
cd project-reporly

# 2. Install
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env: add your LLM_API_KEY (get free from https://aistudio.google.com/apikey)

# 4. Run
streamlit run app.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODEL` | `gemini/gemini-2.0-flash` | Any LiteLLM model string |
| `LLM_API_KEY` | — | Required: API key for chosen provider |
| `EXPORT_FORMAT` | `pdf` | Default export: pdf, pptx, docx |
| `TEMPLATE_NAME` | `minimal` | Default template: minimal, corporate, modern |
| `MAX_FILE_SIZE_MB` | 10 | Max upload size |
| `MAX_INSIGHTS` | 5 | Number of AI insights |
| `MAX_CHARTS` | 5 | Number of charts |

Swap AI provider: change `LLM_MODEL` + `LLM_API_KEY` in `.env`. No code change needed.

## Supported Input Formats

- CSV (.csv)
- Excel (.xlsx, .xls)
- TSV (.tsv)

## Tech Stack

- **UI**: Streamlit
- **AI**: LiteLLM (Gemini, OpenAI, Claude, etc.)
- **Charts**: matplotlib
- **Export**: ReportLab (PDF), python-pptx (PPTX), python-docx (DOCX)
- **Data**: pandas, numpy

## Architecture

```
app.py              <- Streamlit UI (wiring layer)
  |
src/config.py       <- All settings from .env
src/providers/      <- LLM adapter (LiteLLM, swap-ready)
src/core/           <- Business logic (detector + analyzer + models + health)
src/charts/         <- Chart generation (matplotlib)
src/io/             <- File reader + PDF/PPTX/DOCX exporters
src/templates/      <- 3 built-in report styles
```

Dependency direction: config <- providers <- core <- io <- app

## License

MIT
