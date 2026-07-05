# /product write-spec — PRD

## Scopo
Trasformare una feature valutata in una PRD implementabile e verificabile.

## Input
- Feature (idealmente con evaluation esistente in `prodotto/specs/evaluation-{slug}.md`)

## Passi
1. **Spec status check** su `prodotto/specs/INDEX.md`; poi carica evaluation, vision, personas.
2. Tema nuovo senza analisi? Fermati: fai l'analisi del dominio prima (domande una alla
   volta, process map se serve). Mai spec senza aver capito il problema.
3. **Scrivi la PRD** (formato sotto): problem statement, personas sui 3 livelli
   (Partner/Venditore/PMI), user stories "As a… I want… So that…", acceptance criteria
   "Given/When/Then", data model **funzionale** (mai tecnico), requisiti non-funzionali,
   in scope / out of scope espliciti, metriche di successo, dipendenze e rischi.
4. **Compliance impact check**: dati personali? cambia security? → frontmatter
   `compliance-impact: [NIS2/GDPR/ISO27001]`, se serve DPIA → handoff `compliance`.
5. Scope in T-shirt size con razionale; `status: draft` finché il CTO non la valuta.
6. Aggiorna `prodotto/specs/INDEX.md`.

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: prd
status: draft            # draft→evaluated→approved→in-development→shipped
compliance-impact: []
clickup-epic: ""
clickup-doc: ""
last-updated: YYYY-MM-DD
---
# PRD — {feature}
## Problem statement       ## Personas (3 livelli)
## User stories            ## Acceptance criteria (Given/When/Then)
## Data model (funzionale) ## Requisiti non-funzionali
## In scope / Out of scope ## Metriche di successo
## Dipendenze e rischi     ## Implementation status (tabella deliverable)
## Decisions made          ## Deferred / follow-up
```

## Destinazione
Zona `prodotto` → `specs/prd-{slug}.md`. Commit (admin): `[product] spec: PRD {feature}`.

## Handoff
→ `cto` per stima e feasibility · con `compliance-impact` → `compliance` ·
approvata → `/product sync-clickup` (epic + task).
