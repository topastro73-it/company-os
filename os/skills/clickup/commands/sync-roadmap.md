# ClickUp Command: sync-roadmap

Legge `company/prodotto/roadmap.md` e crea o aggiorna un task Epic su ClickUp per ogni feature della roadmap.

## Agenti autorizzati

PM, CTO

## Input richiesto

```
/product clickup sync-roadmap
```

Opzionalmente con filtro trimestre:
```
/product clickup sync-roadmap Q1-2026
```

## Fase 1: PREPARE

### 1.1 Leggi la roadmap

Carica `company/prodotto/roadmap.md`. Per ogni feature/iniziativa estrai:

- **Nome feature** → name del task Epic
- **Descrizione** → markdown_description del task Epic
- **Trimestre/Milestone** → inserito nella descrizione dell'Epic (non come tag)
- **Status** → mappato su stato ClickUp (see mapping sotto)
- **Owner/Team** → Assignee (usa `clickup_resolve_assignees` per risolvere nomi)
- **Priority** → mappato da posizione in roadmap o campo esplicito

Mapping status roadmap → stato ClickUp:
| Roadmap | ClickUp Status |
|---------|---------------|
| planned | to do |
| in-progress | in progress |
| shipped | complete / done |
| cut | closed |

### 1.2 Confronto con ClickUp esistente

Prima di creare, cerca Epic esistenti con tag `from-companyos` nella list Epic:

```
clickup_filter_tasks(
  tags: ["from-companyos"],
  list_ids: ["<list-id-epic>"],
  workspace_id: "<workspace-id>"
)
```

Per ogni feature della roadmap:
- Se esiste già un task con name corrispondente → **UPDATE** (non duplicare)
- Se non esiste → **CREATE**

### 1.3 Genera file di approvazione

Salva in `company/prodotto/clickup-pending/YYYY-MM-DD-sync-roadmap.md`:

```markdown
# ClickUp Sync — sync-roadmap — Approvazione richiesta
Data: YYYY-MM-DD
Sorgente: company/prodotto/roadmap.md
Filtro: Q1-2026 (o "tutti i trimestri")

## Azioni proposte

| # | Azione | Summary | Quarter | Priority | Note |
|---|--------|---------|---------|----------|------|
| 1 | CREATE | "Feature A" | Q1-2026 | high | Nuova |
| 2 | CREATE | "Feature B" | Q2-2026 | normal | Nuova |
| 3 | UPDATE | "Feature C" (ID: abc123) | Q1-2026 | high | Aggiorna priority e tag |
| 4 | SKIP | "Feature D" | Q3-2026 | low | Già aggiornata, nessun cambio |

## Tags standard
`from-companyos`, `{quarter}` (es. Q1-2026)

## Conferma
Per approvare: `/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-sync-roadmap.md`
```

## Fase 2: APPROVE

L'utente esegue:
```
/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-sync-roadmap.md
```

## Fase 3: EXECUTE

Per ogni riga del file approvato:

**CREATE**:
```
clickup_create_task(
  name: "Nome Feature",
  list_id: "<list-id-epic>",
  markdown_description: "...",
  priority: "high",
  tags: ["from-companyos"],
  workspace_id: "<workspace-id>"
)
```

La `markdown_description` di ogni Epic deve essere **autoconsistente**: il dev deve trovare nel task tutto il contesto per capire cosa sviluppare senza cercare altri documenti. Struttura minima:

```
## Contesto
[Perché questa feature esiste, problema che risolve, pillar flywheel (ATTRACT/ENGAGE/MANAGE/GROW)]

## Obiettivo
[Cosa deve essere vero quando l'epic è completata]

## Utenti coinvolti
[I ruoli utente del tuo prodotto — es. Partner / Venditore del partner / Cliente finale]

## Scope
[IN scope. OUT scope.]

## Target
[Quarter/milestone target, es. "Q2 2026 — non negoziabile"]

## Note tecniche / Dipendenze
[Prerequisiti, vincoli architetturali]

## Link spec
[company/prodotto/specs/{nome}.md]
```

**UPDATE**:
```
clickup_update_task(
  task_id: "abc123",
  priority: "high",
  status: "in progress",
  workspace_id: "<workspace-id>"
)
```

### Post-esecuzione

1. Aggiorna `company/prodotto/roadmap.md`: per ogni feature creata/aggiornata, aggiungi campo `clickup-epic: {task_id}`
2. Sposta file di approvazione in `clickup-done/`
3. Committa: `[product] clickup: sync-roadmap → N epic creati, M aggiornati`

## Note

- Non cancellare mai task Epic, anche se la feature è rimossa dalla roadmap
- Se una feature è "cut", aggiorna lo status a "closed" (se disponibile)
- Il name del task deve corrispondere esattamente al nome feature in roadmap per evitare duplicati
