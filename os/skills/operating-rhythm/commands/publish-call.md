---
status: attivo
area: sistema
---

# Command: publish-call

## Trigger
"pubblica questa call", "fai la minuta", "fai il recap", "follow up di questo meeting".

## Scopo
Dopo un meeting, trasformare la trascrizione in una **minuta** nella zona giusta e propagarne gli
effetti: opportunità e scheda aggiornate, decisioni di governo registrate, task ClickUp e recap
email preparati in staging. Un'unica bozza, un solo "ok". Fonti e regole in `../SKILL.md`.

## 1. Trova il meeting e la trascrizione
- Quello che la persona nomina, o il più recente senza minuta (vedi `follow-up-all`).
- Trascrizione: cerca sempre prima nelle fonti configurate (`../SKILL.md` § Transcript),
  poi il testo incollato. Nessuna trascrizione né appunti → niente da pubblicare: dillo.
- Verifica la pertinenza e che non sia già importato (stesso §). Trascrizione non pertinente → fermati:
  non si scrive nulla nel repo. Trascrizione mista → la minuta contiene solo la parte pertinente e lo
  dichiara nella sezione **Pertinenza** (dopo i Metadati: "{azienda}: sì / parziale" (nome da `config/company.yaml`), file toccati,
  account senza file).

## 2. L'account
- Se il meeting riguarda un account o un'opportunità esistente, usa quello (`account:` = slug).
- Altrimenti chiedi a quale account o progetto appartiene, o proponilo e aspetta un sì. **Mai
  dedurlo** da titolo o partecipanti. Account nuovo → `new-project` prima.

## 3. La bozza (non scrivere ancora)
Minuta nel formato delle minute esistenti (`type: minuta`): **Metadati** (titolo, data, durata,
fonte e link alla trascrizione, partecipanti in tabella Persona/Società/Ruolo, assenti) · **Pertinenza** · **Decisioni** (solo ciò che è
stato deciso davvero, e da chi) · **Impegni / action item** (#, Azione, Owner, Scadenza, Stato) ·
**Promesse fatte a terzi** · **Numeri e fatti nuovi** · **Rischi / incoerenze** (confronto con ciò
che il repo già dice) · **Dove è registrato**.
Poi, gli effetti:
- **Opportunità / scheda** — `last-activity`, `next-step`, `next-step-due`, `blockers`, voce in timeline.
- **Decisioni di governo** (prezzi, regole di canale, impegni contrattuali) → file in
  `company/direzione/decisions/` via `record-decision`.
- **Task ClickUp** — solo se c'è un owner che si è impegnato, un deliverable concreto, e una
  scadenza o almeno un'ora circa di lavoro; le cose piccole restano nella tabella impegni.
  Vanno in `company/prodotto/clickup-pending/` (o la zona del contenuto) per l'approvazione.
- **Recap email** ai partecipanti, 5–8 righe → `company/{zona}/mail-pending/`. Mai inviare.
- Prima di chiudere la bozza, guarda le email coi partecipanti dopo il meeting: gli impegni presi
  via email contano, con la stessa soglia.

Mostra tutto come un unico blocco e chiedi: "Pubblico?"

## 4. Pubblica (dopo "ok")
1. Scrivi la minuta: `company/clienti/{slug}/report/YYYY-MM-DD-{slug}-minuta.md` (cliente/partner),
   `company/commerciale/meeting-prep/YYYY-MM-DD-{slug}-minuta.md` (prospect),
   `company/direzione/reports/YYYY-MM-DD-{slug}.md` (interno). Frontmatter: `status: fatto`,
   `area`, `zone`, `tier`, `type: minuta`, `account`, `date`, `source`.
2. Aggiorna opportunità e scheda; scrivi le decisioni approvate.
3. Lascia i file di staging ClickUp/Gmail in `status: pending`: si eseguono dopo la loro
   approvazione (`approvals` o `/{agente} approve`).
4. Commit `[{agente}] meeting: {account} {data} — {sintesi}`; in admin ricorda `osctl publish`
   (o `--only` sui file toccati) per riportarli su Drive.

## 5. Report
Un messaggio: minuta salvata (path), file aggiornati, N decisioni, N task e la bozza recap in
attesa di approvazione.

## Modalità automatica
"Prepara le minute dei meeting di ieri": prepara le bozze, la scrittura aspetta sempre l'ok.
