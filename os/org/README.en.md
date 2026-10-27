# Org-OS — roles, services, decision rights

The organizational layer that lets agent roles work as a team on a goal
(`os/protocols/collaboration.md`, autonomy in `os/protocols/autonomy.md`).

| File | What it contains |
|---|---|
| `os/org/services.yaml` | X-as-a-Service catalog: service, input, output, output zone/tier, SLA |
| `os/org/decision-rights.yaml` | DACI decision classes (a single approver: agent, owner or ceo) and `reports_to` |
| `config/acl.yaml` → `roles` | Domain of each agent role (zones read/write): source of truth |

## Pilot role charters

| Role | Charter | Reports to |
|---|---|---|
| coo | [roles/coo.md](roles/coo.md) | CEO |
| controller | [roles/controller.md](roles/controller.md) | CEO |
| finance | [roles/finance.md](roles/finance.md) | CEO |
| sales | [roles/sales.md](roles/sales.md) | CEO |
| cto | [roles/cto.md](roles/cto.md) | CEO |
| product | [roles/product.md](roles/product.md) | CEO |
| ceo | [roles/ceo.md](roles/ceo.md) | admin (`config/people.yaml`) |

The other agents (cos, delivery, compliance, marketing, admin) are still defined by their
`AGENT.md` and will move to charters in a later phase. The cos reads the ledger and briefs the
coo and the CEO: it neither issues nor assigns work orders.

Each charter has frontmatter `role`, `reports_to`, `autonomy`, `domain` (a copy of
`roles.<slug>`) and `services`; the sections are Purpose, Accountabilities, Domain, Decision
rights, Services, Autonomy.
