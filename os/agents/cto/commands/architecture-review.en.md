# /cto architecture-review — Architecture review

## Purpose
Evaluate the current architecture or a proposal: does it support the roadmap? Does it scale? Is it secure?

## Input
- Scope: overall architecture, a subsystem, or a change proposal

## Steps
1. Load the roadmap and incoming specs (`prodotto` zone) — the review is done against the
   expected future, not just the present; load the relevant ADRs.
2. **Snapshot the current state**: components, dependencies, integrations (ClickUp/HubSpot/ERP…),
   multi-tenancy (if the product is multi-tenant, tenant isolation is architecture, not a detail).
3. **Evaluate by dimension**: scalability (does it support 10x users/tenants?), reliability and single
   points of failure, security (attack surface, secrets, authz across every role),
   maintainability and debt, infrastructure cost.
4. **Compliance check**: does the architecture preserve the mapped controls (ISO 27001, NIS2)?
   Gaps → flag to `compliance` with severity.
5. **Prioritized recommendations**: max 5, each with effort (S/M/L), risk if ignored,
   owner. The simplest one that works comes first.
6. Recommended structural changes → each becomes an ADR (`/cto tech-decision`).

## Output format
```markdown
---
zone: prodotto
tier: 🟡
type: arch-review
date: YYYY-MM-DD
---
# Architecture Review — {scope} — {date}

## Current state (components, dependencies)
## Evaluation | Dimension | Status | Risk | Notes |
## Compliance gaps (if any)
## Prioritized recommendations (effort, risk, owner)
## ADRs to open
```

## Destination
`prodotto` zone → `reviews/arch-review-{YYYY-MM-DD}.md`.
Commit (admin): `[cto] review: architecture {scope}`.

## Handoff
Compliance gaps → `compliance` · work to plan → `product` (backlog) ·
critical risk → `ceo`.
