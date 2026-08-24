# FIC Command: sync-invoices

Syncs invoices issued from Fatture in Cloud and updates `vault/finance/fatturazione.md`.

## Authorized agents

CFO, CEO, Chief of Staff

## Invocation

```
/finance fatture-in-cloud sync-invoices
/finance fatture-in-cloud sync-invoices 2026      # specific year
/finance fatture-in-cloud sync-invoices 2026-01   # specific month
```

## Process

### Step 1 — Run the sync via script

```bash
python3 scripts/fic_sync.py invoices --year 2026
```

The script calls:

```
GET /c/{company_id}/issued_documents
  ?type=invoice
  &date_from=2026-01-01
  &date_to=2026-12-31
  &per_page=50
  &page=1
```

It paginates automatically until it has all documents.

For each invoice it extracts:
- `number` + `number_suffix` → invoice number
- `date` → issue date
- `entity.name` → client
- `subject` → description
- `amount_net` → taxable amount
- `amount_vat` → VAT
- `gross_amount` → gross total
- `payment_status` → `not_paid` | `partial` | `paid`
- `due_date` → due date (from `payments_list[].due_date` if missing in the document)
- Actual collection date from `payments_list[]` where `status = paid`

### Step 2 — Update fatturazione.md

Rewrite the `## Fatture emesse {anno}` table in `vault/finance/fatturazione.md`:

```markdown
| No. | Issue date | Client | Description | Taxable | VAT | Total | Due date | Status | Collected on |
|----|----------------|---------|-------------|-----------|-----|--------|----------|-------|-------------|
| 1/2026 | 2026-01-15 | Acme | Jan fee | €8.197 | €1.803 | €10.000 | 2026-02-14 | ✅ Collected | 2026-02-10 |
| 2/2026 | 2026-01-31 | Beta | Jan fee | €3.415 | €751 | €4.167 | 2026-03-01 | ⚠️ Overdue | — |
```

Mapping `payment_status` → icon:
| FIC status | Icon |
|-----------|-------|
| `paid` | ✅ Collected |
| `not_paid` + future due date | ⏳ Pending |
| `not_paid` + past due date | ⚠️ Overdue |
| `partial` | 🔶 Partial |

### Step 3 — Update monthly summary

Populate the `## Riepilogo mensile {anno}` table:
- `Invoiced` = sum of `gross_amount` per month
- `Collected` = sum of `gross_amount` where `payment_status = paid`, by collection month
- `Overdue` = sum of `gross_amount` where `not_paid` and `due_date` in the past
- `DSO` = average days between issue and collection (paid invoices only)

### Step 4 — Update aging

Populate `## Aging Analysis`:
- 0–30 days: `due_date` between today and -30d, `not_paid`
- 31–60 days: `due_date` between -31 and -60d, `not_paid`
- 61–90 days: `due_date` between -61 and -90d, `not_paid`
- 90+ days: `due_date` beyond -90d, `not_paid`

### Step 5 — Commit

```bash
git add vault/finance/fatturazione.md
git commit -m "[finance] fatture-in-cloud: sync invoices YYYY-MM-DD — N invoices, €X invoiced"
```

## Guardrails

- NEVER delete invoices already present in the file — only update and append
- If `gross_amount` is negative → it is a credit note, mark it with `NC` in the number
- Invoices with `payment_status = partial`: show the remaining amount in the Notes column
- If the script fails due to missing credentials, stop and ask for `FIC_ACCESS_TOKEN`
