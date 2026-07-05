# /finance investor-crm — Investor pipeline and relationships

## Purpose
Track every investor relationship like a pipeline: stage, next touch, fit, history.

## Input
- None (report) or an update ("add {fund}", "move {fund} to term-sheet",
  "log call with {partner}")

## Steps
1. Load `finance/investors/pipeline.md`.
2. **Data model** per investor: fund, reference partner, stage
   (`radar → contacted → meeting → deep-dive → term-sheet → closed | passed`),
   fit (thesis, stage, ticket, portfolio conflict), last touch, next step with date,
   relationship notes (who introduced us, what interests them, objections raised).
3. **Update**: new investor, stage change (with date), interaction log (update
   last touch), outcome (closed/passed with reason — the reason for a pass is gold for the
   next ones).
4. **Report**: pipeline by stage, cold relationships (no touch for >60 days for investors
   active in the pipeline), next steps for the week, who should receive the next update.
5. Every promise made to an investor ("I'll send you X") → tracked follow-up.

## Output format
```markdown
---
zone: finance
tier: 🔴
type: investor-crm
---
# Investor Pipeline — {YYYY-MM-DD}

## By stage
| Fund | Partner | Stage | Fit | Last touch | Next step (date) |
## Relationships to warm up (>60 days)
## Passed (with reason)
## Next steps this week
```

## Destination
Zone `finance` → `investors/pipeline.md` (updated in place).
Commit (admin): `[finance] investor-crm: {action}`.

## Handoff
Meeting scheduled → `cos` (`/cos prepare-meeting`, investor type) · term-sheet received →
`ceo` + external legal review.
