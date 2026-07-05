# Qonto Command: sync-transactions

Downloads the month's bank transactions from Qonto and produces a report.

## Authorized agents

CFO, CEO, Chief of Staff

## Invocation

```
/finance qonto sync-transactions
/finance qonto sync-transactions 2026-03   # specific month
```

## Process

### Step 1 — Download transactions via script

```bash
python3 scripts/qonto_sync.py transactions --month 2026-03
```

The script calls `GET /v2/transactions` with:
- the bank account `slug` (from organization)
- `settled_at_from` / `settled_at_to` for the period
- Automatic pagination (`limit=100`, `offset`)

For each transaction it extracts:
- `settled_at` → booking date
- `emitted_at` → operation date
- `side` → `credit` (inflow) or `debit` (outflow)
- `amount` → amount
- `currency` → currency
- `label` → description/reason
- `counterparty_name` → counterparty (sender or recipient)
- `reference` → reference (useful for invoice matching)
- `category` → Qonto category
- `status` → `completed`, `pending`, `declined`

### Step 2 — Generate report

Output as structured JSON + summary:

```
Inflows:   €X.XXX (N transactions)
Outflows:  €X.XXX (N transactions)
Net:       €X.XXX
```

Top 5 inflows and top 5 outflows by amount.

### Step 3 — Update cashflow.md

Populate the `## Proiezione settimanale` section with actual data for past weeks and projections for future ones.

### Step 4 — Commit

```bash
git add vault/finance/cashflow.md
git commit -m "[cfo] qonto: sync transactions YYYY-MM — €X inflows, €Y outflows"
```
