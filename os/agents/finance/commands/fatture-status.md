# /finance fatture-status — Stato fatturazione

## Scopo
Fotografia completa del ciclo attivo: da emettere, in attesa, scadute, incassate. Le
fatture scadute sono un problema di cassa, non di ordine.

## Input
Nessuno.

## Passi
1. Leggi `finance/fatturazione.md`; se Fatture in Cloud MCP attivo, riconcilia con
   l'emesso/incassato reale.
2. **Da emettere**: revenue maturato non ancora fatturato (contratti attivi da ERP/zona
   `clienti`) — per ognuna: cliente, periodo, importo, "da emettere entro".
3. **In attesa di pagamento**: fattura, cliente, importo, emessa, scadenza, giorni.
4. **Scadute ⚠️**: ordinate per ritardo; 30+ giorni → sollecito proposto (bozza pronta,
   invio via APPROVE), coordinato con `sales` se il partner ha trattative aperte.
5. **Incassate nel mese** e riepilogo: fatturato mese, da incassare, scaduto totale,
   **DSO medio** e trend.
6. Aggiorna gli stati nel registro.

## Formato output
```markdown
---
zone: finance
tier: 🔴
type: fatture-report
---
# Fatturazione — {YYYY-MM-DD}

## Da emettere            | Cliente | Periodo | Importo | Entro |
## In attesa di pagamento | Fattura | Cliente | Importo | Scadenza | Giorni |
## Scadute ⚠️             | Fattura | Cliente | Importo | Ritardo | Azione |
## Incassate questo mese

Riepilogo: fatturato €… · da incassare €… · scaduto €… · DSO {n}gg ({trend})
```

## Destinazione
Report in chat + `finance/fatturazione.md` aggiornato.
Commit (admin): `[finance] fatture: status {YYYY-MM-DD}`.

## Handoff
Scadute 30+gg → sollecito (APPROVE) + `sales` · pattern ritardi di un partner → `delivery`
(segnale health) · impatto cassa → `/finance cashflow`.
