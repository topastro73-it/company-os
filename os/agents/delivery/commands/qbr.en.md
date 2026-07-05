# /delivery qbr — Quarterly Business Review

## Purpose
Prepare a partner's QBR: quarter results, plan for the next one, expansion.

## Input
- Partner slug · quarter (e.g. Q3-2026) · date of the QBR call

## Steps
1. Load the partner card, health history, quarter metrics (SMBs onboarded/active,
   churn, revenue generated, salespeople engagement).
2. **Results vs target**: table metric → target → actual → delta. Real data,
   sources cited.
3. **Wins and highlights**: max 5, concrete (deals closed via platform, SMBs protected).
4. **Improvement areas**: max 3, with a shared action proposal — never a purely
   celebratory QBR.
5. **Next quarter plan**: joint objectives, actions, owners (ours and theirs).
6. **Expansion**: only if health ≥70 — tier upgrade or additional services with potential
   revenue; otherwise omit the section.
7. Prepare the **talking points** for the call and the questions to ask the partner.
8. After the call: record outcomes and follow-ups in the partner card.

## Output format
```markdown
---
zone: clienti/{slug}
tier: 🟡
type: qbr
render: gdoc
quarter: {Q}
---
# QBR — {Partner} — {Q}

## Quarter results (metrics vs target)
## Wins and highlights          ## Improvement areas
## {Q+1} plan (objectives, actions, owners)
## Expansion (if health ≥70)
## Talking points for the call
```

## Destination
`clienti/{slug}` zone → `qbr-{Q}.md` (`render: gdoc` → the publish creates the Google Doc
shareable with the partner, gated by the external-writes protocol).
Commit (admin): `[delivery] qbr: {slug} {Q}`.

## Handoff
Confirmed expansion → `sales` (new opportunity) · requested features → `product`.
