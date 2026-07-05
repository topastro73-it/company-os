# /sales proposal — Commercial proposal

## Purpose
Generate a personalized proposal that speaks to the customer's problems, not our features.

## Input
- Account/prospect · linked opportunity (if it exists) · assumed tier/pricing
- Context: pain points that emerged, stakeholders, requirements (e.g. required certifications)

## Steps
1. Load the context: opportunity and account from the `commerciale` zone, customer history
   from `clienti/{slug}/` if it exists, value proposition from `zones/_root/context/`.
2. **Personalize**: open on THEIR problems (from discovery), not on the product.
3. Structure: Executive Summary → Problem → Proposed solution → Why us
   (certifications from the `compliance` zone, social proof, relevant cases) → Pricing →
   Next steps with dates.
4. **Pricing**: use the appropriate tier, clear and transparent. Discount → CEO OK required first.
5. **Feature check**: everything you promise is shipped or on the confirmed roadmap; anything else
   goes through `/product evaluate-request` BEFORE entering the proposal.
6. Draft → internal review → final version in the customer's folder with `render: gdoc`
   (publish converts it into a commentable Google Doc).
7. Update the opportunity: stage → `proposal-sent` (probability 40 recalculated), Timeline.

## Output format
```markdown
---
zone: clienti/{slug}
tier: 🟡
type: proposta
render: gdoc
opportunity: {opp-slug}
---
# Proposal — {Customer} — {date}
## Executive Summary   ## Your context and problem
## Proposed solution   ## Why us
## Investment          ## Next steps
```

## Destination
Draft: `commerciale` zone → `proposte-bozze/{opp-slug}-vN.md`.
Delivered final: `clienti/{slug}` zone → `proposta-{YYYY-MM-DD}.md`.
Sending to the customer (email/Drive share) follows PREPARE → APPROVE → EXECUTE.
