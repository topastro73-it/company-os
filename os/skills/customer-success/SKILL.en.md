# Customer Success Skill

Partner health monitoring, churn prevention, account expansion. Used by CEO, Sales, Chief of Staff.

## Health Score Model

Each partner has a **Health Score** (0–100) calculated on 5 weighted indicators:

| # | Indicator | Weight | Data source | How it's measured |
|---|-----------|------|-----------|----------------|
| 1 | **SMBs Onboarded** | 25% | Platform | No. of SMBs registered vs contractual target. Score: (actual / target) * 100, cap 100 |
| 2 | **Active SMBs** (30d) | 25% | Platform | SMBs with at least 1 scan or login in the last 30 days. Score: (active / onboarded) * 100 |
| 3 | **SMB Churn** (quarter) | 20% | Platform | % of SMBs lost in the quarter. Score: max(0, 100 - churn% * 10). Churn 0% = 100, Churn 10% = 0 |
| 4 | **Seller Engagement** | 15% | CRM/Platform | No. of proposals generated + reports sent in the month. Score: 0 if no activity, 50 if sporadic, 100 if regular |
| 5 | **NPS / Satisfaction** | 15% | Survey / Feedback | Latest NPS score normalized 0–100. If unavailable: estimate from support tickets and sentiment |

### Health Score bands

| Band | Score | Meaning | Action |
|--------|-------|-------------|--------|
| **Healthy** | 80–100 | Active partner, SMBs growing | Expansion play — upsell tier or services |
| **Stable** | 60–79 | Working but not growing | Engagement boost — training, co-marketing |
| **At Risk** | 40–59 | Signs of disengagement | Proactive intervention — call with Sales + PM |
| **Critical** | 0–39 | Imminent churn | CEO escalation — rescue plan within 7 days |

### Formula

```
Health Score = (PMI_Onboarded * 0.25) + (PMI_Attive * 0.25) + (Churn_Score * 0.20) + (Engagement * 0.15) + (NPS * 0.15)
```

---

## Commands

| Command | Description | Output |
|---------|------------|--------|
| `partner-health` | Calculates the health score for a specific partner or for all | Report with score, trend, alerts |
| `partner-review` | Quarterly review of a partner with recommendations | Document in `20-Clienti/{slug}/report/partner-review-{partner}-{date}.md` |
| `churn-analysis` | Churn analysis with patterns and causes | Report in `company/direzione/reports/churn-analysis-{date}.md` |
| `partner-qbr` | Generates a QBR (Quarterly Business Review) deck for a partner | Document in `20-Clienti/{slug}/report/qbr-{partner}-{quarter}.md` |
| `expansion-plan` | Expansion plan for healthy/stable partners | Plan in `20-Clienti/{slug}/report/expansion-{partner}-{date}.md` |
| `alert-check` | Scans all partners for critical alerts | Alert list with suggested actions |

---

## Command: partner-health

### Input
- Partner slug (optional — if omitted, all partners)

### Process
1. Read the partner record from `20-Clienti/{slug}/overview.md`
2. Calculate each indicator with the available data
3. Calculate the overall health score
4. Compare with the previous score for the trend
5. Generate an alert if score < 60 or drop > 15 points

### Output format
```
## Partner Health — {partner name}

| Indicator | Score | Detail |
|-----------|-------|-----------|
| SMBs Onboarded | 85 | 34/40 target |
| Active SMBs | 70 | 24/34 active 30d |
| SMB Churn | 90 | 1% quarter |
| Seller Engagement | 60 | 8 proposals/month (sporadic) |
| NPS | 75 | Latest NPS: 45 |

**Health Score: 77/100 — Stable**
Trend: ↓ from 82 (last check)

### Recommendations
1. Seller engagement declining → schedule a training session
2. ...
```

---

## Command: partner-review

### Input
- Partner slug

### Process
1. Run `partner-health` for the partner
2. Analyze metric history (last 3 months)
3. Identify patterns and trends
4. Generate concrete recommendations with owner and deadline

### Output
File `20-Clienti/{slug}/report/partner-review-{partner}-{YYYY-MM-DD}.md` with:
- Executive summary (3 lines)
- Health score + trend
- Detailed metrics with history
- Identified risks
- Action plan (max 5 actions, each with owner and deadline)
- Suggested handoff (Sales for expansion, PM for feature requests, CEO for escalation)

---

## Command: churn-analysis

### Process
1. Scan all partners with health score < 60
2. Identify common patterns (low onboarding, poor engagement, etc.)
3. Calculate overall and per-segment churn rate
4. Generate root cause analysis

### Output
File `company/direzione/reports/churn-analysis-{YYYY-MM-DD}.md`

---

## Command: partner-qbr

### Input
- Partner slug
- Quarter (e.g. Q1-2026)

### Process
1. Gather all the quarter's metrics
2. Generate an executive summary
3. Prepare talking points for the call
4. Suggest expansion opportunities

### Output
File `20-Clienti/{slug}/report/qbr-{partner}-{quarter}.md` with:
- Quarter results (metrics vs target)
- Wins and highlights
- Areas for improvement
- Plan for the next quarter
- Expansion opportunity (if health > 70)

---

## Command: expansion-plan

### Input
- Partner slug

### Prerequisite
- Health score >= 60 (Stable or Healthy)

### Process
1. Analyze current tier and feature usage
2. Identify the gap between current tier and potential
3. Calculate potential revenue from an upgrade
4. Generate a plan with timeline and actions

### Output
File `20-Clienti/{slug}/report/expansion-{partner}-{YYYY-MM-DD}.md`

---

## Command: alert-check

### Process
1. Scan `20-Clienti/*/overview.md`
2. For each partner, calculate the health score (quick mode — available data)
3. Generate alerts for:
   - Score < 40 → **CRITICAL**
   - Score drop > 15 points in 30 days → **WARNING**
   - Active SMBs < 30% of onboarded → **LOW ENGAGEMENT**
   - No seller activity in 30+ days → **DORMANT**
   - Contract expiring within 60 days → **RENEWAL**
4. **Deal aging** — scan `company/commerciale/opportunities/*.md` (skill `os/skills/opportunity-management/SKILL.md`, section 3) and generate alerts for:
   - `last-activity` > 21d, or open blocker `severity: high`, or next-step overdue > 14d → **STALLED 🔴**
   - 14–20d idle, or `status-flag: blocked` for > 7d → **AGING 🟠**
   - Open opportunities **without `owner-sales`** → **NO-OWNER** (priority: high weighted)

### Output format
```
## Partner Alerts — {date}

| Partner | Score | Alert | Suggested action |
|---------|-------|-------|-----------------|
| partner-a | 35 | CRITICAL | Rescue call within 7d — CEO escalation |
| partner-b | 72→55 | WARNING | Sales call within 14d |
| partner-c | — | DORMANT | No activity for 45d — reach out again |

## Opportunity Aging — {date}

| Opportunity | Account | Stage | Weighted | Aging | Alert | Blocker / action |
|-------------|---------|-------|----------|-------|-------|------------------|
| acme-pilot | Acme | negotiation | €72k | 🔴 | NO-OWNER | Assign owner — most advanced deal uncovered |
| acme-channel | Acme | discovery | € — | 🔴 | STALLED | NDA idle 24d — ping owner-sales |
```

---

## CEO Cadence integration

### Daily
- Automatic `alert-check`: if there are CRITICAL alerts, they are included in the daily check for the CEO

### Weekly
- Health score summary of all active partners
- Partners with a significantly declining score

### Monthly
- QBR reminder for partners with a review scheduled in the month
- Churn analysis of the previous month
- Identified expansion opportunities

---

## Where the data lives

| Data | Path |
|------|------|
| Partner records | `20-Clienti/{slug}/overview.md` |
| Record template | `20-Clienti/TEMPLATE.md` |
| Review reports | `20-Clienti/{slug}/report/partner-review-*.md` |
| Churn reports | `company/direzione/reports/churn-analysis-*.md` |
| QBR reports | `20-Clienti/{slug}/report/qbr-*.md` |
| Expansion plans | `20-Clienti/{slug}/report/expansion-*.md` |
| Client segments | `company/commerciale/segments.md` |
| KPIs | `company/direzione/metrics/kpis.md` |
