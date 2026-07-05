# /finance investor-update — Investor update

## Purpose
Periodic factual update: real traction, problems with a plan, a clear ask. Investor
trust is built with consistency, not with overselling.

## Input
- Period (month/quarter) · recipients (current investors, prospects, advisors)

## Steps
1. Gather the numbers with their source: revenue/MRR and collections (`finance` zone), weighted
   pipeline (`commerciale` zone), partners and health (`clienti` zone), shipped (`prodotto`
   zone), compliance milestones (`compliance` zone), burn and runway (cashflow).
2. Compare with the previous update (`direzione/investor-updates/`): the narrative must
   be consistent — if a number got worse, say so, with the why and the plan.
3. Structure: **TL;DR** (3 lines) → Highlights → Lowlights (honest, with action) →
   Key numbers (table with trend) → Product → Team → **Ask** (intros, talent,
   skills) → upcoming milestones.
4. **Tier redaction**: the update is 🟡 (it leaves the company): no unnecessary 🔴 details
   (cap table, IBAN, salaries); aggregated numbers, not individual contracts with names unless
   authorized.
5. CEO review → sending via PREPARE → APPROVE → EXECUTE (never send without approval).

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: investor-update
render: gdoc
period: {YYYY-MM|Qn}
---
# Investor Update — {period}
## TL;DR             ## Highlights / Lowlights
## Key numbers (table + trend)
## Product & team    ## Ask
## Upcoming milestones
```

## Destination
Zone `direzione` → `investor-updates/update-{period}.md` (readable by the board).
Commit (admin): `[finance] investor: update {period}`.

## Handoff
Strategic asks → `ceo` · relationship updates → `/finance investor-crm`.
