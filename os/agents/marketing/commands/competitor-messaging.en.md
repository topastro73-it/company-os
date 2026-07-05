# /marketing competitor-messaging — Counter-positioning

## Purpose
Analyze how a competitor positions itself and define our counter-positioning,
for public messaging and for the sales battlecard.

## Input
- Competitor · available sources (website, public pricing, content, what prospects
  say in calls)

## Steps
1. Load our positioning (`marketing/brand/`) and the existing battlecard
   (zone `commerciale/battlecards/`), plus the objections reported from the field.
2. **Analyze their messaging**: who they speak to (segment), main promise, proof
   they bring, communicated pricing/packaging, where they are strong and where they are vague.
3. **Counter-positioning**: where we truly win (with our own proof: certifications,
   white-label model, SMB focus via partners) — never disparage, position on strengths;
   where we do NOT win → how we qualify the fit instead of fighting.
4. Double output:
   - public messaging (how we talk about it without naming them, usually)
   - input for the sales battlecard (ready-made phrases for objections "but {competitor} does X")
5. Every comparative claim → verifiable; no comparisons based on hearsay.

## Output format
```markdown
---
zone: marketing
tier: 🟡
type: competitor-messaging
competitor: {slug}
---
# Messaging vs {Competitor} — {YYYY-MM-DD}

## Their positioning (segment, promise, proof, pricing)
## Where we win (with proof) / Where we don't win (how to qualify)
## Public counter-messaging
## Ready-made phrases for Sales (objection → response)
```

## Destination
Zone `marketing` → `brand/messaging-vs-{competitor}.md`.
Commit (admin): `[marketing] messaging: vs {competitor}`.

## Handoff
Battlecard update → `sales` (zone `commerciale/battlecards/`) · real product gap
surfaced → `product`.
