# /ceo close — Admin session closing

## Purpose
Persist everything: zone snapshots, narrative memory, learnings, commit, push, health.

## Input
None. Runnable only in an admin session (git).

## Steps
1. **Snapshot Drive → git**: run `osctl snapshot` (Drive-master zones → `company/`,
   finance → `vault/finance/`). If Drive is unreachable: report it and proceed with the repo.
2. **Session wiki**: generate `system/wiki/sessions/YYYY-MM-DD-{slug}.md` — decisions made,
   reasoning, promises, open questions. Pseudonymize customer people (initials + role);
   never 🔴/PII data (kernel rule §2).
3. **Learnings**: if reusable patterns emerged, propose max 2 new `LRN-XXX` for
   `system/learnings.md`; update the counters of those applied. The CEO approves/rejects.
4. **Memory**: business data that emerged in chat and is not yet saved → propose the right zone file
   (`os/protocols/memory.md`).
5. **Changelog check**: if the session touched `os/`, `zones/`, `config/`, `tools/`, `CLAUDE.md`
   → verify an entry in `system/CHANGELOG.md` in the same commit; if missing, create it now.
   Then ask: "is `osctl publish` needed to distribute to Drive?" (→ `/admin publish`).
6. **Guardrails**: run `scripts/audit/secret-scan.sh --staged` and `scripts/audit/link-lint.py`.
   If red: stop and fix before committing.
7. **Commit & push**: `git add -A` → commit `[ceo] close: YYYY-MM-DD` → `git fetch` →
   if the remote has new commits, `git merge origin/main --no-edit` → `git push origin main`
   (fallback `--rebase` if rejected).
8. **Health**: run `/admin health` in synthetic mode; report the traffic light.
9. **Final summary**: SHA, files touched, snapshot/publish outcome, conflicts, health alerts.

## Guardrails
- **NEVER** `git reset --hard` or `git push --force`
- Repo already clean → declare it and stop
- Branch ≠ main → warn before proceeding

## Destination
Git (commit) + `system/wiki/` + `system/learnings.md`. No new zone file.
