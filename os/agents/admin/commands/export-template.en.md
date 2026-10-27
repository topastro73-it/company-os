# /admin export-template — Derive the public `company-os` template

## Purpose
Produce the public template repo from this one: same system logic,
zero data from the private source instance. The derivation must be mechanical, not handcrafted.

## Input
- Destination (repo/branch `company-os`) · version to tag

## Steps
1. **Dry-run**: `python3 tools/osctl/osctl.py export-template` (parameters in
   `config/export.yaml`: destination clone, included roots, excluded instance files,
   `template_owned` files, leak-scan terms). It shows new, updated and to-be-deleted files, orphaned
   `.en.md` variants, translations to do and to redo, and the leak-scan result **on what would go out**.
2. **Verify the boundary**: everything instance-specific lives ONLY in `config/*.yaml`,
   `company/`, `vault/`, `zones/*/context/`, or in files listed under `exclude`. Inside a shared
   system file, an instance line is marked with a comment containing `@instance`
   (`<!--`, `#` or `//` depending on the format); a block is enclosed between `@instance-begin` and
   `@instance-end`. The export strips them. A leak-scan hit is a boundary bug: fix it here,
   with changelog, **before** the export. Never add a real term to `allow_terms` to make it
   pass: `allow_terms` is only for generic words that happen to match a client slug.
3. **Apply**: `osctl export-template --apply` writes into the clone's working tree. **The export is
   a merge, not an overwrite**:
   - base files `X.md` are overwritten from the source (`@instance` markers stripped);
   - the template's `X.en.md` variants are **never deleted**, except when their base file
     has disappeared from the source (orphans);
   - `template_owned` files (`CLAUDE.md`, `ARCHITECTURE.md`, README, `LICENSE`, `config/`,
     `company/`, `vault/`, `system/`, `zones/*/context/`, the placeholder brand kit, `i18n-parity`)
     have their own content in the template: the export does not touch them and flags when their
     twin here has changed, because porting there is done by hand;
   - no commit and no push.
4. **In the template clone**: translate the "to translate" files and retranslate the "to retranslate"
   ones (`os/protocols/language.md` §4), update the template's `system/CHANGELOG.md` (new version,
   with the kernel version it started from), then smoke test: `link-lint.py --strict`,
   `convention-check.py --strict`, **`i18n-parity.py --strict`** and `secret-scan.sh`, all green.
   Bootstrap docs coherent: a third party must be able to start from `*.example.yaml`.
5. **PREPARE → APPROVE → EXECUTE** for the push to the public repo; version tag.

## Output format (in chat)
```
## Export template — {version}
Boundary: OK/KO ({hits to fix}) · Leak-scan: OK/KO · Smoke: OK/KO
Push: {repo}@{tag} · Notes: {…}
```

## Destination
External repo `company-os`. In the source repo: no changes (or the boundary fixes,
committed with changelog). Record the version mapping in `system/CHANGELOG.md`
(e.g. kernel 2.10.0 ↔ company-os 0.6.0): it is the starting point for the next export.
