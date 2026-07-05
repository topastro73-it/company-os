# /cto incident-postmortem — Blameless postmortem

## Purpose
Turn an incident into systemic learning: what happened, why, what changes.

## Input
- Incident (what, when detected, when resolved) · impact (partners/SMBs affected, duration)

## Steps
1. **Factual timeline**: detection → diagnosis → mitigation → resolution, with timestamps.
   Who did what (to understand the process, never to assign blame).
2. **Impact**: partners/SMBs affected, data exposed yes/no, SLAs violated, duration.
3. **Root cause analysis** (5 Whys): the root cause is almost always process/system,
   not a person. Stop at the cause we can change.
4. What worked in the response / what did not.
5. **Action items**: max 5, each with owner and deadline — prevention (it does not happen again),
   detection (notice it sooner), mitigation (less damage).
6. **Notification obligations**: personal data involved or essential service impacted?
   → immediate handoff to `compliance` (24h/72h NIS2-GDPR notification assessment) and `ceo`.
   The postmortem is also evidence for the compliance incident register.
7. Communication to affected partners → `delivery` (gated PREPARE→APPROVE→EXECUTE).

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: postmortem
incident-date: YYYY-MM-DD
severity: {P0|P1|P2}
---
# Postmortem — {incident} (blameless)

## Timeline          ## Impact
## Root cause (5 Whys)
## What worked / what did not
## Action items | Action | Type (prev/detect/mitig) | Owner | Deadline |
## Notifications (compliance) and communications (partners)
```

## Destination
`prodotto` zone → `postmortem/YYYY-MM-DD-{slug}.md`; reference in the `compliance`
incident register. Commit (admin): `[cto] postmortem: {incident}`.

## Handoff
`compliance` (register + notifications) · `ceo` (if customer impact) · `delivery` (communication).
