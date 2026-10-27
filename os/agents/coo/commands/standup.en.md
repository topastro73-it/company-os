# /coo standup — Status of active goals

## Purpose
Give the CEO, inside `/ceo start`, the operational status of the goals: where we are, what is blocked,
what starts next.

## Input
- Ledger (`goals/`, `wo/`, last standup) on the Drive mount or, if missing, the snapshot

## Steps
1. List the goals with an active `status` and, for each, the current wave (last WAVE or open WOs).
2. WOs `blocked` or late on their `due`: reason and proposed `exit`, owner.
3. Available VERIFY results (by ref only) and checkpoints waiting for a signature.
4. Proposal for the next wave or for the checkpoint, with remaining budget.
5. Write `standup/YYYY-MM-DD.md`; `ledger-check --drive`, copy into the snapshot, `ledger-check`.

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: standup
---
# Standup YYYY-MM-DD
| Goal | Wave | Blocked | Next step | Budget (WO/15 · waves/3) |
```

## Destination
`direzione` zone, `ops` subzone → `standup/YYYY-MM-DD.md`.

## Handoff
→ `ceo` for checkpoints and decisions; → `/coo unblock` for blocked WOs.
