# /ceo quarterly-review — Quarter retrospective

## Purpose
Close the quarter: results vs plan, lessons, next quarter's priorities.

## Input
- Quarter to close (default: the one just ended)

## Steps
1. **Gather the results** from the zone snapshots:
   - `commerciale`: deals won/lost, coverage vs target, ISP funnel
   - `clienti`: active partners, average health, churn, expansion
   - `prodotto`: features shipped vs planned, spec lifecycle
   - `vault/finance`: revenue, burn, runway, collected vs invoiced
   - `compliance`: certification milestones, gaps closed
   - `marketing`: content produced, campaign results
2. **Final OKR scoring**: run the `/ceo okr-review` logic with an end-of-quarter verdict.
3. **What worked / what didn't**: max 5 points each, with evidence.
4. **Not done**: promises and plans not executed, with the reason if known.
5. **Q+1 plan**: 3 proposed strategic priorities (to be validated with the CEO), OKR draft.
6. **Learnings**: propose the quarter's patterns as `LRN-XXX` candidates (at close).

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: report
render: gdoc
---
# Quarterly Review — {Q}

## Results vs plan (table per area, with source)
## Final OKR scoring
## What worked / What didn't
## Not done
## {Q+1} plan: 3 priorities + OKR draft
```

## Destination
`direzione` zone → `board/quarterly-review-{Q}.md` (readable by the board via direzione ACL).
Commit: `[ceo] review: {Q}`.

## Handoff
- Approved Q+1 OKR draft → new file `direzione/okrs/{Q+1}.md`
- Product priorities → `product` (`/product prioritize`)
