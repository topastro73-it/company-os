# ClickUp Command: read-board

Reads the Delivery Board and Product Roadmap, imports the state into `company/prodotto/clickup-board-current.md`.
Read-only — no approval required.

## Board structure

> The real IDs (folder, list) live in `config/integrations.yaml` (clickup section). The `<...>` placeholders must be replaced with those values.

The "Product Engineering" Space is organized into two main folders:

```
Delivery Board (folder <folder-id-delivery>)
├── Feature (<list-id-feature>)     ← development tasks in progress
├── Bug (<list-id-bug>)         ← bugs to fix
├── Tech-debt (<list-id-techdebt>)   ← technical debt
├── War Room (<list-id-warroom>)    ← urgencies
└── Bug submission form (<list-id-bugform>)

Product Roadmap (folder <folder-id-roadmap>)
├── Epic (<list-id-epic>)        ← roadmap epics
└── Release Planning (<list-id-release>) ← releases
```

## Authorized agents

All

## Required input

```bash
/product clickup read-board              # Everything (default)
/product clickup read-board delivery     # Delivery Board only
/product clickup read-board roadmap      # Product Roadmap / Epic only
/product clickup read-board feature      # Feature list only
/product clickup read-board bug          # Bug list only
```

## Execution

### Lists to read

| List | List ID | MCP command |
|------|---------|------------|
| Feature | <list-id-feature> | `clickup_filter_tasks(list_ids: ["<list-id-feature>"])` |
| Bug | <list-id-bug> | `clickup_filter_tasks(list_ids: ["<list-id-bug>"])` |
| Tech-debt | <list-id-techdebt> | `clickup_filter_tasks(list_ids: ["<list-id-techdebt>"])` |
| War Room | <list-id-warroom> | `clickup_filter_tasks(list_ids: ["<list-id-warroom>"])` |
| Epic | <list-id-epic> | `clickup_filter_tasks(list_ids: ["<list-id-epic>"])` |
| Release Planning | <list-id-release> | `clickup_filter_tasks(list_ids: ["<list-id-release>"])` |

**Note**: always pass `workspace_id: "<workspace-id>"` on every call.

### Fields to extract for each task

`id`, `name`, `status.status`, `priority`, `assignees`, `tags`, `due_date`, `url`

For tasks with many subtasks, use `detail_level: "summary"` to avoid overly large responses.

## Output: company/prodotto/clickup-board-current.md

```markdown
# Product Engineering Board — Snapshot

> Updated: YYYY-MM-DD HH:MM

---

## 🚀 Delivery Board — Feature (List <list-id-feature>)

> Development tasks in progress.

| ID | Summary | Assignee | Priority | Status | Due Date |
|----|---------|----------|----------|--------|----------|
| abc123 | SPF, DKIM, DMARC | mario | urgent | to test | 2026-03-25 |
| def456 | Custom domain setup | Mario Rossi | high | in progress | — |

**Total**: N tasks | By status: To Do: X, In Progress: Y, In Review: Z, Done: W

---

## 🐛 Delivery Board — Bug (List <list-id-bug>)

| ID | Summary | Assignee | Priority | Status | Due Date |
|----|---------|----------|----------|--------|----------|
| ... | | | | | |

**Total**: N tasks

---

## 🔧 Delivery Board — Tech-debt (List <list-id-techdebt>)

| ID | Summary | Priority | Status |
|----|---------|----------|--------|
| ... | | | |

**Total**: N tasks

---

## 🚨 War Room (List <list-id-warroom>)

| ID | Summary | Assignee | Priority | Status |
|----|---------|----------|----------|--------|
| ... | | | | |

**Total**: N tasks

---

## 🗺️ Product Roadmap — Epic (List <list-id-epic>)

| ID | Summary | Priority | Status | Tags |
|----|---------|----------|--------|------|
| ... | | | | |

**Total**: N epics

---

## 📦 Release Planning (List <list-id-release>)

| ID | Summary | Status | Due Date |
|----|---------|--------|----------|
| ... | | | |

**Total**: N releases

---

## Summary

| List | Count |
|------|-------|
| 🚀 Feature | N |
| 🐛 Bug | N |
| 🔧 Tech-debt | N |
| 🚨 War Room | N |
| 🗺️ Epic | N |
| 📦 Release | N |
| **Total** | **N** |
```

## Post-execution

The file is overwritten on each read (it is a snapshot). It is not committed automatically — it is read-only.

Communicate: "Board read. Feature: N tasks, Bug: N, Tech-debt: N, Epic: N."
