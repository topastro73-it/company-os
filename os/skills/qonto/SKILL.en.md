# Qonto Skill

Integration with Qonto (online bank) via API v2.
Syncs balances and bank transactions, and reconciles them with invoicing data.
Used by Finance, CEO, Chief of Staff.

## Prerequisites

Credentials stored in **macOS Keychain** (encrypted, never in the repo).

**One-time setup** (run manually, once per machine):

```bash
security add-generic-password -a "qonto" -s "QONTO_LOGIN"  -w "<qonto-login>" -U
security add-generic-password -a "qonto" -s "QONTO_SECRET" -w "<secret-da-qonto>" -U
```

The secret key can be retrieved from Qonto → Integrations → API key.

Scripts: `scripts/integrations/bank-qonto.sh` (wrapper) → `scripts/integrations/bank_qonto_sync.py`
Dependencies: **none**, standard library only. These are working examples shipped with the template
(`scripts/integrations/README.md`): if you use Qonto they work as they are, otherwise they are a
model to adapt to your own bank.

The bash wrapper reads the credentials from the Keychain and exports the env vars to the
Python process. No plaintext credentials in the repo: the variable names are catalogued in `config/integrations.yaml`.

## Commands

| Command | Description | Output |
|---------|------------|--------|
| `sync-balance` | Reads Qonto account balances | Updates `vault/finance/cashflow.md` balances section |
| `sync-transactions` | Downloads the month's transactions | Transactions report + updates cashflow |
| `reconcile` | Cross-matches transactions with invoices | Identifies collected invoices / unreconciled payments |

> ⚠️ `reconcile` is an **agent** command, not a script one: the agent does the matching by reading
> transactions and invoices. The example script only exposes `balance` and `transactions`.

## Authorized agents

Finance (owner), CEO, Chief of Staff

## Standard flow

Wrapper command (reads Keychain automatically):

```bash
bash scripts/integrations/bank-qonto.sh balance                    # account balances
bash scripts/integrations/bank-qonto.sh transactions --month 2026-04
```

Agent invocation:
```
/finance qonto sync-balance           # every Monday — updates balance in cashflow.md
/finance qonto sync-transactions      # every Monday — downloads the month's transactions
/finance qonto reconcile              # after FIC sync-invoices — matches invoices with collections
```

## API notes

- Base URL: `https://thirdparty.qonto.com/v2`
- Auth: `Authorization: {login}:{secret}` (NO base64)
- Rate limit: 1,000 req/10s, 10,000 req/10min
- Pagination: `limit` + `offset`, max 10,000 results per query
- Accounts: Main account (main) + Marketing
