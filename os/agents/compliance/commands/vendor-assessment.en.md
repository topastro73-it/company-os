# /compliance vendor-assessment — Supplier assessment

## Purpose
Assess a supplier's security posture BEFORE signing. Supply chain security
is also a NIS2 requirement: no supplier with data without an assessment.

## Input
- Vendor · service provided · data processed (personal? of SMB customers? credentials?)
- Criticality for the service (if they go down, do we go down?)

## Steps
1. Check whether an assessment already exists in `compliance/vendors/{slug}.md` (validity:
   12 months) — if fresh, update only the deltas.
2. **Questionnaire/collection**: certifications (ISO 27001, SOC 2…), public policies,
   known incident history, sub-processors, data location (non-EU → SCC/adequacy),
   SLAs and support, exit strategy (data portability).
3. **Risk rating**: Critical / High / Medium / Low, as a function of data processed ×
   service criticality × demonstrated posture.
4. **DPA**: does it process personal data? → DPA mandatory; specific clauses needed
   (sub-processors, breach notification, audit right).
5. **Recommendation**: approve / approve with conditions (listed) / reject.
6. Record it and set the reassessment date (+12 months).

## Output format
```markdown
---
zone: compliance
tier: 🟡
type: vendor-assessment
vendor: {slug}
risk-rating: {critical|high|medium|low}
dpa-required: true
valid-until: YYYY-MM-DD
---
# Vendor Assessment — {vendor} — {YYYY-MM-DD}

## Service and data processed   ## Certifications and posture
## Identified risks             ## DPA and required clauses
## Recommendation: {esito} + conditions
```

## Destination
`compliance` zone → `vendors/{slug}.md`.
Commit (admin): `[compliance] vendor: assessment {vendor}`.

## Handoff
Approved → `finance` (contracting) and the requester (`cto`/`product`) ·
contract to review → `/compliance contract-review`.
