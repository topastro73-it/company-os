# /coo unblock — Sblocco ed escalation

## Scopo
Sbloccare un WO `blocked` o un conflitto tra ruoli, o portare la scelta al CEO.

## Input
- WO bloccato (`reason`, `exit`) o conflitto segnalato da un ruolo

## Passi
1. Classifica con `os/org/decision-rights.yaml`: fuori catalogo, conflitto, sopra soglia,
   accesso a zona 🔴.
2. Se rientra nei tuoi diritti (instradamento, nuovo WO a catalogo, cambio d'ondata): agisci,
   aggiorna il WO (`routed-by: coo` se torna al mittente del parent).
3. Altrimenti escalation al CEO: opzioni (2-3), raccomandazione, impatto sul budget. Il WO resta
   `blocked` finché il CEO decide.
4. `ledger-check --drive`, copia nello snapshot, `ledger-check`.

## Formato output
Aggiornamento del WO (stato, `reason`, `exit`, `routed-by`) e una riga nello standup successivo.

## Destinazione
Zona `direzione`, sottozona `ops` → `wo/WO-NNN.md`.

## Handoff
→ `ceo` per le decisioni oltre i tuoi diritti; → ruolo destinatario per il nuovo instradamento.
