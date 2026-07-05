# /admin publish — git → Drive distribution

## Purpose
Bring the system (agents, protocols, zone CLAUDE.md, viewer, seeds) to the Drive zones,
read-only for collaborators. It is the only way a system change
reaches those who work on Drive.

## Input
- None (full publish) or a scope (`zones/`, `os/agents/`, a specific file)

## Steps
1. **Pre-check**: working tree clean and pushed; `scripts/audit/link-lint.py` and
   `secret-scan.sh` green; changelog up to date for the changes you are distributing.
2. **PREPARE**: run `osctl publish --dry-run` (or simulate): complete list of what
   will be written — file → destination Drive folder, which `.md` files with
   `render: gdoc` will be converted to Google Docs, what will be overwritten.
3. **APPROVE**: show the list to the founder; explicit confirmation. No confirmation =
   no write.
4. **EXECUTE**: `osctl publish`; log the results; partial errors → report of what
   went through and what did not (never leave the state ambiguous).
5. **Verify**: spot-check on Drive (a zone CLAUDE.md, the viewer in `_OS/`).
6. Record: commit `[admin] system: publish {scope}` if the publish updated
   metadata (e.g. Google Doc IDs in the frontmatter).

## Output format (in chat)
```
## Publish — {YYYY-MM-DD}
Scope: {…} · Files written: {n} · Google Docs created/updated: {n}
Errors: {n} (detail) · Spot check: OK/KO
```

## Destination
Drive: `_OS/`, `90-Condivisi/`, zone `CLAUDE.md`. No operational zone file
is touched (those are Drive-master).

## Specific guardrails
- Never publish 🔴 files or contents of `vault/`
- `git_to_drive` zones only: publish NEVER writes to Drive-master zones
