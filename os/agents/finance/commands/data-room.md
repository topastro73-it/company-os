# /finance data-room — Readiness data room

## Scopo
Sapere in ogni momento quanto siamo pronti a una due diligence: cosa c'è, cosa manca,
chi deve produrlo.

## Input
Nessuno; opzionale: round target (cambia la profondità richiesta).

## Passi
1. **Scansiona le zone** contro la checklist per categoria:
   - **Company**: pitch deck, one-pager, vision e OKR (`direzione`)
   - **Financials**: financial model, pricing, KPI, cap table, burn/runway, MRR storico
     (`finance` 🔴)
   - **Product**: roadmap, PRD principali con status, architettura (`prodotto`)
   - **Market**: segmenti, battlecards, TAM/SAM/SOM, case study (`commerciale`, `marketing`)
   - **Team**: ruoli (`config/people.yaml`), organigramma, hiring plan
   - **Legal & compliance**: statuto, certificazioni, policy, contratti tipo, DPA, IP
     (`compliance`, `clienti/*/contratti` 🔴)
2. Per ogni documento: **presente / parziale / mancante**, con path e freschezza.
3. **Gap analysis** prioritizzata: critico → alto → medio, con azione, owner (agente),
   deadline.
4. La condivisione effettiva con un investitore avviene su una cartella Drive dedicata
   con ACL propria (via `admin`), **mai** dando accesso alla zona `finance`; documenti 🔴
   entrano solo se necessari alla fase e dopo APPROVE.

## Formato output
```markdown
---
zone: finance
tier: 🔴
type: data-room-audit
---
# Data Room Readiness — {YYYY-MM-DD}
Presenti: {n}/{tot} ({%}) · Parziali: {n} · Mancanti: {n}

## Gap analysis
| # | Documento | Stato | Priorità | Azione | Owner | Entro |
## Per categoria (dettaglio)
```

## Destinazione
Zona `finance` → `investors/data-room-audit-{YYYY-MM-DD}.md`.
Commit (admin): `[finance] investor: data room audit`.

## Handoff
Doc mancanti → agente owner (product, compliance, marketing…) · condivisione → `admin` (ACL).
