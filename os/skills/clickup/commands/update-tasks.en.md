# ClickUp Command: update-tasks

Updates existing ClickUp tasks: status, comments, priority, assignee. Always with approval.

## Authorized agents

PM, CTO, Chief of Staff

## Required input

Various ways to invoke:

```bash
# Update a single task
/product clickup update-tasks abc123 --status "in progress"
/product clickup update-tasks abc123 --priority high --assignee "Mario Rossi"
/product clickup update-tasks abc123 --comment "Blocked by dependency on def456"

# Batch update from file
/product clickup update-tasks --from-file company/prodotto/clickup-updates.md

# Update all tasks linked to a spec
/product clickup update-tasks --from-spec company/prodotto/specs/{nome-spec}.md
```

## Phase 1: PREPARE

### 1.1 Collect the changes

For each task to update, read the current state:

```
clickup_get_task(task_id: "{TASK_ID}", workspace_id: "<workspace-id>")
```

Compare against the requested changes.

### 1.2 Generate the approval file

Save to `company/prodotto/clickup-pending/YYYY-MM-DD-update-tasks.md`:

```markdown
# ClickUp Update — Approval required
Date: YYYY-MM-DD

## Proposed changes

| # | Task ID | Field | Current value | New value |
|---|---------|-------|---------------|-------------|
| 1 | abc123 | Status | to do | in progress |
| 2 | abc123 | Assignee | — | Mario Rossi |
| 3 | def456 | Priority | low | high |
| 4 | ghi789 | Comment | — | "Blocked by def456, expected Wednesday" |
| 5 | jkl012 | Status | in progress | complete |

## Notes
{Reason for the updates if specified}

## Confirmation
To approve: `/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-update-tasks.md`
```

## Phase 2: APPROVE

The user runs:
```
/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-update-tasks.md
```

## Phase 3: EXECUTE

For each row of the approved file, in order:

**Status/priority/assignee update**:
```
clickup_update_task(
  task_id: "abc123",
  status: "in progress",
  priority: "high",
  workspace_id: "<workspace-id>"
)
```

For assignee, resolve the name first:
```
clickup_resolve_assignees(assignees: ["Mario Rossi"], workspace_id: "<workspace-id>")
```
Then:
```
clickup_update_task(
  task_id: "abc123",
  assignees: ["{resolved_user_id}"],
  workspace_id: "<workspace-id>"
)
```

**Adding a comment**:
```
clickup_create_task_comment(
  task_id: "abc123",
  comment_text: "Comment text",
  workspace_id: "<workspace-id>"
)
```

### Log

```
✓ abc123: Status → in progress
✓ abc123: Assignee → Mario Rossi
✓ def456: Priority → high
✓ ghi789: Comment added
✗ jkl012: Status "complete" not available — skipping
```

### Post-execution

1. Move the file from `clickup-pending/` to `clickup-done/`
2. If the updates derive from a spec, update the spec with the current state
3. Commit: `[product] clickup: update-tasks — N task aggiornati`

## Typical use cases

### End of sprint
```
/cos clickup update-tasks --status complete abc123 def456 ghi789
```

### Bulk assignment
```
/product clickup update-tasks --assignee "Mario Rossi" abc123 def456 ghi789
```

### Priority escalation
```
/product clickup update-tasks abc123 --priority urgent --comment "Escalated by CEO — impacts customer demo on Friday"
```
