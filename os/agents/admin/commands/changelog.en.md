# /admin changelog — System change log

## Purpose
Every system change is tracked and versioned: `system/CHANGELOG.md` is the history
of the brain. No change to `os/`, `zones/`, `config/`, `tools/`, `CLAUDE.md`
gets in without an entry **in the same commit**.

## Input
- Description of the change · category: `feat` | `change` | `fix` | `breaking` | `refactor`
- Files touched (if not deducible from staging)

## Steps
1. Determine the **version**: `breaking` → bump the minor (x.Y.0); feat/change/fix/
   refactor → bump the patch (x.y.Z). The current version is at the top of the CHANGELOG.
2. Write the entry (format below): what changes, why, impact for whoever uses the system
   (which zone/agent will notice), any required action (e.g. "publish needed").
3. `breaking`: also document the rollback path (previous commit + what to
   republish to Drive).
4. Verify that the entry and the change are **in the same commit**
   (`[admin] system: {description}` — or the commit of the agent that made the change).
5. Remember the next step: `/admin publish` to distribute, if the change touches
   files that also live on Drive.

## Output format (entry)
```markdown
## [x.y.z] — YYYY-MM-DD
### {feat|change|fix|breaking|refactor}
- **{area}**: {what changed and why}
  - Impact: {who/what will notice}
  - Action: {publish required? migration? nothing}
  - Rollback (if breaking): {how}
```

## Destination
`system/CHANGELOG.md` (git). Committed together with the change it describes.

## Specific guardrails
- Entry without a change or change without an entry = inconsistency → `/admin health` flags it
- The CHANGELOG never contains business data — it describes the system, not the contents
