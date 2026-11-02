---
status: attivo
area: sistema
---

# Command: project-pulse

## Trigger
"come va {account}", "stato di {opportunità}", "a che punto è P-00N", "aggiorna lo stato",
"scrivi lo status".

## Scopo
Lo stato di **un** account, opportunità o progetto interno, e il suo aggiornamento. Per i
semafori su tutti i workstream c'è `/cos status-check`. Fonti e regole in `../SKILL.md`.

## Leggi
1. **Il file principale** — `company/clienti/{slug}/overview.md`, l'opportunità
   `company/commerciale/opportunities/{opp-slug}.md` o `company/direzione/projects/P-NNN-*.md`.
   Nome ambiguo → elenca i candidati e chiedi.
2. **Collegati** — opportunità con lo stesso `account`, minute degli ultimi 30 giorni
   (`type: minuta`, `account`), decisioni che lo citano, WO/goal in `company/direzione/ops/`.
   Cerca sempre anche le trascrizioni delle fonti configurate col nome dell'account (`../SKILL.md` §
   Transcript): quelle non importate vanno in **Incoerenze** ("meeting del gg/mm senza minuta").
3. **Lavoro** — impegni aperti nelle minute, `next-step`/`blockers`, task ClickUp collegati.
4. **Movimento** — in admin `git log --since=<today-14>` sui file dell'account.

## Output
**Stato** (stage/status, owner, sintesi in una riga) · **Serve adesso** (`next-step` con
scadenza, blocker con owner) · **Ultime decisioni** · **Meeting recenti** (data, link alla
minuta) · **Impegni** (aperti / scaduti) · **Incoerenze** (es. `last-activity` più vecchio
dell'ultima minuta, next-step scaduto, account senza file opportunità).

## Aggiornamento di stato (su richiesta, o proponilo se `last-activity` ha più di 7 giorni)
1. Bozza: i campi del frontmatter da cambiare (`stage`, `probability`, `next-step`,
   `next-step-due`, `blockers`, `last-activity`, `health-score`…) e 4–6 righe di timeline (fatto,
   in corso, rischi, prossimi passi), solo da fonti citate.
2. Aspetta "ok", poi scrivi. Cambio di stage di un'opportunità → anche `PIPELINE.md`.
3. Commit `[{agente}] opportunity|delivery: {slug} → …`.

## Regole
Mai inventare avanzamenti: se non si è mosso nulla, dillo. I cambi che richiedono un altro ruolo
(prezzi, date di consegna, feature) passano dal loro owner (CLAUDE.md, regola 7).
