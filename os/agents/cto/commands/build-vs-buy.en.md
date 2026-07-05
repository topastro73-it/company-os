# /cto build-vs-buy — Build, buy or partnership

## Purpose
Decide in a structured way whether a capability should be built, bought or obtained via a partner.

## Input
- Requested capability · where the need comes from (PRD, partner request, technical gap)

## Steps
1. **Define the capability** and the success criterion; is it core (differentiates the product)
   or context (needed but not differentiating)? Core gets built, context rarely does.
2. **BUILD option**: effort (honest range), time-to-market, maintenance cost over
   time, fit with the stack and the team's skills.
3. **BUY option**: concrete candidates, cost (setup + recurring), lock-in, vendor security and
   compliance (**if it handles data → a `compliance` vendor assessment is required BEFORE
   signing**), API/integration quality.
4. **PARTNER option**: who, what agreement, dependency created.
5. **Comparison** over 3 years (TCO), not just initial cost; risk of each option and
   reversibility.
6. **Recommend** and document as an ADR; if the cost is significant → `ceo` and `finance`.

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: adr
subtype: build-vs-buy
date: YYYY-MM-DD
---
# Build vs Buy — {capability}

## Capability and success criterion · core or context?
## Comparison
| | BUILD | BUY ({vendor}) | PARTNER |
| Initial / recurring cost / 3y TCO | | | |
| Time-to-market · Lock-in · Risk | | | |
| Security & compliance | | | |
## Recommendation and rationale
## Follow-up (vendor assessment, PoC, negotiation)
```

## Destination
`prodotto` zone → `adr/YYYY-MM-DD-build-vs-buy-{slug}.md`.
Commit (admin): `[cto] adr: build-vs-buy {capability}`.

## Handoff
Vendor handling data → `compliance` (vendor assessment) · cost → `finance` · strategic → `ceo`.
