# Qonto Command: reconcile

Cross-matches Qonto transactions with FIC invoices to identify collected invoices and unreconciled payments.

## Authorized agents

CFO, CEO, Chief of Staff

## Invocation

```
/finance qonto reconcile
/finance qonto reconcile 2026-03   # specific month
```

## Prerequisites

Run first:
- `/finance fatture-in-cloud sync-invoices` (to have up-to-date invoices)
- `/finance qonto sync-transactions` (to have up-to-date transactions)

## Process

### Step 1 — Load data

1. Read `vault/finance/fatturazione.md` → invoice list with status and amount
2. Run `python3 scripts/qonto_sync.py transactions --month YYYY-MM` → bank transactions

### Step 2 — Automatic matching

For each Qonto inflow (`side = credit`), look for a matching FIC invoice:

**Match criteria** (in order of priority):
1. **Exact amount** — `transaction.amount == invoice.gross_amount`
2. **Amount + counterparty** — amount matches and `counterparty_name` contains the client name
3. **Invoice reference** — `transaction.reference` contains the invoice number

**Tolerance threshold**: ±€1 (for bank rounding)

### Step 3 — Generate reconciliation report

```markdown
## Reconciliation YYYY-MM

### Matched invoices (collected)
| Invoice | Client | Amount | Qonto collection date | Match type |
|---------|---------|---------|-------------------|------------|
| 8/2026 | Acme | €12.000 | 2026-03-01 | Exact amount |

### Overdue invoices NOT found in Qonto
| Invoice | Client | Amount | Due date | Days |
|---------|---------|---------|----------|--------|
| ... | ... | ... | ... | ... |

### Qonto inflows NOT matched to invoices
| Date | Counterparty | Amount | Reference |
|------|-------------|---------|-------------|
| ... | ... | ... | ... |
```

### Step 4 — Update statuses

For matched invoices:
- Update `fatturazione.md`: status → ✅ Collected, collection date
- Recompute aging analysis
- Update overdue receivables in `kpis.md`

### Step 5 — Commit

```bash
git add vault/finance/fatturazione.md company/direzione/metrics/kpis.md
git commit -m "[finance] qonto: reconciliation YYYY-MM — N invoices matched, €X collected"
```

## Guardrails

- NEVER mark an invoice as collected without a Qonto match — only suggest
- If the match is ambiguous (multiple invoices with the same amount), ask the CEO/CFO for confirmation
- ALWAYS show unmatched inflows — they could be advances, credit notes, or errors
