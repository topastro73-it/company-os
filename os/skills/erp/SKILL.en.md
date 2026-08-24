# ERP Integration Skill

Bidirectional integration with the ERP system via MCP Server and REST API.
Allows reading, writing and syncing financial data, CRM, invoices, contracts and KPIs.

> **Boundary with `financial-import`**: this skill is the *pipe* for **live data**
> (sync via API). To interpret a **static JSON export** (MRR/burn/runway methodology + company-specific
> rules) when the API is unavailable, use `os/skills/financial-import/SKILL.md`. They do not overlap.

## Access modes

### Option 1 — ERP MCP Server (recommended)

Custom MCP server hosted on GitHub, executed via `npx tsx`.
Configuration declared in `config/integrations.yaml` (`erp` section, variable names only — never values):

```json
{
  "company": {
    "command": "npx",
    "args": ["tsx", "https://github.com/<your-org>/<erp-mcp-repo>"],
    "env": {
      "DB_FILE_PATH": "${ERP_DB_URL}"
    }
  }
}
```

**Prerequisites**: Node.js 18+ and `npx` available in the PATH.
The database is loaded from the Google Drive file linked in `DB_FILE_PATH`.

When the MCP is active, agents can query the ERP directly without intermediate Python scripts.

### Option 2 — Sync script (fallback)

If the MCP is unavailable, use the Python script: `scripts/erp_sync.py`
Requires: `ERP_API_URL` and optionally `ERP_AUTH_TOKEN` as env vars.

## When to use this skill

- When live financial data access is needed (not from the static JSON)
- To sync invoices, cashflow, KPIs from the ERP
- To write/update records on the ERP (upsert, bulk)
- To take snapshots/backups of ERP data

## API Reference

**Base URL**: configured in `ERP_API_URL` (env var) or exposed by the ERP MCP server
**Auth**: optional via `ERP_AUTH_TOKEN` (Bearer token)

### Available entities

| Entity | Primary key | Description |
|--------|----------------|-------------|
| `financials` | `id` | P&L transactions (heart of the system) |
| `deals` | `id` | CRM opportunities |
| `accounts` | `id` | CRM companies |
| `contacts` | `id` | CRM contacts |
| `orders` | `id` | Supplier orders |
| `users` | `id` | Users |
| `contracts` | `id` | Contracts |
| `invoices` | `id` | Invoices |
| `payments` | `id` | Invoice payments |
| `funding_rounds` | `id` | Funding rounds |
| `settings` | `key` | Settings and KPIs |
| `cash_balances` | `month` (YYYY-MM) | Monthly cash balances |

### Endpoints

| Action | Method | URL | Notes |
|--------|--------|-----|------|
| Read all | `GET` | `/api/:store` | JSON array |
| Read one | `GET` | `/api/:store/:id` | JSON object |
| Create/Update | `POST` | `/api/:store` | Upsert (must have `id`) |
| Bulk upsert | `POST` | `/api/:store/bulk` | Array of objects |
| Delete one | `DELETE` | `/api/:store/:id` | `{"success": true}` |
| Bulk delete | `POST` | `/api/:store/bulk-delete` | `{"ids": [...]}` |
| Clear entity | `DELETE` | `/api/:store` | ⚠️ Deletes EVERYTHING |

### Technical notes

- **Dates**: ISO 8601 format (e.g. `2026-03-23T08:45:10.000Z`)
- **Values**: always net (taxable base) in the main fields (`netAmount`, `plannedValue`). Gross is calculated by adding `taxRate` or `tax`
- **Content-Type**: `application/json` for all POST/PUT requests

## Commands

| Command | Description | Output |
|---------|------------|--------|
| `sync-all` | Syncs everything: invoices, cashflow, KPIs | Markdown files in `company/` |
| `sync-invoices` | Syncs invoices from the ERP | `vault/finance/fatturazione-erp.md` |
| `sync-cashflow` | Syncs cash balances from the ERP | `vault/finance/cashflow-erp.md` |
| `sync-kpis` | Calculates KPIs from ERP financials | `company/direzione/metrics/kpis-erp.md` |
| `pull` | Downloads entities as JSON | `vault/finance/erp-data/*.json` |
| `snapshot` | Full backup of all entities | `vault/finance/erp-data/snapshot-YYYY-MM-DD.json` |
| `push` | Uploads JSON to an ERP entity | Upsert on the ERP |

---

## Command: sync-all

### Trigger
"sync ERP", "update data from ERP", "ERP sync"

### Process

1. Run `python3 scripts/erp_sync.py sync-all`
2. Verify that the 3 files were generated
3. Commit: `[finance] sync: ERP data update — invoices, cashflow, KPIs`

### Output
- `vault/finance/fatturazione-erp.md`
- `vault/finance/cashflow-erp.md`
- `company/direzione/metrics/kpis-erp.md`

---

## Command: sync-invoices

### Trigger
"sync ERP invoices", "invoices from ERP"

### Process
1. Run `python3 scripts/erp_sync.py sync-invoices`
2. The file includes: paid invoices (with payment method), invoices to be collected (with aging)

### Output
- `vault/finance/fatturazione-erp.md`

---

## Command: sync-cashflow

### Trigger
"sync ERP cashflow", "ERP balances"

### Process
1. Run `python3 scripts/erp_sync.py sync-cashflow`
2. The file includes: monthly balances in chronological order

### Output
- `vault/finance/cashflow-erp.md`

---

## Command: sync-kpis

### Trigger
"KPIs from ERP", "ERP dashboard"

### Process
1. Run `python3 scripts/erp_sync.py sync-kpis`
2. The file includes: MRR/ARR, revenue, costs by category, burn rate, runway, pipeline, active contracts, target vs actual

### Output
- `company/direzione/metrics/kpis-erp.md`

---

## Command: pull

### Trigger
"download ERP data", "pull ERP"

### Process
1. Run `python3 scripts/erp_sync.py pull [entity1 entity2 ...]`
2. If no entity is specified, downloads all of them
3. Saves as JSON in `vault/finance/erp-data/`

---

## Command: snapshot

### Trigger
"ERP backup", "ERP snapshot"

### Process
1. Run `python3 scripts/erp_sync.py snapshot`
2. Generates a complete JSON file with timestamp

### Output
- `vault/finance/erp-data/snapshot-YYYY-MM-DD.json`

---

## Command: push

### Trigger
"upload to ERP", "push ERP", "update ERP"

### Process
1. Run `python3 scripts/erp_sync.py push ENTITY FILE`
2. Supports both single record and array (bulk)

### Guardrails
- ⚠️ **NEVER** use the `clear` command (empties an entity) without explicit CEO confirmation
- ⚠️ **NEVER** push data without prior verification (show a preview first)
- ⚠️ **NEVER** overwrite production data with demo/test data

---

## Integration with other skills

| Skill | How it integrates |
|-------|----------------|
| **Financial Import** | ERP is the live source; Financial Import handles the static JSON as fallback |
| **Fatture in Cloud** | FIC is the Italian electronic invoicing system; ERP is the aggregated management system |
| **Qonto** | Qonto is the bank account; ERP aggregates balances in `cash_balances` |
| **Data & Metrics** | KPIs calculated from ERP feed the metrics dashboard |
| **Admin & Controllo** | The ERP provides the base data for management control |

## Data model: financials[]

The `financials` record is the heart of the system. Main fields:

| Field | Type | Description |
|-------|------|-------------|
| `treatment` | string | `Cost` or `Recurring Revenue` or `Project-based` |
| `pnl` | string | P&L category (`COGS`, `R&D`, `S&M`, `G&A`, `Subscription Revenue`, etc.) |
| `status` | string | `Pipeline`, `Unpaid`, `Paid`, `Lost` |
| `frequency` | int | Service duration in months (1=monthly, 12=annual) |
| `plannedValue` | number | Forecast (positive=revenue, negative=cost) |
| `bookingValue` | number | Contracted |
| `actualValue` | number | Actual (cash) |
| `mrr` | number | The record's MRR (if subscription) |
| `tax` | number | VAT % (22 = 22%) |
| `resource` | string | Client/vendor name |
