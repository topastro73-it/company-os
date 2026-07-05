# /cto tech-decision — ADR

## Purpose
Analyze and document a technical decision so that in 6 months it is clear why it was made.

## Input
- Decision topic · known constraints (budget, timeline, team, compliance)

## Steps
1. **Define the technical problem** and the constraints; check in `prodotto/adr/` whether a
   related ADR exists (never contradict it without stating what has changed).
2. **Identify 2-3 concrete options** with pros/cons for each.
3. **Evaluate** each option on: performance, scalability, maintainability, cost (setup +
   recurring), team skills, time-to-market, security.
4. **Compliance check**: does the decision change encryption, access control, logging or data
   flow? → document the impact on the mapped controls in the `compliance` zone and flag it.
5. **Recommend** with a clear rationale; make the accepted technical debt explicit (if any)
   and the reversibility of the choice.
6. Document as an ADR; if the decision is strategic (stack, critical vendor, high cost)
   → propose it to the CEO before considering it made.

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: adr
status: accepted         # proposed | accepted | superseded-by: {slug}
date: YYYY-MM-DD
compliance-impact: []
---
# ADR — {title}

## Context and problem      ## Constraints
## Options evaluated (pros/cons, costs)
## Decision and rationale
## Compliance impact        ## Accepted technical debt
## Consequences and follow-up (owner + deadline)
```

## Destination
`prodotto` zone → `adr/YYYY-MM-DD-{slug}.md`. ADRs are immutable: they are superseded by
a new ADR (`superseded-by`). Commit (admin): `[cto] adr: {topic}`.

## Handoff
Compliance impact → `compliance` · roadmap/priority impact → `product` ·
strategic → `ceo` (`/ceo decision` if a company decision is needed).
