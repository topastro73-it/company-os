# Qonto Skill

Integration with Qonto (online bank) via API v2.
Syncs balances and bank transactions, and reconciles them with invoicing data.
Used by CFO, CEO, Chief of Staff.

## Prerequisites

Credentials stored in **macOS Keychain** (encrypted, never in the repo).

**One-time setup** (run manually, once per machine):

```bash
security add-generic-password -a "qonto" -s "QONTO_LOGIN"  -w "<qonto-login>" -U
security add-generic-password -a "qonto" -s "QONTO_SECRET" -w "<secret-da-qonto>" -U
```

The secret key can be retrieved from Qonto → Integrations → API key.

Scripts: `scripts/qonto.sh` (wrapper) → `scripts/qonto_sync.py` (Python)
Dependencies: `pip3 install requests`

The bash wrapper reads the credentials from the Keychain and exports the env vars to the
Python process. No plaintext credentials in the repo: the variable names are catalogued in `config/integrations.yaml`.

## Commands

| Command | Description | Output |
|---------|------------|--------|
| `sync-balance` | Reads Qonto account balances | Updates `vault/finance/cashflow.md` balances section |
| `sync-transactions` | Downloads the month's transactions | Transactions report + updates cashflow |
| `reconcile` | Cross-matches Qonto transactions with FIC invoices | Identifies collected invoices / unreconciled payments |

## Authorized agents

CFO (owner), CEO, Chief of Staff

## Standard flow

Wrapper command (reads Keychain automatically):

```bash
bash scripts/qonto.sh balance                    # account balances
bash scripts/qonto.sh transactions --month 2026-04
bash scripts/qonto.sh reconcile --month 2026-04
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
