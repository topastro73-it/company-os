# /delivery onboarding-status — Onboarding status

## Purpose
See at a glance where all onboarding partners are and what is behind schedule.

## Input
- Partner slug (optional — if omitted, all partners with active onboarding)

## Steps
1. Scan the partner cards in `clienti/*/scheda-partner.md` with
   `onboarding-phase` ≠ completed.
2. For each partner: current phase, week (1-12), % completion of the phase's tasks,
   next milestone with deadline.
3. **Detect delays**: tasks past deadline, phase lasting longer than the planned weeks
   (SETUP >2, ENABLEMENT >2, LAUNCH >4, OPTIMIZE >4).
4. **Critical milestones**: first scan (d.14), team trained (wk.4), first deal (wk.8),
   health baseline (wk.12) — if one is missed, the onboarding is at risk: flag it.
5. For a single partner: also show the current phase's checklist with per-task status.

## Output format
```markdown
---
zone: commerciale
tier: 🟡
type: report
---
# Onboarding Status — {YYYY-MM-DD}

| Partner | Phase | Wk. | Completion | Next milestone | Alert |
|---|---|---|---|---|---|
| {name} | LAUNCH | 6/12 | 75% | First deal (wk.8) | — |
| {name} | SETUP | 2/12 | 40% | First scan (d.7) | task 1.4 behind schedule |

## Delays and proposed actions (owner + deadline)
```
Single-partner drill-down: phase checklist with `[x]`/`[ ]`, deadlines, on-track yes/no.

## Destination
Cross-partner report: `commerciale` zone → `delivery/onboarding-status-{YYYY-MM-DD}.md`.
Single-partner status updates: in its `clienti/{slug}/onboarding-checklist.md`.

## Handoff
Technical task behind schedule → `cto`; uncooperative partner → `sales`/`ceo`.
