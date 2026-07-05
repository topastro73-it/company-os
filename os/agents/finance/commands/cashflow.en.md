# /finance cashflow — Cash projection

## Purpose
Always know how much oxygen we have: projected balance over 3 months, week by week.

## Input
None; optional: a scenario to simulate ("what if deal X slips by a month?").

## Steps
1. Load `finance/cashflow.md`, `fatturazione.md`, `costi-ricorrenti.md`,
   `scadenzario.md`; actual balance from Qonto if MCP is active.
2. **Expected inflows**: issued invoices (with a realistic collection date, not the contractual one:
   use historical DSO), recurring revenue, pipeline collections ONLY if weighted and
   declared as such. **Loans/financing: separate line, never among revenue.**
3. **Expected outflows**: recurring costs, tax deadlines (from the payment schedule), director
   compensation (**quarterly, never monthly**), known one-off suppliers.
4. **Project** the balance week by week for 12 weeks; then a pessimistic
   scenario (collections +30 days, no new deals) — the worst case is mandatory.
5. **Alert**: projected balance below the critical threshold in any week → at the top of the
   report, with the 2-3 available levers (payment reminders, deferring outflows, credit line).
6. Runway: months to zero balance in the base scenario and in the pessimistic one.

## Output format
```markdown
---
zone: finance
tier: 🔴
type: cashflow
---
# Cashflow — {YYYY-MM-DD}
Current balance: €… · Base runway: {n} months · pessimistic: {n} months
## ⚠️ Alerts (if any)
## 12-week projection | Week | Inflows | Outflows | Balance |
## Pessimistic scenario   ## Assumptions (explicit, always)
```

## Destination
Zone `finance` → `reports/cashflow-{YYYY-MM-DD}.md` + `cashflow.md` updated.
Commit (admin): `[finance] cashflow: projection {YYYY-MM-DD}`.

## Handoff
Runway <9 months → `ceo` (immediate alert, options on the table).
