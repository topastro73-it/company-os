# /compliance policy-review — Review del policy register

## Scopo
Verificare che tutte le policy esistano, siano aggiornate, approvate e comunicate.
Cadenza consigliata: trimestrale.

## Input
Nessuno; opzionale: singola policy da rivedere in profondità.

## Passi
1. Inventario in `compliance/policies/` contro il set atteso: Information Security,
   Acceptable Use, Incident Response, Business Continuity, Data Classification,
   Access Control, Encryption, Vendor Management, Change Management, HR Security
   (onboarding/offboarding).
2. Per ogni policy, quattro check: **esiste? aggiornata** (<12 mesi o dopo cambi rilevanti)?
   **approvata** (dal management, con data)? **comunicata** (al team, con evidenza)?
3. Policy mancanti o stale → piano di creazione/aggiornamento con owner e deadline.
4. **Coerenza con la realtà**: una policy che descrive processi che non facciamo è un
   rischio in audit, non un punto — flag delle divergenze note (chiedi a `cto` conferma
   sui controlli tecnici dichiarati).
5. Approvazioni e comunicazioni fatte → registra l'evidenza in `compliance/evidence/`.

## Formato output
```markdown
---
zone: compliance
tier: 🟡
type: policy-review
---
# Policy Review — {YYYY-MM-DD}

| Policy | Esiste | Aggiornata | Approvata | Comunicata | Azione |
|---|---|---|---|---|---|

## Mancanti / stale (piano con owner e deadline)
## Divergenze policy ↔ pratica reale
## Evidenze registrate
```

## Destinazione
Zona `compliance` → `audits/policy-review-{YYYY-MM-DD}.md`; policy aggiornate in
`compliance/policies/`. Commit (admin): `[compliance] policy: review {YYYY-MM-DD}`.

## Handoff
Approvazione policy → `ceo` · controlli tecnici dichiarati → `cto` (verifica).
