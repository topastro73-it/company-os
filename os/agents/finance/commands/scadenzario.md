# /finance scadenzario — Scadenze fiscali e amministrative

## Scopo
Nessuna scadenza fiscale/societaria scoperta: cosa scade, quando, chi la gestisce.

## Input
Nessuno; opzionale: orizzonte (default 30 giorni + trimestre).

## Passi
1. Leggi `finance/scadenzario.md` (fonte di verità — se non aggiornato, segnalalo:
   il sistema non deve fingere di sapere).
2. Classifica per urgenza:
   - 🔴 **scadute non completate** (in cima, sempre)
   - 🟡 prossimi 7 giorni · 🟢 prossimi 30 giorni · prossimo trimestre (visibilità)
3. Per ogni scadenza: data, tipo (F24, IVA, INPS, bilancio, diritto camerale, titolare
   effettivo, requisiti startup innovativa…), importo stimato, owner (noi / commercialista).
4. **Anticipo**: segnala 7gg prima le mensili, 30gg prima le annuali; per quelle in carico
   al commercialista, la domanda è "gliel'abbiamo chiesto? ha confermato?"
5. Azioni concrete: "emetti", "paga", "chiedi allo studio" — mai interpretazioni fiscali
   (quelle sono del commercialista).

## Formato output
```markdown
---
zone: finance
tier: 🔴
type: scadenzario-report
---
# Scadenzario — {YYYY-MM-DD}

## 🔴 Scadute (non completate!)
| Scadenza | Data | Tipo | Importo stimato | Owner | Azione |
## 🟡 Prossimi 7 giorni
## 🟢 Prossimi 30 giorni
## Prossimo trimestre (solo visibilità)
```

## Destinazione
Report in chat + aggiornamento stati in `finance/scadenzario.md`.
Commit (admin): `[finance] scadenzario: check {YYYY-MM-DD}`.

## Handoff
Scadenza che richiede decisione di cassa → `ceo`; documenti per lo studio →
copia in `finance/per-commercialista/` (vetrina one-way, via APPROVE).
