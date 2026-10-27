# Org-OS — ruoli, servizi, diritti decisionali

Il livello organizzativo che permette ai ruoli-agente di lavorare in squadra su un goal
(`os/protocols/collaboration.md`, autonomia in `os/protocols/autonomy.md`).

| File | Cosa contiene |
|---|---|
| `os/org/services.yaml` | Catalogo X-as-a-Service: servizio, input, output, zona/tier di output, SLA |
| `os/org/decision-rights.yaml` | Classi di decisione DACI (un solo approver: agent, owner o ceo) e `reports_to` |
| `config/acl.yaml` → `roles` | Domain di ogni ruolo-agente (zone in lettura/scrittura): fonte di verità |

## Charter dei ruoli pilota

| Ruolo | Charter | Risponde a |
|---|---|---|
| coo | [roles/coo.md](roles/coo.md) | CEO |
| controller | [roles/controller.md](roles/controller.md) | CEO |
| finance | [roles/finance.md](roles/finance.md) | CEO |
| sales | [roles/sales.md](roles/sales.md) | CEO |
| cto | [roles/cto.md](roles/cto.md) | CEO |
| product | [roles/product.md](roles/product.md) | CEO |
| ceo | [roles/ceo.md](roles/ceo.md) | admin (`config/people.yaml`) |

Gli altri agenti (cos, delivery, compliance, marketing, admin) restano definiti dal loro
`AGENT.md` e migrano a charter in una fase successiva. Il cos legge il ledger e fa briefing al
servizio di coo e CEO: non emette né assegna work order.

Ogni charter ha frontmatter `role`, `reports_to`, `autonomy`, `domain` (copia di
`roles.<slug>`) e `services`; le sezioni sono Purpose, Accountabilities, Domain, Decision
rights, Servizi, Autonomia.
