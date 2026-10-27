# /controller verify — Plan-blind verification against the sources

## Purpose
Establish for each criterion PASS, FAIL or not yet observable, with reproducible evidence
taken from the sources, not from the agents' account.

## Input
- The subagent's prompt contains **only** the paths of `GOAL.md`, `CRITERIA.md` and the list of
  observable sources (from the CONTEXT). No PLAN, `wo/`, WAVE, delivery notes.

## Steps
1. Run in a **fresh subagent**. First check the session: if `vault/finance/` does not exist,
   refuse ("🔴 verification only in admin session").
2. For each `### C<n>`: run the Observe on the sources (zone files, MCP read-only).
   MCP missing or source missing → "not verifiable" (never PASS).
3. Outcome: PASS | FAIL | not yet observable | not verifiable, with the evidence (path, query,
   read date) that someone else can re-run.
4. **Detail** (numbers, extracts, calculations) in the finance zone: `verify/G-NNN-verify-YYYY-MM-DD.md`.
5. **Ledger**: `VERIFY.md` with only the outcome per criterion and a ref to the detail. It does
   not mention WOs or the plan.
6. `ledger-check --drive`, copy into the snapshot, `ledger-check`.

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: verify
goal: G-NNN
---
| Criterio | Esito | Prova (ref) |
```

## Destination
Ledger: zone `direzione`, subzone `ops` → `goals/G-NNN-slug/VERIFY.md`.
Detail: zone `finance` (in admin `vault/finance/verify/`).

## Handoff
→ `coo` (`checkpoint`); → `ceo` if a critical criterion is FAIL.
