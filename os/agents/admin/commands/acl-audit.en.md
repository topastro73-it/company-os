# /admin acl-audit — Drive permissions audit

## Purpose
Verify that the **actual** Drive permissions match the `config/acl.yaml` matrix.
ACLs are the system's enforcement: drift is a breach, not a detail.

## Input
None. Cadence: part of `/admin health`; in any case after every change of people or zones.

## Steps
1. Run `osctl acl-audit`: it reads the permissions via the Drive API for every zone and subfolder
   and compares them with `config/acl.yaml` + `config/people.yaml`.
2. **Detect drift**:
   - person with extra access (not in the matrix) → 🔴 remove
   - missing person (in the matrix but without access) → 🟡 add
   - client folder `20-Clienti/{slug}/` without an assigned owner → 🟡
   - sensitive subfolders (`contratti/`, `per-commercialista/`, `evidence/`) with a wider
     ACL than expected → 🔴
   - externals (accountant, auditor, grants consultant) with access beyond their subzone → 🔴
3. **Propose the fixes**: for each drift, the exact Drive action. Applying it is an
   external write → PREPARE → APPROVE → EXECUTE.
4. If the drift is intentional (new person, assigned client) → update
   `config/acl.yaml`/`people.yaml` FIRST (commit + changelog), then apply.
5. Dated report; 🔴 drift on data → also flag to `compliance`.

## Output format
```markdown
## ACL Audit — {YYYY-MM-DD}
Zones checked: {n} · Drift: {n} (🔴 {n} · 🟡 {n})

| Zone/folder | Expected | Actual | Drift | Proposed fix |
|---|---|---|---|---|
```

## Destination
Report in chat + `system/audits/acl-audit-{YYYY-MM-DD}.md` (git).
Commit: `[admin] system: acl-audit {YYYY-MM-DD}`.
