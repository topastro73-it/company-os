# /cto build-vs-buy — Costruire, comprare o partnership

## Scopo
Decidere in modo strutturato se una capability va costruita, comprata o ottenuta via partner.

## Input
- Capability richiesta · da dove nasce il bisogno (PRD, richiesta partner, gap tecnico)

## Passi
1. **Definisci la capability** e il criterio di successo; è core (differenzia il prodotto)
   o context (serve ma non differenzia)? Il core si costruisce, il context raramente.
2. **Opzione BUILD**: effort (range onesto), time-to-market, costo di mantenimento nel
   tempo, fit con lo stack e le skill del team.
3. **Opzione BUY**: candidati concreti, costo (setup + ricorrente), lock-in, sicurezza e
   compliance del vendor (**se tratta dati → serve vendor assessment `compliance` PRIMA
   della firma**), qualità API/integrazione.
4. **Opzione PARTNER**: chi, che accordo, dipendenza creata.
5. **Confronto** a 3 anni (TCO), non solo al costo iniziale; rischio di ogni opzione e
   reversibilità.
6. **Raccomanda** e documenta come ADR; se costo rilevante → `ceo` e `finance`.

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: adr
subtype: build-vs-buy
date: YYYY-MM-DD
---
# Build vs Buy — {capability}

## Capability e criterio di successo · core o context?
## Confronto
| | BUILD | BUY ({vendor}) | PARTNER |
| Costo iniziale / ricorrente / TCO 3y | | | |
| Time-to-market · Lock-in · Rischio | | | |
| Sicurezza & compliance | | | |
## Raccomandazione e razionale
## Follow-up (vendor assessment, PoC, negoziazione)
```

## Destinazione
Zona `prodotto` → `adr/YYYY-MM-DD-build-vs-buy-{slug}.md`.
Commit (admin): `[cto] adr: build-vs-buy {capability}`.

## Handoff
Vendor con dati → `compliance` (vendor assessment) · costo → `finance` · strategica → `ceo`.
