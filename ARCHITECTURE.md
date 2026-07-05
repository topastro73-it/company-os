# CompanyOS — Architettura

> Blueprint del sistema operativo aziendale AI.
> Questo documento è la fonte di verità architetturale. Versione: 2.0.0

## 1. Principio fondante: due piani

Un sistema che simula i permessi con convenzioni markdown (tier 🔴🟡🟢 nel frontmatter)
non enforca davvero nulla. CompanyOS separa **cervello** e **corpo**:

| Piano | Dove vive | Master | Chi scrive | Enforcement |
|---|---|---|---|---|
| **Sistema** (agenti, protocolli, guardrail, template, config) | Repo git `company-os` | **Git** | Solo admin (il founder) | Branch protection + CI |
| **Operativo** (clienti, pipeline, deliverable, finance, compliance) | Google Drive aziendale | **Drive** | Chi ha ACL sulla cartella | **Permessi Drive nativi** |

I collaboratori **non toccano mai git**. Ognuno lavora col proprio Claude Code **dentro il
folder Drive aziendale** (Google Drive for Desktop). I file di sistema (CLAUDE.md di zona,
agenti, protocolli) arrivano su Drive **in sola lettura** via publish da git: il Claude del
collaboratore li carica come contesto ma non può alterarli. Gli output operativi finiscono
nella cartella giusta (es. cartella cliente) e **i permessi sono quelli di Drive**: chi non ha
accesso alla cartella, non vede quegli output. Punto.

## 2. Zone

Ogni file appartiene a una zona. Una zona = una cartella Drive top-level + una ACL + una
direzione di sync. Mappa completa in `config/acl.yaml`.

| Zona | Drive | Scrive | Legge | Sync |
|---|---|---|---|---|
| `_os` (sistema) | `_OS/` + `CLAUDE.md` per zona | admin via git | tutti | git → Drive (publish) |
| `direzione` | `00-Direzione/` | CEO | CEO, board | Drive-master, snapshot → git |
| `commerciale` | `10-Commerciale/` | team commerciale, CEO | team commerciale + CEO + CoS | Drive-master, snapshot → git |
| `clienti` | `20-Clienti/{slug}/` | **per-cartella** (chi segue quel cliente) | per-cartella | Drive-master, snapshot → git |
| `prodotto` | `30-Prodotto/` | team prodotto, CTO, CEO | tutti gli interni | Drive-master, snapshot → git |
| `finance` | `40-Finance/` | CEO, consulente bandi | CEO + finance; commercialista solo su `per-commercialista/` | Drive-master, snapshot → **vault** |
| `compliance` | `50-Compliance/` | CEO, legal | interni; auditor esterno solo su `evidence/` | Drive-master, snapshot → git |
| `marketing` | `60-Marketing/` | marketing, CEO | tutti gli interni | Drive-master, snapshot → git |
| `shared` | `90-Condivisi/` | admin | tutti (interni + esterni selezionati) | git → Drive (publish) |
| `contratti` | `70-Contratti-Riservati/{slug}/` | CEO | CEO + Head of Sales | Drive-master, snapshot → **vault** |

Regole:
- **Cartella cliente** (`20-Clienti/{slug}/`): contiene TUTTI gli output *operativi* relativi a
  quel cliente (proposte, report, QBR, assessment). L'ACL della cartella È il permesso.
- **Contratti firmati: zona separata, non sottocartella.** Google Drive eredita i permessi solo
  verso il basso (chi ha accesso a una cartella lo eredita in ogni sua sottocartella; non esiste
  un modo nativo di "restringere" una sottocartella sotto il livello del genitore). Una
  sottocartella `contratti/` dentro `20-Clienti/{slug}/` sarebbe quindi visibile a chiunque lavori
  su quel cliente (delivery, CS), non solo a CEO+Sales. Per questo i contratti vivono nella zona
  **`contratti`** (`70-Contratti-Riservati/{slug}/`), top-level e isolata — nessuno con accesso più
  ampio sopra di essa. Nella cartella cliente resta solo un puntatore (`contratti/README.md`).
- **Privacy tiers** 🔴🟡🟢 restano nel frontmatter come *classificazione* (per publish esterni,
  redazione PII, secret-scan), ma l'*accesso* lo decide la zona/ACL Drive.
- 🔴 RESTRICTED in git vive solo in `vault/` (repo privato separato via submodule, o directory
  presente solo sul clone dell'admin).

## 3. Identità per zona: CLAUDE.md pubblicati

Ogni zona Drive riceve da git un proprio `CLAUDE.md` (sola lettura) che configura il Claude Code
di chi ci lavora:

- **chi sei qui**: quale agente di default (es. in `10-Commerciale/` → agente Sales)
- **cosa puoi leggere**: le zone accessibili e il contesto condiviso (`_OS/context/`)
- **dove scrivi**: output rules della zona (es. output cliente → `20-Clienti/{slug}/`)
- **cosa non fai**: niente modifiche ai file `_OS/`, niente dati 🔴 fuori zona, escalation al CEO
- **come chiedi**: handoff e richieste cross-zona (es. "serve una spec" → richiesta in
  `30-Prodotto/richieste/`)

Il root del folder aziendale ha il `CLAUDE.md` kernel-lite (identità azienda, glossario,
regole comuni); le zone aggiungono il profilo di ruolo. Sorgenti in `zones/` nel repo.

## 4. Sync engine: `osctl`

CLI Python in `tools/osctl/` (richiede service account Google o OAuth admin). Comandi:

- `osctl bootstrap` — crea l'albero Drive da `config/acl.yaml`, imposta le ACL, scrive i folder-ID
  ottenuti in `config/acl.yaml` (idempotente).
- `osctl publish` — git → Drive: sistema (`zones/`, `os/` selezionati, `company/` seed) verso le
  zone; i deliverable `.md` con frontmatter `render: gdoc` vengono anche **convertiti in Google Doc**.
- `osctl snapshot` — Drive → git: scarica le zone Drive-master in `company/` (e `vault/` per
  finance) e committa. Eseguito nightly (GitHub Action con service account) o da `/close` admin.
  Git resta così **versioning e backup completo** anche delle zone operative.
- `osctl acl-audit` — legge i permessi reali via Drive API e li confronta con `config/acl.yaml`:
  segnala drift (persona in più/in meno, cartella cliente senza owner). Parte del `/system health`.

Direzione per zona = `sync:` in `acl.yaml`. Mai two-way sullo stesso file: ogni file ha un solo
master. Conflitto = il master vince, il resto è copia.

## 5. Lettore markdown senza frizioni

Tre livelli, dal più universale:

1. **Google Doc automatico**: ogni deliverable per umani (report, proposta, QBR, investor update)
   viene pubblicato ANCHE come Google Doc nella stessa cartella (conversione in publish).
   Chiunque con accesso Drive lo apre, legge e commenta — desktop e mobile, zero install.
2. **Viewer HTML standalone** (`tools/viewer/viewer.html`, pubblicato in `_OS/`): file unico
   auto-contenuto; aperto in Chrome/Edge dal folder Drive sincronizzato, chiede di selezionare la
   cartella aziendale e naviga/renderizza tutti i `.md` con indice, ricerca e badge di zona.
   Per chi lavora nel folder desktop.
3. **Claude Code**: chi ha il proprio Claude nella zona legge e interroga tutto in chat.

## 6. Agenti

Un agente per funzione, mappato sulle persone reali (`config/people.yaml`). Definizioni in
`os/agents/{slug}/AGENT.md` + `commands/`.

| Agente | Slug | Persone servite | Missione |
|---|---|---|---|
| CEO Routine | `ceo` | il founder (admin) | Entry point sessione admin: start/close, decisioni, OKR, cadence |
| Chief of Staff | `cos` | il founder (admin) | Briefing, digest, tracking cross-zona, preparazione meeting |
| Sales | `sales` | team commerciale | Pipeline (account+opportunità), funnel, proposte, outbound |
| Delivery / CS | `delivery` | Customer Success | Onboarding partner 90gg, health score, QBR, churn/expansion |
| Product | `product` | team prodotto | Spec lifecycle, backlog RICE, ClickUp sync, UAT/QA |
| CTO | `cto` | engineering | Decisioni tecniche, ADR, architettura, security review |
| Finance | `finance` | CEO, consulente bandi | Fatturazione, scadenzario, cashflow, bandi, investor relations |
| Compliance | `compliance` | CEO (legal) | ISO/NIS2, policy register, evidence, vendor assessment, contratti |
| Marketing | `marketing` | marketing | Content, sequenze outbound, launch, posizionamento |
| Admin | `admin` | il founder (admin) | Modifiche al sistema, changelog, propagazione template, ACL |

Meta-skill `agent-creator` e `skill-creator` per estendere senza codice (solo admin).

## 7. Memoria a tre strati (ereditata e mantenuta)

| Strato | Dove | Cosa |
|---|---|---|
| **Stato** | zone operative (Drive) + snapshot in `company/` | I fatti correnti: pipeline, health, scadenze |
| **Storia** | `system/wiki/` (git) | Il perché: sessioni, entità, narrativa |
| **Regole** | `system/learnings.md` (git) | LRN-XXX appresi, con apply-loop |

## 8. Guardrail meccanici

- `scripts/audit/secret-scan.sh` — token/chiavi/IBAN/file 🔴 fuori zona: **CI + pre-commit** (ereditato, esteso a `vault/`).
- `scripts/audit/link-lint.py` — i path citati nei file di sistema esistono.
- `scripts/audit/frontmatter-check.py` — zona+tier dichiarati su ogni file operativo.
- `osctl acl-audit` — drift permessi Drive vs matrice.
- `.github/workflows/audit.yml` — tutto in CI su push/PR; snapshot nightly.
- Human-in-the-loop: scritture su sistemi esterni (ClickUp, HubSpot, Drive publish, email)
  sempre PREPARE → APPROVE → EXECUTE (`os/protocols/external-writes.md`).

## 9. Integrazioni

Config in `config/integrations.yaml` (solo nomi di variabili, mai valori).
ClickUp (execution prodotto), HubSpot (CRM specchio della pipeline, repo/Drive master),
Gmail e Calendar (contesto), fatturazione + banca + pagamenti + ERP (finance),
Google Drive (piano operativo). Graceful degradation: MCP assente → si prosegue coi file, si segnala.

## 10. Template `company-os` e istanze private

Tutto ciò che è specifico dell'azienda vive SOLO in: `config/*.yaml`, `company/`, `vault/`,
`zones/*/context/` e nei dati citati dagli agenti via config. La derivazione del template è
meccanica: svuota `config/` (lascia `*.example.yaml`), `company/`, `vault/`; gli agenti,
protocolli, osctl, viewer e guardrail sono già generici. Un comando `/admin export-template`
produce il repo `company-os` pulito con leak-scan automatico.
