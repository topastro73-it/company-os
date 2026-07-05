# Admin & Management Control Skill

Skill for managing operational administration and management control
of an Italian startup. It extends the CFO Agent with the operational
side that the accountant does not cover proactively.

## Context: Italian startup

The company is an Italian company (e.g. innovative SRL).
This entails specific obligations: VAT, INPS, statutory financial statements,
tax filings, and specific opportunities (R&D tax credit, innovative
startup regime, incentives).

## Areas covered

### 1. Tax and administrative deadline calendar
### 2. Invoicing and collections
### 3. Operational cash management
### 4. Management control
### 5. Corporate obligations
### 6. Incentives and subsidies
### 7. Vendor and cost management

---

## Available commands

### `/admin scadenzario`
Shows all upcoming admin/tax deadlines.

**Process**:
1. Read `vault/finance/scadenzario.md`
2. Filter: next 30 days
3. Classify by urgency
4. Flag: past deadlines not marked as completed

**Output format**:
```markdown
# 📅 Deadline calendar — {date}

## 🔴 Overdue (not completed!)
| Deadline | Date | Type | Estimated amount | Owner |
|----------|------|------|----------------|-------|

## 🟡 Next 7 days
| Deadline | Date | Type | Estimated amount | Owner |
|----------|------|------|----------------|-------|

## 🟢 Next 30 days
| Deadline | Date | Type | Estimated amount | Owner |
|----------|------|------|----------------|-------|

## Next quarter
| Deadline | Date | Type | Notes |
|----------|------|------|------|
```

### `/admin cashflow`
Operational cashflow analysis: expected inflows, planned outflows, projected balance.

**Process**:
1. Load `vault/finance/cashflow.md`
2. Inflows: issued invoices (when do we collect?), recurring revenue
3. Outflows: salaries, vendors, taxes, SaaS subscriptions, rent, other
4. Projection: account balance for the next 3 months, week by week
5. Alert: if the projected balance drops below the critical threshold

**Output**: `vault/finance/reports/cashflow-{date}.md`

### `/admin fatture-status`
Invoicing status: issued, to be issued, collected, overdue.

**Process**:
1. Read `vault/finance/fatturazione.md`
2. Show:
   - Invoices to be issued (accrued revenue not yet invoiced)
   - Issued invoices awaiting payment (with due date)
   - Overdue invoices (unpaid beyond terms)
   - Invoices collected during the month
3. Calculate: DSO (Days Sales Outstanding), aging analysis
4. Alert: invoices overdue by 30+ days

**Output format**:
```markdown
## 💶 Invoicing — {date}

### To be issued
| Client/Partner | Period | Amount | Issue by |
|----------------|---------|---------|------------------|

### Awaiting payment
| Invoice no. | Client | Amount | Issued | Due date | Days |
|-----------|---------|---------|--------|----------|--------|

### Overdue ⚠️
| Invoice no. | Client | Amount | Due date | Days late |
|-----------|---------|---------|----------|---------------|

### Collected this month
| Invoice no. | Client | Amount | Collected on |
|-----------|---------|---------|-------------|

### Summary
- Invoiced this month: €—
- To be collected: €—
- Overdue: €—
- Average DSO: — days
```

### `/admin costi-ricorrenti`
Maps all recurring costs: SaaS, infrastructure, services, salaries.

**Process**:
1. Read `vault/finance/costi-ricorrenti.md`
2. Categorize: infra/cloud, SaaS tools, professional services, salaries, rent, other
3. For each cost: monthly amount, annual amount, renewal date, cut potential
4. Calculate: detailed operational burn rate
5. Identify: optimizable costs, expiring contracts, duplications

**Output**: `vault/finance/reports/costi-ricorrenti-{date}.md`

### `/admin controllo-gestione`
Management control report: budget vs actual, margins per line.

**Process**:
1. Compare budget (from the CFO) vs actual (from operational data)
2. Analysis by cost center: R&D, Sales & Marketing, G&A, Infra
3. Margin per partner: partner revenue - allocated direct costs
4. Variance analysis: where we spend more/less than planned
5. Propose corrective actions

**Output**: `vault/finance/reports/controllo-gestione-{period}.md`

### `/admin incentivi-check`
Checks incentives and subsidies available for Italian innovative startups.

**Process**:
1. Verify requirements for:
   - **R&D tax credit** (research and development)
   - **Patent box** (if applicable)
   - **Innovative startup regime** (tax, corporate, labor benefits)
   - **Smart&Start Italia** or other MISE/Invitalia calls
   - **Regional calls** (e.g. calls from your own region)
   - **Hiring incentives** (under 36, South, women, NEET)
   - **Training 4.0 credit**
   - **Sabatini** (for investments in capital goods)
2. For each incentive: are we eligible? Are we using it? How much could we obtain?
3. Deadlines for applications/reporting
4. ⚠️ Disclaimer: validate with the accountant

**Output**: `vault/finance/reports/incentivi-check-{date}.md`

### `/admin vendor-costs [vendor]`
Cost analysis of a vendor: history, contract, alternatives, optimization.

**Process**:
1. How much are we spending? History over the last 12 months
2. The contract: duration, renewal, exit clauses, planned increases
3. Are there cheaper alternatives?
4. Can we renegotiate?

**Output**: `vault/finance/reports/vendor-cost-{vendor}.md`

### `/admin adempimenti-societari`
Annual corporate obligations checklist.

**Process**:
1. Verify status:
   - [ ] Financial statements approved and filed (within 120 days of fiscal year close)
   - [ ] Income tax return (IRES/IRAP)
   - [ ] Annual VAT return
   - [ ] Beneficial owner communication
   - [ ] Annual Chamber of Commerce fee
   - [ ] Maintenance of innovative startup requirements (if applicable)
   - [ ] Company registration certificate update
   - [ ] Shareholders' meeting / board minutes
   - [ ] Shareholders' register up to date
2. For each obligation: deadline, status, owner (you / accountant)

**Output**: `vault/finance/reports/adempimenti-{anno}.md`

---

## Data structure in the repo

```
vault/finance/
├── financial-model.md          # (already existing - CFO)
├── pricing.md                  # (already existing)
├── cap-table.md                # (already existing - IR)
├── investor-pipeline.md        # (already existing - IR)
├── scadenzario.md              # Tax and admin deadlines
├── cashflow.md                 # Operational cashflow
├── fatturazione.md             # Invoice register
├── costi-ricorrenti.md         # Fixed cost map
├── incentivi.md                # Active incentives and subsidies
```

---

## Workflow integration

### CEO Decision Cadence

**Daily**:
- Alert if a tax/admin deadline falls within the next 3 days
- Alert if an invoice is overdue by 30+ days and not collected

**Weekly**:
- "Invoices: €[X] to be collected, of which €[Y] overdue"
- "Cashflow next 4 weeks: €[projected balance]"
- Next week's deadlines

**Monthly**:
- Management control: budget vs actual
- Recurring costs: upcoming renewals, possible optimizations
- "Have you checked available incentives? Last check: [date]"
- 3-month cashflow

### CEO Routine Agent

When the Routine Agent runs the daily check, it also reads the deadline calendar:
- "The F24 is due the day after tomorrow — has the accountant prepared it?"
- "February's client invoice hasn't been issued yet — shall we issue it?"

### CFO Agent

The CFO uses this data for:
- `financial-model`: detailed burn rate from costi-ricorrenti
- `burn-analysis`: operational cashflow as input
- `scenario-analysis`: impact of new hires or vendors

---

## Rules

- **ALWAYS** flag tax deadlines in advance (7 days for monthly ones, 30 for annual ones)
- **NEVER** give specific tax advice — defer to the accountant for interpretations
- **ALWAYS** propose concrete actions: "Issue the invoice", "Ask the accountant"
- The deadline calendar is the source of truth — if it's outdated, the system flags it
- Overdue invoices are a cash problem, not just a tidiness one — treat them as urgent
- For incentives: flag the opportunity, the accountant validates
