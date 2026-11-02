---
status: attivo
area: sistema
---

# Command: record-decision

## Trigger
"registra che abbiamo deciso…", "segna questa decisione", "abbiamo deciso che…".

## Scopo
Registrare una decisione emersa in conversazione o in un meeting, perché l'azienda la ritrovi.
Per una decisione ancora da prendere, con opzioni e raccomandazione, c'è `/ceo decision`.
Fonti e regole in `../SKILL.md`.

## Processo
1. **Fissala** in una frase: *cosa* è stato deciso. Poi chiedi ciò che manca:
   - **chi ha deciso** (persona da `config/people.yaml`, o "il team");
   - **perché** (con le parole della persona — mai inventarlo);
   - **account / progetto** e **meeting** d'origine (path della minuta, se c'è);
   - **review date** o scadenza, se la decisione la contiene.
2. **Non è già registrata?** — cerca in `company/direzione/decisions/` e nelle tabelle "Decisioni"
   delle minute recenti. Se ne esiste una uguale o contraria, dillo: le decisioni sono immutabili,
   una nuova la **supera** citandola.
3. **Chi può deciderla** — `os/org/decision-rights.yaml`: se la persona non ha il diritto,
   registrala come `**Stato**: Proposta` (finisce in `approvals` di chi decide).
4. Mostra il file come verrà scritto e aspetta "ok".
5. Scrivi `company/direzione/decisions/YYYY-MM-DD-{slug}.md` secondo `TEMPLATE.md` (Data, Agente,
   Stato, Review Date, Contesto, Decisione, Conseguenze; le opzioni solo se sono state discusse).
   Se supera una decisione precedente, annotalo in entrambe. Collega la minuta d'origine.
6. Se la decisione porta un lavoro, aggiorna il `next-step` dell'account o proponi un task via
   `clickup-pending/`. Commit `[{agente}] decision: {slug}`.

## Regole
Solo decisioni vere: non opinioni, non domande aperte. Mai PII o dati 🔴 nel testo.
