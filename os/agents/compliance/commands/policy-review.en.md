# /compliance policy-review — Policy register review

## Purpose
Verify that all policies exist, are up to date, approved and communicated.
Recommended cadence: quarterly.

## Input
None; optional: a single policy to review in depth.

## Steps
1. Inventory in `compliance/policies/` against the expected set: Information Security,
   Acceptable Use, Incident Response, Business Continuity, Data Classification,
   Access Control, Encryption, Vendor Management, Change Management, HR Security
   (onboarding/offboarding).
2. For each policy, four checks: **does it exist? up to date** (<12 months or after relevant changes)?
   **approved** (by management, with date)? **communicated** (to the team, with evidence)?
3. Missing or stale policies → creation/update plan with owner and deadline.
4. **Consistency with reality**: a policy describing processes we don't actually follow is a
   risk in an audit, not a point in our favor — flag known divergences (ask `cto` to confirm
   the declared technical controls).
5. Approvals and communications completed → record the evidence in `compliance/evidence/`.

## Output format
```markdown
---
zone: compliance
tier: 🟡
type: policy-review
---
# Policy Review — {YYYY-MM-DD}

| Policy | Exists | Up to date | Approved | Communicated | Action |
|---|---|---|---|---|---|

## Missing / stale (plan with owner and deadline)
## Divergences policy ↔ actual practice
## Evidence recorded
```

## Destination
`compliance` zone → `audits/policy-review-{YYYY-MM-DD}.md`; updated policies in
`compliance/policies/`. Commit (admin): `[compliance] policy: review {YYYY-MM-DD}`.

## Handoff
Policy approval → `ceo` · declared technical controls → `cto` (verification).
