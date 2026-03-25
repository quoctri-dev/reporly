# Reporly — CONTINUITY

## State
- Phase: 2 — PAUSED (2026-03-25). PD1-PD4 code done, UI/UX cần redesign.
- Product: AI Report Generator — upload CSV/Excel → AI analyze → PDF/PPTX/DOCX đẹp
- Name: Reporly (confirmed)
- Stack: Python 3.13 + Streamlit + Gemini 2.5 Flash (LiteLLM swap) + pandas + matplotlib + ReportLab
- Billing: Gemini POSTPAY (Visa ••8596, threshold ₫2M)

## Blockers
- UI/UX quá basic (Streamlit default) — cần redesign modern, multi-layer, professional

## Key Decisions
- 2026-03-23: Focus AI Report Generator. Positioning = OUTPUT QUALITY.
- 2026-03-23: Dual-purpose: product + Upwork portfolio.
- 2026-03-25: Tên = Reporly. General MVP. Python 3.13. Stage 2 modular.
- 2026-03-25: gemini-2.0-flash deprecated → swap gemini-2.5-flash + max_tokens 8000
- 2026-03-25: Cowork build structure → CC fix/test = best workflow for code projects

## Phase 1 Results
- 10/10 checklist PASS. 3/3 sample files OK (incl. messy edge cases)
- 5/5 AI-driven insights (actionable, specific)
- PDF export: 92-136 KB, professional layout
- Portfolio: 2 sample PDFs saved in portfolio/
- Competitor search done: Powerdrill Bloom = main threat, gap still valid

## Open Questions
- Vertical niche: marketing reports? survey reports? (post Phase 3)
- Open-source strategy? (competitive advantage vs Powerdrill $19.90/mo)

## Phase 2 Progress
- PD1 DONE: PPTX + DOCX export + template system (3 styles)
- PD2 DONE: Sidebar + multi-format + analytics
- PD3 DONE: Input validation + self-healing
- PD4 DONE: Deploy config + git init
- PENDING: UI/UX redesign (modern, multi-layer)

## Next
- UI/UX redesign: search trends + Grok input → modern professional interface
- Test 3 formats × 3 templates × 3 datasets
- Deploy Streamlit Cloud
