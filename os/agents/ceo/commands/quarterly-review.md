# /ceo quarterly-review — Retrospettiva di trimestre

## Scopo
Chiudere il quarter: risultati vs piano, lezioni, priorità del prossimo trimestre.

## Input
- Quarter da chiudere (default: quello appena concluso)

## Passi
1. **Raccogli i risultati** dagli snapshot di zona:
   - `commerciale`: deal won/lost, coverage vs target, funnel ISP
   - `clienti`: partner attivi, health medio, churn, expansion
   - `prodotto`: feature shipped vs pianificate, spec lifecycle
   - `vault/finance`: revenue, burn, runway, incassato vs fatturato
   - `compliance`: milestone certificazioni, gap chiusi
   - `marketing`: content prodotto, risultati campagne
2. **Scoring OKR finale**: esegui la logica di `/ceo okr-review` con verdetto di fine quarter.
3. **Cosa ha funzionato / cosa no**: max 5 punti ciascuno, con evidenza.
4. **Non fatto**: promesse e piani non eseguiti, con motivo se noto.
5. **Piano Q+1**: 3 priorità strategiche proposte (da validare col CEO), bozza OKR.
6. **Learnings**: proponi i pattern del quarter come candidati `LRN-XXX` (al close).

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: report
render: gdoc
---
# Quarterly Review — {Q}

## Risultati vs piano (tabella per area, con fonte)
## Scoring OKR finale
## Cosa ha funzionato / Cosa no
## Non fatto
## Piano {Q+1}: 3 priorità + bozza OKR
```

## Destinazione
Zona `direzione` → `board/quarterly-review-{Q}.md` (leggibile dal board via ACL direzione).
Commit: `[ceo] review: {Q}`.

## Handoff
- Bozza OKR Q+1 approvata → nuovo file `direzione/okrs/{Q+1}.md`
- Priorità di prodotto → `product` (`/product prioritize`)
