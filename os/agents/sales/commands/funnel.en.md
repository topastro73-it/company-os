# /sales funnel — Segment funnel

## Purpose
Maintain the consolidated target list for the segments declared in
`config/company.yaml`: who is active, who is warm, who is cold,
and what to do next for each.

## Input
- None (read/report) or updates ("move {company} to warm", "add {list}")

## Steps
1. Load `commerciale/target-funnel.md` — the consolidated target list.
2. **Classify** each target:
   - **Active**: conversation in progress → a linked opportunity must exist
   - **Warm**: reply/interest but not qualified → next touch planned
   - **Cold**: never contacted or sequence exhausted with no reply → outbound candidate
3. **Consistency with the cockpit**: every "active" without an opportunity → create it (`/sales opportunity`);
   every open opportunity whose account is not in the funnel → add it.
4. **Warm aging**: warm with no touch for >14 days → flag, propose the next touch.
5. **Report**: numbers per band, movements since the last update, next actions
   per owner (who contacts whom, by when).

## Output format
```markdown
---
zone: commerciale
tier: 🟡
type: funnel
updated: YYYY-MM-DD
---
# Segment Funnel — {YYYY-MM-DD}

## Summary: active {n} · warm {n} · cold {n} · cold→warm→active conversions this month

## Active   | Company | Opportunity | Stage | Owner | Next step |
## Warm     | Company | Last touch | Interest | Next touch (date) | Owner |
## Cold     | Company | Segment | List source | In sequence? |

## Next actions (owner + deadline)
```

## Destination
`commerciale` zone → `target-funnel.md` (in-place update).
Commit (admin): `[sales] funnel: update {YYYY-MM-DD}`.

## Handoff
Batch of cold targets to activate → `/sales outbound`; qualified active → `/sales opportunity`.
