# ClickUp Command: sync-roadmap

Reads `company/prodotto/roadmap.md` and creates or updates an Epic task on ClickUp for each roadmap feature.

## Authorized agents

PM, CTO

## Required input

```
/product clickup sync-roadmap
```

Optionally with a quarter filter:
```
/product clickup sync-roadmap Q1-2026
```

## Phase 1: PREPARE

### 1.1 Read the roadmap

Load `company/prodotto/roadmap.md`. For each feature/initiative extract:

- **Feature name** → name of the Epic task
- **Description** → markdown_description of the Epic task
- **Quarter/Milestone** → included in the Epic description (not as a tag)
- **Status** → mapped to ClickUp status (see mapping below)
- **Owner/Team** → Assignee (use `clickup_resolve_assignees` to resolve names)
- **Priority** → mapped from roadmap position or explicit field

Roadmap status → ClickUp status mapping:
| Roadmap | ClickUp Status |
|---------|---------------|
| planned | to do |
| in-progress | in progress |
| shipped | complete / done |
| cut | closed |

### 1.2 Compare against existing ClickUp

Before creating, search for existing Epics with tag `from-companyos` in the Epic list:

```
clickup_filter_tasks(
  tags: ["from-companyos"],
  list_ids: ["<list-id-epic>"],
  workspace_id: "<workspace-id>"
)
```

For each roadmap feature:
- If a task with a matching name already exists → **UPDATE** (do not duplicate)
- If it does not exist → **CREATE**

### 1.3 Generate the approval file

Save to `company/prodotto/clickup-pending/YYYY-MM-DD-sync-roadmap.md`:

```markdown
# ClickUp Sync — sync-roadmap — Approval required
Date: YYYY-MM-DD
Source: company/prodotto/roadmap.md
Filter: Q1-2026 (or "all quarters")

## Proposed actions

| # | Action | Summary | Quarter | Priority | Notes |
|---|--------|---------|---------|----------|------|
| 1 | CREATE | "Feature A" | Q1-2026 | high | New |
| 2 | CREATE | "Feature B" | Q2-2026 | normal | New |
| 3 | UPDATE | "Feature C" (ID: abc123) | Q1-2026 | high | Update priority and tags |
| 4 | SKIP | "Feature D" | Q3-2026 | low | Already up to date, no changes |

## Standard tags
`from-companyos`, `{quarter}` (e.g. Q1-2026)

## Confirmation
To approve: `/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-sync-roadmap.md`
```

## Phase 2: APPROVE

The user runs:
```
/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-sync-roadmap.md
```

## Phase 3: EXECUTE

For each row of the approved file:

**CREATE**:
```
clickup_create_task(
  name: "Feature Name",
  list_id: "<list-id-epic>",
  markdown_description: "...",
  priority: "high",
  tags: ["from-companyos"],
  workspace_id: "<workspace-id>"
)
```

The `markdown_description` of each Epic must be **self-consistent**: the dev must find in the task all the context needed to understand what to build without looking for other documents. Minimum structure:

```
## Context
[Why this feature exists, problem it solves, flywheel pillar (ATTRACT/ENGAGE/MANAGE/GROW)]

## Objective
[What must be true when the epic is completed]

## Users involved
[Your product's user roles — e.g. Partner / Partner's salesperson / End customer]

## Scope
[IN scope. OUT scope.]

## Target
[Target quarter/milestone, e.g. "Q2 2026 — non-negotiable"]

## Technical notes / Dependencies
[Prerequisites, architectural constraints]

## Spec link
[company/prodotto/specs/{nome}.md]
```

**UPDATE**:
```
clickup_update_task(
  task_id: "abc123",
  priority: "high",
  status: "in progress",
  workspace_id: "<workspace-id>"
)
```

### Post-execution

1. Update `company/prodotto/roadmap.md`: for each feature created/updated, add the field `clickup-epic: {task_id}`
2. Move the approval file to `clickup-done/`
3. Commit: `[product] clickup: sync-roadmap → N epic creati, M aggiornati`

## Notes

- Never delete Epic tasks, even if the feature is removed from the roadmap
- If a feature is "cut", update the status to "closed" (if available)
- The task name must match the feature name in the roadmap exactly to avoid duplicates
