# /compliance evidence-check — Evidence verification

## Purpose
Evidence is what the auditor sees: verify that it exists, is up to date and
archived in `compliance/evidence/` (the only subzone visible to the external auditor).

## Input
None; optional: a specific framework. Recommended cadence: quarterly.

## Steps
1. For each active framework, verify the required evidence set:
   logs and monitoring · vulnerability scan reports · training records (incl. onboarding
   security training — comes from the CEO) · management approval minutes · previous
   audit reports · DR tests · incident register (from postmortems in the `prodotto` zone) ·
   vendor assessments (from `compliance/vendors/`) · security reviews (from `cto`).
2. For each piece of evidence: **does it exist? up to date** (within the required window: e.g. DR test
   every six months, training annually)? **archived** in `evidence/` with dated naming?
3. Evidence living elsewhere (postmortems, reviews) → copy/reference in `evidence/`,
   so the auditor finds it without accessing other zones.
4. Alerts for missing or expired evidence, with owner and date by which to regenerate it.
5. Update the index `compliance/evidence/README.md` (map evidence → where → freshness).

## Output format
```markdown
---
zone: compliance
tier: 🟡
type: evidence-check
---
# Evidence Check — {YYYY-MM-DD}

| Evidence | Framework | Required every | Last | Status | Regeneration owner |
|---|---|---|---|---|---|

## ⚠️ Missing or expired (actions with deadline)
## Index updated: yes/no
```

## Destination
`compliance` zone → `audits/evidence-check-{YYYY-MM-DD}.md` + `evidence/README.md`
updated. Commit (admin): `[compliance] evidence: check {YYYY-MM-DD}`.

## Handoff
Missing technical evidence (scans, DR tests) → `cto` · expired training → `ceo`.
