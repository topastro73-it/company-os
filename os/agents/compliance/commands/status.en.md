# /compliance status — Compliance dashboard

## Purpose
A single view of the compliance status: frameworks, percentages, critical gaps, milestones.

## Input
None. Recommended cadence: monthly.

## Steps
1. Load `compliance/status.md` and the requirements mapped in `compliance/frameworks/`
   (NIS2, GDPR, ISO 27001/9001/27017/27018, SOC 2 if active).
2. For each framework: requirements mapped, satisfied **with evidence**, gaps.
   A requirement without archived evidence does NOT count as satisfied.
3. Classify the gaps: **critical** (they block certification/renewal or expose to a penalty)
   vs **important** (with deadline); each gap → action, effort S/M/L, owner.
4. **Deadlines**: upcoming surveillance/renewal audits, policies to re-approve,
   evidence about to expire, annual training.
5. Update `compliance/status.md` and generate the dated report.

## Output format
```markdown
---
zone: compliance
tier: 🟡
type: compliance-dashboard
---
# Compliance Dashboard — {YYYY-MM-DD}

## Overview
| Framework | Requirements | Satisfied (with evidence) | Gaps | % | Status |
|---|---|---|---|---|---|

## Critical gaps
| Gap | Framework | Effort | Owner | Deadline |
## Important gaps
## Upcoming deadlines and milestones
## Recommendations (max 3)

> Internal assessment. Formal certifications require an accredited auditor.
```

## Destination
`compliance` zone → `status.md` (updated) + `audits/dashboard-{YYYY-MM-DD}.md`.
Commit (admin): `[compliance] status: dashboard {YYYY-MM-DD}`.

## Handoff
Technical gaps → `cto` · gaps with a cost → `finance` · alerts → `cos` (compliance section
in briefings).
