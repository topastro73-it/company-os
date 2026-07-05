# Fatture in Cloud Skill

Integration with Fatture in Cloud (TeamSystem) via REST API v2.
Syncs issued invoices, payments and cashflow into the repo.
Used by CFO, CEO, Chief of Staff.

## Authentication — Personal Access Token (no browser)

FIC supports **personal access tokens** generated directly from the settings — no OAuth2, no browser flow.

**How to generate the token (one time only)**:
1. FIC → **Settings → Developer → Access tokens**
2. Create a new token with scopes: `issued_documents`, `entity.clients`, `entity.suppliers`, `products`, `settings`
3. Copy the token and add it to `~/.zshrc`:
   ```bash
   export FIC_ACCESS_TOKEN="your-token"
   export FIC_COMPANY_ID="<fic-company-id>"
   ```
4. `source ~/.zshrc` and restart Claude Code → the MCP starts automatically

**The token is stable** (it does not expire like OAuth2) — no re-authentication needed.

---

## Access modes

### Option 1 — MCP Server (recommended)

Custom MCP server in `mcp-servers/fattureincloud-mcp/server.py`.
Provides read **and write** tools directly accessible by agents.

**Setup** (variable names declared in `config/integrations.yaml`, `fatture_in_cloud` section; values only in local env):
```bash
# ~/.zshrc
export FIC_ACCESS_TOKEN="your-personal-token"
export FIC_COMPANY_ID="<fic-company-id>"
```

**Available MCP tools**:

| Tool | Type | Description |
|------|------|------------|
| `fic_list_companies` | read | List accessible companies |
| `fic_get_company_info` | read | Company info (name, VAT number (P.IVA), address) |
| `fic_list_invoices` | read | Issued invoices with filters by type, year, SQL-like query |
| `fic_get_invoice` | read | Single invoice detail with line items and payments |
| `fic_list_clients` | read | Client records |
| `fic_list_suppliers` | read | Supplier records |
| `fic_list_products` | read | Products and services |
| `fic_list_received_documents` | read | Received invoices / expenses |
| `fic_list_payment_accounts` | read | Payment accounts |
| `fic_list_payment_methods` | read | Payment methods |
| `fic_list_vat_types` | read | VAT rates (with IDs needed to create invoices) |
| `fic_get_tax_profile` | read | Tax profile |
| `fic_create_invoice` | **write** | Create a draft or issued invoice |

All tools support `markdown` (default) or `json` output.

### Workflow: create an invoice via MCP

```
1. fic_list_clients → find the client's entity_id
2. fic_list_vat_types → verify the VAT rate id (e.g. 22%)
3. fic_create_invoice(entity_id=..., date="YYYY-MM-DD", items=[...], is_draft=True)
4. Verify the draft in FIC → is_draft=False to issue
```

### Option 2 — Sync script (legacy)

Python script: `scripts/fic_sync.py`
Dependencies: `pip3 install requests python-dateutil`

## Prerequisites

Required environment variables:

```bash
FIC_ACCESS_TOKEN=<bearer token from FIC → Settings → API (OAuth2)>
FIC_COMPANY_ID=<company ID — visible in the URL after /c/>
```

Configure them in the local environment (never commit the values; the names are catalogued in `config/integrations.yaml`) or in the shell:
```bash
export FIC_ACCESS_TOKEN="..."
export FIC_COMPANY_ID="..."
```

## Agent commands

| Command | Description | Output |
|---------|------------|--------|
| `sync-invoices` | Syncs issued invoices (current year) | `vault/finance/fatturazione.md` |
| `aging-report` | Computes overdue receivables aging | Updates `company/direzione/metrics/kpis.md` receivables section |
| `sync-cashflow` | Reads the cash journal (prima nota) and updates balances | `vault/finance/cashflow.md` |

## Authorized agents

CFO (owner), CEO, Chief of Staff

## Standard flow (weekly)

```
# With MCP active — direct queries
→ fic_list_invoices(year=2026) for yearly revenue
→ fic_list_clients() for updated client records
→ fic_list_received_documents(year=2026) for expenses

# Or via agent commands
/finance fatture-in-cloud sync-invoices
/finance fatture-in-cloud aging-report
```

The CFO runs it every Monday to keep data fresh in the weekly cadence.

## API notes

- Base URL: `https://api-v2.fattureincloud.it`
- Auth: OAuth2 Bearer — `Authorization: Bearer {FIC_ACCESS_TOKEN}`
- Rate limit: ~1,000 req/hour, 20,000 req/month (sliding window, HTTP 429 with Retry-After)
- Pagination: `page` (from 1) + `per_page` (default 5, max 100)
- Query filter: `q` parameter with SQL-like syntax (e.g. `date >= '2026-01-01'`)
- Docs: https://developers.fattureincloud.it/docs

## Integration with other skills

| Skill | Integration |
|-------|-------------|
| **Stripe** | Reconciles FIC invoices (Italian fiscal) with Stripe payments |
| **Qonto** | Verifies bank collections with `qonto reconcile` |
| **Admin & Controllo** | Invoicing data feeds management control |
| **Data & Metrics** | Revenue, aging, DSO computed from FIC invoices |
