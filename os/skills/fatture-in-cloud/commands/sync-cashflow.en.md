# FIC Command: sync-cashflow

Reads the cash journal (prima nota) from Fatture in Cloud and updates `vault/finance/cashflow.md`.

## Authorized agents

CFO, CEO, Chief of Staff

## Invocation

```
/finance fatture-in-cloud sync-cashflow
/finance fatture-in-cloud sync-cashflow 2026-03   # specific month
```

## Process

### Step 1 — Read the cash journal via script

```bash
python3 scripts/fic_sync.py cashflow --month 2026-03
```

The script calls:

```
GET /c/{company_id}/cashbook
  ?date_from=2026-03-01
  &date_to=2026-03-31
  &kind=all
```

Each cash journal record has:
- `date` → transaction date
- `description` → description
- `kind` → `cashbook_in` (inflow) | `cashbook_out` (outflow)
- `amount_in` → inflow amount
- `amount_out` → outflow amount
- `entity_name` → counterparty (if linked)
- `document.id` / `document.type` → linked document (invoice, expense report, etc.)

### Step 2 — Compute account balance

Sum all inflows and outflows up to today to get the current balance.
Update `## Saldo corrente` in `vault/finance/cashflow.md`:

```markdown
| Main current account | €XXX.XXX | 2026-03-23 |
```

### Step 3 — Update expected inflows

From the `not_paid` invoice list (already obtained via `sync-invoices`), populate:

```markdown
### Issued invoices awaiting collection
| Invoice No. | Client | Amount | Due date | Collection probability |
| 5/2026 | Acme | €4.167 | 2026-02-01 | High (51d, active client) |
```

Automatic probability based on aging:
- 0–30d → High
- 31–60d → Medium
- 61–90d → Low
- 90+d → Critical

### Step 4 — Weekly projection

Compute the projected balance week by week for the next 12 weeks:
- Expected inflows: invoices due per week (from FIC) + recurring MRR (from kpis.md)
- Expected outflows: fixed outflows from `cashflow.md` + tax deadlines from `scadenzario.md`

Update the `## Proiezione settimanale` table.

### Step 5 — Commit

```bash
git add vault/finance/cashflow.md
git commit -m "[cfo] fatture-in-cloud: sync cashflow YYYY-MM-DD — balance €X, 12-week projection"
```

## Notes

- The FIC balance only reflects transactions entered in the cash journal — verify against the bank statement
- Bank transactions not reconciled in FIC do not appear — reconcile before syncing
- If `amount_in` and `amount_out` are both 0 on a record, it is an internal transfer — ignore it
