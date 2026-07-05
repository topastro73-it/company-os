# /sales deal-review — Analisi strategica di un deal

## Scopo
Capire se e come chiudere un deal: fit, rischi, strategia, next steps.

## Input
- `opp-slug` dell'opportunità (o prospect se non ancora in pipeline)

## Passi
1. Carica l'opportunità e l'account dalla zona `commerciale`, la storia dalla cartella
   `clienti/{slug}/` se già cliente, i learnings sales attivi (`⚡ LRN-XXX`, max 1).
2. **Qualifica** (MEDDICC-lite):
   - fit ICP (segmento, dimensione, pain) · decision maker e champion identificati?
   - budget · timeline · compelling event · competition in gara
3. **Rischi**: deal killer potenziali, obiezioni probabili (con risposta preparata),
   blocker aperti e aging corrente (calcolato in lettura).
4. **Strategia**: next steps concreti con owner e data, messaging chiave, ask specifiche
   per il prossimo meeting, cosa NON promettere (check roadmap `prodotto`).
5. **Probabilità**: resta quella derivata dallo stage — se il tuo giudizio diverge molto,
   il segnale è che lo stage è sbagliato: proponi di muovere lo stage, non il numero.
6. Aggiorna l'opportunità (next-step, blocker) e salva la review.

## Formato output
```markdown
---
zone: commerciale
tier: 🟡
type: deal-review
opportunity: {opp-slug}
---
# Deal Review — {account} / {opp-slug} — {data}

## Fotografia (stage, valore, aging, owner)
## Qualifica (tabella MEDDICC-lite)
## Rischi e obiezioni (con risposte)
## Strategia e next steps (owner + data)
## Cosa non promettere
```

## Destinazione
Zona `commerciale` → `reviews/deal-{opp-slug}-{YYYY-MM-DD}.md`.
Commit (admin): `[sales] review: {opp-slug}`.

## Handoff
Deal >€50k o discount → `ceo` · feature richiesta → `product` · contratto → `compliance`.
