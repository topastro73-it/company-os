# /coo checkpoint — End-of-cycle human decision

## Purpose
Prepare the summary for the human owner or the CEO, who decides whether to continue, correct or
stop. The checkpoint resets the wave counter.

## Input
- The goal's VERIFY (results per criterion), last WAVE-NN, last standup

## Steps
1. Summary: results per criterion (refs only), delivered and blocked WOs, tokens consumed, budget.
2. Options: continue (next wave), correct (what changes in the plan), stop.
3. Explicit recommendation.
4. Present the draft in chat. **You stop and ask**: only the human decides and signs. Never sign
   on their behalf. A draft without a signature does not enter the ledger (ledger-check rejects it).
5. Once signed: write `CHECKPOINT-NN.md` with `decided-by: human:<slug>`, `decided-at` and
   `decision` as given by the human; `ledger-check --drive`, copy into the snapshot, `ledger-check`.

## Output format
Frontmatter: `zone: direzione`, `tier: 🟡`, `type: checkpoint`, `goal`, `wave` (last wave
covered), `decided-by`, `decided-at`, `decision` (prosegui | correggi | ferma — continue | correct | stop).

## Destination
`direzione` zone, `ops` subzone → `goals/G-NNN-slug/CHECKPOINT-NN.md`.

## Handoff
→ `ceo` (signature); after the signature → `/coo dispatch` or `/coo plan-goal` (correction).
