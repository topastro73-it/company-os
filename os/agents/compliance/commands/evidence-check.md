# /compliance evidence-check — Verifica evidenze

## Scopo
Le evidenze sono ciò che l'auditor vede: verificare che esistano, siano aggiornate e
archiviate in `compliance/evidence/` (l'unica sottozona visibile all'auditor esterno).

## Input
Nessuno; opzionale: framework specifico. Cadenza consigliata: trimestrale.

## Passi
1. Per ogni framework attivo, verifica il set di evidenze richieste:
   log e monitoring · vulnerability scan report · record formazione (incl. security
   training onboarding — arriva dal CEO) · verbali approvazione management · report
   audit precedenti · test DR · registro incidenti (dai postmortem in zona `prodotto`) ·
   vendor assessment (da `compliance/vendors/`) · security review (da `cto`).
2. Per ogni evidenza: **esiste? aggiornata** (dentro la finestra richiesta: es. DR test
   semestrale, formazione annuale)? **archiviata** in `evidence/` con naming datato?
3. Evidenze che vivono altrove (postmortem, review) → copia/riferimento in `evidence/`,
   così l'auditor le trova senza accedere ad altre zone.
4. Alert per evidenze mancanti o scadute, con owner e data entro cui rigenerarle.
5. Aggiorna l'indice `compliance/evidence/README.md` (mappa evidenza → dove → freschezza).

## Formato output
```markdown
---
zone: compliance
tier: 🟡
type: evidence-check
---
# Evidence Check — {YYYY-MM-DD}

| Evidenza | Framework | Richiesta ogni | Ultima | Stato | Owner rigenerazione |
|---|---|---|---|---|---|

## ⚠️ Mancanti o scadute (azioni con deadline)
## Indice aggiornato: sì/no
```

## Destinazione
Zona `compliance` → `audits/evidence-check-{YYYY-MM-DD}.md` + `evidence/README.md`
aggiornato. Commit (admin): `[compliance] evidence: check {YYYY-MM-DD}`.

## Handoff
Evidenze tecniche mancanti (scan, DR test) → `cto` · formazione scaduta → `ceo`.
