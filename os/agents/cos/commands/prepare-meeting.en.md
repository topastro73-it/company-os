# /cos prepare-meeting — Pre-meeting brief

## Purpose
Arrive at every meeting with background, sourced data, open questions, and an agenda.

## Input
- Topic · participants (internal/external) · goal (decision, alignment, discovery, update)
- Date and expected duration

## Steps
1. **Identify the meeting** and what it must produce.
2. **Load the right context** based on the topic:
   - client/partner → `clienti/{slug}/` (account file, QBR, proposals) + opportunities in `commerciale`
   - product/tech → `prodotto` (roadmap, specs, relevant ADRs)
   - strategic → `direzione` (vision, OKRs, recent decisions)
   - investor → `vault/finance` + `direzione/investor-updates/` (admin only)
   - always: `direzione/decisions/` for open decisions on the topic
3. **Build the brief**: background (3-5 points with references), key data (every number
   with a source), open questions (with possible answers and pros/cons), 2-4 possible outcomes
   with implications.
4. **Agenda** in time slots: topic, discussion owner, goal of the slot.
5. If meeting with an active partner: re-read the history (wiki entity / account file) —
   do not restart conversations that already happened.

## Output format
```markdown
---
zone: {direzione | clienti/{slug}}
tier: 🟡
type: meeting-brief
---
# Meeting Prep — {topic} — {date}
**Participants**: … · **Goal**: … · **Duration**: …

## Background        ## Key data (with sources)
## Open questions    ## Possible outcomes
## Agenda | Slot | Topic | Owner | Goal |
## Post-meeting: follow-ups to track (fill in afterwards)
```

## Destination
Internal/strategic meeting → zone `direzione/briefing/meeting-{slug}-{data}.md`.
Meeting with a client → zone `clienti/{slug}/meeting-prep-{data}.md`.
