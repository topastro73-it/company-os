# FIC Command: aging-report

Computes the aging of overdue receivables from Fatture in Cloud and updates `company/direzione/metrics/kpis.md`.

## Authorized agents

CFO, CEO, Chief of Staff

## Invocation

```
/finance fatture-in-cloud aging-report
```

## Process

### Step 1 — Run aging via script

```bash
python3 scripts/fic_sync.py aging
```

The script fetches all invoices with `payment_status != paid` from the last 24 months
and computes for each one the days overdue: `today - due_date`.

### Step 2 — Generate aging table

For each overdue invoice (days > 0):

| Client | Invoice No. | Amount | Due date | Days overdue | Bucket |
|---------|-----------|---------|----------|---------------|--------|
| Acme Srl | 5/2026 | €4,167 | 2026-02-01 | 51d | 31–60 |
| Beta Spa | 3/2026 | €10,290 | 2025-12-31 | 83d | 61–90 |
| Gamma Srl | 12/2025 | €5,000 | 2025-10-02 | 172d | 90+ |

Bucket:
- `0–30d` — monitoring
- `31–60d` — first payment reminder
- `61–90d` — second reminder + CEO alert
- `90+d` — legal escalation / write-off

### Step 3 — Update kpis.md

In the `## Financial` section of `company/direzione/metrics/kpis.md`, update the row:

```
| Overdue receivables | €XX.XXX | ⚠️ |
```

And update the detail comment with the list by client and days:

```markdown
> **Overdue receivables (€XX.XXX)**: Client A €X.XXX (Nd), Client B €X.XXX (Nd), ...
```

### Step 4 — Alert to CEO Routine

If there are receivables in the 90+ days bucket, add a line in `company/direzione/ceo-cadence.md`
in the answers Log section with an alert:

```
- ⚠️ RECEIVABLES 90+d: [client] €[amount] ([Nd]) — requires decision (legal reminder / write-off)
```

### Step 5 — Commit

```bash
git add vault/finance/fatturazione.md company/direzione/metrics/kpis.md company/direzione/ceo-cadence.md
git commit -m "[cfo] fatture-in-cloud: aging report YYYY-MM-DD — €X overdue, N invoices"
```

## Action thresholds

| Bucket | Automatic action |
|--------|-----------------|
| 31–60d | Note in the cadence log |
| 61–90d | CEO alert in the next daily briefing |
| 90+d | Urgent in the daily briefing + options A/B/C (legal reminder / settlement / write-off) |
| >€50,000 total overdue | Flag in the Financial section of the weekly digest |
