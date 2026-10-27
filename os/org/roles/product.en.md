---
role: product
reports_to: ceo
autonomy: L2
domain:
  read: [prodotto, direzione.ops]
  write: [prodotto, direzione.ops]
services: [product/stima-effort-progetto]
---

# Charter — Product

## Purpose

Ties product, delivery and QA effort to the roadmap, so that per-project costs can be planned.

## Accountabilities

- Estimate product, delivery and QA effort per project, tied to the roadmap
- Align the estimate with the cto's technical estimate

## Domain

Refers to `config/acl.yaml` → `roles.product` (source of truth; the frontmatter mirrors it and ledger-check verifies they match).

- **read**: prodotto, direzione.ops
- **write**: prodotto, direzione.ops

## Decision rights

Classes from `os/org/decision-rights.yaml`:

- `esecuzione-wo-catalogo` — driver

## Services

Offered in the catalog (`os/org/services.yaml`):

- `product/stima-effort-progetto` → prodotto 🟡, SLA 5 business days

## Autonomy

Level **L2** (`os/protocols/autonomy.md`): autonomous internal steps, external writes via PREPARE → APPROVE → EXECUTE, maximum state `verified`. Reports to: **ceo**.

No currency in the output: finance does the conversion.

Operational definition of the agent: `os/agents/product/AGENT.md`. Collaboration: `os/protocols/collaboration.md`.
