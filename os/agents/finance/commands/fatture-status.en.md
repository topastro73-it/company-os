# /finance fatture-status — Invoicing status

## Purpose
Complete snapshot of the active billing cycle: to be issued, awaiting payment, overdue, collected. Overdue
invoices are a cash problem, not a tidiness problem.

## Input
None.

## Steps
1. Read `finance/fatturazione.md`; if the Fatture in Cloud MCP is active, reconcile with
   what was actually issued/collected.
2. **To be issued**: accrued revenue not yet invoiced (active contracts from ERP/`clienti`
   zone) — for each: client, period, amount, "to be issued by".
3. **Awaiting payment**: invoice, client, amount, issued, due date, days.
4. **Overdue ⚠️**: sorted by delay; 30+ days → proposed payment reminder (draft ready,
   sent via APPROVE), coordinated with `sales` if the partner has open negotiations.
5. **Collected this month** and summary: monthly invoiced amount, to be collected, total overdue,
   **average DSO** and trend.
6. Update the statuses in the registry.

## Output format
```markdown
---
zone: finance
tier: 🔴
type: fatture-report
---
# Invoicing — {YYYY-MM-DD}

## To be issued           | Client | Period | Amount | By |
## Awaiting payment       | Invoice | Client | Amount | Due date | Days |
## Overdue ⚠️             | Invoice | Client | Amount | Delay | Action |
## Collected this month

Summary: invoiced €… · to collect €… · overdue €… · DSO {n} days ({trend})
```

## Destination
Report in chat + `finance/fatturazione.md` updated.
Commit (admin): `[finance] fatture: status {YYYY-MM-DD}`.

## Handoff
Overdue 30+ days → payment reminder (APPROVE) + `sales` · a partner's late-payment pattern → `delivery`
(health signal) · cash impact → `/finance cashflow`.
