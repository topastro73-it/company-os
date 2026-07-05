# /delivery alert-check — Partner alert scan

## Purpose
Quick scan of all partners to surface the alerts that require action now.
Also feeds the CoS briefing and the CEO's start.

## Input
None.

## Steps
1. Scan the cards in `clienti/*/scheda-partner.md` (quick mode: available data,
   declare their freshness).
2. Generate alerts according to the thresholds:
   - health **< 40** → **CRITICAL** (rescue call ≤7d, CEO escalation)
   - drop **> 15 points in 30d** → **WARNING** (delivery call ≤14d)
   - active SMBs **< 30%** of onboarded → **LOW ENGAGEMENT**
   - no salespeople activity for **30+d** → **DORMANT**
   - contract expiring within **60d** → **RENEWAL**
   - onboarding: critical milestone missed (first scan d.14, first deal wk.8) → **ONBOARDING**
3. For each alert: suggested action, owner, deadline.
4. Sort by severity; if there are zero alerts, state it explicitly.

## Output format
```markdown
---
zone: commerciale
tier: 🟡
type: alert-report
---
# Partner Alerts — {YYYY-MM-DD}

| Partner | Health | Alert | Suggested action | Owner | By |
|---|---|---|---|---|---|
| {slug} | 35 | CRITICAL | Rescue call + CEO escalation | {owner} | 7d |
| {slug} | 72→55 | WARNING | Check-in call | {owner} | 14d |
```

## Destination
`commerciale` zone → `delivery/alerts-{YYYY-MM-DD}.md` (overwritable: the latest one counts).
Also deliver in chat. Commit (admin): `[delivery] alerts: {YYYY-MM-DD}`.

## Handoff
CRITICAL → `ceo` (within 24h) · RENEWAL → `finance` + `sales` ·
recurring pattern → `/delivery churn-analysis`.
