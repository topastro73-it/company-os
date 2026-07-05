# /product uat — UAT / QA con verdetto GO/NO-GO

## Scopo
Verificare che una feature faccia ciò che la PRD promette, prima del rilascio.
Owner operativo: il PMO/QA.

## Input
- Spec slug · fase: `plan` (genera il piano) o `report` (registra i risultati di un ciclo)

## Passi
### Fase plan (alla transizione `in-development`)
1. Leggi la PRD: user stories e acceptance criteria sono la base dei test case.
2. Genera il **test plan**: scope, ambienti, dati di test necessari, matrice
   test case ↔ acceptance criteria (Given/When/Then → passi verificabili),
   edge case, test di regressione sui flussi core toccati.
3. Se la spec ha `compliance-impact` o tocca auth/dati: aggiungi checklist security
   (input validation, authz per i 3 livelli utente, PII nei log) — review con `cto`.

### Fase report (a fine ciclo di test)
4. Esegui/raccogli i risultati: per ogni test case pass/fail, bug con severità P0-P3.
5. **Verdetto**: **GO** (nessun P0/P1 aperto, AC coperti) / **NO-GO** (motivi espliciti,
   bug bloccanti, retest necessario).
6. Il verdetto GO è **condizione necessaria** per `status: shipped` (con epic ClickUp
   Released). NO-GO → la spec resta in-development, bug → `/product sync-clickup`.

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: uat
spec: {slug}
cycle: 1
verdict: null            # GO | NO-GO
---
# UAT — {feature} — ciclo {N}
## Test plan / risultati
| TC | Acceptance criterion | Passi | Esito | Bug |
## Bug aperti (severità, owner)   ## Verdetto e motivazione
```

## Destinazione
Zona `prodotto` → `testing/uat-{slug}-cycle{N}.md`.
Commit (admin): `[product] uat: {slug} ciclo {N} — {verdetto}`.

## Handoff
NO-GO → `cto` (fix) · GO → aggiorna spec a shipped + `/product release-notes`.
