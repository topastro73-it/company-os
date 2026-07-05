# Workflow: Customer Escalation

A client has a critical problem or an urgent request.

## 1. Intake (Sales / Delivery)
- **Trigger**: report from client/partner (email, call, partner channel)
- **Action**: document client, problem, impact (how many users/end-customers), urgency,
  what was promised
- **Output**: `20-Clienti/{slug}/escalations/{YYYY-MM-DD}-{slug}.md` (client folder:
  visible only to those following the client)
- **Handoff → Product**: escalation documented, with proposed severity

## 2. Triage (Product)
- **Input**: escalation file in the client folder
- **Action**: classify —
  - **Bug** → handoff CTO (if outage/degradation: move to `incident-response.md`)
  - **Urgent feature request** → `feature-lifecycle.md` phase 2, fast-track but **without
    skipping the framework** (no shortcuts)
  - **Configuration / usage** → handoff Delivery
- **Output**: triage annotated in the escalation file (type, owner, first-response ETA)

## 3. Resolution (by type)
- **Critical bug (CTO)**: fix + verification; ClickUp task via external-writes; if
  communication to impacted clients is needed → coordinate with CEO/Marketing
- **Urgent feature (Product)**: evaluation with an explicit outcome and a reply date for the client
- **Configuration (Delivery)**: resolve, document the solution in
  `30-Prodotto/knowledge-base/` (reusable, pseudonymized)
- **Exit criterion**: resolution verified (not just deployed) and noted in the file

## 4. Follow-up (Sales / Delivery)
- **Action**: communicate the resolution to the client (email draft via external-writes);
  update the client's health score in the `clienti` zone
- **If it impacts the deal**: update the opportunity in `10-Commerciale/`
- **Lesson learned**: if a generalizable pattern emerges → propose an LRN-XXX learning
  at close (`os/protocols/memory.md` §3)

## Rules
- First-response SLA: within the business day for high severity
- Every escalation stays in the client folder — never in broader zones
- Recurring escalations on the same topic (≥3) → flag to Product as a backlog signal
