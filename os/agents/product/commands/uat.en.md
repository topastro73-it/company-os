# /product uat — UAT / QA with GO/NO-GO verdict

## Purpose
Verify that a feature does what the PRD promises, before release.
Operational owner: the PMO/QA.

## Input
- Spec slug · phase: `plan` (generate the plan) or `report` (record the results of a cycle)

## Steps
### Plan phase (at the `in-development` transition)
1. Read the PRD: user stories and acceptance criteria are the basis of the test cases.
2. Generate the **test plan**: scope, environments, test data needed,
   test case ↔ acceptance criteria matrix (Given/When/Then → verifiable steps),
   edge cases, regression tests on the core flows touched.
3. If the spec has `compliance-impact` or touches auth/data: add a security checklist
   (input validation, authz for the 3 user levels, PII in logs) — review with `cto`.

### Report phase (at the end of a test cycle)
4. Run/collect the results: pass/fail for each test case, bugs with severity P0-P3.
5. **Verdict**: **GO** (no open P0/P1, ACs covered) / **NO-GO** (explicit reasons,
   blocking bugs, retest needed).
6. The GO verdict is a **necessary condition** for `status: shipped` (with the ClickUp epic
   Released). NO-GO → the spec stays in-development, bugs → `/product sync-clickup`.

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: uat
spec: {slug}
cycle: 1
verdict: null            # GO | NO-GO
---
# UAT — {feature} — cycle {N}
## Test plan / results
| TC | Acceptance criterion | Steps | Outcome | Bug |
## Open bugs (severity, owner)   ## Verdict and rationale
```

## Destination
Zone `prodotto` → `testing/uat-{slug}-cycle{N}.md`.
Commit (admin): `[product] uat: {slug} cycle {N} — {verdict}`.

## Handoff
NO-GO → `cto` (fix) · GO → update spec to shipped + `/product release-notes`.
