# /cos daily-briefing — Briefing of the day

## Purpose
Give the CEO in 2 minutes: what changed, what needs attention today, pipeline status.

## Input
None. Trigger: "today's briefing", "what do I need to know?".

## Steps
1. **Cadence check**: if in an admin session and a rhythm fires (`direzione/ceo-cadence.md`),
   let `/ceo start` ask its questions BEFORE the briefing; otherwise proceed.
2. **News from the last 24-48h**: in admin `git log --since="48 hours ago"`; on Drive, the
   recently modified files in the readable zones. Group by agent/area.
3. **Signals that need the CEO**:
   - follow-ups due today/tomorrow (from `direzione/decisions/` and zone reports)
   - open decisions with no owner or no date · uncollected handoffs
4. **Pipeline — blocked & aging** (live from the frontmatter of `commerciale/opportunities/`):
   top 🔴🟠 with account, stage, blocker, owner, days stalled, next step. Highlight deals
   without an owner and high weighted value blocked. Board stale >3d → suggest `/sales board`.
5. **Partner alerts** (`clienti` zone): Critical/At-Risk health, delayed onboarding.
6. **Finance flash** (`vault/finance/`, admin only): due dates ≤3d, invoices 30+d overdue.
7. **Compliance** (only if there is something): deadlines ≤7d, missing evidence, upcoming audits.
8. **Today's priorities**: 3-5 actions, each with 1-line context and estimated time.

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: briefing
---
# Briefing — {YYYY-MM-DD}

## What changed             ## Needs your attention today
## Pipeline — blocked & aging (🔴🟠 table)
## Partner alerts           ## Finance flash
## Compliance (if present)  ## Today's priorities (3-5, with owners)
```
Every data point cites its source (zone file).

## Destination
Zone `direzione` → `briefing/daily-{YYYY-MM-DD}.md`. Also deliver in chat.
Commit (admin): `[cos] briefing: {YYYY-MM-DD}`.
