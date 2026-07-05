# Financial Import Skill

**Boundary with the `erp` skill (delimited in the 2026-07-03 audit):**
- **`erp`** = *pipe* for syncing **live data** via ERP API (`scripts/erp_sync.py sync-*`) →
  updates `vault/finance/*` and `company/direzione/metrics/kpis.md`. Use it when `ERP_API_URL` is configured.
- **`financial-import`** (this one) = *methodology* for parsing and analyzing a **static JSON export**
  (`Company_PRODUCTION.json`) when the API is unavailable: data dictionary, MRR/burn/backlog/runway
  formulas and **company-specific rules** (compensation periodicity, clients with
  unusual periodicity, grants, bank loans). This domain knowledge is **not** duplicated in `erp`.

In short: `erp` brings the numbers (live), `financial-import` knows how to **interpret** them (from export). They do not overlap.

Import and analysis of financial data. Supports two modes:
1. **ERP API** (preferred) — live data via `os/skills/erp/SKILL.md` and `scripts/erp_sync.py`
2. **JSON file** (fallback) — static export `Company_PRODUCTION.json`

Used by CFO, CEO, Chief of Staff.

## When to use this skill

- **If the ERP API is available** (`ERP_API_URL` configured): use `python3 scripts/erp_sync.py sync-all` for live data. See `os/skills/erp/SKILL.md` for details.
- **If the CEO provides a JSON file** of a financial export: use the manual process described below.

## Commands

| Command | Description | Output |
|---------|------------|--------|
| `import-financials` | Imports financial JSON, analyzes, updates KPIs | Updates `company/direzione/metrics/kpis.md` + report |

---

## Command: import-financials

### Trigger
When the CEO provides a financial export JSON file, or says "update the financial data", "import the numbers", or similar.

### Input
- JSON file attached by the user (the company's export format)

### Process

#### Step 1 — Parsing the JSON

The JSON has this top-level structure:

```
{
  "version", "timestamp", "settings",
  "financials",      // Main array — the HEART of the data
  "deals",           // CRM pipeline
  "accounts",        // Client/prospect companies
  "contacts",        // Natural persons
  "orders",          // Orders to suppliers
  "users",           // System users
  "contracts",       // Active contracts
  "invoices",        // Issued invoices
  "payments",        // Payments received
  "funding_rounds",  // Investment rounds
  "cash_balances"    // Cash balance per month
}
```

#### Step 2 — Data Dictionary (how to interpret the data)

##### The financial engine: `financials[]`

Each record has **3 value levels**:
- `plannedValue` — Forecast/budget (positive = revenue, negative = cost)
- `bookingValue` — Ordered/invoiced (contracted)
- `actualValue` — Cash (actually collected/paid)

**Key dates**:
- `bookingDate` — Contract / order signing date
- `plannedCashInDate` — Expected payment due date
- `actualCashInDate` — Actual collection/payment date
- `competenceDate` — Service accrual start date (FUNDAMENTAL for MRR)

**Classification**:
- `status`: `Pipeline` | `Unpaid` | `Paid` | `Lost`
- `pnl`: P&L category (`Subscription Revenue`, `COGS`, `R&D`, `S&M`, `G&A`, etc.)
- `capexOpex`: `CAPEX` | `OPEX`
- `frequency`: Service duration in months (1 = monthly, 12 = annual)
- `resource`: Client/supplier name

##### MRR calculation

1. Take `financials[]` where `status` is NOT `Pipeline` or `Lost`
2. Filter where `pnl` contains "Subscription"
3. For each record, compute `endDate = competenceDate + frequency` (months)
4. If the month under analysis falls between `competenceDate` and `endDate`, the record generates MRR
5. MRR value: use the `mrr` field if present, otherwise `bookingValue / frequency`

##### Receivables calculation

`bookingValue - actualValue` for each revenue record with `status = Unpaid`

##### Burn rate calculation

Filter `financials[]` where `plannedValue < 0`, group by month (`actualMonth`, `actualYear`)

##### Backlog calculation (contracted but not yet invoiced)

`contracts[].totalAmount` - sum of `invoices[]` linked via `contractId`

#### Step 3 — Company-specific rules

**CRITICAL — Compensation periodicity**:
- **Only some people** have a monthly salary (identify them in the financials via the `resource` field)
- Other compensations (e.g. CEO, CTO, contractors) are often quarterly or per-project
- For the average burn rate: annualize each person based on the actual payment frequency, do NOT assume everyone is monthly
- Identify the periodicity by looking at the `frequency` field and the distance between successive `competenceDate` values for the same `resource`

**Clients without a contract — Non-contracted revenue**:
- Some clients generate variable monthly revenue but may not have a `contract` in the system
- Look for it in `financials[]` filtering by the client's `resource`
- Add it separately to the adjusted MRR

**Grants and pass-through**:
- Grants (pnl contains "Grant") are NOT operating revenue
- Watch out for consortium pass-through costs (pnl = "Consortium pass-through") — they are costs tied to grant disbursement
- Always compute each grant's net impact: `grant collected - associated consortium costs`

**Bank loans**:
- Bank loans (pnl contains "Mortgage" or "Funding") are NOT revenue
- Installments are recurring financial costs

#### Step 3b — Pipeline from HubSpot (NOT from the JSON)

**Operational choice** (see `decisions/`): the sales pipeline is read from **HubSpot CRM** (via the `search_crm_objects` MCP tool), NOT from the JSON. The JSON has stale and incomplete pipeline data.

To read the pipeline:
1. Call `get_user_details` to verify access
2. Call `search_crm_objects` with objectType `DEAL`, properties `["dealname", "amount", "dealstage", "pipeline", "hs_deal_stage_probability", "closedate", "hubspot_owner_id"]`, sort by amount DESC, limit 200
3. Call `get_properties` for objectType `DEAL`, propertyNames `["dealstage"]` to obtain the stage ID → label mapping
4. Call `search_owners` to map owner ID → name

**HubSpot stage mapping** (the actual stage IDs are in `config/integrations.yaml`; here is the logical mapping):
- `<stage-id>` = Discovery & Qualification (prob. 20%)
- `<stage-id>` = Technical Alignment (prob. 30%)
- `<stage-id>` = Proposal Sent (prob. 40%)
- `<stage-id>` = Negotiation & Verbal Agreement (prob. 60%)
- `<stage-id>` = Contract Sent (prob. 80%)
- `<stage-id>` = Won (prob. 100%)
- `<stage-id>` = Lost (prob. 0%)

**Warning**: many deals in Discovery have amount = €1 (placeholder). Filter them out or flag them as "value TBD" in the analysis.

#### Step 4 — Analyses to produce

1. **P&L per quarter** — Operating revenue vs costs, by pnl category (from JSON)
2. **MRR and ARR** — From active contracts, with breakdown by client (from JSON)
3. **Burn rate** — Fixed monthly costs + variable quarterly costs (monthly average) (from JSON)
4. **Monthly cash flow** — Inflows vs outflows, per month, trend (from JSON)
5. **Receivables aging** — Amount, due date, days overdue, per client (from JSON)
6. **Unit economics** — ARPU, average/median ACV, client segmentation (from JSON)
7. **Pipeline** — Deals per stage, weighted value, owner, recent deals (**from HubSpot**)
8. **Revenue concentration** — Top clients, HHI index, cumulative % (from JSON)
9. **Grant status** — Collected vs pipeline, net impact after pass-through (from JSON)
10. **Runway** — 3 scenarios (base 5% growth, optimistic 8%, pessimistic 2% + churn) (from JSON + HubSpot pipeline)

#### Step 5 — Output

1. Update `company/direzione/metrics/kpis.md` with the actual numbers
2. Save the full report in `vault/finance/reports/burn-analysis-{YYYY-MM-DD}.md`
3. Commit: `[cfo] analysis: financial import and burn analysis from production export`

### Guardrails

- NEVER treat quarterly compensations as if they were monthly
- NEVER count bank loans as revenue
- NEVER count gross grants as liquidity — always compute the net after pass-through
- ALWAYS present 3 scenarios (base, optimistic, pessimistic)
- ALWAYS state the assumptions behind every projection
- ALWAYS flag overdue receivables with aging > 30 days as a risk
