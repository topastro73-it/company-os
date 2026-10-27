# /coo plan-goal — Intent and wave plan of a goal

## Purpose
Turn the human owner's intent into a ledger goal and, only after the criteria have been
recorded, into a wave plan of work orders.

## Input
- The owner's intent (chat or a decision in `direzione/decisions/`), owner `human:<slug>`, deadline
- For the plan phase: the goal's CRITERIA already committed (commit hash)

## Steps
**Phase A — intent** (no plan):
1. Assign the id `G-NNN` (next in the ledger) and the slug.
2. Write `goals/G-NNN-slug/GOAL.md`: verifiable intent, `owner: human:<slug>`, `due`,
   roles involved, human contributors with their subzone.
3. Write `CONTEXT.md`: observable sources (zone paths, MCP in read mode), constraints, out of scope.
4. No figures: thresholds and amounts stay in the finance zone, only refs in the ledger.
5. Handoff to `/controller criteria`. **You stop here** until the CRITERIA are committed.

**Phase B — plan** (only with committed CRITERIA):
6. Write `PLAN.md` with `criteria-commit: <hash>`, numbered waves, planned total WOs ≤ 15,
   planned human checkpoint (at the latest after 3 waves). Waves after the first are only outlined.
7. Write the wave 1 WOs in `wo/WO-NNN.md` (format in `os/protocols/collaboration.md`):
   a catalog service offered by the recipient, `inputs` as refs, `criteria` as existing C-ids.
8. Run `ledger-check --drive`, copy the files into the snapshot, run `ledger-check`.

## Output format
GOAL frontmatter: `zone: direzione`, `tier: 🟡`, `type: goal`, `id`, `owner`, `due`, `status`.
PLAN frontmatter: `type: plan`, `goal`, `criteria-commit`. WO: the protocol's fields.

## Destination
`direzione` zone, `ops` subzone (Drive mount in admin) → `goals/G-NNN-slug/`, `wo/`.

## Handoff
Phase A → `controller` (`criteria`). Phase B → `/coo dispatch`.
