# /sales proposal — Proposta commerciale

## Scopo
Generare una proposta personalizzata che parli dei problemi del cliente, non delle nostre feature.

## Input
- Account/prospect · opportunità collegata (se esiste) · tier/pricing ipotizzato
- Contesto: pain point emersi, stakeholder, requisiti (es. certificazioni richieste)

## Passi
1. Carica il contesto: opportunità e account dalla zona `commerciale`, storia del cliente
   da `clienti/{slug}/` se esiste, value proposition da `zones/_root/context/`.
2. **Personalizza**: apri sui LORO problemi (dal discovery), non sul prodotto.
3. Struttura: Executive Summary → Problema → Soluzione proposta → Perché noi
   (certificazioni dalla zona `compliance`, social proof, case rilevanti) → Pricing →
   Next steps con date.
4. **Pricing**: usa il tier appropriato, chiaro e trasparente. Discount → serve OK CEO prima.
5. **Feature check**: tutto ciò che prometti è shipped o in roadmap confermata; il resto
   passa da `/product evaluate-request` PRIMA di entrare in proposta.
6. Bozza → review interna → versione finale nella cartella del cliente con `render: gdoc`
   (publish la converte in Google Doc commentabile).
7. Aggiorna l'opportunità: stage → `proposal-sent` (probability 40 ricalcolata), Timeline.

## Formato output
```markdown
---
zone: clienti/{slug}
tier: 🟡
type: proposta
render: gdoc
opportunity: {opp-slug}
---
# Proposta — {Cliente} — {data}
## Executive Summary   ## Il vostro contesto e problema
## Soluzione proposta  ## Perché noi
## Investimento        ## Next steps
```

## Destinazione
Bozza: zona `commerciale` → `proposte-bozze/{opp-slug}-vN.md`.
Finale consegnata: zona `clienti/{slug}` → `proposta-{YYYY-MM-DD}.md`.
L'invio al cliente (email/Drive share) segue PREPARE → APPROVE → EXECUTE.
