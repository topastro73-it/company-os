# Investor Relations Skill

Investor relationship management, fundraising readiness, board governance. Used by CEO, CFO, Legal.

## Principles

1. **Constructive transparency**: share real data, frame problems as opportunities with an action plan
2. **Consistent narrative**: every touchpoint with an investor reinforces the same story (vision → traction → ask)
3. **Preparation > improvisation**: never go to a call without a brief, never send data without context
4. **Compliance**: legal disclaimer on every term sheet or contract clause analysis

---

## Commands

| Command | Description | Output |
|---------|------------|--------|
| `data-room` | Complete data room checklist for fundraising | Report with gap analysis |
| `pitch-prep` | Preparation for a call with a specific investor | Brief in `company/direzione/investor-updates/` |
| `term-sheet-review` | Term sheet clause analysis with benchmarks | Analysis in `company/direzione/investor-updates/` |
| `board-prep` | Board meeting preparation | Deck outline in `company/direzione/investor-updates/` |
| `cap-table` | Generate/update cap table | `vault/finance/cap-table.md` |
| `investor-crm` | Track investor relationships and pipeline | `vault/finance/investor-pipeline.md` |

---

## Command: data-room

### Process

1. Scan the repo to verify the presence of each required document
2. For each category, mark: present / partial / missing
3. Generate report with completion priorities

### Data Room Checklist

#### 1. Company Overview
| Document | Expected path | Check |
|-----------|------------|---------|
| Updated pitch deck | `company/direzione/investor-updates/pitch-deck-*.md` | Scan |
| One-pager / Executive summary | `company/direzione/investor-updates/exec-summary.md` | Scan |
| Company profile | `zones/_root/context/COMPANY.md` | Always present |
| Vision and strategy | `company/direzione/strategy/vision.md` | Scan |
| Current OKRs | `company/direzione/strategy/okr-*.md` | Scan |

#### 2. Financials
| Document | Expected path | Check |
|-----------|------------|---------|
| Financial model / projections | `vault/finance/financial-model.md` | Scan |
| Current pricing | `vault/finance/pricing.md` | Scan |
| KPI dashboard | `company/direzione/metrics/kpis.md` | Scan |
| Cap table | `vault/finance/cap-table.md` | Scan |
| Burn rate and runway | In `company/direzione/metrics/kpis.md` | Verify data filled in |
| MRR / ARR history | In `company/direzione/metrics/kpis.md` | Verify data filled in |

#### 3. Product
| Document | Expected path | Check |
|-----------|------------|---------|
| Roadmap | `company/prodotto/roadmap.md` | Scan |
| Main specs / PRDs | `company/prodotto/specs/*.md` | Count and verify status |
| Backlog | `company/prodotto/backlog.md` | Scan |
| Architecture overview | `company/direzione/reports/architecture-*.md` | Scan |
| Demo / screenshots | `company/marketing/demo-*` | Scan |

#### 4. Market
| Document | Expected path | Check |
|-----------|------------|---------|
| Customer segments | `company/commerciale/segments.md` | Scan |
| Competitor analysis / battlecards | `company/commerciale/competitors/battlecards/*.md` | Count |
| TAM/SAM/SOM | `company/direzione/strategy/market-sizing.md` | Scan |
| Case studies / testimonials | `company/marketing/case-study-*.md` | Scan |

#### 5. Team
| Document | Expected path | Check |
|-----------|------------|---------|
| Team overview | `config/people.yaml` | Always present |
| Org chart | `company/direzione/operations/operating-model.md` | Scan |
| Hiring plan | `company/direzione/team/hiring-plan.md` | Scan |

#### 6. Legal
| Document | Expected path | Check |
|-----------|------------|---------|
| Bylaws / articles of incorporation | `vault/legal/statuto.md` or `.pdf` | Scan |
| Certifications (e.g. ISO 27001 — if applicable) | In `zones/_root/context/COMPANY.md` | Verify section |
| Privacy policy / GDPR | `vault/legal/privacy-*.md` | Scan |
| Standard partner contracts | `vault/legal/contract-template-*.md` | Scan |
| IP ownership / patents | `vault/legal/ip-*.md` | Scan |

### Output format
```
## Data Room Readiness — {date}

### Summary
- Present: N/M documents (X%)
- Partial: N (incomplete data)
- Missing: N

### Gap Analysis (priority high → low)

| # | Document | Status | Priority | Suggested action | Owner |
|---|-----------|-------|----------|-----------------|-------|
| 1 | Financial model | MISSING | CRITICAL | CFO must create 3Y projections | CFO |
| 2 | Cap table | PARTIAL | HIGH | Complete with current round | CFO + Legal |
| 3 | Case study {customer} | MISSING | MEDIUM | Marketing produces case study | Marketing |

### Next steps
1. [Action with owner and deadline]
```

Save to: `company/direzione/investor-updates/data-room-audit-{YYYY-MM-DD}.md`
Commit: `[ceo] investor: data room readiness audit`

---

## Command: pitch-prep

### Input
- Investor / fund name
- Meeting type (intro call, deep dive, follow-up, partner meeting)
- Meeting date

### Process
1. Look up information about the investor:
   - Portfolio: which similar startups have they funded?
   - Thesis: which sectors/stages are they focused on?
   - Partner: who will be on the call? What is their background?
2. Analyze fit with the company:
   - Thesis-product alignment
   - Portfolio conflict (have they already invested in B2B cybersecurity?)
   - Stage fit (do they invest in seed/pre-seed?)
3. Prepare brief with:
   - Likely questions (top 10 based on the investor profile)
   - Red flags to anticipate (weak metrics, team gaps, market)
   - Personalized talking points (what in our pitch resonates with their thesis)
   - Clear ask (how much, for what, timeline)

### Output format
```
## Pitch Prep — {investor name}
Meeting date: {date} | Type: {type}

### Investor profile
- Fund: {name}
- Focus: {sectors, stage, geography}
- Relevant portfolio: {similar startups}
- Partner on call: {name, background}

### Fit Analysis
| Dimension | Score | Notes |
|-----------|-------|------|
| Thesis alignment | High/Medium/Low | {why} |
| Stage fit | High/Medium/Low | {why} |
| Portfolio conflict | Yes/No | {details} |

### Top 10 likely questions
1. {Question} → **Suggested answer**: {answer}
2. ...

### Red flags to manage
1. {Red flag} → **Framing**: {how to present it}

### Personalized talking points
1. {Point that resonates with the investor's thesis}

### Ask
- Amount: €{X}
- Use of funds: {breakdown}
- Timeline: {when to close}
```

Save to: `company/direzione/investor-updates/pitch-prep-{slug-investitore}-{YYYY-MM-DD}.md`
Commit: `[ceo] investor: pitch prep for {investor}`

---

## Command: term-sheet-review

### Input
- Term sheet (text or reference to the document)

### Disclaimer

> ⚠️ **LEGAL DISCLAIMER**: This analysis is generated by an AI system for informational and internal preparation purposes. It does NOT constitute legal advice. Before signing any term sheet or binding agreement, ALWAYS consult a lawyer specialized in venture capital and corporate law. The company assumes no liability for decisions made based on this analysis.

This disclaimer MUST be included at the beginning of every `term-sheet-review` output.

### Process
1. Extract the key clauses from the term sheet
2. For each clause:
   - Explain what it means in simple terms
   - Indicate whether it is standard / favorable / unfavorable compared to the market benchmark
   - Suggest negotiation points if unfavorable
3. Generate summary with overall recommendation

### Clauses analyzed
| Clause | What to check |
|----------|-----------------|
| Valuation (pre/post-money) | Implied dilution, comparison with comparables |
| Liquidation preference | 1x non-participating = standard; >1x or participating = red flag |
| Anti-dilution | Weighted average = standard; full ratchet = unfavorable |
| Board composition | Founder majority = ideal; investor majority pre-Series A = red flag |
| Vesting | 4 years with 1 year cliff = standard |
| Drag-along / Tag-along | Thresholds, activation conditions |
| ESOP pool | Size pre/post money, implied dilution |
| Pro-rata rights | Standard for lead investor |
| Information rights | Frequency and detail of reporting |
| Protective provisions | Which decisions require investor approval |
| No-shop / Exclusivity | Duration (30-60 days = standard; >90 days = excessive) |
| Governing law | Applicable jurisdiction |

### Output format
```
## Term Sheet Analysis — {investor}

⚠️ DISCLAIMER: [full disclaimer]

### Summary
| Clause | Status | Notes |
|----------|--------|------|
| Valuation | ✅ Standard | Pre-money €Xm, dilution Y% |
| Liquidation pref | ⚠️ To negotiate | 1.5x participating — ask for 1x non-participating |
| Anti-dilution | ✅ Standard | Weighted average |
| Board | 🔴 Red flag | 2 investors out of 3 — request parity |

### Detailed analysis
[For each clause: explanation, benchmark, recommendation]

### Recommendation
[Proceed / Negotiate / Decline — with rationale]

### Priority negotiation points
1. {Clause} — {what to ask for} — {why}
```

Save to: `company/direzione/investor-updates/term-sheet-review-{slug}-{YYYY-MM-DD}.md`
Commit: `[ceo] investor: term sheet analysis for {investor}`

Handoff: **Legal** for formal review

---

## Command: board-prep

### Input
- Board meeting date
- Agenda (optional — if not provided, use the standard agenda)

### Process
1. Gather updated data from:
   - `company/direzione/metrics/kpis.md` — current KPIs
   - `company/prodotto/roadmap.md` — roadmap status
   - `vault/finance/pricing.md` — pricing and revenue
   - `20-Clienti/*/overview.md` — partner status
   - `decisions/` — recent decisions
   - `company/direzione/strategy/` — OKRs and strategy
2. Identify gaps in the data (metrics not updated)
3. Generate the board deck outline

### Standard board meeting agenda
1. **KPI Update** (5 min) — MRR, ARR, churn, pipeline, runway
2. **Product Update** (10 min) — shipped, in-dev, roadmap changes
3. **Go-to-Market** (10 min) — partner pipeline, deal status, marketing highlights
4. **Financial Update** (5 min) — burn, runway, cash position
5. **Team** (5 min) — hiring, org changes
6. **Asks** (10 min) — what is needed from the board (intros, advice, decisions)
7. **Discussion** (15 min) — strategic topic of the quarter

### Output
```
## Board Meeting Prep — {date}

### Pre-meeting checklist
- [ ] KPIs updated (last update: {date})
- [ ] Financial update from the CFO
- [ ] Product demo/screenshots ready
- [ ] Partner pipeline updated
- [ ] Asks defined

### Deck outline
[Section by section with data and talking points]

### Missing data
| Data | Owner | Deadline |
|------|-------|----------|
```

Save to: `company/direzione/investor-updates/board-prep-{YYYY-MM-DD}.md`
Commit: `[ceo] investor: board meeting prep {date}`

---

## Command: cap-table

### Process
1. Read `vault/finance/cap-table.md`
2. If empty/template: ask the user for the fundamental data:
   - Founding shareholders and % stakes
   - Previous rounds (amount, valuation, equity sold)
   - ESOP pool (if present)
3. Calculate: fully diluted ownership, dilution per future round
4. Update the file

### Output
Update `vault/finance/cap-table.md`
Commit: `[finance] finance: updated cap table`

---

## Command: investor-crm

### Process
1. Read `vault/finance/investor-pipeline.md`
2. Show the current pipeline status
3. Allow adding/updating contacts:
   - Fund name + partner
   - Stage (cold / warm intro / first call / deep dive / term sheet / closed)
   - Notes from last contact
   - Next step
   - Fit score (1-5)
4. Update the file

### Output
Update `vault/finance/investor-pipeline.md`
Commit: `[ceo] investor: updated investor pipeline`

---

## CEO Cadence integration

### Monthly
- **Runway alert**: if runway < 9 months (calculated from burn rate and cash in `company/direzione/metrics/kpis.md`), generate automatic alert:
  ```
  🚨 **RUNWAY ALERT** — Estimated runway: {N} months ({estimated depletion date}).
  Action: start the fundraising process or reduce burn. Do you want me to prepare the data room?
  ```
- If the investor pipeline has deals in stage `deep dive` or `term sheet`, remind in the monthly check

### Weekly
- If there are investor meetings scheduled during the week, remind to prepare pitch-prep

---

## Where the data lives

| Data | Path |
|------|------|
| Cap table | `vault/finance/cap-table.md` |
| Investor pipeline | `vault/finance/investor-pipeline.md` |
| Pitch prep, board prep, term sheet review | `company/direzione/investor-updates/` |
| Data room audit | `company/direzione/investor-updates/` |
| Financial model | `vault/finance/financial-model.md` |
| KPIs (for runway calc) | `company/direzione/metrics/kpis.md` |
| Pricing | `vault/finance/pricing.md` |
