# /product write-spec — PRD

## Purpose
Turn an evaluated feature into an implementable and verifiable PRD.

## Input
- Feature (ideally with an existing evaluation in `prodotto/specs/evaluation-{slug}.md`)

## Steps
1. **Spec status check** on `prodotto/specs/INDEX.md`; then load evaluation, vision, personas.
2. New topic without analysis? Stop: do the domain analysis first (questions one at a
   time, process map if needed). Never a spec without having understood the problem.
3. **Write the PRD** (format below): problem statement, personas across the 3 levels
   (Partner/Salesperson/SMB), user stories "As a… I want… So that…", acceptance criteria
   "Given/When/Then", **functional** data model (never technical), non-functional requirements,
   explicit in scope / out of scope, success metrics, dependencies and risks.
4. **Compliance impact check**: personal data? changes security? → frontmatter
   `compliance-impact: [NIS2/GDPR/ISO27001]`, if a DPIA is needed → handoff `compliance`.
5. Scope in T-shirt size with rationale; `status: draft` until the CTO evaluates it.
6. Update `prodotto/specs/INDEX.md`.

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: prd
status: draft            # draft→evaluated→approved→in-development→shipped
compliance-impact: []
clickup-epic: ""
clickup-doc: ""
last-updated: YYYY-MM-DD
---
# PRD — {feature}
## Problem statement       ## Personas (3 levels)
## User stories            ## Acceptance criteria (Given/When/Then)
## Data model (functional) ## Non-functional requirements
## In scope / Out of scope ## Success metrics
## Dependencies and risks  ## Implementation status (deliverables table)
## Decisions made          ## Deferred / follow-up
```

## Destination
Zone `prodotto` → `specs/prd-{slug}.md`. Commit (admin): `[product] spec: PRD {feature}`.

## Handoff
→ `cto` for estimate and feasibility · with `compliance-impact` → `compliance` ·
approved → `/product sync-clickup` (epic + tasks).
