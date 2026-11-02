---
status: attivo
area: sistema
---

# Command: my-day

## Trigger
"com'è la mia giornata", "cosa ho oggi", "brief del mattino", "aggiornami", o un run schedulato
"esegui la mia giornata". Sola lettura.

## Scopo
Una pagina che dice alla persona dove si trova stamattina: i **suoi** meeting, impegni,
approvazioni e account. Per la vista aziendale del CEO c'è `/cos daily-briefing`.
Fonti e regole comuni in `../SKILL.md`.

## Processo (in parallelo dove si può)
1. **Chi e quando** — la persona (`config/people.yaml`) e la data di oggi.
2. **Meeting di oggi** — dal connector Calendar. Per ognuno con un account noto, il link alla
   scheda o all'opportunità e se esiste già un brief in `meeting-prep/`.
3. **Meeting senza minuta** — trascrizioni pertinenti delle fonti configurate degli ultimi 7 giorni
   (`../SKILL.md` § Transcript) non ancora importate, più gli eventi Calendar con esterni senza
   minuta (proponi `follow-up-all`).
4. **I miei impegni** — righe "Impegni / action item" delle minute recenti con owner = io e stato
   non `fatto`; `next-step`/`next-step-due` e `blockers` delle opportunità dove sono owner; task
   ClickUp assegnati a me nel workspace dell'azienda (se ClickUp non risponde: non verificati).
5. **Da approvare** — file `status: pending` in `company/*/*-pending/` e decisioni
   `**Stato**: Proposta` che toccano me o il mio ruolo; file `status: in-attesa` con `waiting_on` = io.
6. **Novità sui miei account** — in admin `git log --since=<ieri>` sui file dove sono owner;
   nuove decisioni in `company/direzione/decisions/`.
7. **Email da rispondere** (facoltativo, skill gmail) — fino a 5 thread da persone dei miei account.

## Output
Prima la cosa che richiede un'azione. Poi, solo se non vuote:
**Oggi** (ora Roma, titolo, account) · **Senza minuta** · **Da approvare** (proponi `approvals`) ·
**I miei impegni** (scaduti, poi oggi, poi il resto) · **Novità sui miei account** ·
**Bloccato** (blocker aperti) · **Email da rispondere**. Ogni voce con il path del file.
Con gli artifact disponibili: una pagina a card con i conteggi nei titoli.

## Ogni mattina
Una skill non si schedula da sola: crea un task schedulato nei giorni feriali alle 08:00 col
prompt **"esegui la mia giornata"**.
