# /coo unblock — Unblocking and escalation

## Purpose
Unblock a `blocked` WO or a conflict between roles, or bring the choice to the CEO.

## Input
- Blocked WO (`reason`, `exit`) or a conflict reported by a role

## Steps
1. Classify with `os/org/decision-rights.yaml`: off catalog, conflict, above threshold,
   access to a 🔴 zone.
2. If it falls within your rights (routing, new catalog WO, wave change): act,
   update the WO (`routed-by: coo` if it goes back to the parent's sender).
3. Otherwise escalate to the CEO: options (2-3), recommendation, budget impact. The WO stays
   `blocked` until the CEO decides.
4. `ledger-check --drive`, copy into the snapshot, `ledger-check`.

## Output format
WO update (status, `reason`, `exit`, `routed-by`) and one line in the next standup.

## Destination
`direzione` zone, `ops` subzone → `wo/WO-NNN.md`.

## Handoff
→ `ceo` for decisions beyond your rights; → target role for the new routing.
