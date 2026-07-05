# /admin export-template — Derive the public `company-os` template

## Purpose
Produce the public template repo from this one: same system logic,
zero data from the private source instance. The derivation must be mechanical, not handcrafted.

## Input
- Destination (repo/branch `company-os`) · version to tag

## Steps
1. **Verify the boundary**: everything specific to the private source instance lives ONLY in
   `config/*.yaml`, `company/`, `vault/`, `zones/*/context/`. Control grep over
   `os/`, `tools/`, `scripts/` for proper names (company name, clients, people, workspace
   IDs) → every hit outside the boundary is a bug to fix BEFORE the export.
2. **Build the template**:
   - empty `company/`, `vault/`; `config/` → only `*.example.yaml` (same fields,
     empty/placeholder values); `zones/*/context/` → placeholder files with instructions
   - keep: `os/` (agents, protocols, skills), `tools/osctl/`, `tools/viewer/`,
     `scripts/audit/`, `.github/workflows/`, `ARCHITECTURE.md` and `CLAUDE.md` genericized
   - reset `system/` (CHANGELOG restarted from 0.1.0, learnings empty, wiki empty)
3. **Mandatory leak-scan**: `secret-scan.sh` + dedicated scan for real names/data
   (people, clients, amounts, emails, ClickUp/Drive IDs). A single hit → export blocked.
4. **Smoke test**: in the derived repo, `link-lint.py` green and bootstrap docs coherent
   (a third party must be able to start from `*.example.yaml`).
5. **PREPARE → APPROVE → EXECUTE** for the push to the public repo; version tag.

## Output format (in chat)
```
## Export template — {version}
Boundary: OK/KO ({hits to fix}) · Leak-scan: OK/KO · Smoke: OK/KO
Push: {repo}@{tag} · Notes: {…}
```

## Destination
External repo `company-os`. In the source repo: no changes (or the boundary fixes,
committed with changelog).
