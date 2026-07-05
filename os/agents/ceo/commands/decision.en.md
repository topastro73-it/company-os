# /ceo decision — Documented strategic decision

## Purpose
Analyze an important decision and record it in an immutable, traceable way.

## Input
- Decision topic ("I need to decide on [topic]")
- Context: why now, who is pushing for it, known constraints

## Steps
1. **Define the problem**: what is the real question? Why does it matter now?
2. **Check precedents**: search `direzione/decisions/` and `system/wiki/` for related decisions.
   Never contradict a recent decision without making explicit what changed.
3. **Identify 2-3 concrete options**. For each, evaluate:
   - pros / cons · effort and resources · impact (strategy, product, team, cash)
   - risks and mitigations · **reversibility** (two-way or one-way door?)
4. **Preventive handoffs if data is needed**: estimate → `cto`, feature evaluation → `product`,
   economic impact → `finance`. No decision on made-up data.
5. **Recommend** one option with explicit rationale.
6. **Next steps**: who does what, by when. **Review date**: when we reassess.
7. Save and commit `[ceo] decision: {slug}`.

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: decision
date: YYYY-MM-DD
status: active
review-date: YYYY-MM-DD
---
# DEC — {title}

## Context           ## Options considered
## Decision          ## Rationale
## Consequences and accepted risks
## Follow-up (owner + deadline)
```

## Destination
`direzione` zone → `decisions/YYYY-MM-DD-{slug}.md`. **Immutable**: superseded by a
new decision that cites the previous one.
