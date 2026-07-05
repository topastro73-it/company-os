# /compliance gap-analysis — Gap analysis per framework

## Purpose
Requirement-by-requirement analysis of a framework with a remediation roadmap.

## Input
- Framework: `nis2` | `gdpr` | `iso27001` | `iso27017` | `iso27018` | `soc2`

## Steps
1. Load the mapped requirements from `compliance/frameworks/{framework}-requirements.md`
   (for ISO 27001: the 93 Annex A 2022 controls; for NIS2: the 10 key requirements —
   risk mgmt, incident response 24h/72h, tested BC/DR, supply chain, vulnerability
   mgmt, encryption, MFA/access control, network monitoring, training, periodic audits).
2. For each requirement: status **compliant / partial / non-compliant / N/A**, available
   evidence (link in `evidence/`), gap if present.
3. For each gap: what is concretely missing, effort (S/M/L), owner, priority
   (does it block certification? expose to a penalty? required by an ongoing RFP?).
4. **Remediation roadmap** in phases with realistic dates; for ISO: ISMS review →
   controls update → internal audit → external audit.
5. Honest verdict: "ready for the audit? If not, what is missing and when will we be."

## Output format
```markdown
---
zone: compliance
tier: 🟡
type: gap-analysis
framework: {framework}
---
# Gap Analysis — {framework} — {YYYY-MM-DD}
Compliant: {n}/{tot} ({%}) · Partial: {n} · Non-compliant: {n} · N/A: {n}

## Gaps by priority
| Requirement | Status | Gap | Effort | Owner | Deadline |
## Remediation roadmap (phases + dates)
## Readiness verdict

> Internal assessment — the formal audit is up to the accredited body.
```

## Destination
`compliance` zone → `audits/gap-{framework}-{YYYY-MM-DD}.md`.
Commit (admin): `[compliance] gap: {framework}`.

## Handoff
Technical gaps → `cto` · process/training gaps → `ceo` · documentation gaps →
`/compliance policy-review`.
