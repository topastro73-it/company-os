# /product evaluate-request — Feature request evaluation

## Purpose
Decide in a defensible way what to do with a request: BUILD, CONFIGURE, CUSTOM or DECLINE.

## Input
- Feature/request · who is asking (partner? deal in progress?) · business context
  (deal size, urgency) — requests also come from `prodotto/richieste/`

## Steps
1. **Spec status check**: stale specs in `prodotto/specs/INDEX.md` → flag them before proceeding.
2. Load vision (`direzione`), roadmap and backlog (`prodotto`), any past evaluations
   of the same request (never re-evaluate from scratch without citing the previous outcome).
3. **Extract the real need**: job-to-be-done; distinguish "what they ask for" from "why".
4. **Apply the framework**, evaluating across the 3 levels (Partner, Salesperson, SMB):
   - Strategic Fit: High/Medium/Low (vision, core segment, differentiation)
   - Scalability: Scalable / Partially / Custom ("does it serve 1 or 100?")
   - Market Demand: Broad / Niche / Single-customer
   - Effort vs Value: effort XS-XL, business value, opportunity cost
5. **Recommendation**:
   - **BUILD** (product): high fit + scalable + broad demand
   - **CONFIGURE** (configurable): medium-high fit + partially scalable + multi-customer
   - **CUSTOM**: low fit, or single-customer with economic value that justifies it
   - **DECLINE/DEFER**: low fit + niche, or conflict with product integrity (+ review-date if defer)
6. **Red flags** (if from Sales): unvalidated single-customer · unrealistic timeline ·
   scope creep. If present → say so explicitly.
7. Reply to the requester: outcome + rationale in partner language ("in evaluation",
   never dates).

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: evaluation
status: evaluated
requested-by: {partner|interno}
---
# Evaluation — {feature}
## Real need  ## Framework (table 4 dimensions × 3 levels)
## Recommendation: {BUILD|CONFIGURE|CUSTOM|DECLINE} + rationale and trade-offs
## Next step
```

## Destination
Zone `prodotto` → `specs/evaluation-{slug}.md`. Commit (admin): `[product] eval: {slug}`.

## Handoff
BUILD/CONFIGURE approved → `/product write-spec` · reply to the requester → `sales`/`delivery`.
