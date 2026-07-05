# /cto security-review — Analisi rischi di sicurezza

## Scopo
Valutare la postura di sicurezza (di una feature, di un componente o complessiva) e
proporre mitigazioni. Vendiamo cybersecurity: dobbiamo essere più sicuri dei nostri clienti.

## Input
- Scope: feature/spec, componente, integrazione, o postura complessiva

## Passi
1. Carica lo scope (PRD o architettura) e i controlli mappati in zona `compliance`
   (ISO 27001 Annex A, requisiti NIS2) — la review parla la loro lingua.
2. **Threat modeling essenziale** sullo scope: superficie di attacco, attori (partner,
   venditore, PMI, esterno), asset critici (dati scan PMI, credenziali, PII).
3. **Checklist minima**: authn/authz sui 3 livelli utente e isolamento tenant ·
   input validation e injection · secrets management (mai in repo/log) · encryption
   at rest/in transit · logging e audit trail (senza PII) · dipendenze vulnerabili ·
   backup e recovery.
4. Per ogni rischio: severità (Critical/High/Medium/Low), scenario, mitigazione proposta,
   effort, owner.
5. **Evidenza compliance**: la review firmata e datata è un'evidenza — segnala a
   `compliance` per l'archiviazione in `compliance/evidence/`.
6. Rischi Critical → escalation immediata `ceo`; fix → backlog `product` con priorità.

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: security-review
scope: {…}
date: YYYY-MM-DD
---
# Security Review — {scope} — {data}

## Threat model (attori, asset, superficie)
## Rischi | Severità | Scenario | Mitigazione | Effort | Owner |
## Quick wins (≤1 settimana)
## Evidenze per compliance
```

## Destinazione
Zona `prodotto` → `reviews/security-review-{scope}-{YYYY-MM-DD}.md`;
riferimento in `compliance/evidence/`. Commit (admin): `[cto] security: review {scope}`.

## Handoff
Evidenza → `compliance` · fix → `product` (backlog) · Critical → `ceo` entro 24h.
