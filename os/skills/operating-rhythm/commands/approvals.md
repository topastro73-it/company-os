---
status: attivo
area: sistema
---

# Command: approvals

## Trigger
"cosa devo approvare", "coda approvazioni", "cosa aspetta la mia approvazione".

## Scopo
Tutto ciò che nel repo aspetta l'ok della persona, in un'unica coda: approva (esegui) o rifiuta.
Fonti e regole in `../SKILL.md`; esecuzione secondo `os/protocols/external-writes.md`.

## 1. Carica la coda
- **Scritture esterne** — file con `status: pending` in `company/*/clickup-pending/`,
  `hubspot-pending/`, `mail-pending/`, `publish-pending/`.
- **Decisioni proposte** — `company/direzione/decisions/` con `**Stato**: Proposta`.
- **In attesa di me** — file con `status: in-attesa` e `waiting_on` = la persona o il suo ruolo;
  bozze marcate "da approvare" (es. regole di canale, listini in `proposte-bozze/`).
- La coda dipende da chi decide: `os/org/decision-rights.yaml`. Mostra solo ciò che la persona
  può approvare; il resto, se rilevante, come "in attesa di {altri}".

## 2. Mostrala
Per zona. Per ogni voce una card: cosa (sistema e azioni, o titolo) · da chi e da quando ·
età (oltre 7 giorni → "da rivalidare", come da protocollo) · path.
Con gli artifact: una pagina di card numerate 1…N; altrimenti una lista numerata.

## 3. Decidi
La persona risponde in una riga, es. "approva 1, 3 · rifiuta 2 · 4 solo righe 1-2". Agisci solo
sulle voci nominate: un "ok" generico non approva tutto.
- **Approva** — esegui le azioni del file nell'ordine (EXECUTE), annota esito e ID, `status: executed`,
  sposta in `*-done/`. Decisione: `**Stato**: Approvata`. Sistema esterno non raggiungibile: il file
  resta `approved` e si esegue al prossimo avvio.
- **Approva in parte** — esegui solo le righe indicate, annota le altre come non approvate.
- **Rifiuta** — `status: cancelled` con una riga di motivo se la persona l'ha dato.
- **Salta** — resta com'è.

## 4. Report
"Approvati N (eseguiti N, falliti N), rifiutati N, in attesa N." Commit `[{agente}] approve: …`.

## Regole
Mai approvare al posto della persona senza la sua istruzione esplicita per quella voce.
