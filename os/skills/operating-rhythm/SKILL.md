---
status: attivo
area: sistema
---

# Skill: Operating Rhythm

## Scopo

Il ritmo di lavoro quotidiano di una persona sul repo: la sua giornata, la preparazione e il recap
dei meeting, le decisioni, le approvazioni, lo stato di un account o progetto, cosa fanno gli
altri. Tutto si legge e si scrive **nei file delle zone** (`company/`, `vault/` solo admin) e nei
sistemi dell'azienda censiti in `config/integrations.yaml`: nessun backend esterno di contesto.

Nove comandi, in `commands/`:

| Comando | Trigger tipici | Scrive? |
|---|---|---|
| `my-day` | "com'è la mia giornata", "cosa ho oggi", "aggiornami" | no |
| `meeting-prep` | "preparami la call con…", "brief per il meeting", "chi c'è alla riunione" | brief in zona |
| `publish-call` | "pubblica questa call", "fai la minuta", "fai il recap" | minuta + file collegati; ClickUp/Gmail via staging |
| `follow-up-all` | "segui i miei meeting", "smaltisci i follow-up" | tramite `publish-call` |
| `approvals` | "cosa devo approvare", "coda approvazioni" | esegue ciò che approvi |
| `project-pulse` | "come va {account}", "stato di {opportunità/progetto}", "aggiorna lo stato" | aggiornamento di stato |
| `new-project` | "apri il progetto…", "nuovo cliente", "nuova opportunità" | nuovo file da template |
| `record-decision` | "registra che abbiamo deciso…", "segna questa decisione" | `direzione/decisions/` |
| `team-radar` | "cosa sta facendo {persona}", "cosa è successo questa settimana" | no |

Agenti: CoS (owner), CEO, Sales, Delivery, Product. I comandi CoS restano la vista aziendale
(`/cos daily-briefing`, `prepare-meeting`, `follow-up-tracker`, `status-check`, `weekly-digest`);
questa skill è la vista **della persona** e il ciclo meeting → minuta → impegni.

## Dove vivono i dati

| Cosa | Dove |
|---|---|
| Persone, ruoli, email | `config/people.yaml` (chiave breve, `name`, `role`, `emails`, `default_agent`) |
| Account cliente/partner | `company/clienti/{slug}/overview.md` (frontmatter `status`, `owner-sales`, `owner-pm`, `health-score`) |
| Opportunità | `company/commerciale/opportunities/{opp-slug}.md` (`account`, `stage`, `owner-sales`, `next-step`, `next-step-due`, `blockers`, `last-activity`) · board `PIPELINE.md` |
| Progetti interni | `company/direzione/projects/P-NNN-*.md` (registro `INDEX.md`) · goal e WO in `company/direzione/ops/` |
| Meeting tenuti | minute con frontmatter `type: minuta`, `account`, `date`, `source`: `company/clienti/{slug}/report/`, `company/commerciale/meeting-prep/`, `company/direzione/reports/` |
| Trascrizioni | le fonti di `config/integrations.yaml → meeting_transcripts.sources`, sempre (§ Transcript dei meeting) · testo incollato |
| Meeting futuri | connector Google Calendar; senza, il calendario "non è stato verificato" |
| Decisioni | `company/direzione/decisions/YYYY-MM-DD-slug.md` (immutabili, si superano con una nuova) · tabella "Decisioni" delle minute |
| Impegni e task | tabella "Impegni / action item" delle minute · `next-step`/`blockers` delle opportunità · ClickUp (`config/integrations.yaml → clickup`) |
| Approvazioni | file in `company/*/*-pending/` con `status: pending` · decisioni `**Stato**: Proposta` · file `status: in-attesa` con `waiting_on` |
| Email | skill `os/skills/gmail/` (sola lettura; bozze solo via `mail-pending/`) |
| Cronologia | `git log` (solo admin; i collaboratori lavorano su Drive) |

## Transcript dei meeting

**Ogni comando che parla di meeting** (`my-day`, `meeting-prep`, `publish-call`, `follow-up-all`,
`project-pulse`, `team-radar`) **cerca sempre** tra le trascrizioni, non solo tra le minute già
nel repo. Le fonti sono URL configurate in `config/integrations.yaml → meeting_transcripts.sources`
(per ognuna `url`, `provider`, `label`, `title_format`, `shared`); i termini di pertinenza
(`include_terms`, `exclude_terms`) valgono per tutte. Per aggiungere o cambiare una fonte si
modifica solo la config. Nessuna fonte configurata → solo minute del repo e testo incollato.

1. **Cerca**, per ogni fonte, nel periodo del comando (default ultimi 14 giorni), leggendo **ogni
   pagina** dei risultati; per un account o una persona aggiungi la parola chiave. Secondo il
   `provider` (dedotto dall'host se manca):
   - `clickup` — il workspace è il numero dopo `app.clickup.com/` nell'URL: `clickup_search` con
     `asset_types: [doc]`, ordinati per `created_at` desc, fino a esaurire `next_cursor`. I Doc
     del Notetaker non hanno cartella; il riassunto AI è nella prima pagina del Doc.
   - `drive` — l'URL è una cartella: elenca i file del periodo col connector Drive (o, in admin,
     dal mount `OS_DRIVE_MOUNT`) e leggi i documenti di trascrizione.
   - `url` — leggi la pagina o il feed indicato così com'è; ogni voce è un meeting.
   La data del meeting si ricava dal titolo secondo `title_format` (es. `MM/DD/YYYY` = data USA:
   convertila in gg/mm/aaaa) o, in mancanza, dalla data di creazione.
2. **Filtra la pertinenza** — obbligatorio per le fonti `shared: true` (condivise con altre
   aziende), consigliato per tutte. Per ogni trascrizione:
   - **pertinente** se il titolo contiene un `include_terms`, il nome o lo slug di un account
     (`company/clienti/`), di un'opportunità o di un progetto `P-NNN`, oppure se nel riassunto
     compaiono persone di `config/people.yaml` diverse dall'admin (l'admin può partecipare anche a
     meeting di altre aziende: da solo non basta);
   - **escluso** se il titolo contiene un `exclude_terms` e niente lo collega al repo;
   - **dubbio** altrimenti: leggi solo il riassunto e decidi; se resta incerto, chiedi all'utente
     con un'unica domanda che elenca tutti i dubbi;
   - **misto** (si parla anche di altro): si tiene solo la parte pertinente; la minuta lo dice
     nella sezione "Pertinenza".
3. **Già importato?** — una trascrizione è già nel repo se una minuta ha in `source:` il suo titolo
   o nel corpo il suo link. Mai importarla due volte: si aggiorna la minuta esistente.
4. **Riservatezza** — dei meeting esclusi non si copia nulla nel repo, né nei report né nei commit:
   al massimo il conteggio ("N meeting di altre aziende esclusi"). Mai citarne contenuti o persone.
5. **Fonte nella minuta** — `source: "{label} — {titolo originale}"` e il link alla trascrizione
   nei Metadati.

Fonte non raggiungibile → le sue trascrizioni "non sono state verificate": dillo, e prosegui con
le altre fonti e con le minute del repo.

## Chi sono "io"

In sessione admin "io" è `config/people.yaml → admin`. Altrimenti la persona si riconosce
dall'email con cui lavora (`people.*.emails`); in dubbio chiedi. "I miei" file sono quelli in cui
la persona è owner (`owner-sales`, `owner-pm`, `Owner` nelle tabelle, `to:`/`from:` dei WO) o
partecipante (tabella "Partecipanti" della minuta).

## Date

Oggi = data di sistema, fuso Europe/Rome. "Questa settimana" = lunedì–domenica. Ogni data mostrata
porta l'etichetta passata / oggi / futura rispetto a oggi.

## Scritture

- **File del repo** (minute, opportunità, schede, decisioni, brief): bozza in chat → "ok" →
  scrittura nella zona giusta, con frontmatter `status`/`area` e `zone`/`tier` dove la zona lo
  chiede (`zones/{zona}/CLAUDE.md`). Le zone `company/` sono Drive-master: in admin si editano
  solo se poi si pubblica (CLAUDE.md, regola 5). Commit `[agente] meeting|decision|…: …`.
- **Sistemi esterni** (ClickUp, Gmail, HubSpot, Calendar): sempre PREPARE → APPROVE → EXECUTE
  (`os/protocols/external-writes.md`) con staging in `clickup-pending/`, `mail-pending/`,
  `hubspot-pending/`. I task ClickUp seguono `config/integrations.yaml → clickup.rules`
  (inglese, status iniziale, tag obbligatori).
- Un "sì" generico non sceglie tra opzioni: se c'erano più opzioni o una risposta per voce,
  chiedi quali e agisci solo su quelle.

## Regole

- Riporta solo ciò che un file o un tool dice davvero, con il path come fonte. Una fonte non
  raggiungibile (ClickUp, Calendar, Gmail) = "non verificato", mai "vuoto".
- Mai inventare un account, un motivo, un impegno o una scadenza: se il file non lo dice, non è registrato.
- Privacy: mai PII o dati 🔴 fuori da `vault/` e `40-Finance/`; finance solo in admin.
- Dati business emersi in chat → proponi il salvataggio nel file di zona (`os/protocols/memory.md`).
