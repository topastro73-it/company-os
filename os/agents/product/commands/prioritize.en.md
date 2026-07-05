# /product prioritize — Backlog prioritization (RICE)

## Purpose
Re-prioritize the backlog with a defensible method, not by whoever shouted last.

## Input
None; optional: new items to add before scoring.

## Steps
1. **Spec status check**; then load `prodotto/backlog.md`, roadmap, OKRs (`direzione`).
2. For each item apply **RICE**:
   - **Reach**: how many partners/salespeople/SMBs impacted (number, per quarter)
   - **Impact**: 3 Massive · 2 High · 1 Medium · 0.5 Low · 0.25 Minimal
   - **Confidence**: 100% / 80% / 50% (below 50% the item is not ready for scoring:
     it needs discovery, not priority)
   - **Effort**: person-weeks (CTO estimate if available, otherwise flag "to be estimated")
   - **Score = (R × I × C) / E**
3. **Strategic fit overlay**: the score bends to strategy only explicitly —
   if you promote an item beyond its RICE, write down why.
4. Propose 3 tiers: **Must-do / Should-do / Nice-to-have**; identify dependencies and
   a recommended sequence.
5. Highlight deltas versus the previous prioritization (what moved up/down and why).

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: backlog
last-prioritized: YYYY-MM-DD
---
# Backlog — prioritized {YYYY-MM-DD}

## Must-do
| Item | R | I | C | E | Score | Fit | Notes |
## Should-do   ## Nice-to-have
## Delta vs previous   ## Dependencies and sequence
```

## Destination
Zone `prodotto` → `backlog.md` (update in place, history kept in the deltas).
Commit (admin): `[product] backlog: RICE re-prioritization`.

## Handoff
Top Must-do without a PRD → `/product write-spec` · missing efforts → `cto` ·
priority change relevant to OKRs → `ceo`.
