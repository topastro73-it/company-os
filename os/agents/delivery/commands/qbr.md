# /delivery qbr — Quarterly Business Review

## Scopo
Preparare il QBR di un partner: risultati del quarter, piano del prossimo, expansion.

## Input
- Partner slug · quarter (es. Q3-2026) · data della call QBR

## Passi
1. Carica scheda partner, storico health, metriche del quarter (PMI onboarded/attive,
   churn, revenue generato, engagement venditori).
2. **Risultati vs target**: tabella metrica → target → actual → delta. Dati reali,
   fonti citate.
3. **Wins e highlights**: max 5, concreti (deal chiusi via piattaforma, PMI protette).
4. **Aree di miglioramento**: max 3, con proposta di azione condivisa — mai QBR solo
   celebrativo.
5. **Piano prossimo quarter**: obiettivi congiunti, azioni, owner (nostro e loro).
6. **Expansion**: solo se health ≥70 — tier upgrade o servizi aggiuntivi con revenue
   potenziale; altrimenti ometti la sezione.
7. Prepara i **talking points** per la call e le domande da fare al partner.
8. Dopo la call: registra esiti e follow-up nella scheda partner.

## Formato output
```markdown
---
zone: clienti/{slug}
tier: 🟡
type: qbr
render: gdoc
quarter: {Q}
---
# QBR — {Partner} — {Q}

## Risultati del quarter (metriche vs target)
## Wins e highlights          ## Aree di miglioramento
## Piano {Q+1} (obiettivi, azioni, owner)
## Expansion (se health ≥70)
## Talking points per la call
```

## Destinazione
Zona `clienti/{slug}` → `qbr-{Q}.md` (`render: gdoc` → il publish crea il Google Doc
condivisibile col partner, gated dal protocollo external-writes).
Commit (admin): `[delivery] qbr: {slug} {Q}`.

## Handoff
Expansion confermata → `sales` (nuova opportunità) · feature richieste → `product`.
