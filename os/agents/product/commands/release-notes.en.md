# /product release-notes — Release notes

## Purpose
Document what shipped: complete internal version + version communicable to partners.

## Input
- Release/version · specs included (shipped in this release)

## Steps
1. Verify prerequisites for each included spec: UAT with a **GO** verdict and ClickUp epic
   Released. If anything is missing → the spec does not go into the notes (and is not shipped).
2. **Spec-reconciliation**: compare the PRD with what was actually built (epic tasks and
   comments); if they diverge, update the PRD first, then write the notes.
3. **Internal version**: what changed, for which user level (Partner / Salesperson /
   SMB), migrations or required actions, known issues, links to spec and UAT.
4. **Partner version** (non-technical language): benefit before the feature, what
   they need to do (if anything), screenshots/assets if available. Never promises about what
   is coming — only what is shipped.
5. Update `prodotto/specs/INDEX.md` (status shipped) and the roadmap.

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: release-notes
release: {vX.Y}
date: YYYY-MM-DD
---
# Release {vX.Y} — {date}

## What's new (by user level)
| Feature | Level | Spec | UAT |
## Required actions   ## Known issues

---
## Partner version (communicable)
{text ready to send/publish}
```

## Destination
Zone `prodotto` → `releases/release-{vX.Y}.md`.
Commit (admin): `[product] release: {vX.Y}`.

## Handoff
Tier 1/2 features → `marketing` (`/marketing launch-plan`) · communication to partners →
`delivery` (gated send PREPARE→APPROVE→EXECUTE).
