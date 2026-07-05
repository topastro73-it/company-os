# /finance investor-crm — Pipeline e relazioni investitori

## Scopo
Tracciare ogni relazione investitore come una pipeline: stage, prossimo touch, fit, storia.

## Input
- Nessuno (report) oppure aggiornamento ("aggiungi {fondo}", "sposta {fondo} a term-sheet",
  "logga call con {partner}")

## Passi
1. Carica `finance/investors/pipeline.md`.
2. **Modello dati** per investitore: fondo, partner di riferimento, stage
   (`radar → contacted → meeting → deep-dive → term-sheet → closed | passed`),
   fit (thesis, stage, ticket, portfolio conflict), ultimo touch, next step con data,
   note relazione (chi ci ha introdotto, cosa gli interessa, obiezioni emerse).
3. **Aggiorna**: nuovo investitore, cambio stage (con data), log interazione (aggiorna
   ultimo touch), esito (closed/passed con motivo — il motivo del pass è oro per i
   prossimi).
4. **Report**: pipeline per stage, relazioni fredde (nessun touch da >60gg per investitori
   attivi in pipeline), next steps della settimana, chi deve ricevere il prossimo update.
5. Ogni promessa fatta a un investitore ("ti mando X") → follow-up tracciato.

## Formato output
```markdown
---
zone: finance
tier: 🔴
type: investor-crm
---
# Investor Pipeline — {YYYY-MM-DD}

## Per stage
| Fondo | Partner | Stage | Fit | Ultimo touch | Next step (data) |
## Relazioni da riscaldare (>60gg)
## Passed (con motivo)
## Next steps settimana
```

## Destinazione
Zona `finance` → `investors/pipeline.md` (aggiornamento in place).
Commit (admin): `[finance] investor-crm: {azione}`.

## Handoff
Meeting fissato → `cos` (`/cos prepare-meeting`, tipo investor) · term-sheet ricevuto →
`ceo` + revisione legale esterna.
