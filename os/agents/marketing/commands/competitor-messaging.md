# /marketing competitor-messaging — Counter-positioning

## Scopo
Analizzare come si posiziona un competitor e definire il nostro counter-positioning,
per il messaging pubblico e per la battlecard di vendita.

## Input
- Competitor · fonti disponibili (sito, pricing pubblico, content, quello che dicono
  i prospect nelle call)

## Passi
1. Carica il nostro positioning (`marketing/brand/`) e la battlecard esistente
   (zona `commerciale/battlecards/`), più le obiezioni riportate dal campo.
2. **Analizza il loro messaging**: a chi parlano (segmento), promessa principale, prove
   che portano, pricing/packaging comunicato, dove sono forti e dove sono vaghi.
3. **Counter-positioning**: dove vinciamo davvero (con prove nostre: certificazioni,
   modello white-label, focus PMI via partner) — mai denigrare, posizionarsi sui punti
   di forza; dove NON vinciamo → come qualifichiamo il fit invece di combattere.
4. Output doppio:
   - messaging pubblico (come ne parliamo senza nominarli, di solito)
   - input per la battlecard sales (frasi pronte per le obiezioni "ma {competitor} fa X")
5. Ogni claim comparativo → verificabile; niente confronti basati su sentito dire.

## Formato output
```markdown
---
zone: marketing
tier: 🟡
type: competitor-messaging
competitor: {slug}
---
# Messaging vs {Competitor} — {YYYY-MM-DD}

## Il loro posizionamento (segmento, promessa, prove, pricing)
## Dove vinciamo (con prove) / Dove non vinciamo (come qualificare)
## Counter-messaging pubblico
## Frasi pronte per Sales (obiezione → risposta)
```

## Destinazione
Zona `marketing` → `brand/messaging-vs-{competitor}.md`.
Commit (admin): `[marketing] messaging: vs {competitor}`.

## Handoff
Aggiornamento battlecard → `sales` (zona `commerciale/battlecards/`) · gap di prodotto
reale emerso → `product`.
