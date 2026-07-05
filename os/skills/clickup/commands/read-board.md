# ClickUp Command: read-board

Legge la Delivery Board e Product Roadmap, importa lo stato in `company/prodotto/clickup-board-current.md`.
Solo lettura — nessuna approvazione richiesta.

## Struttura della board

> Gli ID reali (folder, list) vivono in `config/integrations.yaml` (sezione clickup). I placeholder `<...>` vanno sostituiti con quei valori.

La Space "Product Engineering" è organizzata in due folder principali:

```
Delivery Board (folder <folder-id-delivery>)
├── Feature (<list-id-feature>)     ← task di sviluppo in corso
├── Bug (<list-id-bug>)         ← bug da fixare
├── Tech-debt (<list-id-techdebt>)   ← debito tecnico
├── War Room (<list-id-warroom>)    ← urgenze
└── Bug submission form (<list-id-bugform>)

Product Roadmap (folder <folder-id-roadmap>)
├── Epic (<list-id-epic>)        ← epic di roadmap
└── Release Planning (<list-id-release>) ← release
```

## Agenti autorizzati

Tutti

## Input richiesto

```bash
/product clickup read-board              # Tutto (default)
/product clickup read-board delivery     # Solo Delivery Board
/product clickup read-board roadmap      # Solo Product Roadmap / Epic
/product clickup read-board feature      # Solo list Feature
/product clickup read-board bug          # Solo list Bug
```

## Esecuzione

### List da leggere

| List | List ID | Comando MCP |
|------|---------|------------|
| Feature | <list-id-feature> | `clickup_filter_tasks(list_ids: ["<list-id-feature>"])` |
| Bug | <list-id-bug> | `clickup_filter_tasks(list_ids: ["<list-id-bug>"])` |
| Tech-debt | <list-id-techdebt> | `clickup_filter_tasks(list_ids: ["<list-id-techdebt>"])` |
| War Room | <list-id-warroom> | `clickup_filter_tasks(list_ids: ["<list-id-warroom>"])` |
| Epic | <list-id-epic> | `clickup_filter_tasks(list_ids: ["<list-id-epic>"])` |
| Release Planning | <list-id-release> | `clickup_filter_tasks(list_ids: ["<list-id-release>"])` |

**Nota**: passare sempre `workspace_id: "<workspace-id>"` a ogni chiamata.

### Campi da estrarre per ogni task

`id`, `name`, `status.status`, `priority`, `assignees`, `tags`, `due_date`, `url`

Per task con molti subtask, usare `detail_level: "summary"` per evitare risposte troppo grandi.

## Output: company/prodotto/clickup-board-current.md

```markdown
# Board Product Engineering — Snapshot

> Aggiornato: YYYY-MM-DD HH:MM

---

## 🚀 Delivery Board — Feature (List <list-id-feature>)

> Task di sviluppo in corso.

| ID | Summary | Assignee | Priority | Status | Due Date |
|----|---------|----------|----------|--------|----------|
| abc123 | SPF, DKIM, DMARC | mario | urgent | to test | 2026-03-25 |
| def456 | Custom domain setup | Mario Rossi | high | in progress | — |

**Totale**: N task | Per stato: To Do: X, In Progress: Y, In Review: Z, Done: W

---

## 🐛 Delivery Board — Bug (List <list-id-bug>)

| ID | Summary | Assignee | Priority | Status | Due Date |
|----|---------|----------|----------|--------|----------|
| ... | | | | | |

**Totale**: N task

---

## 🔧 Delivery Board — Tech-debt (List <list-id-techdebt>)

| ID | Summary | Priority | Status |
|----|---------|----------|--------|
| ... | | | |

**Totale**: N task

---

## 🚨 War Room (List <list-id-warroom>)

| ID | Summary | Assignee | Priority | Status |
|----|---------|----------|----------|--------|
| ... | | | | |

**Totale**: N task

---

## 🗺️ Product Roadmap — Epic (List <list-id-epic>)

| ID | Summary | Priority | Status | Tags |
|----|---------|----------|--------|------|
| ... | | | | |

**Totale**: N epic

---

## 📦 Release Planning (List <list-id-release>)

| ID | Summary | Status | Due Date |
|----|---------|--------|----------|
| ... | | | |

**Totale**: N release

---

## Riepilogo

| List | Count |
|------|-------|
| 🚀 Feature | N |
| 🐛 Bug | N |
| 🔧 Tech-debt | N |
| 🚨 War Room | N |
| 🗺️ Epic | N |
| 📦 Release | N |
| **Totale** | **N** |
```

## Post-esecuzione

Il file viene sovrascritto ad ogni lettura (è uno snapshot). Non viene committato automaticamente — è read-only.

Comunica: "Board letta. Feature: N task, Bug: N, Tech-debt: N, Epic: N."
