# /sales deal-review — Strategic analysis of a deal

## Purpose
Understand whether and how to close a deal: fit, risks, strategy, next steps.

## Input
- `opp-slug` of the opportunity (or prospect if not yet in the pipeline)

## Steps
1. Load the opportunity and the account from the `commerciale` zone, the history from the
   `clienti/{slug}/` folder if already a customer, the active sales learnings (`⚡ LRN-XXX`, max 1).
2. **Qualification** (MEDDICC-lite):
   - ICP fit (segment, size, pain) · decision maker and champion identified?
   - budget · timeline · compelling event · competition in the running
3. **Risks**: potential deal killers, likely objections (with prepared answers),
   open blockers and current aging (computed at read time).
4. **Strategy**: concrete next steps with owner and date, key messaging, specific asks
   for the next meeting, what NOT to promise (check `prodotto` roadmap).
5. **Probability**: it remains the one derived from the stage — if your judgment diverges strongly,
   the signal is that the stage is wrong: propose moving the stage, not the number.
6. Update the opportunity (next-step, blockers) and save the review.

## Output format
```markdown
---
zone: commerciale
tier: 🟡
type: deal-review
opportunity: {opp-slug}
---
# Deal Review — {account} / {opp-slug} — {date}

## Snapshot (stage, value, aging, owner)
## Qualification (MEDDICC-lite table)
## Risks and objections (with answers)
## Strategy and next steps (owner + date)
## What not to promise
```

## Destination
`commerciale` zone → `reviews/deal-{opp-slug}-{YYYY-MM-DD}.md`.
Commit (admin): `[sales] review: {opp-slug}`.

## Handoff
Deal >€50k or discount → `ceo` · requested feature → `product` · contract → `compliance`.
