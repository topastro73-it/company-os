# /cos weekly-digest — Weekly digest

## Purpose
Snapshot of the week: output by area, decisions, overdue follow-ups, outlook.

## Input
None. Trigger: "digest of the week".

## Steps
1. **Activity of the week**: in admin `git log --since="7 days ago"` grouped by
   agent; on Drive, new/modified files per zone. Areas with no activity → flag the gap.
2. **Decisions of the week**: new entries in `direzione/decisions/` with status and review
   date; decisions with follow-ups not yet assigned.
3. **Overdue follow-ups**: `[ ]` checkboxes with a deadline in the past week → what was
   planned, owner, escalation yes/no.
4. **Pipeline health** (`commerciale` zone): weighted coverage vs target, distribution by
   stage, stage movements of the week, top 🔴🟠 with days stalled, deals without an owner.
5. **Delivery & partners** (`clienti` zone): health scores in motion (↑/↓), onboarding
   status per phase, upcoming QBRs.
6. **Product** (`prodotto` zone): stale specs (draft >7d, evaluated/approved >14d,
   in-development >30d), UAT/tests in progress, releases of the week.
7. **Compliance & finance**: active alerts, next week's deadlines (finance admin only).
8. **Outlook**: follow-ups and milestones for the next 7 days.

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: digest
---
# Weekly Digest — week {start} → {end}

## Output by area (table)         ## Decisions made
## Overdue follow-ups             ## Pipeline — health & aging
## Delivery & partners            ## Product — specs & releases
## Compliance / Finance           ## Outlook next week
```

## Destination
Zone `direzione` → `briefing/weekly-{YYYY-MM-DD}.md`.
Commit (admin): `[cos] digest: week {date}`.
