---
type: learnings
updated: template
total: 1
active: 1
zone: _os
tier: 🟡
---

# Learnings — rules learned from experience

Operational rules that the system applies proactively (protocol: `os/protocols/memory.md`).
The template starts almost empty: learnings grow as your company operates. One seed
remains, generic and useful to anyone, about the Drive permission model.

## Format

```markdown
### LRN-XXX: Title
- **Rule**: When [situation], [what to do / what happens].
- **Source**: [session / event]
- **Applied**: 0 times
- **Tags**: ...
- **Status**: active
```

## Active learnings

### LRN-001: Google Drive inherits permissions only downward — never a "more restricted" subfolder
- **Rule**: When designing a zone/subzone with a tighter ACL than its parent folder (e.g.
  "contratti/ inside the client folder, for just a few people"), check FIRST whether someone
  with broader access to the parent already exists: if so, they will inherit access to the
  subfolder anyway — Google Drive does not allow *removing* permissions deeper down, only
  adding them. Zones "more restricted than the parent" must be **separate top-level folders**
  (e.g. `70-Contratti-Riservati/`), never subfolders of a more permissive zone. Subzones in
  `acl.yaml` remain valid ONLY when they *add* people (e.g. a `bandi/` subfolder that
  grants access to a consultant otherwise excluded from the finance zone).
- **Source**: Template seed — CompanyOS permission model
- **Applied**: 0 times
- **Tags**: sistema, drive, acl, permessi, architettura
- **Status**: active

---

## Archived learnings

*(none)*
