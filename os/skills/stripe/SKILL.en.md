# Stripe Skill

Integration with Stripe via MCP connector (Cowork).
Manages payments, invoices, customers, subscriptions and products.
Used by CFO, CEO, Chief of Staff, Sales.

## Prerequisites

**Stripe** MCP connector installed and connected in Cowork.
(No environment variables needed — auth is handled by the connector.)

Availability check: if the `mcp__*__list_invoices`, `mcp__*__list_customers` etc. tools respond, Stripe is active.

## Available MCP tools

| Tool | Description | When to use it |
|------|------------|---------------|
| `retrieve_balance` | Current Stripe balance (available, pending, instant) | Cashflow snapshot, daily briefing |
| `list_invoices` | List invoices (filter by customer, limit) | Revenue, aging, reconciliation |
| `list_payment_intents` | List payments (filter by customer, limit) | Transactions, collection confirmation |
| `list_customers` | List Stripe customers | Customer records, segmentation |
| `list_subscriptions` | List active subscriptions | MRR, churn analysis |
| `list_products` | List products/plans | Pricing catalog |
| `list_prices` | List prices associated with products | Pricing tiers, comparisons |
| `list_coupons` | List coupons/discounts | Active promotions |
| `list_disputes` | List disputes/chargebacks | Risk management |
| `fetch_stripe_resources` | Single object detail by ID (in_, pi_, cus_, sub_, prod_, price_, ch_) | Deep dive on invoice, customer, payment |
| `search_stripe_resources` | Full-text search over Stripe resources | Find objects by name, email, amount |
| `get_stripe_account_info` | Stripe account info (business, country, capabilities) | Setup verification |
| `search_stripe_documentation` | Search the Stripe documentation | Troubleshooting, best practices |

## Commands

| Command | Description | Output |
|---------|------------|--------|
| `stripe-snapshot` | Balance + recent invoices + active subscriptions | Section in daily briefing or report |
| `stripe-invoices [anno]` | List invoices filtered by year with totals | Report in `vault/finance/reports/` |
| `stripe-mrr` | Computes MRR from active subscriptions | Updates `company/direzione/metrics/kpis.md` MRR section |
| `stripe-customers` | Stripe customer records with subscription status | Cross-ref with `20-Clienti/` |
| `stripe-reconcile` | Cross-matches Stripe payments with FIC/Qonto invoices | Identifies discrepancies |

## Authorized agents

CFO (owner), CEO, Chief of Staff, Sales

## Standard flow

```
# Daily (in the CEO/CoS morning briefing)
→ retrieve_balance for current balance
→ list_invoices (limit 5) for latest invoices

# Weekly (Monday, after FIC and Qonto sync)
→ stripe-invoices for period revenue
→ stripe-reconcile for cross-platform reconciliation

# Monthly (financial review)
→ stripe-mrr for MRR/churn calculation
→ stripe-customers for customer records update
→ list_disputes for chargeback check
```

## Important notes

- **Amounts**: Stripe returns amounts in cents (minor units). Divide by 100 for EUR.
- **Timestamps**: Stripe uses Unix timestamps (seconds). Convert with `datetime.fromtimestamp()`.
- **Currency**: Account configured in EUR.
- **Rate limit**: handled by the MCP connector, no practical limit for normal use.
- **Fallback**: if the MCP connector is unavailable, the most recent data is in `vault/finance/` (last sync). Report to the CEO that the Stripe MCP is offline.
- **Cross-reference**: Stripe customers (cus_*) must be mapped to the partner files in `20-Clienti/` and to HubSpot CRM contacts.

## Integration with other skills

| Skill | Integration |
|-------|-------------|
| **Fatture in Cloud** | Reconciles FIC invoices (Italian fiscal) with Stripe invoices (payments) |
| **Qonto** | Stripe payouts land on Qonto — verify with `qonto reconcile` |
| **Data & Metrics** | MRR, churn rate, ARPU computed from Stripe subscriptions |
| **ERP** | Stripe as revenue data source for the ERP finance module |
| **Customer Success** | Customer payment status from Stripe informs the health score |
| **Admin & Controllo** | Stripe dashboard for revenue management control |
