# /sales board — Pipeline cockpit

## Purpose
Regenerate the synoptic view of the pipeline. The board is a **convenience snapshot**:
the truth lives in the opportunities' frontmatter.

## Input
None.

## Steps
1. Scan `commerciale/opportunities/*.md` (excluding the template).
2. For each open opportunity compute **live aging** (🟢 ≤6 days · 🟡 7-13 · 🟠 14-20 · 🔴 ≥21;
   overdue next-step and blockers raise the band; the most severe wins).
3. Check consistency: `probability` ≠ stage map → fix it (it is derived); opportunities
   without `owner-sales` → flag NO-OWNER.
4. Compute summary: n. open, gross, weighted, coverage vs target, subtotals per stage
   and per segment.
5. Write the board.

## Output format
```markdown
---
zone: commerciale
tier: 🟡
type: board
generated: YYYY-MM-DD
---
# Pipeline — Commercial Cockpit (regenerated {YYYY-MM-DD})

## Summary
- Open: {n} · Gross: €{…} · Weighted: €{…} · Coverage vs target: {…}%
- Per stage: Discovery {n}/€{w} · Technical Alignment {n}/€{w} · … · Won {n}/€{gross}
- Per segment: {subtotals}

## 🔴🟠🟡 Blocked & Aging   ← key view, by severity then days stalled desc
| Band | Opportunity | Account | Stage | Weighted | Blocker/reason | Owner | Days | Next step (due) |

## Per stage   (one table per stage, opps by weighted desc, linked)
## Per owner   (n deals, gross, weighted, n critical — highlight NO-OWNER)
```

## Destination
`commerciale` zone → `PIPELINE.md` (overwrite).
Commit (admin): `[sales] board: pipeline cockpit {YYYY-MM-DD}`.

## Handoff
🔴 deal with high weighted → `deal-review`; NO-OWNER → assignment (Head of Sales/CEO).
