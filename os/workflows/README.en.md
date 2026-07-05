# Workflows — index

Workflows coordinate multiple agents on an end-to-end process. Each workflow defines phases,
responsible agent, input/output **in terms of zones**, and handoff criteria.
Agents live in `os/agents/`; external writes inside a workflow always follow
`os/protocols/external-writes.md`.

| Workflow | Trigger | Agents involved |
|---|---|---|
| [feature-lifecycle.md](feature-lifecycle.md) | Feature request from a client/prospect | Sales → Product → CTO → Marketing → Sales |
| [customer-escalation.md](customer-escalation.md) | Critical problem or urgent request from a client | Sales/Delivery → Product → CTO/Delivery |
| [quarterly-planning.md](quarterly-planning.md) | Start of the quarter | CEO → Product → CTO → Sales → Marketing |
| [incident-response.md](incident-response.md) | Outage or technical/security incident | CTO → CEO → Delivery → Compliance |

Conventions:
- **Handoff** = the agent closes its phase with output in the indicated zone + explicit
  indication of the next agent and command. Cross-zone without direct access → formal
  request (e.g. `30-Prodotto/richieste/` to request a spec from the sales side).
- A workflow does not skip phases: if a phase is not needed, the agent declares it in the handoff.
