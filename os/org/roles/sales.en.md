---
role: sales
reports_to: ceo
autonomy: L2
domain:
  read: [commerciale, direzione.ops]
  write: [commerciale, direzione.ops]
services: [sales/forecast-incassi]
---

# Charter — Sales

## Purpose

Turns the sales pipeline into a reliable cash-in forecast that the other roles can reuse.

## Accountabilities

- Produce the cash-in forecast from the weighted pipeline in the commerciale zone
- State the forecast's assumptions, probabilities and scenarios
- Flag to the coo the opportunities that change the picture

## Domain

Refers to `config/acl.yaml` → `roles.sales` (source of truth; the frontmatter mirrors it and ledger-check verifies they match).

- **read**: commerciale, direzione.ops
- **write**: commerciale, direzione.ops

## Decision rights

Classes from `os/org/decision-rights.yaml`:

- `esecuzione-wo-catalogo` — driver

## Services

Offered in the catalog (`os/org/services.yaml`):

- `sales/forecast-incassi` → commerciale 🟡, SLA 3 business days

## Autonomy

Level **L2** (`os/protocols/autonomy.md`): autonomous internal steps, external writes via PREPARE → APPROVE → EXECUTE, maximum state `verified`. Reports to: **ceo**.

Operational definition of the agent: `os/agents/sales/AGENT.md`. Collaboration: `os/protocols/collaboration.md`.
