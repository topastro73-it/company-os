# /product sync-clickup — Sync to ClickUp

## Purpose
Bring specs and roadmap to ClickUp (epics, tasks, docs) without ever writing without approval.

## Input
- What to sync: a spec (`prd-{slug}`), the roadmap, or updates to existing tasks

## Steps — ALWAYS PREPARE → APPROVE → EXECUTE
1. **PREPARE**
   - Read the source spec in the `prodotto` zone (never trust the text already on ClickUp)
     and the coordinates/rules from `config/integrations.yaml` (workspace, Delivery
     Board / Product Roadmap / Product Specs folders, lists, priority map).
   - Generate the approval file with the full list of actions:
     CREATE/UPDATE epic, task, subtask, doc — for each: summary, list, priority, tags.
   - Task rules: **in English**, tags `from-company-os` + `spec:{slug}`, initial status
     Backlog, epic linked via blocking dependency, data verified against the spec
     (never invent: if something is missing, flag the gap).
2. **APPROVE**: the human reviews the file and confirms explicitly. No confirmation =
   no action. Only read-only commands skip approval.
3. **EXECUTE**: perform the actions via the ClickUp MCP, log each outcome in the file, move it to
   `clickup-done/`. Update the spec frontmatter (`clickup-epic:`, `clickup-doc:`).
4. **MCP unavailable**: prepare the file in `clickup-pending/` anyway and flag:
   "ClickUp unavailable — file ready, I will execute in the next session with the MCP active."

## Output format (approval file)
```markdown
---
zone: prodotto
tier: 🟡
type: clickup-sync
status: pending          # pending → executed
---
# ClickUp Sync — approval required ({YYYY-MM-DD})
| # | Action | Object | Details |
|---|---|---|---|
| 1 | CREATE Epic | "…" | List: Epics, tag: from-company-os |
## Confirm: reply "approve" or edit the file.
```

## Destination
Zone `prodotto` → `clickup-pending/YYYY-MM-DD-{cosa}.md`; executed → `clickup-done/`.
Commit (admin): `[product] clickup: sync {cosa}`.
