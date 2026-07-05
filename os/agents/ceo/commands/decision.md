# /ceo decision — Decisione strategica documentata

## Scopo
Analizzare una decisione importante e registrarla in modo immutabile e tracciabile.

## Input
- Topic della decisione ("Devo decidere su [topic]")
- Contesto: perché ora, chi la sollecita, vincoli noti

## Passi
1. **Definisci il problema**: qual è la vera domanda? Perché è importante ora?
2. **Verifica precedenti**: cerca in `direzione/decisions/` e `system/wiki/` decisioni correlate.
   Mai contraddire una decisione recente senza esplicitare cosa è cambiato.
3. **Identifica 2-3 opzioni concrete**. Per ognuna valuta:
   - pro / contro · effort e risorse · impatto (strategia, prodotto, team, cassa)
   - rischi e mitigazioni · **reversibilità** (porta a due vie o a una via?)
4. **Handoff preventivi se servono dati**: stima → `cto`, valutazione feature → `product`,
   impatto economico → `finance`. Niente decisione su dati inventati.
5. **Raccomanda** un'opzione con razionale esplicito.
6. **Next steps**: chi fa cosa, entro quando. **Review date**: quando rivalutiamo.
7. Salva e committa `[ceo] decision: {slug}`.

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: decision
date: YYYY-MM-DD
status: active
review-date: YYYY-MM-DD
---
# DEC — {titolo}

## Contesto        ## Opzioni valutate
## Decisione       ## Razionale
## Conseguenze e rischi accettati
## Follow-up (owner + deadline)
```

## Destinazione
Zona `direzione` → `decisions/YYYY-MM-DD-{slug}.md`. **Immutabile**: si supera con una
nuova decisione che cita la precedente.
