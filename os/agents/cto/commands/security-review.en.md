# /cto security-review — Security risk analysis

## Purpose
Assess the security posture (of a feature, a component or overall) and
propose mitigations. We sell cybersecurity: we must be more secure than our customers.

## Input
- Scope: feature/spec, component, integration, or overall posture

## Steps
1. Load the scope (PRD or architecture) and the mapped controls in the `compliance` zone
   (ISO 27001 Annex A, NIS2 requirements) — the review speaks their language.
2. **Essential threat modeling** on the scope: attack surface, actors (partner,
   seller, SMB, external), critical assets (SMB scan data, credentials, PII).
3. **Minimum checklist**: authn/authz across the 3 user levels and tenant isolation ·
   input validation and injection · secrets management (never in repos/logs) · encryption
   at rest/in transit · logging and audit trail (without PII) · vulnerable dependencies ·
   backup and recovery.
4. For each risk: severity (Critical/High/Medium/Low), scenario, proposed mitigation,
   effort, owner.
5. **Compliance evidence**: the signed and dated review is evidence — flag it to
   `compliance` for archiving in `compliance/evidence/`.
6. Critical risks → immediate escalation to `ceo`; fixes → `product` backlog with priority.

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: security-review
scope: {…}
date: YYYY-MM-DD
---
# Security Review — {scope} — {date}

## Threat model (actors, assets, surface)
## Risks | Severity | Scenario | Mitigation | Effort | Owner |
## Quick wins (≤1 week)
## Evidence for compliance
```

## Destination
`prodotto` zone → `reviews/security-review-{scope}-{YYYY-MM-DD}.md`;
reference in `compliance/evidence/`. Commit (admin): `[cto] security: review {scope}`.

## Handoff
Evidence → `compliance` · fixes → `product` (backlog) · Critical → `ceo` within 24h.
