# Workflow — indice

I workflow coordinano più agenti su un processo end-to-end. Ogni workflow definisce fasi,
agente responsabile, input/output **in termini di zone** e criteri di handoff.
Gli agenti sono in `os/agents/`; le scritture esterne dentro un workflow seguono sempre
`os/protocols/external-writes.md`.

| Workflow | Trigger | Agenti coinvolti |
|---|---|---|
| [feature-lifecycle.md](feature-lifecycle.md) | Richiesta feature da cliente/prospect | Sales → Product → CTO → Marketing → Sales |
| [customer-escalation.md](customer-escalation.md) | Problema critico o richiesta urgente di un cliente | Sales/Delivery → Product → CTO/Delivery |
| [quarterly-planning.md](quarterly-planning.md) | Inizio trimestre | CEO → Product → CTO → Sales → Marketing |
| [incident-response.md](incident-response.md) | Outage o incidente tecnico/sicurezza | CTO → CEO → Delivery → Compliance |

Convenzioni:
- **Handoff** = l'agente chiude la propria fase con output nella zona indicata + indicazione
  esplicita di agente e comando successivo. Cross-zona senza accesso diretto → richiesta
  formale (es. `30-Prodotto/richieste/` per chiedere una spec dal commerciale).
- Un workflow non salta fasi: se una fase non serve, l'agente lo dichiara nell'handoff.
