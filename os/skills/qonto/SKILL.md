# Qonto Skill

Integrazione con Qonto (banca online) via API v2.
Sincronizza saldi, movimenti bancari e riconcilia con i dati fatturazione.
Usata da CFO, CEO, Chief of Staff.

## Prerequisiti

Credenziali memorizzate in **macOS Keychain** (encrypted, mai nel repo).

**Setup one-time** (eseguire manualmente, una sola volta per macchina):

```bash
security add-generic-password -a "qonto" -s "QONTO_LOGIN"  -w "<qonto-login>" -U
security add-generic-password -a "qonto" -s "QONTO_SECRET" -w "<secret-da-qonto>" -U
```

La secret key si recupera da Qonto → Integrazioni → API key.

Script: `scripts/integrations/bank-qonto.sh` (wrapper) → `scripts/integrations/bank_qonto_sync.py`
Dipendenze: **nessuna**, solo standard library. Sono esempi funzionanti inclusi nel template
(`scripts/integrations/README.md`): se usi Qonto funzionano così come sono, altrimenti sono un
modello da adattare alla tua banca.

Il wrapper bash legge le credenziali dal Keychain ed esporta le env vars al
processo Python. Niente credenziali in chiaro nel repo: i nomi delle variabili sono censiti in `config/integrations.yaml`.

## Comandi

| Comando | Descrizione | Output |
|---------|------------|--------|
| `sync-balance` | Legge saldi conti Qonto | Aggiorna `vault/finance/cashflow.md` sezione saldi |
| `sync-transactions` | Scarica movimenti del mese | Report movimenti + aggiorna cashflow |
| `reconcile` | Incrocia movimenti con le fatture | Identifica fatture incassate / pagamenti non riconciliati |

> ⚠️ `reconcile` è un comando **dell'agente**, non dello script: l'incrocio lo fa l'agente leggendo
> movimenti e fatture. Lo script di esempio espone solo `balance` e `transactions`.

## Agenti autorizzati

Finance (owner), CEO, Chief of Staff

## Flusso standard

Comando wrapper (legge Keychain automaticamente):

```bash
bash scripts/integrations/bank-qonto.sh balance                    # saldi conti
bash scripts/integrations/bank-qonto.sh transactions --month 2026-04
```

Invocazione agente:
```
/finance qonto sync-balance           # ogni lunedi — aggiorna saldo in cashflow.md
/finance qonto sync-transactions      # ogni lunedi — scarica movimenti mese
/finance qonto reconcile              # dopo sync-invoices FIC — incrocia fatture con incassi
```

## Note API

- Base URL: `https://thirdparty.qonto.com/v2`
- Auth: `Authorization: {login}:{secret}` (NO base64)
- Rate limit: 1.000 req/10s, 10.000 req/10min
- Pagination: `limit` + `offset`, max 10.000 risultati per query
- Conti: Conto principale (main) + Marketing
