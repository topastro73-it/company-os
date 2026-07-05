# /finance cashflow — Proiezione di cassa

## Scopo
Sapere sempre quanto ossigeno abbiamo: saldo proiettato a 3 mesi, settimana per settimana.

## Input
Nessuno; opzionale: scenario da simulare ("e se il deal X slitta di un mese?").

## Passi
1. Carica `finance/cashflow.md`, `fatturazione.md`, `costi-ricorrenti.md`,
   `scadenzario.md`; saldo reale da Qonto se MCP attivo.
2. **Entrate attese**: fatture emesse (con data incasso realistica, non contrattuale:
   usa il DSO storico), ricavi ricorrenti, incassi da pipeline SOLO se weighted e
   dichiarati come tali. **Prestiti/finanziamenti: riga separata, mai tra i ricavi.**
3. **Uscite previste**: costi ricorrenti, scadenze fiscali (dallo scadenzario), compensi
   amministratori (**trimestrali, mai mensili**), fornitori una-tantum noti.
4. **Proietta** il saldo settimana per settimana per 12 settimane; poi scenario
   pessimistico (incassi +30gg, nessun nuovo deal) — il worst case è obbligatorio.
5. **Alert**: saldo proiettato sotto soglia critica in qualunque settimana → in cima al
   report, con le 2-3 leve disponibili (solleciti, slittamento uscite, linea di credito).
6. Runway: mesi al saldo zero nello scenario base e nel pessimistico.

## Formato output
```markdown
---
zone: finance
tier: 🔴
type: cashflow
---
# Cashflow — {YYYY-MM-DD}
Saldo attuale: €… · Runway base: {n} mesi · pessimistico: {n} mesi
## ⚠️ Alert (se presenti)
## Proiezione 12 settimane | Sett | Entrate | Uscite | Saldo |
## Scenario pessimistico   ## Assunzioni (esplicite, sempre)
```

## Destinazione
Zona `finance` → `reports/cashflow-{YYYY-MM-DD}.md` + `cashflow.md` aggiornato.
Commit (admin): `[finance] cashflow: proiezione {YYYY-MM-DD}`.

## Handoff
Runway <9 mesi → `ceo` (alert immediato, opzioni sul tavolo).
