# Collaboration between agents — ledger, work orders, waves

How agent roles work as a team on a company goal. The loop: intent → pre-registered
(plan-blind) criteria → wave plan of work orders (WOs) → execution by competence →
plan-blind verification by the Controller → human accept. It is coordinated by the **coo** agent, which answers to the
**CEO**. Every goal has **a single accountable human owner**. Autonomy levels: `os/protocols/autonomy.md`.
Roles, services and decisions: `os/org/services.yaml`, `os/org/decision-rights.yaml`, domains in
`config/acl.yaml → roles`.

## Ledger (`direzione` zone, `ops` subzone, Drive-master)

```
ops/goals/G-NNN-slug/  GOAL.md · CONTEXT.md · CRITERIA.md · PLAN.md · VERIFY.md
                       WAVE-NN.md · CHECKPOINT-NN.md · ACCEPT.md
ops/wo/WO-NNN.md       one file per work order (global numbering)
ops/scorecard.md       dated weekly rows (measurable, owner, status, ref)
ops/standup/YYYY-MM-DD.md
```

You write on Drive (in admin: local mount `OS_DRIVE_MOUNT`), then the snapshot brings the files into
`company/direzione/ops/`. Never two-way on the same file.

**Common frontmatter** for every file: `zone: direzione`, `tier: 🟡`, `type:` ∈ {goal, context,
criteria, plan, verify, checkpoint, wave, accept, wo, scorecard, standup}.

- GOAL: `id`, `owner: human:<slug>`, `due`, `status`.
- PLAN: `criteria-commit: <hash>` of the commit that recorded the CRITERIA.
- CHECKPOINT: `decided-by: human:<slug>`, `decided-at`, `decision` (prosegui | correggi | ferma — continue | correct | stop).
- ACCEPT: `accepted-by: human:<slug>`, `accepted-at`.

## Work order

```yaml
id: WO-NNN            # = file name
goal: G-NNN           # reference goal
from: coo             # issuing agent role
to: <ruolo> | human:<slug>
service: <servizio>   # offered by `to` in os/org/services.yaml
intent: "one line: why it is needed"
inputs: [<path o id>] # references only, never pasted data
output-zone: <zona or zona.sotto from config/acl.yaml>
output-tier: 🔴 | 🟡 | 🟢
criteria: [C1, C3]    # existing C-ids in the goal's CRITERIA
due: YYYY-MM-DD
status: proposed
wave: 1
parent:               # WO it derives from (empty if none)
routed-by:            # `coo` if `to` is the parent's sender
accepted-by:          # human:<slug> — required with status closed
accepted-at:
```

**States**: `proposed → accepted → in-progress → delivered → verified → closed`; exits
`rejected` and `blocked`, which require `reason` (why) and `exit` (proposed way out).
The delivery note (`delivered`) contains only refs to the output and `tokens: <n>`.

**Who issues WOs**: the coo and the pilot roles, only toward catalog services. The `cos` **does not
issue or assign WOs**: it reads the ledger and briefs the coo and the CEO.

## Interaction modes (Team Topologies)

| Mode | When | Does it go through the coo? |
|---|---|---|
| **X-as-a-Service** | catalog service, known inputs/outputs | no: direct WO between roles, the coo sees it in the ledger |
| **Collaboration** | new work, off catalog, several roles together | yes: the coo opens the WOs and decides the wave |
| **Facilitating** | one role helps another use a service | yes, time-boxed, with a dedicated WO |

The coo also decides priorities between goals and conflicts; above the thresholds in
`os/org/decision-rights.yaml` the CEO decides.

## Escalation

Role → **coo** → **CEO**. A `blocked` WO goes to the coo within the day; the coo unblocks it
(`/coo unblock`) or brings the choice to the CEO with options and a recommendation.

## Anti-loop and budget

- **≤ 15 WOs per goal** and **≤ 3 waves** after the last human CHECKPOINT.
- At the limit: stop, no new WOs, escalation to the CEO with a CHECKPOINT to sign.
- **No bounce back to the sender**: a derived WO does not go back to the role that issued the parent,
  unless `routed-by: coo`.
- At the end of a wave the coo writes `WAVE-NN.md` with the cost **in tokens** per WO and in total (never currency),
  written `<n> tok`.

## Blackboard + dispatcher

Subagents do not launch subagents. So the coo runs **in the main session**: it reads the
ledger (blackboard), launches the wave's subagents with a tight brief (WO + output path),
collects the WOs they issue and routes them into the next wave.

## Sensitive data (ADR-004)

- **Only references** in the ledger: no amounts, IBANs, tax codes/VAT numbers, balances or salaries.
- Criteria thresholds are expressed in months or percentages; amounts live in a file in the finance zone.
- The ledger's VERIFY contains only the **result per criterion** and the ref; the detail with the
  numbers lives in the finance zone.
- A WO with 🔴 output goes only toward a 🔴 zone (`tier: restricted` or `snapshot_target: vault`) and
  toward a recipient with access to that zone.
- The WAVE reports costs in tokens.
- **Numbers allowed in the ledger** (`scripts/audit/ledger-check.py`, list of allowed numbers):
  0–99, dates, ISO weeks, years, ids (`G-NNN`, `WO-NNN`, `P-NNN`), percentages, versions,
  commit hashes, `tokens: <n>` and `<n> tok`. Any other number with 3+ digits blocks the commit:
  it moves to the finance zone and only the reference stays in the ledger.

## Plan-blind

The goal's CRITERIA are **committed before** the PLAN, written by the Controller reading only GOAL,
CONTEXT and canon. The PLAN cites `criteria-commit`. The CRITERIA do not cite WOs or waves; the VERIFY
does not cite WOs or the PLAN: the evidence is always an observable source.

## Mechanical guardrail

`scripts/audit/` → ledger-check.py enforces this protocol (format, states, WO contracts,
🔴 routing, human signatures, budget, plan-blind) in pre-commit, CI, snapshot and
`/admin health`. Red = stop and fix it.
