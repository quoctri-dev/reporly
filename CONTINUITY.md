# Reporly — CONTINUITY

## State
- Phase: 2 — IN PROGRESS (2026-03-25). CC instruction ready.
- Product: AI Report Generator — upload CSV/Excel → AI analyze → PDF/PPTX/DOCX đẹp
- Name: Reporly (confirmed)
- Stack: Python 3.13 + Streamlit + Gemini 2.5 Flash (LiteLLM swap) + pandas + matplotlib + ReportLab
- Billing: Gemini POSTPAY (Visa ••8596, threshold ₫2M)

## Blockers
- Không có blocker. CC instruction tại opus-reports/2026-03-25_08-00_cc-reporly-phase2.md

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

## Next
- Anh paste CC instruction → CC build Phase 2 (PD1→PD2→PD3→PD4)
- Sau CC xong: test 3 samples + review report → chuẩn bị deploy Streamlit Cloud
