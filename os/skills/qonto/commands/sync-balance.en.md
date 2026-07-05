# Qonto Command: sync-balance

Reads the current balances of the Qonto accounts and updates `vault/finance/cashflow.md`.

## Authorized agents

CFO, CEO, Chief of Staff

## Invocation

```
/finance qonto sync-balance
```

## Process

### Step 1 — Read balances via script

```bash
python3 scripts/qonto_sync.py balance
```

The script calls `GET /v2/organization` and extracts for each `bank_accounts[]`:
- `name` → account name
- `iban` → IBAN
- `balance` → current balance
- `authorized_balance` → authorized balance (net of pending operations)
- `updated_at` → last update date

### Step 2 — Update cashflow.md

Rewrite the `## Saldo corrente` section:

```markdown
| Account | Balance | Verification date |
|-------|-------|---------------|
| Main account (Qonto) | €X.XXX,XX | 2026-03-23 |
| Marketing (Qonto) | €XXX,XX | 2026-03-23 |
| **Total available** | **€X.XXX,XX** | |
```

### Step 3 — Update KPIs

If the total balance differs significantly from the "Estimated cash" in `company/direzione/metrics/kpis.md`, update the value.

### Step 4 — Commit

```bash
git add vault/finance/cashflow.md
git commit -m "[cfo] qonto: sync balances — €X.XXX total available"
```

## Notes

- The Qonto balance reflects booked transactions, not operations awaiting settlement
- Qonto is not the only account — check whether there are other bank accounts (e.g. BPM) not on Qonto
