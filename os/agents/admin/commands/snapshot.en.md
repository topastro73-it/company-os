# /admin snapshot — Drive → git backup

## Purpose
Download the Drive-master operational zones into the repo (`company/`, `vault/finance/`) and
commit: git remains the versioning and full backup of the operational plane too.
Runs nightly (GitHub Action) and manually at `/ceo close`.

## Input
- None (all Drive-master zones) or a specific zone

## Steps
1. Run `osctl snapshot`: for every zone with `sync: drive_master` in `config/acl.yaml`
   download the files into the destination (`company/{zona}/`; `finance` → `vault/finance/`).
2. **One direction only**: the snapshot writes ONLY from Drive to git. If `company/`
   contains unpublished local changes that would be overwritten → stop and flag
   the conflict (the master wins, but the loss must be declared, never silent).
3. **Secret-scan** on the downloaded material: 🔴 files out of place (e.g. a signed contract
   in the wrong zone) → alert, do not commit until it is relocated.
4. Commit: `[snapshot] drive: {YYYY-MM-DD}` (vault: separate commit in the private repo).
5. Report: new/modified/removed files per zone, anomalies, unexpected sizes.

## Output format (in chat)
```
## Snapshot — {YYYY-MM-DD}
| Zone | New | Modified | Removed | Anomalies |
|---|---|---|---|---|
Commit: {sha} · Vault: {sha|n/a} · Alerts: {…}
```

## Destination
Git: `company/{zona}/` and `vault/finance/`. No writes to Drive.

## Specific guardrails
- Drive unreachable → flag it and stop without an ambiguous partial commit
- Never resolve a conflict by writing to Drive from here: the fix happens on the master (Drive)
