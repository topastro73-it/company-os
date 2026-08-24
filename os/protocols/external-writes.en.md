# External writes — PREPARE → APPROVE → EXECUTE

Every **write to an external system** goes through three mandatory phases, with explicit
human approval in the middle. It applies to: ClickUp (tasks, epics, docs), HubSpot (CRM), Gmail
(even just drafts), Drive publish to third parties (`per-commercialista/`, `evidence/`, shares),
Calendar, and any future integration. **Reads** are unrestricted.

## Phase 1 — PREPARE

The agent analyzes the input (spec, roadmap, pipeline, email thread) and generates a **staging
file** with the complete list of proposed actions. The file goes in the relevant zone:

| System | Staging | Executed log |
|---|---|---|
| ClickUp | `company/prodotto/clickup-pending/` (Drive: `30-Prodotto/clickup-pending/`) | `company/prodotto/clickup-done/` |
| HubSpot | `company/commerciale/hubspot-pending/` | `company/commerciale/hubspot-done/` |
| Gmail (drafts/sends) | `company/{zona}/mail-pending/` of the content's zone | `company/{zona}/mail-done/` |
| Publish to third parties | `company/{zona}/publish-pending/` | `company/{zona}/publish-done/` |

Naming: `YYYY-MM-DD-{comando}.md` (e.g. `2026-07-04-sync-spec-bulk-import.md`).

### Approval file format

```markdown
---
zone: prodotto
tier: 🟡
system: clickup            # clickup | hubspot | gmail | drive-publish
command: sync-spec         # command that generated the staging
status: pending            # pending | approved | executed | cancelled
---
# {System} — Approval required
Date: YYYY-MM-DD · Agent: {slug} · Source: {spec/pipeline/thread file}

## Proposed actions

| # | Type | Object | Details |
|---|------|---------|---------|
| 1 | CREATE Task | "Task name" | List: Feature, Priority: High, Status: Backlog |
| 2 | UPDATE Task | TASK-123 | Status: In Progress → Done |
| 3 | CREATE Draft | to: {recipient} | Subject: "Pilot annex", attachment: … |

## Confirmation
Review the actions, then: `/{agente} approve {path-del-file}`. To cancel: status → cancelled.
```

Each row must be detailed enough to evaluate the action **without opening the external
system**. Quoted data (thresholds, ACs, amounts, recipients) verified against the source in the repo/zone
— never copied from stale versions, never invented: if a data point is missing, flag the gap instead of filling it in.

## Phase 2 — APPROVE

A human reviews the file and approves explicitly (`approve` command or chat confirmation on the
specific file). Rules:
- **Never execute without explicit approval** — a generic "ok" about something else does not count
- Partial approval: the human deletes/comments the unwanted rows; the rest is executed
- File older than 7 days → re-validate the data before executing (PREPARE again if needed)

## Phase 3 — EXECUTE

The agent executes the approved actions via MCP, in the file's order:
1. Each executed action is marked in the file with outcome and created ID (e.g. `→ done, task TASK-456`)
2. Error on an action → note it, continue with the next ones, report the final tally
3. When done: `status: executed`, file moved to the corresponding `*-done/` folder
4. Summary in chat: successful/failed actions, links to created objects

## MCP not available

The flow does not block: PREPARE completes anyway, the file stays in `*-pending/` and you
flag "external system unavailable — file ready, will execute at the next startup with MCP active".
When the tool returns, resume from Phase 2 (or 3 if already approved and still fresh).
