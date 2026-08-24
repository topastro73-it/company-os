# /delivery churn-analysis — Cross-partner churn analysis

## Purpose
Understand why we lose (or risk losing) partners and SMBs, and what to change.

## Input
- Period (default: last quarter)

## Steps
1. Scan all partner cards: churned in the period, health <60, SMBs lost per
   partner.
2. **Churn rate**: partner-level and end-customer-level, by segment (`config/company.yaml`) and by tier.
3. **Root cause** for each churn or At-Risk/Critical: onboarding never completed? Salespeople
   engagement at zero? Value not perceived (low active SMBs)? Product problem? Price?
   Look for the pattern, not the anecdote — use the 5 indicators as a grid.
4. **Common patterns**: e.g. "partners without a first deal by wk.8 churn in 70%
   of cases" → candidate learning `LRN-XXX` (propose at close).
5. **Preventive actions**: for each at-risk partner, one action with owner and deadline;
   for patterns, a proposed change to the process (onboarding, enablement, product).

## Output format
```markdown
---
zone: commerciale
tier: 🟡
type: report
---
# Churn Analysis — {period}

## Numbers: partner churn {n}/{%} · SMB churn {%} · by segment/tier
## Churned in the period (partner, root cause, ignored signals)
## At risk now
| Partner | Health | Band | Main cause | Action | Owner | Deadline |
## Identified patterns (candidate learnings)
## Proposed process changes
```

## Destination
`commerciale` zone → `delivery/churn-analysis-{YYYY-MM-DD}.md`.
Commit (admin): `[delivery] churn: analysis {period}`.

## Handoff
Product patterns → `product` · sales/expectation patterns → `sales` ·
significant churn risk → `ceo`.
