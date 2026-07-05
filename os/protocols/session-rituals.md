# Session rituals — start e close

Due rituali, due varianti: **admin** (il founder, sessione sul repo git) e **collaboratore**
(sessione nella propria zona Drive). Il rituale è dell'agente di ingresso: `ceo` per l'admin,
l'agente di default della zona per i collaboratori (`config/people.yaml`).

## START

### 1. Identifica la persona
- **Admin (repo)**: `git config user.email` → match in `config/people.yaml`
- **Collaboratore (Drive)**: la zona in cui gira la sessione + il `CLAUDE.md` di zona
  determinano ruolo e agente di default; in ambiguità, chiedi una volta e basta
- Saluta col **ruolo** (es. "Ciao {persona} — Head of Sales") ed entra nell'agente primario

### 2. Allinea lo stato
- **Admin**: `git fetch` + pull (recupera snapshot nightly e modifiche mergiate);
  se osctl disponibile, verifica che l'ultimo snapshot non sia più vecchio di 24h
- **Collaboratore**: verifica che Google Drive for Desktop sia in sync (file `_OS/` presenti);
  se la zona non è raggiungibile → graceful degradation (`zones-and-permissions.md` §7)

### 3. "Dove eravamo rimasti"
Estrai dall'ultima sessione wiki (`system/wiki/sessions/`, per i collaboratori la copia
pubblicata se disponibile) e dai file di stato della zona:
- decisioni prese, domande aperte, promesse — con **alert su quelle scadute**
- **aging**: opportunità/task fermi oltre soglia nella zona della persona
- **scadenze**: prossime deadline rilevanti per il ruolo (scadenzario, review-date, follow-up)
- **health**: esito ultimo `/system health` e acl-audit (solo admin) — se 🔴, si sistema prima

**Stale session detector** (solo admin): se l'ultima sessione risulta lavorata ma senza wiki
page (close saltato), proponi una recovery wiki da log/commit/decisioni PRIMA del briefing di oggi.

### 4. Carica il contesto minimo
Contesto condiviso (`zones/_root/context/` o `_OS/context/`) una volta per sessione;
learnings attivi in memoria (apply-loop, `memory.md` §3). Poi si lavora.

Se la persona invoca subito un agente specifico: quick check (max 1 alert urgente) e via.

## CLOSE

### Collaboratore (zona Drive)
1. **Salva la memoria**: proponi i dati business emersi e non ancora persistiti
   (`memory.md` §1) → file di zona
2. Output della sessione nella cartella giusta della zona (niente file orfani sul desktop)
3. Richieste cross-zona formalizzate (es. richiesta spec in `30-Prodotto/richieste/`)
4. Fine: niente commit — lo **snapshot nightly** versiona il lavoro del collaboratore

### Admin (repo) — sequenza completa
1. **Memoria**: dati business non persistiti → proponi salvataggio nei file di zona/snapshot
2. **Wiki session**: genera `system/wiki/sessions/YYYY-MM-DD-{slug}.md` (inglese,
   pseudonimizzato — `memory.md` §2); riconcilia promesse/domande delle sessioni recenti
   (fatte → chiuse, aperte → riportate avanti); aggiorna entity pages toccate e `index.md`
3. **Learnings**: proponi max 2 candidati; verifica candidati non promossi degli ultimi
   30 giorni (anti-deriva); incrementa `Applied:` degli LRN usati in sessione
4. **Snapshot**: `osctl snapshot` (Drive → `company/` + `vault/`) così il commit include lo
   stato operativo reale; osctl assente → segnala e prosegui
5. **Commit & push**: `git add -A` → commit `[ceo] close: YYYY-MM-DD` → `git fetch` →
   se il remote è avanti, `git merge origin/main --no-edit` → `git push origin main`
   - Mai `git reset --hard`, mai `push --force`
   - Conflitti non risolvibili → file `CONFLICTS.md` con dettaglio e notifica
   - Repo già clean → dichiaralo e fermati
6. **Health check**: `scripts/audit/` (secret-scan, link-lint, frontmatter-check) +
   `osctl acl-audit`; esito nel summary. Se una modifica di sistema è stata mergiata in
   sessione → verifica publish fatto (`changelog.md`)
7. **Summary finale**: commit SHA, file toccati, esito push/snapshot/health, promesse aperte

## Regole comuni

- Il close non è opzionale: senza close niente wiki, contatori fermi, promesse appese —
  lo start successivo lo rileva e propone il recovery
- Mai chiedere due volte la stessa cosa nello stesso rituale; max 1 domanda urgente se la
  persona ha fretta
- Tutto ciò che il rituale scrive rispetta zone e tier (`zones-and-permissions.md`)
