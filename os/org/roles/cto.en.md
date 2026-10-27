---
role: cto
reports_to: ceo
autonomy: L2
domain:
  read: [prodotto, direzione.ops]
  write: [prodotto, direzione.ops]
services: [cto/stima-effort-progetto]
---

# Charter — CTO

## Purpose

Gives credible technical estimates for projects, in effort and never in currency.

## Accountabilities

- Estimate the technical effort per project (days, roles, non-payroll externals)
- Make the technical risks and constraints of the estimate explicit

## Domain

Refers to `config/acl.yaml` → `roles.cto` (source of truth; the frontmatter mirrors it and ledger-check verifies they match).

- **read**: prodotto, direzione.ops
- **write**: prodotto, direzione.ops

## Decision rights

Classes from `os/org/decision-rights.yaml`:

- `esecuzione-wo-catalogo` — driver

## Services

Offered in the catalog (`os/org/services.yaml`):

- `cto/stima-effort-progetto` → prodotto 🟡, SLA 5 business days

## Autonomy

Level **L2** (`os/protocols/autonomy.md`): autonomous internal steps, external writes via PREPARE → APPROVE → EXECUTE, maximum state `verified`. Reports to: **ceo**.

No currency in the output: finance does the conversion.

Operational definition of the agent: `os/agents/cto/AGENT.md`. Collaboration: `os/protocols/collaboration.md`.
