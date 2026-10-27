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
6. **Scorecard** (Org-OS): for each weekly measurable of the active goals, append a dated row
   to `00-Direzione/ops/scorecard.md` (ledger, `direzione` zone; in admin on the Drive mount):
   date, measurable, owner `human:<slug>`, week, status 🟢/🔴 against the criterion's threshold,
   path of the flash report in the finance zone. **Never figures**: the value stays in the 🔴 flash report.
   If the file does not exist, create it from the template below. Then
   `python3 scripts/audit/ledger-check.py --drive`, copy into the snapshot `company/direzione/ops/`,
   `python3 scripts/audit/ledger-check.py`.

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

Scorecard template (ledger, no amounts):
```markdown
---
zone: direzione
tier: 🟡
type: scorecard
---
# Weekly scorecard

| Date | Measurable | Owner | Week | Status | Ref |
|---|---|---|---|---|---|
| YYYY-MM-DD | {goal measurable, e.g. runway in months vs threshold} | human:{slug} | YYYY-Wnn | 🟢/🔴 | `vault/finance/sync/sync-{YYYY-Wnn}.md` |
```

## Destination
Zone `finance` → `sync/sync-{YYYY-Wnn}.md` + registries updated in place.
Ledger (`direzione` zone, `ops` subzone) → row in `scorecard.md`.
Commit (admin): `[finance] sync: week {n}`.

## Handoff
Invoices 30+ days overdue → `/finance fatture-status` + `sales` for payment reminder.
