# /product evaluate-request — Valutazione richiesta feature

## Scopo
Decidere in modo difendibile cosa fare di una richiesta: BUILD, CONFIGURE, CUSTOM o DECLINE.

## Input
- Feature/richiesta · chi la chiede (partner? deal in corso?) · contesto business
  (deal size, urgenza) — le richieste arrivano anche da `prodotto/richieste/`

## Passi
1. **Spec status check**: spec stale in `prodotto/specs/INDEX.md` → segnala prima di procedere.
2. Carica vision (`direzione`), roadmap e backlog (`prodotto`), eventuali valutazioni
   passate della stessa richiesta (mai rivalutare da zero senza citare l'esito precedente).
3. **Estrai il bisogno reale**: job-to-be-done; distingui "cosa chiedono" da "perché".
4. **Applica il framework**, valutando sui 3 livelli (Partner, Venditore, PMI):
   - Strategic Fit: High/Medium/Low (visione, segmento core, differenziazione)
   - Scalability: Scalable / Partially / Custom ("serve a 1 o a 100?")
   - Market Demand: Broad / Niche / Single-customer
   - Effort vs Value: effort XS-XL, business value, opportunity cost
5. **Raccomandazione**:
   - **BUILD** (product): high fit + scalable + broad demand
   - **CONFIGURE** (configurabile): medium-high fit + partially scalable + multi-customer
   - **CUSTOM**: low fit o single-customer con valore economico che lo giustifica
   - **DECLINE/DEFER**: low fit + niche, o conflitto con integrità prodotto (+ review-date se defer)
6. **Red flags** (se da Sales): single-customer non validata · timeline irrealistica ·
   scope creep. Presenti → dillo esplicitamente.
7. Rispondi a chi ha chiesto: esito + motivazione in linguaggio partner ("in evaluation",
   mai date).

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: evaluation
status: evaluated
requested-by: {partner|interno}
---
# Evaluation — {feature}
## Bisogno reale  ## Framework (tabella 4 dimensioni × 3 livelli)
## Raccomandazione: {BUILD|CONFIGURE|CUSTOM|DECLINE} + razionale e trade-off
## Next step
```

## Destinazione
Zona `prodotto` → `specs/evaluation-{slug}.md`. Commit (admin): `[product] eval: {slug}`.

## Handoff
BUILD/CONFIGURE approvato → `/product write-spec` · risposta al richiedente → `sales`/`delivery`.
