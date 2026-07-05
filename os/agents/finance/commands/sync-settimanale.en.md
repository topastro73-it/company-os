# /finance sync-settimanale — Weekly reconciliation

## Purpose
Keep the zone registries aligned with reality: bank, invoices, subscriptions — once
a week, 20 minutes, zero surprises at month-end.

## Input
None. Cadence: weekly (Monday, or first access of the week).

## Steps
1. **Live sources** (if MCPs are active, otherwise ask for the data and state its freshness):
   - Qonto: balance and week's transactions · Fatture in Cloud: issued/received/paid
   - Stripe: subscription collections · an ERP: contracts and accrued revenue
2. **Reconcile collections**: payments received ↔ open invoices in `fatturazione.md`
   → mark as collected; flag payments that cannot be reconciled.
3. **Reconcile outflows**: charges ↔ `costi-ricorrenti.md`; new unmapped recurring
   costs → add them; anomalies (different amount, double charge) → flag.
4. **Update the registries**: `fatturazione.md` (statuses), `cashflow.md` (actual balance vs
   projection — if deviation >10%, understand why), `scadenzario.md` (tick off what
   has been paid).
5. **Flash report**: 6 lines — balance, collected, spent, overdue, next 7-day deadlines,
   anomalies. Loans/financing received: separate line, **never inside revenue**.

## Output format
```markdown
---
zone: finance
tier: 🔴
type: sync-report
week: YYYY-Wnn
---
# Weekly sync — {week}
Balance: €… (Δ vs projection: …) · Collected: €… · Spent: €…
Overdue to collect: €… · 7-day deadlines: … · Anomalies: …
## Reconciliation detail  ## Actions (owner + due by)
```

## Destination
Zone `finance` → `sync/sync-{YYYY-Wnn}.md` + registries updated in place.
Commit (admin): `[finance] sync: week {n}`.

## Handoff
Invoices 30+ days overdue → `/finance fatture-status` + `sales` for payment reminder.
