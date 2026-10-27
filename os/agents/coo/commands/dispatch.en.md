# /coo dispatch — Running a wave

## Purpose
Have the roles execute the WOs of a wave and record results and cost.

## Input
- Goal and wave number; the wave's WOs in `accepted` status

## Steps
1. Check the budget: the goal's WOs ≤ 15, waves since the last CHECKPOINT ≤ 3. Beyond that → stop,
   `/coo checkpoint`.
2. For each WO launch a **subagent** with a tight brief: the target role's `AGENT.md`,
   the WO, the command or service to run, the `inputs` (refs) and the output path in the
   `output-zone`. No access to zones outside the role's domain (`config/acl.yaml → roles`).
3. WOs addressed to `human:<slug>` are not launched: they stay `accepted` until the person delivers.
4. On delivery: WO → `delivered`, delivery note with refs only and `tokens: <n>` (the
   subagent's `total_tokens`). A WO that cannot proceed → `blocked` with `reason`/`exit`.
5. WOs issued by roles during the wave are routed into the next wave (never bounced back to the
   sender without `routed-by: coo`).
6. Write `WAVE-NN.md`: tokens per WO and total, WOs used out of 15, waves since the last checkpoint.
   Tokens only, never currency. Every count is written `<n> tok` (or `tokens: <n>` in the
   frontmatter): it is the only form in which `ledger-check` allows large numbers in the ledger.
7. `ledger-check --drive`, copy into the snapshot, `ledger-check`.

## Output format
`WAVE-NN.md`: frontmatter `zone: direzione`, `tier: 🟡`, `type: wave`, `goal`, `wave`; table
WO | role | status | tokens (cells in the form `<n> tok`).

## Destination
`direzione` zone, `ops` subzone → `goals/G-NNN-slug/WAVE-NN.md` and `wo/`.

## Handoff
→ `controller` (`verify`) at the end of the wave; → `/coo checkpoint` if the budget is at its limit.
