# Reporly — ROADMAP
> Last updated: 2026-03-24 | Phase hiện tại: 0

---

## Vision
> Upload any data → AI understands it → Professional report in 2 minutes
> Positioning: Julius/Powerdrill phân tích giỏi nhưng OUTPUT xấu. Reporly = REPORT ĐẸP.
> Gap: tools hiện tại output = charts trong browser. Reporly output = PDF/PPTX chuyên nghiệp sẵn sàng present.

---

## Phase 0 — FOUNDATION ✅ (current)
> Mục tiêu: Research + setup + hiểu market

**Done:**
- [x] Market research: AI automation tools demand (Upwork validated)
- [x] Competitive landscape: Julius ($20-37/mo), Powerdrill, DashThis, Relevance AI
- [x] Stack assessment: 6/6 match
- [x] Name candidates: Reporly (reporly.ai likely available)
- [x] Project folder + CONTINUITY created

**Deliverables:** Reports trong opus-reports/ (3 files)

**Portfolio value:** Chưa có — foundation chỉ cho internal

---

## Phase 1 — MVP PROTOTYPE (next)
> Mục tiêu: Build bản đầu tiên CHẠY ĐƯỢC — chưa đẹp, chưa scale, chỉ cần HOẠT ĐỘNG
> Timeline estimate: 2-3 tuần (làm chắc, không gấp)

**Scope (STRICT — không thêm):**
- [ ] Upload CSV/Excel file (1 file, max 10MB)
- [ ] AI auto-detect: column types, data structure, basic stats
- [ ] AI analyze: top 5 insights (trends, outliers, correlations)
- [ ] Generate charts: 3-5 charts phù hợp nhất (matplotlib/plotly)
- [ ] Export PDF report: cover page + summary + charts + insights
- [ ] Streamlit UI: upload → loading → preview → download

**Tech decisions:**
- AI: Groq free tier (Llama 3.1 70B) via LiteLLM → swap Claude khi cần
- Charts: plotly (interactive preview) + matplotlib (PDF export)
- PDF: ReportLab hoặc skill /pdf
- Data: pandas + openpyxl
- UI: Streamlit single-page
- Hosting: local dev trước, Streamlit Cloud sau

**KHÔNG làm ở Phase 1:**
- ❌ User accounts / auth
- ❌ Multiple file upload
- ❌ PPTX export (Phase 2)
- ❌ Custom templates
- ❌ API
- ❌ Deployment / hosting

**Khi xong Phase 1 → SEARCH LẠI:**
- [ ] Check competitors có update gì mới không
- [ ] Test với 3-5 sample datasets → list bugs/gaps
- [ ] Đánh giá lại: có đáng tiếp không? Pivot?

**Portfolio value:** Screenshot + demo GIF cho Upwork profile "AI Data Analysis"

---

## Phase 2 — POLISH + DEPLOY
> Mục tiêu: Từ prototype → product dùng được, deploy online
> Timeline estimate: 2 tuần sau Phase 1

**Scope:**
- [ ] UI polish: clean design, loading states, error messages
- [ ] Add PPTX export (skill /pptx)
- [ ] Add DOCX export (skill /docx)
- [ ] Report templates: 3 styles (Minimal, Corporate, Modern)
- [ ] Validate input: file size, format, encoding errors
- [ ] Self-healing: error classification + user-friendly messages (dev-patterns M4)
- [ ] Deploy Streamlit Cloud (free tier)
- [ ] Basic analytics: track usage (Plausible free / simple counter)

**Khi xong Phase 2 → SEARCH LẠI:**
- [ ] Check Streamlit Cloud limitations (traffic, memory)
- [ ] Search SEO keywords: "free AI report generator", "CSV to PDF report"
- [ ] Tìm 5 communities để share (Reddit, IndieHackers, ProductHunt upcoming)

**Portfolio value:** LIVE LINK trên Upwork profile → client click = thấy product thật
- Upwork portfolio piece: "Built AI Report Generator — [link]"
- GitHub repo: public, clean README (platform-engine GitHub Engine)

---

## Phase 3 — PORTFOLIO INTEGRATION + SOFT LAUNCH
> Mục tiêu: Dùng Reporly nâng cấp Upwork profile + lấy users đầu tiên
> Timeline estimate: 1 tuần

**Scope:**
- [ ] Upwork profile update: thêm Reporly vào portfolio
- [ ] GitHub repo: public, README 7-section (platform-engine skill)
- [ ] Create sample reports: 3 industry-specific (marketing, sales, ecommerce)
- [ ] Share trên LinkedIn + X (1 post mỗi nền tảng)
- [ ] Gửi 5-10 người quen/community → feedback
- [ ] Track: bao nhiêu người dùng? Report nào popular nhất?

**Khi xong Phase 3 → SEARCH LẠI:**
- [ ] Analyze feedback: feature requests, bugs, complaints
- [ ] Check adoption metrics: unique users, reports generated
- [ ] Search: "how to launch on Product Hunt 2026" → plan launch
- [ ] Re-evaluate pricing strategy based on real usage

**Portfolio compound:**
- Upwork: "I built this tool that [X] people use" → credibility
- GitHub: stars + forks = social proof
- LinkedIn: post engagement = authority building

---

## Phase 4 — DISTRIBUTION + GROWTH
> Mục tiêu: Grow users từ 0 → 100 active users
> Timeline estimate: 4-6 tuần (ongoing)

**Scope:**
- [ ] SEO: landing page tối ưu cho "AI report generator free"
- [ ] Product Hunt launch: prepare assets + schedule
- [ ] Content marketing: 3-5 blog posts (use cases, tutorials)
- [ ] Community: post trên relevant subreddits, IndieHackers, HackerNews
- [ ] Partnerships: reach out to data/analytics communities
- [ ] Referral: "Made with Reporly" watermark on free tier reports

**Khi xong Phase 4 → SEARCH LẠI:**
- [ ] Traffic sources: SEO working? Product Hunt impact?
- [ ] User retention: bao nhiêu quay lại?
- [ ] Feature requests: nhóm theo frequency → prioritize Phase 5
- [ ] Competitor moves: ai mới launch? pricing changes?

**Portfolio compound:**
- Product Hunt badge → Upwork profile
- "100+ users" metric → proposals
- Blog posts → LinkedIn authority → client trust

---

## Phase 5 — MONETIZATION
> Mục tiêu: Đi từ free → revenue ($1 đầu tiên)
> Timeline estimate: Bắt đầu khi có 50+ weekly active users
> KHÔNG bắt đầu phase này nếu chưa có users thật

**Scope:**
- [ ] Implement freemium tiers:
      Free: 3 reports/month, watermark, basic templates
      Pro $19-29/mo: unlimited, no watermark, premium templates, PPTX/DOCX
      Business $49-79/mo: team sharing, API access, custom branding
- [ ] Payment: Stripe Checkout (hoặc Lemon Squeezy — easier for solo)
- [ ] User accounts: simple auth (Streamlit auth hoặc Supabase free)
- [ ] Usage tracking: reports generated, exports, feature usage
- [ ] Email: simple onboarding sequence (3 emails)

**Khi xong Phase 5 → SEARCH LẠI:**
- [ ] Conversion rate: free → paid? Benchmark vs industry (2-5% typical)
- [ ] Revenue per user: đủ cover costs?
- [ ] Churn: tại sao unsubscribe?
- [ ] Pricing: quá rẻ? quá đắt? A/B test?

**Portfolio compound:**
- "Revenue-generating SaaS" → Upwork credibility LEVEL UP
- Case study: "How I built and monetized an AI tool" → blog + LinkedIn
- Pricing page = proof of real product

---

## Phase 6 — SCALE + EXPAND
> Mục tiêu: Từ side project → real business
> Timeline: Bắt đầu khi MRR > $500 và growing
> Phase này SẼ THAY ĐỔI dựa trên data thật — chỉ outline hướng

**Possible directions (chọn SAU khi có data):**

### 6A. Vertical Niches
- Marketing report templates
- Sales/CRM report templates
- Real estate market reports
- Ecommerce analytics reports
- HR/recruitment reports
- → Mỗi vertical = new user segment + higher willingness-to-pay

### 6B. Platform Expansion
- API cho developers (embed report gen vào app khác)
- MCP plugin cho Claude users (combo Hướng 3)
- Zapier/Make/n8n integration (auto-generate reports from triggers)
- White-label cho agencies

### 6C. AI Enhancement
- Multiple data source connections (Google Sheets, Airtable, databases)
- Natural language queries: "So sánh revenue Q1 vs Q2"
- Scheduled reports: auto-generate weekly/monthly
- AI recommendations: "Based on your data, you should..."

### 6D. Team/Enterprise
- Multi-user workspaces
- Brand kit: custom colors, logos, fonts
- Collaboration: comments, share, approve
- SSO + enterprise security

**Portfolio compound (Phase 6):**
- "SaaS founder" credential → premium Upwork rates ($75-150/hr)
- Speaking/writing opportunities
- Product income supplements freelance income
- Eventually: product > freelance (nếu MRR > freelance income)

---

## Nguyên tắc xuyên suốt

### SEARCH LẠI mỗi phase:
> Cuối MỖI phase → em search competitors, market, pricing, tools mới
> Update ROADMAP nếu cần pivot/adjust
> Không bao giờ build 2 phases liên tục mà không re-validate

### Portfolio compound:
> Mỗi phase PHẢI tạo ra ít nhất 1 portfolio asset cho Upwork
> Phase 1: screenshot/GIF
> Phase 2: live link
> Phase 3: GitHub + social proof
> Phase 4: Product Hunt badge + user metrics
> Phase 5: revenue proof
> Phase 6: "SaaS founder" credential

### Upwork lane riêng:
> Project này KHÔNG ảnh hưởng Upwork work
> Upwork = short-term income → nuôi project
> Project = long-term asset → eventually supplement/replace Upwork
> Feedback loop: Upwork clients' pain → Reporly features

### Technical debt management:
> Phase 1-2: prototype quality OK (ship fast)
> Phase 3+: refactor before adding features
> Every 2 phases: code review + cleanup
> CC bridge: Phase 4+ nếu quá 10 files → chuyển VS Code (build-engine Stage 3)

---

## Competitive Moat Strategy (build dần qua các phases):
1. **Phase 1-2:** No moat — just ship. Product quality = only advantage.
2. **Phase 3-4:** Template library + community feedback → data moat bắt đầu
3. **Phase 5:** Switching cost (user data, saved reports, templates)
4. **Phase 6:** Network effects (shared templates) + vertical expertise + API ecosystem

---

## Risk Registry

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| ChatGPT adds PDF export | High | Medium | Focus UX + templates + niche = differentiation |
| No one pays | Medium | High | Validate ở Phase 3-4 TRƯỚC Phase 5. Pivot nếu cần |
| Streamlit Cloud limits | Medium | Low | Migrate VPS ($5/mo) khi cần |
| API costs exceed free tier | Low (early) | Low | Groq free → Claude khi revenue covers |
| Solo founder burnout | Medium | High | Upwork = income safety net. Không gấp. |

---

*Roadmap v1.0 — Phase 0 complete, ready for Phase 1*
