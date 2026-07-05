# /sales opportunity — Deal drill-down and update

## Purpose
Create or update a single opportunity: stage, activities, blockers, closing.

## Input
- `opp-slug` (= `{account}-{progetto}`) or a natural-language instruction
  (e.g. "move acme-pilot to negotiation", "log today's call", "block on NDA owner M.R.")

## Steps
1. **Create**: new file from the opportunity template; fill in the frontmatter (`account`, `segment`
   ∈ telco-tier1 | isp-tier2 | msp-mssp | vendor-channel | tic, `stage`, `value-gross`,
   `owner-sales`, `opened` and `last-activity` = today). Add the row to the account's
   opportunity index (`commerciale/accounts/{slug}.md`).
2. **Move stage**: update `stage`, **recalculate** `probability` (stage map) and
   `value-weighted`; `last-activity` = today; entry in Timeline.
3. **Log activity**: `last-activity` = today + entry in Timeline (who, what, outcome, next step).
4. **Blockers**: add/resolve entry in `blockers:` (what/owner/since/due/severity);
   `status-flag: blocked` if at least one blocker is open.
5. **Close**: `stage: won|lost`, clear open blockers, record the outcome in Timeline.
   If **won** → handoff `delivery` (new-partner) and `finance` (invoicing).
6. After every change: regenerate the board (`/sales board`) or flag that it is stale.

## Output format (opportunity frontmatter)
```yaml
---
zone: commerciale
tier: 🟡
type: opportunity
account: {slug}
segment: isp-tier2
stage: negotiation          # probability DERIVED: 20/30/40/60/80/100/0
probability: 60
value-gross: 48000
value-weighted: 28800
owner-sales: {persona}
opened: YYYY-MM-DD
last-activity: YYYY-MM-DD
next-step: "…"
next-step-due: YYYY-MM-DD
blockers: []
hubspot-id: ""
---
```

## Destination
`commerciale` zone → `opportunities/{opp-slug}.md`.
Commit (admin): `[sales] opportunity: {opp-slug} — {action}`.
