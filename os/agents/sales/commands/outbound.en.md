# /sales outbound — Outbound / ABM sequence

## Purpose
Create or update an outbound sequence for a funnel segment
(the real segments are declared in `config/company.yaml`).

## Input
- Target segment (from `zones/_root/context/` ICP) · goal (meeting, free trial/evaluation)
- Target list (from `commerciale/target-funnel.md`) · channel (email, LinkedIn, phone)

## Steps
1. Load the funnel (`commerciale/target-funnel.md`) and the active outbound learnings.
2. **Define the sequence**: 4-6 touches over 2-3 weeks, alternating channels.
   For each touch: day, channel, goal, message (personalizable with variables
   `{azienda}`, `{pain}`, `{trigger}`).
3. **Message**: speak to the segment's problem — its buying driver
   (regulatory, e.g. a directive such as NIS2; or cost, risk or growth) —
   a single CTA per touch, zero unsupported claims, zero unshipped features.
4. **Exit criteria**: reply → move to opportunity (`/sales opportunity` in discovery);
   no reply after the full sequence → nurture/cold in the funnel.
5. Save the sequence; the **actual send** (Gmail/HubSpot) is an external write:
   PREPARE (drafts) → APPROVE (human review) → EXECUTE. Never automatic sends.
6. Track results per touch (sent/open/reply) to iterate.

## Output format
```markdown
---
zone: commerciale
tier: 🟡
type: sequence
segment: segment-a
---
# Sequence — {segment} — {goal}

| # | Day | Channel | Goal | Subject/hook |
|---|---|---|---|---|

## Touch 1 — {channel}
{text with variables}
…
## Exit criteria and metrics
```

## Destination
`commerciale` zone → `sequences/{segmento}-{slug}.md`.
Commit (admin): `[sales] outbound: sequence {segment}`.

## Handoff
Copy to refine or long-term nurture → `marketing` (`/marketing sequence`).
