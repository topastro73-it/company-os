# /coo standup — Stato dei goal attivi

## Scopo
Dare al CEO, dentro `/ceo start`, lo stato operativo dei goal: dove siamo, cosa è bloccato,
cosa parte dopo.

## Input
- Ledger (`goals/`, `wo/`, ultimo standup) sul mount Drive o, se assente, lo snapshot

## Passi
1. Elenca i goal con `status` attivo e, per ognuno, l'ondata corrente (ultimo WAVE o WO aperti).
2. WO `blocked` o in ritardo sul `due`: motivo ed `exit` proposta, owner.
3. Esiti VERIFY disponibili (solo per ref) e checkpoint in attesa di firma.
4. Proposta per la prossima ondata o per il checkpoint, con budget residuo.
5. Scrivi `standup/YYYY-MM-DD.md`; `ledger-check --drive`, copia nello snapshot, `ledger-check`.

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: standup
---
# Standup YYYY-MM-DD
| Goal | Ondata | Bloccati | Prossimo passo | Budget (WO/15 · ondate/3) |
```

## Destinazione
Zona `direzione`, sottozona `ops` → `standup/YYYY-MM-DD.md`.

## Handoff
→ `ceo` per checkpoint e decisioni; → `/coo unblock` per i WO bloccati.
