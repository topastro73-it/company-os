# Decisions — immutable decisions

## Where

Zone `direzione`: `00-Direzione/decisions/` (snapshot: `company/direzione/decisions/`).
File: `YYYY-MM-DD-{slug}.md` — e.g. `2026-07-04-pricing-tier-enterprise.md`.
Frontmatter: `zone: direzione`, `tier: 🟡` (🔴 if it mentions restricted amounts/contracts → then
the 🔴 detail lives in finance/vault and the decision references it without reproducing it).

## When to record a decision

Record as a decision (not as a simple note) when the choice:
- constrains the future (pricing, positioning, architecture, framework contract, hire)
- closes off a real alternative (A was chosen **instead of** B)
- will need to be explainable months later ("why did we decide that?")

Do not record: operational tasks, reversible preferences with no cost, exploratory hypotheses.
The memory protocol (`memory.md` §1) intercepts decisions that emerge in chat and proposes
recording them — always with human confirmation.

## Immutability

Decisions **are not modified** and are not deleted: they are **superseded** by a new decision.
- The new decision links the old one in the Context ("supersedes DEC-012")
- The old one receives ONLY the status update: `Status: Superseded` + link to the new one
- Everything else in the file stays as it was: it is the historical record of what was known then

## Template

```markdown
---
zone: direzione
tier: 🟡
status: approved           # proposed | approved | superseded
superseded-by:             # path of the decision that supersedes it (if superseded)
---
# DEC-{NNN}: {Decision title}

- **Date**: YYYY-MM-DD
- **Agent/Owner**: {ceo/product/cto/sales/…} — {person}
- **Status**: Proposed | Approved | Superseded
- **Review date**: YYYY-MM-DD (optional — when to re-check it)

## Context
What is the problem or opportunity? What was known at the time of the decision?

## Options considered

### Option A: {name}
- **Pros**: … · **Cons**: … · **Effort**: S/M/L · **Expected impact**: …

### Option B: {name}
- **Pros**: … · **Cons**: … · **Effort**: S/M/L · **Expected impact**: …

## Decision
We chose **Option X** because …

## Consequences
- What changes after this decision
- Next steps
- Risks to monitor

## Follow-up
- [ ] Action 1 — Owner: {person} — Due: YYYY-MM-DD
- [ ] Action 2 — Owner: {person} — Due: YYYY-MM-DD
```

## Links

- The **wiki** may have an entity page `system/wiki/entities/decisions/{slug}.md` with
  the narrative evolution; the file in `decisions/` remains the formal source
- Technical architecture decisions (ADRs) follow the same principle but live in the
  `prodotto` zone under the CTO; only decisions with directional impact go here
- At close, the decisions taken in the session appear in the "Where we left off" block
  of the next session (see `session-rituals.md`)
