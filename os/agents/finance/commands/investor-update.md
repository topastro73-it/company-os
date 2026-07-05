# /finance investor-update — Update investitori

## Scopo
Update periodico factuale: trazione reale, problemi con piano, ask chiara. La fiducia
degli investitori si costruisce con la coerenza, non con l'overselling.

## Input
- Periodo (mese/trimestre) · destinatari (investitori attuali, prospect, advisor)

## Passi
1. Raccogli i numeri con fonte: revenue/MRR e incassato (zona `finance`), pipeline
   weighted (zona `commerciale`), partner e health (zona `clienti`), shipped (zona
   `prodotto`), milestone compliance (zona `compliance`), burn e runway (cashflow).
2. Confronta con l'update precedente (`direzione/investor-updates/`): la narrativa deve
   essere coerente — se un numero è peggiorato, si dice, con il perché e il piano.
3. Struttura: **TL;DR** (3 righe) → Highlights → Lowlights (onesti, con azione) →
   Numeri chiave (tabella con trend) → Prodotto → Team → **Ask** (intro, talenti,
   competenze) → prossimi milestone.
4. **Redazione tier**: l'update è 🟡 (esce dall'azienda): niente dettagli 🔴 non necessari
   (cap table, IBAN, salari); numeri aggregati, non contratti singoli con nomi se non
   autorizzati.
5. Review CEO → invio via PREPARE → APPROVE → EXECUTE (mai inviare senza approvazione).

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: investor-update
render: gdoc
period: {YYYY-MM|Qn}
---
# Investor Update — {periodo}
## TL;DR             ## Highlights / Lowlights
## Numeri chiave (tabella + trend)
## Prodotto & team   ## Ask
## Prossimi milestone
```

## Destinazione
Zona `direzione` → `investor-updates/update-{periodo}.md` (leggibile dal board).
Commit (admin): `[finance] investor: update {periodo}`.

## Handoff
Ask strategiche → `ceo` · aggiornamento relazioni → `/finance investor-crm`.
