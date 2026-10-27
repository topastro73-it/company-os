# /controller criteria — Plan-blind criteria for a goal

## Purpose
Register falsifiable criteria for the goal before any plan exists, so that the verification
cannot bend to fit the work done.

## Input
- Only the goal's `GOAL.md` and `CONTEXT.md`, the canon, the sources listed in the CONTEXT
- Never PLAN, WO or WAVE (they must not exist yet; if they do, you don't open them)

## Steps
1. Run in a **fresh subagent** whose prompt holds only the paths above.
2. For each outcome expected from the intent, write a criterion `### C<n> — title` with
   **Observe** (what gets opened or measured, on which source) and **Fails if** (what falsifies it).
3. Thresholds in months or percentages; amounts live in a file in the finance zone,
   referenced. No monetary figures in the ledger.
4. The text does not mention work orders, waves or plan choices.
5. **Propose the thresholds to the owner and wait for confirmation** in chat. Without
   confirmation the file is not registered.
6. Once confirmed: frontmatter `confirmed-by: human:<slug>`, `registered-at`; write to the
   mount, `ledger-check --drive`, copy into the snapshot, `ledger-check`.
7. Commit it **on its own**, before any PLAN: the hash is the plan's `criteria-commit`.

## Output format
Frontmatter: `zone: direzione`, `tier: 🟡`, `type: criteria`, `goal`, `confirmed-by`,
`registered-at`. Body: `### C<n>` with Observe / Fails if.

## Destination
Zone `direzione`, subzone `ops` → `goals/G-NNN-slug/CRITERIA.md`.

## Handoff
→ `coo` (`plan-goal`, plan phase) with the commit hash.
