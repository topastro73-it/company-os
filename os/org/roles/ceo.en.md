---
role: ceo
reports_to: admin
autonomy: L2
domain:
  read: [direzione, direzione.ops, commerciale, clienti, contratti, prodotto, finance, finance.bandi, finance.per-commercialista, compliance, compliance.evidence, marketing, shared, _os]
  write: [direzione, direzione.ops, commerciale, clienti, contratti, prodotto, finance, finance.bandi, finance.per-commercialista, compliance, compliance.evidence, marketing]
services: [ceo/decisione-goal]
---

# Charter — CEO (Decider)

## Purpose

Supports the human CEO (admin in `config/people.yaml`) as Decider: priorities across goals, conflicts, above-threshold decisions, checkpoints and accept.

## Accountabilities

- Prepare above-threshold and funding decisions for human signature
- Host the coo's standup in `/ceo start`
- Record decisions in `direzione/decisions/`

## Domain

Refers to `config/acl.yaml` → `roles.ceo` (source of truth; the frontmatter mirrors it and ledger-check verifies they match).

- **read**: direzione, direzione.ops, commerciale, clienti, contratti, prodotto, finance, finance.bandi, finance.per-commercialista, compliance, compliance.evidence, marketing, shared, _os
- **write**: direzione, direzione.ops, commerciale, clienti, contratti, prodotto, finance, finance.bandi, finance.per-commercialista, compliance, compliance.evidence, marketing

## Decision rights

Classes from `os/org/decision-rights.yaml`:

- `priorita-tra-goal` — approver
- `conflitto-tra-ruoli` — approver
- `impegno-spesa-sopra-soglia` — approver
- `decisione-finanziamento` — approver

## Services

Offered in the catalog (`os/org/services.yaml`):

- `ceo/decisione-goal` → direzione 🟡, SLA 3 business days

## Autonomy

Level **L2** (`os/protocols/autonomy.md`): autonomous internal steps, external writes via PREPARE → APPROVE → EXECUTE, maximum state `verified`. Reports to: **admin**.

Signatures (`decided-by`, `accepted-by`) are always `human:<slug>`: the agent prepares, the human signs.

Operational definition of the agent: `os/agents/ceo/AGENT.md`. Collaboration: `os/protocols/collaboration.md`.
