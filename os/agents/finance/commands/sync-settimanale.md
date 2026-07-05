# /finance sync-settimanale — Riconciliazione settimanale

## Scopo
Tenere i registri di zona allineati alla realtà: banca, fatture, abbonamenti — una volta
a settimana, 20 minuti, zero sorprese a fine mese.

## Input
Nessuno. Cadenza: settimanale (lunedì, o primo accesso della settimana).

## Passi
1. **Fonti live** (se MCP attivi, altrimenti chiedi i dati e dichiara la freschezza):
   - Qonto: saldo e movimenti settimana · Fatture in Cloud: emesse/ricevute/pagate
   - Stripe: incassi subscription · un ERP: contratti e ricavi maturati
2. **Riconcilia incassi**: pagamenti ricevuti ↔ fatture aperte in `fatturazione.md`
   → marca incassate; segnala pagamenti non riconciliabili.
3. **Riconcilia uscite**: addebiti ↔ `costi-ricorrenti.md`; nuovi costi ricorrenti
   non mappati → aggiungili; anomalie (importo diverso, doppio addebito) → flag.
4. **Aggiorna i registri**: `fatturazione.md` (stati), `cashflow.md` (saldo reale vs
   proiezione — se scostamento >10%, capisci perché), `scadenzario.md` (spunta ciò che
   è stato pagato).
5. **Flash report**: 6 righe — saldo, incassato, uscito, scaduto, prossime scadenze 7gg,
   anomalie. Prestiti/finanziamenti ricevuti: riga separata, **mai dentro i ricavi**.

## Formato output
```markdown
---
zone: finance
tier: 🔴
type: sync-report
week: YYYY-Wnn
---
# Sync settimanale — {settimana}
Saldo: €… (Δ vs proiezione: …) · Incassato: €… · Uscito: €…
Scaduto da incassare: €… · Scadenze 7gg: … · Anomalie: …
## Dettaglio riconciliazioni  ## Azioni (owner + entro)
```

## Destinazione
Zona `finance` → `sync/sync-{YYYY-Wnn}.md` + registri aggiornati in place.
Commit (admin): `[finance] sync: settimana {n}`.

## Handoff
Fatture scadute 30+gg → `/finance fatture-status` + `sales` per sollecito.
