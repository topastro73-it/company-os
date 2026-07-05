# /compliance status — Dashboard compliance

## Scopo
Una vista unica sullo stato di compliance: framework, percentuali, gap critici, milestone.

## Input
Nessuno. Cadenza consigliata: mensile.

## Passi
1. Carica `compliance/status.md` e i requisiti mappati in `compliance/frameworks/`
   (NIS2, GDPR, ISO 27001/9001/27017/27018, SOC 2 se attivo).
2. Per ogni framework: requisiti mappati, soddisfatti **con evidenza**, gap.
   Un requisito senza evidenza archiviata NON conta come soddisfatto.
3. Classifica i gap: **critici** (bloccano certificazione/rinnovo o espongono a sanzione)
   vs **importanti** (con deadline); ogni gap → azione, effort S/M/L, owner.
4. **Scadenze**: audit di sorveglianza/rinnovo in arrivo, policy da re-approvare,
   evidenze in scadenza, formazione annuale.
5. Aggiorna `compliance/status.md` e genera il report datato.

## Formato output
```markdown
---
zone: compliance
tier: 🟡
type: compliance-dashboard
---
# Compliance Dashboard — {YYYY-MM-DD}

## Overview
| Framework | Requisiti | Soddisfatti (con evidenza) | Gap | % | Status |
|---|---|---|---|---|---|

## Gap critici
| Gap | Framework | Effort | Owner | Deadline |
## Gap importanti
## Prossime scadenze e milestone
## Raccomandazioni (max 3)

> Assessment interno. Per certificazioni formali serve un auditor accreditato.
```

## Destinazione
Zona `compliance` → `status.md` (aggiornato) + `audits/dashboard-{YYYY-MM-DD}.md`.
Commit (admin): `[compliance] status: dashboard {YYYY-MM-DD}`.

## Handoff
Gap tecnici → `cto` · gap con costo → `finance` · alert → `cos` (sezione compliance
nei briefing).
