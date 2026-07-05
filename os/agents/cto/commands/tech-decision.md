# /cto tech-decision — ADR

## Scopo
Analizzare e documentare una decisione tecnica in modo che tra 6 mesi si capisca perché.

## Input
- Topic della decisione · vincoli noti (budget, timeline, team, compliance)

## Passi
1. **Definisci il problema tecnico** e i vincoli; verifica in `prodotto/adr/` se esiste
   un ADR correlato (mai contraddirlo senza esplicitare cosa è cambiato).
2. **Identifica 2-3 opzioni** concrete con pro/contro ciascuna.
3. **Valuta** ogni opzione su: performance, scalabilità, mantenibilità, costo (setup +
   ricorrente), skill del team, time-to-market, sicurezza.
4. **Compliance check**: la decisione cambia encryption, access control, logging o data
   flow? → documenta l'impatto sui controlli mappati in zona `compliance` e segnala.
5. **Raccomanda** con razionale chiaro; esplicita il debito tecnico accettato (se c'è)
   e la reversibilità della scelta.
6. Documenta come ADR; se la decisione è strategica (stack, vendor critico, costo alto)
   → proponi al CEO prima di considerarla presa.

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: adr
status: accepted         # proposed | accepted | superseded-by: {slug}
date: YYYY-MM-DD
compliance-impact: []
---
# ADR — {titolo}

## Contesto e problema      ## Vincoli
## Opzioni valutate (pro/contro, costi)
## Decisione e razionale
## Impatto compliance       ## Debito tecnico accettato
## Conseguenze e follow-up (owner + deadline)
```

## Destinazione
Zona `prodotto` → `adr/YYYY-MM-DD-{slug}.md`. Gli ADR sono immutabili: si superano con
un nuovo ADR (`superseded-by`). Commit (admin): `[cto] adr: {topic}`.

## Handoff
Impatto compliance → `compliance` · impatto roadmap/priorità → `product` ·
strategica → `ceo` (`/ceo decision` se serve una decisione aziendale).
