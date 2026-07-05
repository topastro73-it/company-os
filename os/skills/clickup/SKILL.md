# ClickUp Skill

Integrazione con ClickUp via MCP (Model Context Protocol). Disponibile per agenti: PM, CTO, Chief of Staff.

## Regole globali ClickUp

### Lingua dei task

Tutti i task ClickUp (titolo, descrizione, acceptance criteria, DoD) devono essere scritti **sempre in lingua inglese**. Nessuna eccezione. Anche se la spec sorgente è in italiano, il task su ClickUp è in inglese.

### Verifica spec + epic prima di scrivere/riscrivere un task

Prima di creare o riscrivere qualsiasi task, l'agente DEVE:

1. **Leggere la spec sorgente** (`company/prodotto/specs/prd-{slug}.md`) per estrarre i dati corretti — non fidarsi del testo esistente nel task
2. **Leggere l'epic** (su ClickUp o nel repo) per capire il contesto complessivo e le relazioni tra task
3. **Verificare i dati citati** — se il task menziona regole, mapping, domini, soglie, confrontarli con la spec sorgente per assicurarsi che siano corretti e aggiornati
4. **Non inventare dati** — se un'informazione non è nella spec, non includerla nel task. Segnalare il gap al PM

Questa regola previene task che copiano informazioni stale o errate da versioni precedenti.

### Come trovare l'epic di un task

Le epic vivono nella lista **Epics** (<list-id-epic>) nella board **Product Roadmap** (Folder <folder-id-roadmap>). I Feature task sono collegati all'epic tramite una **dependency di tipo `blocking`** (Feature blocks Epic). Per trovare l'epic di un task:

1. Leggere il campo `dependencies` del task
2. Il task con `type: 1` (blocking) che si trova nella lista Epics è l'epic parent
3. In alternativa: il frontmatter della spec ha il campo `clickup-epic:` con ID e link diretto

**Frontmatter spec**: ogni spec DEVE avere `clickup-epic:` nel frontmatter con il formato `"[{epic_id}](https://app.clickup.com/t/{epic_id})"`. Il vecchio campo `jira-epic:` non è più usato (migrato ad aprile 2026).

### ClickUp Docs — Product Specs

Le spec del prodotto sono pubblicate come **Doc ClickUp individuali** dentro il Folder **"Product Specs"**:

```yaml
folder_id: "<folder-id-specs>"
folder_name: "Product Specs"
location: Space Product Engineering (<space-id>) → Product Specs (<folder-id-specs>)
```

**Naming convention**: ogni Doc ha il nome esplicativo della spec (es. `PRD — Assessment Report: Gap Analysis & Remediation Plan`), NON un nome generico. Il nome del Doc DEVE corrispondere al titolo `# ...` della spec.

**Struttura**:
```
Product Engineering (Space)
├── Product Specs (Folder <folder-id-specs>)
│   ├── Doc: "PRD — Assessment Report: Gap Analysis & Remediation Plan"
│   ├── Doc: "PRD — AI Sales Assistant"
│   ├── Doc: "PRD — Offer Generation"
│   └── ...
├── Delivery Board (Folder)
└── Product Roadmap (Folder)
```

- **Un Doc per spec** — il nome del Doc è il titolo della spec
- **Il repo è il source of truth** — il Doc ClickUp è un mirror. Gli edit vanno fatti nel repo, poi ri-pubblicati sul Doc
- **Ogni spec ha `clickup-doc:`** nel frontmatter con doc ID e link diretto
- **I task ClickUp linkano alla spec** nella sezione References con il link al Doc (non a GitHub)
- **Sync**: quando una spec viene creata o aggiornata (sync-spec, write-spec), il Doc viene creato o aggiornato automaticamente

---

## Flusso semi-automatico: PREPARE → APPROVE → EXECUTE

Ogni operazione di scrittura su ClickUp segue 3 fasi obbligatorie:

### Fase 1: PREPARE

L'agente analizza l'input (PRD, roadmap, backlog) e genera un **file di approvazione** in `company/prodotto/clickup-pending/YYYY-MM-DD-{comando}.md` con la lista completa delle azioni proposte:

```markdown
# ClickUp Sync — Approvazione richiesta
Data: YYYY-MM-DD
Comando: sync-spec | sync-roadmap | update-tasks

## Azioni proposte

| # | Tipo | Summary | Dettagli |
|---|------|---------|---------|
| 1 | CREATE Task | "Nome Task" | List: Feature, Priority: High, Tags: from-companyos |
| 2 | CREATE Subtask | "Nome Subtask" | Parent: #1, Assignee: — |
| 3 | UPDATE Task | CYB-123 | Status: In Progress → Done |

## Conferma

Rivedi le azioni sopra, poi esegui: `/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-{comando}.md`
Per annullare: elimina il file o non eseguire il comando approve.
```

### Fase 2: APPROVE

L'utente rivede il file di approvazione e conferma esplicitamente. L'agente **non esegue mai azioni su ClickUp senza approvazione esplicita** (eccezione: comandi read-only come `read-board`).

Invocazione approvazione:
```
/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-{comando}.md
```

### Fase 3: EXECUTE

L'agente esegue le azioni approvate chiamando i tool MCP ClickUp. Ogni azione viene loggata. Al termine, il file di approvazione viene spostato in `company/prodotto/clickup-done/`.

---

## Workspace e Struttura

> Gli ID reali (workspace, space, folder, list) vivono in `config/integrations.yaml` (sezione clickup). I placeholder `<...>` qui sotto vanno sostituiti con quei valori.

```yaml
workspace_id: "<workspace-id>"
workspace_name: <workspace-name>
space_name: Product Engineering
space_id: "<space-id>"
```

### Gerarchia Space "Product Engineering"

```
Product Engineering (Space <space-id>)
├── Delivery Board (Folder <folder-id-delivery>)
│   ├── Feature (List <list-id-feature>)      ← task di feature/sviluppo
│   ├── Bug (List <list-id-bug>)          ← bug report
│   ├── Tech-debt (List <list-id-techdebt>)    ← debito tecnico
│   ├── Bug submission form (List <list-id-bugform>)
│   └── War Room (List <list-id-warroom>)     ← urgenze/incidenti
├── Product Roadmap (Folder <folder-id-roadmap>)
│   ├── Epic (List <list-id-epic>)         ← epic di roadmap
│   └── Release Planning (List <list-id-release>)
└── 01 - Internal Projects (List <list-id-internal>)
```

---

## Tag standard

Ogni task creato dal sistema porta il tag **`from-companyos`** per tracciabilità. Questo tag è **sempre obbligatorio, nessuna eccezione**.

Tag aggiuntivi:
- `spec:{slug}` — collegato a una PRD specifica

**Regola esplicita**: non aggiungere mai tag di trimestre/quarter (es. `Q1-2026`, `Q2-2026`). Le informazioni temporali vanno nella descrizione del task, non nei tag.

---

## Mapping tipi issue → List ClickUp

| Startup OS | ClickUp List | Note |
|-----------|-------------|------|
| Feature / Iniziativa (Epic) | Product Roadmap → Epic (`<list-id-epic>`) | Task parent, raggruppa subtask |
| User Story / Feature task | Delivery Board → Feature (`<list-id-feature>`) | Task di sviluppo |
| Bug / Defect | Delivery Board → Bug (`<list-id-bug>`) | Bug report |
| Task tecnico / Tech debt | Delivery Board → Tech-debt (`<list-id-techdebt>`) | No user value diretto |
| Release | Product Roadmap → Release Planning (`<list-id-release>`) | Pianificazione release |

## Epic: status e priority

La lista Epic usa **4 status operativi**: `NOW`, `NEXT`, `LATER`, `RELEASED`.

**Regola `shipped` per le spec**: una spec in `company/prodotto/specs/` può essere marcata `shipped` **solo quando TUTTI i task della Epic associata sono in stato `Released`** su ClickUp. Non è sufficiente che siano `Done` o `Tested`. Prima di aggiornare il frontmatter `status: shipped`, verificare lo stato di ogni task della Epic via `clickup_filter_tasks` o `clickup_get_task`.

**Regola `spec-reconciliation`**: prima di marcare una spec come `shipped`, l'agente deve leggere i task e i commenti della Epic (via `clickup_get_task` + `clickup_get_task_comments` per ogni task) e verificare se durante lo sviluppo sono emersi cambiamenti rispetto alle specifiche originali. Esempi di divergenze da rilevare: AC modificati, funzionalità rimosse o ridotte di scope, comportamenti diversi da quanto scritto, nuove eccezioni o edge case gestiti diversamente. Se ci sono divergenze, aggiorna la PRD prima di impostare `status: shipped`. La PRD finita deve descrivere il prodotto come è stato costruito, non come era pianificato.

**Regola di creazione Epic**: ogni nuova Epic viene creata SEMPRE con status **`ON HOLD`**. La priority viene impostata in base alla classificazione Customer Backward:

| Classificazione | ClickUp Priority | ClickUp Status iniziale |
|----------------|-----------------|------------------------|
| Now | `urgent` | `NOW` |
| Next | `high` | `NEXT` |
| Later | `normal` | `LATER` |

## Mapping priority (Feature / Bug / Tech-debt)

| Startup OS | ClickUp Priority |
|-----------|-----------------|
| P0 - Critical | `urgent` |
| P1 - High | `high` |
| P2 - Medium | `normal` |
| P3 - Low | `low` |

## Delivery Board — Stati della list Feature e flusso di lavoro

### Stati della list Feature

| Stato | Chi lo gestisce | Significato |
|-------|----------------|-------------|
| `Backlog` | PM / sistema | **Serbatoio principale di tutto il lavoro da fare.** Ogni task creato dal sistema entra qui. |
| `To Do` | PM (weekly planning) | Task selezionati dal Backlog per lo sprint/settimana corrente, pronti per pickup dev. |
| `In Progress` | Dev | Task in lavorazione attiva. |
| `In Review` | Dev / PM | PR aperta o in QA. |
| `Done` | Dev / PM | Completato e verificato. |
| `Idea` | CEO (uso manuale) | **Solo uso manuale del CEO.** Il sistema non scrive mai in questo stato. |

### Regola fondamentale per la creazione di task

**Ogni task creato dal sistema (sync-spec, sync-roadmap, update-tasks) viene creato SEMPRE con status `Backlog`.**

Mai creare task in `To Do`, `Idea` o altri stati. Il Backlog è l'unico punto di ingresso per i task generati automaticamente.

### Flusso settimanale

```
BACKLOG (tutto il lavoro disponibile)
    ↓ weekly planning — PM seleziona per priority
TO DO (sprint corrente — pronto per pickup dev)
    ↓ dev prende il task
IN PROGRESS → IN REVIEW → DONE
```

### Regola pickup per il Dev Team

I dev prendono i task da **To Do** in ordine di priority:

**urgent → high → normal → low**

A parità di priority, prendere il task con il tag dell'epic più critica (verificare lo status dell'epic su Product Roadmap: NOW > NEXT > LATER).

### Significato operativo delle priority

| Priority | Significato | Quando usare |
|----------|-------------|--------------|
| `urgent` | Blocca release o cliente live | Bug critici, P0 fixes, hotfix |
| `high` | Core feature dello sprint goal | Task principali delle epic NOW |
| `normal` | Importante ma non bloccante | Task secondari, edge cases, infra |
| `low` | Nice-to-have | Minor UI, polish, tech debt non urgente |

### Regola per il PM

Ogni task che entra in **To Do** DEVE avere una priority assegnata. Nessun task in To Do con priority null.

---

## Tool MCP disponibili

### Server MCP attivi

Sono disponibili **due** server ClickUp. Usa il primo per default:

| Server | Tool prefix | Stato | Quando usarlo |
|--------|-------------|-------|---------------|
| **claude.ai ClickUp** (remoto, OAuth) | `mcp__claude_ai_ClickUp__*` | ✅ Default | Sempre, finché funziona |
| `clickup` (locale, @taazkareem) | `mcp__clickup__*` | Fallback | Solo se il remoto è giù o serve un tool che il remoto non offre |

> ⚠️ Il server remoto **non rileva il workspace di default** quando l'utente ha più workspace. Devi passare `workspace_id: "<workspace-id>"` (l'azienda) **a ogni call**, anche su tool read-only. Senza questo parametro la call fallisce con `Multiple workspaces available`.

### Lettura (read-only, nessuna approvazione richiesta)

| Tool | Uso |
|------|-----|
| `clickup_search` | Cerca task, doc, qualsiasi asset nel workspace |
| `clickup_get_task` | Dettagli di un singolo task (supporta custom ID) |
| `clickup_filter_tasks` | Filtra task per tag, lista, status, assignee, date |
| `clickup_get_workspace_hierarchy` | Struttura space/folder/list |
| `clickup_get_task_comments` | Commenti di un task |
| `clickup_get_custom_fields` | Campi custom disponibili |

### Scrittura (SEMPRE con approvazione)

| Tool | Uso |
|------|-----|
| `clickup_create_task` | Crea task in una list (richiede `name` + `list_id`) |
| `clickup_update_task` | Aggiorna campi di un task esistente |
| `clickup_create_task_comment` | Aggiunge commento a un task |
| `clickup_add_tag_to_task` | Aggiunge tag a un task |
| `clickup_add_task_dependency` | Imposta dipendenza tra task |
| `clickup_move_task` | Sposta task in altra list |

### Note sull'uso dei tool

- **workspace_id**: passa SEMPRE `"<workspace-id>"` (l'azienda) come parametro — obbligatorio sul server remoto, ignorato dal server locale ma innocuo
- **list_id**: usa gli ID dalla gerarchia sopra per creare task nella list corretta
- **assignees**: usa `clickup_resolve_assignees` per convertire nomi/email in user ID
- **tags**: i tag devono già esistere nello space; usa `from-companyos` + `spec:{slug}`
- **subtask**: usa il parametro `parent` con l'ID del task parent per creare subtask
- **dependency Feature → Epic**: quando crei Feature task collegati a un'Epic, aggiungi SEMPRE una dependency di tipo `blocking` (Feature blocks Epic) usando `clickup_add_task_dependency` con `task_id` = feature, `depends_on` = epic, `type` = "blocking". Questo crea la relazione "Block" visibile in ClickUp.
- **descrizioni**: usa SEMPRE `markdown_description` (non `description`) con markdown reale. NON usare `\n` escaped — usa newline reali nel parametro. Formattazione richiesta:
  - Titoli sezione con `##` (es. `## Description`, `## Acceptance Criteria`)
  - Testo importante in **bold** con `**testo**`
  - Elenchi puntati con `-`
  - Acceptance criteria come checkbox con `- [ ]`
  - Separatore `---` tra sezioni Description e Acceptance Criteria
- **autoconsistenza**: ogni descrizione di task (Epic, Feature, Subtask) deve essere **completamente autosufficiente**. Il dev che prende il task non deve cercare la PRD, chiedere al PM o leggere altri documenti. La descrizione deve includere: contesto del prodotto (perché questa feature esiste), il problema che risolve, il comportamento atteso, tutti gli acceptance criteria dettagliati. Il link alla spec è un riferimento opzionale, non un sostituto del contesto.

---

## Task Readiness Checklist (pass/fail)

**Un task è "ready" solo se TUTTI i check sotto passano. Se anche uno fallisce, il task resta in backlog/refinement e non può essere approvato.**

### Tre regole cardinali

1. **Regola dei 2 minuti** — Se un dev legge il task per 2 minuti e non sa cosa fare → task da rifare.
2. **Auto-consistenza** — Il task deve bastare a sé stesso. Il dev PUÒ consultare spec/epic come approfondimento, ma NON ne ha BISOGNO per capire cosa costruire.
3. **Zero architettura** — Mai inserire soluzioni tecniche, architettura software, nomi DB, endpoint, stack. La parte tech è responsabilità dell'architetto/engineer, che è una persona diversa fuori da questo sistema. Solo requisiti funzionali.

### Checklist completa

#### 1) Identity and traceability
- [ ] Titolo chiaro, specifico, orientato all'outcome (non vago)
- [ ] Linked all'Epic tramite "Dependencies"
- [ ] Linked alla spec (doc + sezione, se possibile)
- [ ] Tag `from-companyos` + `spec:{slug}` presenti

#### 2) Ownership and accountability
- [ ] Esattamente un owner accountable (no "team" come assegnatario)
- [ ] Se ci sono contributor, sono in commenti/collaborators, non co-owner
- [ ] Acceptance owner/reviewer definito (chi conferma il "done")

#### 3) Problem and intent clarity
- [ ] **Perché** questo task esiste (ragione di business/prodotto)
- [ ] **Outcome atteso** in una frase
- [ ] **Scope esplicito** — cosa è incluso
- [ ] **Out of scope esplicito** — cosa è escluso

#### 4) Execution clarity
- [ ] Descrizione implementativa actionable (il dev può partire senza indovinare)
- [ ] Dipendenze listate (servizi, team, task precedenti, dati, infra) — descritte funzionalmente
- [ ] Vincoli listati (compliance, UX, performance, deadline)
- [ ] Blocker noti alla creazione documentati

#### 5) Definition of Done (DoD) quality
- [ ] DoD esplicita, testabile, osservabile
- [ ] Metodo di validazione definito (test/review/demo/query/screenshot)
- [ ] Evidenza richiesta definita (PR, CI run, screenshot, doc update)
- [ ] Criteri di done evitano testo vago ("implementato", "fixato", "completato")
- [ ] DoD proporzionale al tipo di task (feature/bug/refactor/discovery)

#### 6) Test and verification requirements
- [ ] Livello di test richiesto dichiarato (unit/integration/e2e/manual)
- [ ] Acceptance check listati
- [ ] Aspettativa di regressione dichiarata (cosa NON deve rompersi)
- [ ] Edge case rilevanti documentati

#### 7) Operational planning fields
- [ ] Priority impostata
- [ ] Due date solo se significativa (non arbitraria)

#### 8) Workflow policy checks
- [ ] Nessun duplicato di task attivo/pianificato esistente
- [ ] Naming segue la convenzione del team

### Minimum "Ready" (set minimo obbligatorio)

Un task è ready quando ha **almeno**: titolo outcome-oriented, perché (why), scope / out of scope, un owner, epic + spec links, DoD checklist testabile, dipendenze/vincoli, priority, aspettative di validazione/evidenza.

---

## Comandi disponibili

| Comando | File | Accesso |
|---------|------|---------|
| sync-spec | `os/skills/clickup/commands/sync-spec.md` | PM, CTO |
| sync-roadmap | `os/skills/clickup/commands/sync-roadmap.md` | PM, CTO |
| read-board | `os/skills/clickup/commands/read-board.md` | Tutti |
| update-tasks | `os/skills/clickup/commands/update-tasks.md` | PM, CTO, CoS |
| sync-ceo-actions | `os/skills/clickup/commands/sync-ceo-actions.md` | CoS |

## Configurazione

Vedi `config/integrations.yaml (sezione clickup)` per setup completo.
