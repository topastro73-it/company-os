# /marketing content-plan — Editorial plan

## Purpose
Plan the period's content with measurable goals, not publish at random.

## Input
- Period (month/quarter) · realistic capacity (how many pieces we can actually produce)

## Steps
1. Load ICP and segments (zone `commerciale`), roadmap/releases (zone `prodotto`),
   recurring objections from the field, existing content (`marketing/content/index.md` —
   don't redo what's there, update or relaunch it).
2. **Identify the themes**: segment pains (NIS2 for SMBs, revenue for partners),
   upcoming releases (only shipped or certain), recurring keywords/questions.
3. **Map onto the funnel**: Awareness → Consideration → Decision; balance thought
   leadership, product content, case studies, SEO plays. Every piece serves a segment
   and a stage — if you don't know who it serves, it doesn't go in the plan.
4. For each piece of content: working title, format (blog, LinkedIn, email, one-pager),
   target persona, keyword, CTA, date, owner, success metric.
5. **Compliance check** on security topics: we only recommend what we do ourselves.
6. Update `marketing/content/index.md` with the planned pieces.

## Output format
```markdown
---
zone: marketing
tier: 🟡
type: content-plan
period: {periodo}
---
# Content Plan — {periodo}

## Goals for the period (measurable)
## Calendar
| Date | Title | Format | Persona | Funnel stage | Keyword | CTA | Metric |
|---|---|---|---|---|---|---|---|
## Idea backlog (not planned)
```

## Destination
Zone `marketing` → `content/plan-{periodo}.md`.
Commit (admin): `[marketing] plan: content {periodo}`.

## Handoff
Enablement pieces → `sales` · release-related pieces → `/marketing launch-plan`.
