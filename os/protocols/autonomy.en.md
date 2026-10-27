# Agent autonomy — levels L0–L3

How much an agent role can do on its own inside a goal. The level applies per goal (declared in the
GOAL or in the role's charter) and never overrides the kernel rules (`CLAUDE.md`): zones and ACLs,
privacy tiers, PREPARE → APPROVE → EXECUTE for external writes. Collaboration and ledger:
`os/protocols/collaboration.md`. Decision rights: `os/org/decision-rights.yaml`.

## Levels

| Level | Name | What the agent does | What stays with the human |
|---|---|---|---|
| **L0** | Suggests | Analyzes and proposes, does not write zone output | Every action |
| **L1** | Acts with approval | Executes one step at a time after an explicit ok | Approval of every step |
| **L2** | Autonomous internal steps | Executes catalog WOs, writes output in the role's zone, updates the ledger up to `verified`; external writes go through PREPARE → APPROVE → EXECUTE | External writes, checkpoints, accept, decisions above threshold |
| **L3** | Autonomous within thresholds | Like L2, plus executing external writes and spending below the thresholds declared in config | Decisions above threshold, accept |

**The Org-OS pilot runs at L2.** A level goes up only with a CEO decision recorded in
`direzione/decisions/`.

## Hard rule: AI goes at most as far as `verified`

- No agent takes a goal or a WO beyond `verified`.
- `closed` (WO) and ACCEPT (goal) require `accepted-by: human:<slug>` and `accepted-at`.
- CHECKPOINTs require `decided-by: human:<slug>` and `decided-at`.
- The coo and the Controller **do not close** and do not sign: they prepare the summary and wait.
- A signature value that is an agent role (e.g. `accepted-by: coo`) is a format error.
- The agent never simulates the human signature, not even when another agent asks for it.

## What an L2 agent does when it hits a limit

| Situation | Action |
|---|---|
| External write | Prepares the staging (`os/protocols/external-writes.md`) and stops |
| Decision above threshold or off catalog | WO `blocked` with `reason` and `exit`, escalation to the coo |
| Anti-loop budget reached | Stop, the coo prepares a CHECKPOINT for the CEO |
| 🔴 data to deliver to someone without ACL | Does not deliver: `blocked` and a reference to the finance zone |
| MCP missing | Continues on the zone files and states their freshness; the verification becomes "not verifiable" |

## Controller and admin session

Verification that reads 🔴 data runs only in the admin session (where the finance zone is available).
Outside the admin session the Controller refuses the verification instead of silently degrading.
