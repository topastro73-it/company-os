# ClickUp Command: sync-ceo-actions

Syncs pending decisions, actions to do and follow-ups to the CEO's personal ClickUp list.

## Authorized agents

- Chief of Staff

## Required input

```
/cos sync-ceo-actions
/cos sync-ceo-actions [fonte]
```

Optional sources: `daily-briefing`, `action-plan`, `follow-up-tracker`, `decision-review`, `status-check`. If not specified, scan all sources.

## Target list

```yaml
list_id: "<list-id-ceo-personal>"
list_name: Personal List
space: <workspace-name>
```

---

## Phase 1: PREPARE

### Step 1 — Scan the sources

Read and analyze the following sources from the repo to extract actionable items for the CEO:

| Source | File | What to look for |
|-------|------|--------------|
| Pending decisions | `company/direzione/decisions/*.md` | Decisions with `status: open` or `status: pending` |
| Overdue follow-ups | `company/direzione/decisions/*.md`, `company/direzione/reports/follow-ups-*.md` | Open checkboxes `- [ ]` with CEO owner or no owner |
| P0/P1 actions | `company/direzione/reports/action-plan-*.md` | Actions with CEO owner or requiring CEO approval |
| Stale specs | `company/prodotto/specs/INDEX.md` | Specs with an expired status check (see protocol in CLAUDE.md) |
| Briefing urgencies | `company/direzione/reports/briefing-*.md` (most recent) | Items flagged as urgent/P0 |
| Roadmap blockers | `company/prodotto/roadmap.md` | Blocked items requiring a CEO decision |

### Step 2 — Check for duplicates on ClickUp

Before proposing the creation of a task, search the CEO Personal list for an existing task with a similar name:

```
clickup_filter_tasks(list_id: "<list-id-ceo-personal>")
```

If a task with the same (or very similar) title already exists:
- If it is `open` / `to do` / `in progress` → **SKIP** (already present)
- If it is `closed` / `done` → **CREATE** new (the decision/action is recurring or new)

### Step 3 — Classify each item

Each extracted item is classified with:

| Field | Rule |
|-------|--------|
| **Type** | `decision` · `action` · `follow-up` · `review` · `blocker` |
| **Priority** | `urgent` if P0 or overdue, `high` if P1 or within the next 3 days, `normal` otherwise |
| **Due date** | Deadline date if present in the source, otherwise empty |
| **Tag** | `from-companyos` + `ceo-action` + type tag (e.g. `decision`, `follow-up`) |

### Step 4 — Generate the approval file

Save to `company/prodotto/clickup-pending/YYYY-MM-DD-sync-ceo-actions.md`:

```markdown
---
command: sync-ceo-actions
date: YYYY-MM-DD
status: pending-approval
source: [list of scanned sources]
---

# ClickUp Sync — CEO Actions — Approval required

Date: YYYY-MM-DD
Target list: CEO Personal (<list-id-ceo-personal>)

## Proposed actions

| # | Type | Title | Priority | Due | Source | Action |
|---|------|--------|----------|-----|-------|--------|
| 1 | decision | "Decide Enterprise pricing tier" | urgent | 2026-03-25 | decisions/2026-03-20-pricing.md | CREATE |
| 2 | follow-up | "Review bulk-import spec (expired)" | high | — | specs/INDEX.md | CREATE |
| 3 | action | "Approve Q2 sprint planning" | normal | 2026-03-28 | reports/action-plan.md | SKIP (already in ClickUp) |

## Summary

- CREATE: N tasks
- SKIP: N tasks (already present)
- Total sources scanned: N

## Confirmation

Review the actions above, then run:
`/cos clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-sync-ceo-actions.md`
```

**Commit**: `[cos] clickup: prepare sync-ceo-actions — N azioni proposte`

---

## Phase 2: APPROVE

The user reviews and confirms:
```
/cos clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-sync-ceo-actions.md
```

The user can edit the file before approving (remove rows, change priority, add due dates).

---

## Phase 3: EXECUTE

### For each row with a CREATE action

Create the task in the CEO Personal list:

```
clickup_create_task(
  list_id: "<list-id-ceo-personal>",
  name: "[TYPE] Title",
  markdown_description: "## Context\n\n{description from the repo}\n\n---\n\n## Source\n\n{source file path}\n\n---\n\n## Required action\n\n{what the CEO must do}",
  priority: {mapped priority},
  due_date: {timestamp if present},
  tags: ["from-companyos", "ceo-action", "{tipo}"]
)
```

**Task name format**: `[DECISION] Title`, `[ACTION] Title`, `[FOLLOW-UP] Title`, `[REVIEW] Title`, `[BLOCKER] Title`

**Description format** (use `markdown_description` with real newlines):

```markdown
## Context

Brief context extracted from the source (2-3 lines max).

---

## Source

`decisions/2026-03-20-pricing.md`

---

## Required action

- [ ] What the CEO must concretely do
```

### Execution log

For each task created, show:
```
✅ #1 — [DECISION] Decide Enterprise pricing tier → task_id: abc123
✅ #2 — [FOLLOW-UP] Review bulk-import spec → task_id: def456
⏭️ #3 — SKIP (already present as task xyz789)
```

### Post-execution

1. Update the file frontmatter: `status: executed`, add `executed_date` and the list of created task IDs
2. Move the file to `company/prodotto/clickup-done/`
3. **Commit**: `[cos] clickup: sync-ceo-actions — N task creati su CEO Personal`

---

## Bidirectional sync: ClickUp → Repo

When invoked, the command also performs a **reverse sync**: it reads the tasks completed on ClickUp and updates the corresponding files in the repo.

### Step 1 — Read completed tasks from ClickUp

Filter tasks in the CEO Personal list with tag `from-companyos` and status `complete` / `closed` / `done`:

```
clickup_filter_tasks(list_id: "<list-id-ceo-personal>", tags: ["from-companyos"], statuses: ["complete", "closed", "done"])
```

### Step 2 — For each completed task, identify the source

From the task description, extract the **Source** path (the `## Fonte` field in the description). This indicates the repo file to update.

### Step 3 — Update the repo based on the task type

| Task type | Repo file | Update |
|-----------|-----------|---------------|
| `[DECISION]` | `company/direzione/decisions/*.md` | Update frontmatter: `status: decided`, add `decided-date: YYYY-MM-DD` if not present |
| `[ACTION]` | Source file indicated | Mark checkboxes as completed `- [x]`, update `status` if present in the frontmatter |
| `[FOLLOW-UP]` | Source file indicated | Mark follow-up checkboxes as completed `- [x]` |
| `[REVIEW]` | `company/prodotto/specs/*.md` | Update frontmatter: `last-status-check: YYYY-MM-DD`, update `status` if the CEO indicated a new status in the ClickUp task comment |
| `[BLOCKER]` | Source file indicated | Update the blockers section (remove/mark as resolved), update `status` if present |

**PRD/spec update rules**:
- Read the ClickUp task **comments** (`clickup_get_task_comments`) to understand the outcome (e.g. "approved", "deferred", "shipped")
- If the comment indicates a status change → update the spec's frontmatter `status` (e.g. `approved` → `in-development`, `in-development` → `shipped`)
- Always update `last-updated: YYYY-MM-DD` in the frontmatter
- Update `company/prodotto/specs/INDEX.md` accordingly

**Decision update rules**:
- If the decision had `status: open` or `status: pending` → update to `status: decided`
- Read the task comments to extract the decision outcome and add it to the `outcome` field if present in the template

### Step 4 — Generate the updates report in the approval file

Add a section to the approval file with the proposed repo updates:

```markdown
## Repo updates from completed tasks

| # | ClickUp Task | Repo file | Proposed update |
|---|-------------|-----------|----------------------|
| 1 | abc123 — [DECISION] Pricing | decisions/2026-03-20-pricing.md | status: open → decided, decided-date: 2026-03-22 |
| 2 | def456 — [REVIEW] Spec bulk-import | company/prodotto/specs/prd-bulk-import.md | status: approved → in-development, last-updated: 2026-03-22 |
| 3 | ghi789 — [FOLLOW-UP] Onboarding check | company/direzione/reports/follow-ups-2026-03.md | 2 checkboxes marked as completed |
```

**These repo updates follow the same PREPARE → APPROVE → EXECUTE flow**: they are executed only after explicit CEO approval.

### Step 5 — Executing repo updates (post-approval)

After approval, for each row in the "Repo updates" section:
1. Read the repo file
2. Apply the changes (frontmatter, checkboxes, status)
3. Update `company/prodotto/specs/INDEX.md` if specs were modified
4. Commit: `[cos] clickup: sync-repo-from-completed — N file aggiornati`

---

## Completed tasks cleanup (repo → ClickUp)

When invoked, the command also checks the existing tasks in the CEO Personal list with tag `from-companyos`:
- If the decision has been made (file in `decisions/` has `status: decided`) → flag as completable
- If the follow-up has been done (checkboxes completed in the repo) → flag as completable

These tasks are listed at the end of the approval file as an optional section:

```markdown
## Completable tasks (optional)

| Task ID | Title | Reason | Suggested action |
|---------|--------|--------|-----------------|
| abc123 | [DECISION] Pricing | Decision made on 2026-03-22 | CLOSE |
```

---

## Error handling

- If the CEO Personal list is not accessible → clear error, suggest verifying the list ID
- If `clickup_create_task` fails → log the error, continue with the next tasks, report the failures in the summary
- If there are no items to sync → still generate the report but with the message "No pending actions for the CEO"
