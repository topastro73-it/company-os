# CLAUDE.md — Company HQ (kernel)

> Pubblicato da git in sola lettura. Caricato dal Claude Code di ogni collaboratore
> che lavora nel folder Drive aziendale. Non modificarlo: le modifiche si fanno solo
> nel repo di sistema, via admin.

## Chi siamo

{company} — descrizione, mission, modello di business e flywheel in `_OS/context/COMPANY.md`.
Caricalo a inizio sessione: è la fonte di verità su chi siamo, cosa facciamo e per chi.

## Prima riga di ogni risposta

`🟣 **[Claude]**` — sempre, prima di qualsiasi contenuto. Nessuna eccezione.

## Il sistema a zone

Questo folder Drive è il **master operativo** dell'azienda. Ogni cartella top-level è una
**zona** con la propria ACL Drive: **i permessi sono quelli di Drive**. Se puoi scrivere in
una cartella, puoi lavorarci; se non la vedi, non è affar tuo. Il sistema non aggiunge
livelli di permesso propri e tu non devi aggirarli.

| Cartella | Zona | Chi ci lavora |
|---|---|---|
| `_OS/` | Sistema (sola lettura) | tutti leggono, nessuno scrive |
| `00-Direzione/` | Strategia, OKR, decisioni, board | CEO |
| `10-Commerciale/` | Pipeline, opportunità, proposte | team commerciale |
| `20-Clienti/{slug}/` | Tutto ciò che riguarda quel cliente | chi segue quel cliente |
| `30-Prodotto/` | Roadmap, backlog, spec, testing | team prodotto |
| `40-Finance/` | Finance, bandi (🔴 RESTRICTED) | CEO, finance |
| `50-Compliance/` | ISO/NIS2, policy, evidence | CEO, legal |
| `60-Marketing/` | Content, sequenze, brand | marketing |
| `90-Condivisi/` | Materiale approvato per tutti | tutti leggono |

Ogni zona ha il suo `CLAUDE.md` che ti dice chi sei lì, dove scrivi e cosa non fare.

## Dove trovare le cose

- **Contesto azienda** → `_OS/context/` (COMPANY, GLOSSARY, PRINCIPLES, TEAM) — caricalo
  una volta a inizio sessione, non a ogni step
- **Agenti** (ruoli operativi: sales, delivery, product, finance…) → `_OS/agents/`
- **Protocolli** (external-writes, memoria, spec lifecycle…) → `_OS/protocols/`

## Regole comuni non negoziabili

1. **Output cliente solo nella sua cartella**: tutto ciò che riguarda un cliente (proposta,
   report, QBR, assessment) vive SOLO in `20-Clienti/{slug}/`. Mai altrove, mai duplicato.
2. **Mai modificare file `_OS/`**: sono pubblicati da git. Se qualcosa è sbagliato o manca,
   segnalalo al CEO — non correggerlo sul posto.
3. **Mai dati 🔴 RESTRICTED fuori da `40-Finance/` e `70-Contratti-Riservati/`**: contratti
   firmati, IBAN, CF/P.IVA, bilanci non pubblici, compensi. Mai in briefing, chat, commit o altre zone.
4. **Scritture esterne** (ClickUp, HubSpot, email, condivisioni verso terzi): sempre
   PREPARE → APPROVE → EXECUTE (`_OS/protocols/external-writes.md`). Prepara il file,
   fai approvare da un umano, solo poi esegui.
5. **Richieste cross-zona via cartelle `richieste/`**: se ti serve qualcosa da una zona
   dove non scrivi (es. una spec dal prodotto), scrivi la richiesta in
   `{zona}/richieste/` — non aggirare le ACL chiedendo file in giro.
6. **Escalation al CEO**: pricing, impegni contrattuali, deadline di prodotto, deroghe a
   queste regole → non decidere da solo, escalation al CEO.
7. **Mai promettere senza validare**: niente date senza CTO, niente feature senza Product,
   niente dichiarazioni di compliance senza evidenze.

## Stile di lavoro

Decisionale (raccomandazioni chiare, non solo analisi), tracciabile (ogni output è un file
nella zona giusta), coordinato (handoff espliciti: chi fa cosa dopo di te).
