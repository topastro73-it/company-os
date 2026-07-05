---
zone: _os
tier: 🟡
---

# Glossario

> Termini di sistema (validi per ogni istanza) + termini di business (da adattare alla tua azienda).

## Sistema
- **Zona** — una cartella Drive top-level con una ACL e una direzione di sync (vedi `config/acl.yaml`).
- **ACL** — i permessi Drive nativi: sono l'enforcement reale dell'accesso, non una convenzione.
- **Tier 🔴🟡🟢** — classificazione di sensibilità (RESTRICTED / INTERNAL / PUBLIC): decide cosa
  può uscire e come, ortogonale a chi accede (quello è l'ACL).
- **Master unico** — ogni file ha una sola fonte di verità (git *oppure* Drive), mai due.
- **PREPARE → APPROVE → EXECUTE** — protocollo per ogni scrittura su sistemi esterni.
- **Handoff** — passaggio di consegne tra agenti (indicato a fine attività).
- **LRN-XXX** — regola appresa (learning) che il sistema applica proattivamente.

## Business (esempi comuni — adatta alla tua azienda)
- **ICP** — Ideal Customer Profile: chi è il cliente ideale.
- **ACV / MRR / ARR** — Annual Contract Value / Monthly / Annual Recurring Revenue.
- **NRR** — Net Revenue Retention (incl. upsell/downsell). **Churn** — tasso di abbandono.
- **CAC / LTV** — costo di acquisizione / lifetime value.
- **Health score** — indice di salute cliente (vedi skill customer-success per la formula).
- **QBR** — Quarterly Business Review.
- **North Star** — la metrica che conta più di tutte.

<Aggiungi qui i termini specifici del tuo settore/prodotto.>
