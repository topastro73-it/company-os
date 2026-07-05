# /finance bandi-status — Grants and incentives pipeline

## Purpose
Track grants and public incentives (Invitalia, MIMIT, regional programs, R&D tax credit, Formazione 4.0):
what we are pursuing, deadlines, reporting obligations. Area shared with the grants consultant (external,
writes ONLY here).

## Input
- None (report) or an update ("add grant {X}", "application {Y} submitted")

## Steps
1. Load `finance/bandi/` — one file per grant + a `status.md` summary.
2. **Data model** per grant: issuing body, subject, potential amount, stage
   (`radar → valutazione → in-preparazione → presentato → ammesso | respinto →
   in-rendicontazione → chiuso`), submission deadline, reporting deadlines,
   owner (grants consultant/CEO), required documents with status.
3. **Alerts**: submission deadline ≤14 days with missing documents → 🔴; reporting
   ≤30 days → 🟡; requirements at risk (e.g. maintaining innovative-startup requirements) → flag.
4. **Eligibility for new grants**: flag the opportunity with requirements and effort; the
   tax/formal eligibility confirmation belongs to **the accountant** — never take it for granted.
5. Update `status.md`; awarded amounts enter the cashflow as inflows **only
   after formal admission**, with a realistic disbursement date (never as revenue).

## Output format
```markdown
---
zone: finance/bandi
tier: 🔴
type: bandi-status
---
# Grants — {YYYY-MM-DD}

## Alerts (deadlines and missing documents)
## Pipeline
| Grant | Body | Amount | Stage | Next deadline | Owner | Notes |
## In reporting (obligations and dates)
## New opportunities to evaluate (validate with the accountant)
```

## Destination
Subzone `finance/bandi` → `status.md` + one file per grant.
Commit (admin): `[finance] bandi: status {YYYY-MM-DD}`.

## Handoff
Admission/disbursement → `/finance cashflow` · decision to participate (high effort) → `ceo`.
