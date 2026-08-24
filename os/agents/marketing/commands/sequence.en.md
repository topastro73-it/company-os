# /marketing sequence — Email nurture sequence

## Purpose
Build an email sequence that warms up a segment over time (nurture), complementary
to sales outbound (which belongs to Sales).

## Input
- Target segment (from `config/company.yaml`) · goal (cold to warm,
  reactivation, content onboarding) · entry trigger (download, event, list)

## Steps
1. Load the segment's ICP, available content to reuse (`marketing/content/index.md`),
   learnings on opens/replies.
2. **Design the sequence**: 4-7 emails over 3-6 weeks; each email = one single message,
   one single piece of valuable content, one single CTA. Progression: problem → deep dive
   → social proof → value offer (assessment, demo).
3. Write each email: subject line (≤50 characters, no clickbait), short body,
   personalization variables `{nome}`, `{azienda}`, `{pain}`.
4. **Exit criteria**: reply or qualifying click → handoff `sales` (opportunity);
   sequence end with no signals → cold list.
5. **Verify claims and compliance** (shipped features, practices we follow, GDPR: legal
   basis for the contact and unsubscribe always present).
6. Actual activation (ESP/HubSpot) follows PREPARE → APPROVE → EXECUTE.

## Output format
```markdown
---
zone: marketing
tier: 🟡
type: sequence
segment: {segmento}
---
# Nurture — {segmento} — {goal}

| # | Day | Subject | Key message | Linked content | CTA |
|---|---|---|---|---|---|

## Email 1
{text with variables}
…
## Exit criteria and metrics (open, click, reply target)
```

## Destination
Zone `marketing` → `email-templates/nurture-{segmento}.md`.
Commit (admin): `[marketing] sequence: nurture {segmento}`.

## Handoff
Qualified lead → `sales` (`/sales opportunity`) · cold outbound sequences → `sales`
(`/sales outbound`, which reuses these templates).
