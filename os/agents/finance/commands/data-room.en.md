# /finance data-room — Data room readiness

## Purpose
Know at any time how ready we are for due diligence: what exists, what is missing,
who must produce it.

## Input
None; optional: target round (changes the required depth).

## Steps
1. **Scan the zones** against the checklist by category:
   - **Company**: pitch deck, one-pager, vision and OKRs (`direzione`)
   - **Financials**: financial model, pricing, KPIs, cap table, burn/runway, historical MRR
     (`finance` 🔴)
   - **Product**: roadmap, main PRDs with status, architecture (`prodotto`)
   - **Market**: segments, battlecards, TAM/SAM/SOM, case studies (`commerciale`, `marketing`)
   - **Team**: roles (`config/people.yaml`), org chart, hiring plan
   - **Legal & compliance**: articles of association, certifications, policies, standard contracts, DPA, IP
     (`compliance`, `clienti/*/contratti` 🔴)
2. For each document: **present / partial / missing**, with path and freshness.
3. Prioritized **gap analysis**: critical → high → medium, with action, owner (agent),
   deadline.
4. Actual sharing with an investor happens on a dedicated Drive folder
   with its own ACL (via `admin`), **never** by granting access to the `finance` zone; 🔴 documents
   go in only if needed for the phase and after APPROVE.

## Output format
```markdown
---
zone: finance
tier: 🔴
type: data-room-audit
---
# Data Room Readiness — {YYYY-MM-DD}
Present: {n}/{tot} ({%}) · Partial: {n} · Missing: {n}

## Gap analysis
| # | Document | Status | Priority | Action | Owner | Due by |
## By category (detail)
```

## Destination
Zone `finance` → `investors/data-room-audit-{YYYY-MM-DD}.md`.
Commit (admin): `[finance] investor: data room audit`.

## Handoff
Missing docs → owner agent (product, compliance, marketing…) · sharing → `admin` (ACL).
