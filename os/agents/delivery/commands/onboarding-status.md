# /delivery onboarding-status — Stato onboarding

## Scopo
Vedere a colpo d'occhio dove sono tutti i partner in onboarding e cosa è in ritardo.

## Input
- Partner slug (opzionale — se omesso, tutti i partner con onboarding attivo)

## Passi
1. Scansiona le schede partner in `clienti/*/scheda-partner.md` con
   `onboarding-phase` ≠ completed.
2. Per ogni partner: fase attuale, settimana (1-12), % completamento task della fase,
   prossima milestone con deadline.
3. **Rileva ritardi**: task oltre deadline, fase che dura più delle settimane previste
   (SETUP >2, ENABLEMENT >2, LAUNCH >4, OPTIMIZE >4).
4. **Milestone critiche**: primo scan (g.14), team formato (sett.4), primo deal (sett.8),
   health baseline (sett.12) — se una salta, l'onboarding è a rischio: flag.
5. Per il singolo partner: mostra anche la checklist della fase corrente con stato per task.

## Formato output
```markdown
---
zone: commerciale
tier: 🟡
type: report
---
# Onboarding Status — {YYYY-MM-DD}

| Partner | Fase | Sett. | Completamento | Prossima milestone | Alert |
|---|---|---|---|---|---|
| {nome} | LAUNCH | 6/12 | 75% | Primo deal (sett.8) | — |
| {nome} | SETUP | 2/12 | 40% | Primo scan (g.7) | task 1.4 in ritardo |

## Ritardi e azioni proposte (owner + deadline)
```
Drill-down singolo partner: checklist fase con `[x]`/`[ ]`, deadline, on-track sì/no.

## Destinazione
Report cross-partner: zona `commerciale` → `delivery/onboarding-status-{YYYY-MM-DD}.md`.
Aggiornamenti di stato del singolo partner: nella sua `clienti/{slug}/onboarding-checklist.md`.

## Handoff
Task tecnico in ritardo → `cto`; partner non collaborativo → `sales`/`ceo`.
