# /cto architecture-review — Review architetturale

## Scopo
Valutare l'architettura corrente o una proposta: regge la roadmap? Scala? È sicura?

## Input
- Scope: architettura complessiva, un sottosistema, o una proposta di cambiamento

## Passi
1. Carica roadmap e spec in arrivo (zona `prodotto`) — la review si fa contro il futuro
   previsto, non solo contro il presente; carica gli ADR rilevanti.
2. **Fotografa lo stato**: componenti, dipendenze, integrazioni (ClickUp/HubSpot/ERP…),
   multi-tenancy (se il prodotto è multi-tenant, l'isolamento fra tenant è architettura, non dettaglio).
3. **Valuta per dimensione**: scalabilità (regge 10x utenti/tenant?), affidabilità e single
   point of failure, sicurezza (superficie di attacco, secrets, authz su ogni ruolo),
   mantenibilità e debito, costo infrastrutturale.
4. **Compliance check**: l'architettura mantiene i controlli mappati (ISO 27001, NIS2)?
   Gap → segnala a `compliance` con severità.
5. **Raccomandazioni prioritizzate**: max 5, ognuna con effort (S/M/L), rischio se ignorata,
   owner. La più semplice che funziona prima.
6. Cambiamenti strutturali raccomandati → ognuno diventa un ADR (`/cto tech-decision`).

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: arch-review
date: YYYY-MM-DD
---
# Architecture Review — {scope} — {data}

## Stato attuale (componenti, dipendenze)
## Valutazione | Dimensione | Stato | Rischio | Note |
## Gap compliance (se presenti)
## Raccomandazioni prioritizzate (effort, rischio, owner)
## ADR da aprire
```

## Destinazione
Zona `prodotto` → `reviews/arch-review-{YYYY-MM-DD}.md`.
Commit (admin): `[cto] review: architettura {scope}`.

## Handoff
Gap compliance → `compliance` · lavori da pianificare → `product` (backlog) ·
rischio critico → `ceo`.
