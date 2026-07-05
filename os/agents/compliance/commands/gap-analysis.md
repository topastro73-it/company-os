# /compliance gap-analysis — Gap analysis per framework

## Scopo
Analisi requisito-per-requisito di un framework con roadmap di remediation.

## Input
- Framework: `nis2` | `gdpr` | `iso27001` | `iso27017` | `iso27018` | `soc2`

## Passi
1. Carica i requisiti mappati da `compliance/frameworks/{framework}-requirements.md`
   (per ISO 27001: i 93 controlli Annex A 2022; per NIS2: i 10 requisiti chiave —
   risk mgmt, incident response 24h/72h, BC/DR testato, supply chain, vulnerability
   mgmt, encryption, MFA/access control, network monitoring, training, audit periodici).
2. Per ogni requisito: stato **compliant / partial / non-compliant / N/A**, evidenza
   disponibile (link in `evidence/`), gap se presente.
3. Per ogni gap: cosa manca concretamente, effort (S/M/L), owner, priorità
   (blocca certificazione? espone a sanzione? richiesto da RFP in corso?).
4. **Roadmap di remediation** in fasi con date realistiche; per ISO: review ISMS →
   aggiornamento controlli → audit interno → audit esterno.
5. Verdetto onesto: "pronti per l'audit? Se no, cosa manca e quando lo saremo."

## Formato output
```markdown
---
zone: compliance
tier: 🟡
type: gap-analysis
framework: {framework}
---
# Gap Analysis — {framework} — {YYYY-MM-DD}
Compliant: {n}/{tot} ({%}) · Partial: {n} · Non-compliant: {n} · N/A: {n}

## Gap per priorità
| Requisito | Stato | Gap | Effort | Owner | Deadline |
## Roadmap di remediation (fasi + date)
## Readiness verdict

> Assessment interno — l'audit formale spetta all'ente accreditato.
```

## Destinazione
Zona `compliance` → `audits/gap-{framework}-{YYYY-MM-DD}.md`.
Commit (admin): `[compliance] gap: {framework}`.

## Handoff
Gap tecnici → `cto` · gap di processo/formazione → `ceo` · gap documentali →
`/compliance policy-review`.
