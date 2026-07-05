---
zone: _os
tier: 🟡
---

# Glossary

> System terms (valid for every instance) + business terms (to adapt to your company).

## System
- **Zone** — a top-level Drive folder with one ACL and one sync direction (see `config/acl.yaml`).
- **ACL** — the native Drive permissions: they are the real enforcement of access, not a convention.
- **Tier 🔴🟡🟢** — sensitivity classification (RESTRICTED / INTERNAL / PUBLIC): decides what
  can go out and how, orthogonal to who accesses (that's the ACL).
- **Single master** — every file has one source of truth (git *or* Drive), never two.
- **PREPARE → APPROVE → EXECUTE** — protocol for every write to external systems.
- **Handoff** — passing the baton between agents (indicated at the end of an activity).
- **LRN-XXX** — a learned rule (learning) that the system applies proactively.

## Business (common examples — adapt to your company)
- **ICP** — Ideal Customer Profile: who the ideal customer is.
- **ACV / MRR / ARR** — Annual Contract Value / Monthly / Annual Recurring Revenue.
- **NRR** — Net Revenue Retention (incl. upsell/downsell). **Churn** — attrition rate.
- **CAC / LTV** — acquisition cost / lifetime value.
- **Health score** — customer health index (see the customer-success skill for the formula).
- **QBR** — Quarterly Business Review.
- **North Star** — the metric that matters most of all.

<Add here the terms specific to your industry/product.>
