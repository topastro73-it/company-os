# /ceo okr-review — OKR Review

## Purpose
Snapshot the quarter's OKR progress, identify at-risk KRs, correct course.

## Input
- None required; optional: quarter (default: current)

## Steps
1. Load the `direzione` zone → `okrs/{quarter}.md` and the metrics from the zone snapshots
   (`commerciale` for pipeline/revenue, `clienti` for health/churn, `prodotto` for delivery).
2. For each **Objective**: status On Track / At Risk / Off Track.
3. For each **Key Result**: current value vs target, % progress, trend since the last
   review, identified blockers. Cite the source of every number (zone file).
4. **Corrective actions** for At Risk/Off Track KRs: action, owner (agent), deadline.
5. **Propose adjustments** only when justified: KRs to drop, targets to revise, new KRs.
   A target change is a decision → if accepted, record it with `/ceo decision`.
6. Append the review section to the OKR file (append, don't rewrite the history).

## Output format
```markdown
## Review {YYYY-MM-DD}

| Objective / KR | Target | Current | Progress | Trend | Status |
|---|---|---|---|---|---|

### At-risk KRs
- [KR] — why — corrective action (owner, deadline)

### Notes and proposed decisions
```

## Destination
`direzione` zone → `okrs/{quarter}.md` (review section appended).
Commit: `[ceo] okr: review {quarter}`.

## Handoff
- At-risk product KR → `product` (reprioritization) or `cto` (capacity)
- At-risk revenue KR → `sales` (`/sales board` + `deal-review` on top deals)
- At-risk retention KR → `delivery` (`/delivery alert-check`)
