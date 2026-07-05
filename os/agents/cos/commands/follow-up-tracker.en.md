# /cos follow-up-tracker — Follow-up and commitments tracking

## Purpose
A single place to see all open follow-ups, who owns them, and what is overdue.

## Input
None; optional: filter by owner or area.

## Steps
1. **Scan the follow-up sources**:
   - `direzione/decisions/*.md` — follow-up sections with checkboxes and deadlines
   - `direzione/ceo-routine.md` — the CEO's open commitments
   - recent zone reports (QBR, postmortem, review) — actions with owner and deadline
   - opportunities in `commerciale` — next steps with an expired `next-step-due`
2. **Classify** each item: 🔴 overdue · 🟡 due within 7d · 🟢 planned · ⚫ no
   owner or no date (an anomaly to fix, not to ignore).
3. **For overdue items**: how many days, who was the owner, impact if it stays stalled, proposal
   (do now / reschedule / explicitly cancel).
4. **Patterns**: if a type of follow-up recurrently expires and matches a learning,
   flag `⚡ LRN-XXX` (max 1).

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: report
---
# Follow-up Tracker — {YYYY-MM-DD}

## 🔴 Overdue
| Item | Source | Owner | Deadline | Days | Proposal |
## ⚫ No owner or no date
## 🟡 Due soon (7d)
## 🟢 Planned

## Proposed escalations (max 3)
```

## Destination
Zone `direzione` → `briefing/follow-up-{YYYY-MM-DD}.md`.
Commit (admin): `[cos] tracker: follow-up {YYYY-MM-DD}`.

## Handoff
Overdue P0 follow-up → `ceo` (decision: do/reschedule/cancel).
