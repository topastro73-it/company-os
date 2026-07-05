# ClickUp Command: sync-spec

Syncs a PRD/spec with ClickUp: creates 1 Epic task + N linked subtasks/tasks from the acceptance criteria.

## Authorized agents

PM, CTO

## Required input

```
/product clickup sync-spec company/prodotto/specs/{nome-spec}.md
```

Optionally to sync only a specific section:
```
/product clickup sync-spec company/prodotto/specs/{nome-spec}.md --section 6.6
```

## Phase 1: PREPARE

### 1.1 Read the spec

Load the indicated spec file. Extract:

- **Feature title** → becomes the name of the Epic task
- **Objective / Problem Statement** → becomes the description of the Epic task
- **User Stories** (format: "As a [role], I want [action], So that [benefit]") → become tasks in the Feature list
- **Acceptance Criteria** for each story → become subtasks of the story task
- **Priority** indicated in the spec → map to ClickUp priority (`urgent`/`high`/`normal`/`low`)
- **Milestone/Target** → included in the task description (not as a tag)

### 1.2 Check whether the Epic already exists

Search for existing tasks with tags `from-companyos` and `spec:{slug}` in the Epic list:

```
clickup_filter_tasks(tags: ["from-companyos", "spec:{slug}"], list_ids: ["<list-id-epic>"], workspace_id: "<workspace-id>")
```

If it exists: propose UPDATE (do not duplicate).
If it does not exist: propose CREATE.

### 1.3 Structure to generate

```
Epic (in list "Epic" <list-id-epic>): [Feature Title]
  └── self-consistent description (see rule below)

Task (in list "Feature" <list-id-feature>): [User Story 1]
  ├── self-consistent description (see rule below)
  └── linked to the Epic (dependency: waiting_on)

Task (in list "Feature" <list-id-feature>): [User Story 2]
  ├── self-consistent description
  └── linked to the Epic
```

**Note**: if the spec has a single feature/story with no epic-level separation, create a single Task in the Feature list (not Epic) with subtasks for the acceptance criteria.

### Fundamental rule: self-consistent descriptions

**Every task description (Epic, Feature, Subtask) must be completely self-sufficient.**

The dev who picks up the task must not: look up the PRD, ask the PM, read other files, or ask questions to understand what to build. They should just open the task and have all the context needed to start working.

**Rule 1 — Functional approach only, zero technical/architectural details.**
Descriptions describe the expected behavior from the user's and the product's point of view. Do not mention: DB field names, table names, endpoint names, architectural choices, technology stack. Those are dev/CTO decisions, not the PM's. If there is a technical dependency, describe it functionally ("this feature requires that data X is already available in the system") without specifying how it is implemented.

**Rule 2 — Critical data goes inside the task, not in external links.**
If the task needs specific data to be completed (e.g. scoring weights, calculation rules, thresholds, classification logic), that data must be copied into the task description. Do not write "the details are in the spec section X.Y" — the dev must not open other files. The spec link is only an optional additional reference, not a substitute for the content.

**Mandatory structure for every Epic task:**

```markdown
## Context
[Explain why this feature exists in the product: which problem it solves, for which user, where it fits in the flywheel (ATTRACT/ENGAGE/MANAGE/GROW)]

## Objective
[What must be true when this epic is completed — from the user's and the business's point of view]

## Users involved
[Who uses this feature: MSP Partner / Telco Salesperson / SMB end-customer]

## Scope
[What is IN scope. What is explicitly OUT of scope.]

## Functional dependencies
[Which other capabilities must already be operational for this epic to be developed — described functionally, not technically]

## Spec link (optional)
[company/prodotto/specs/{nome}.md]
```

**Mandatory structure for every Feature task (User Story):**

```markdown
## Context
[In 2-3 lines: why this story exists, which flow it fits into, what happens before and after from the user's point of view]

## User Story
As a [role], I want [action], so that [benefit].

## Acceptance Criteria
- [ ] AC 1: [verifiable behavior — written in terms of what the user sees/can do]
- [ ] AC 2: ...
- [ ] AC 3: ...

## Functional details
[Everything the dev needs to know to implement correctly: business rules, thresholds, calculation logic, corner cases, expected behaviors in edge cases. This data lives HERE, not in other documents.]
```

**It is not enough** to copy only the user story title or paste the acceptance criteria without context. The dev must understand *why* they are building this thing and have *all the necessary data* directly in the task.

### 1.4 Generate the approval file

Save to `company/prodotto/clickup-pending/YYYY-MM-DD-sync-spec-{slug}.md`:

```markdown
# ClickUp Sync — sync-spec — Approval required
Date: YYYY-MM-DD
Spec: company/prodotto/specs/{nome-spec}.md
Command executed by: [agent]

## Proposed structure

| # | Type | List | Parent | Summary | Priority | Tags |
|---|------|------|--------|---------|----------|------|
| 1 | Task (Epic) | Epic | — | "Feature Title" | high | from-companyos, spec:{slug} |
| 2 | Task | Feature | linked #1 | "User Story 1" | high | from-companyos, spec:{slug} |
| 3 | Subtask | Feature | #2 | "AC: The user can..." | normal | |
| 4 | Subtask | Feature | #2 | "AC: The system verifies..." | normal | |
| 5 | Task | Feature | linked #1 | "User Story 2" | normal | from-companyos, spec:{slug} |

## Tags
All tasks will have tags: `from-companyos`, `spec:{slug}`

## Notes
{Any notes or assumptions made during extraction}

## Confirmation
To approve: `/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-sync-spec-{slug}.md`
To cancel: delete or ignore this file.
```

Communicate to the user: "Approval file generated in `company/prodotto/clickup-pending/YYYY-MM-DD-sync-spec-{slug}.md`. Review and approve to proceed."

## Phase 2: APPROVE

The user runs:
```
/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-sync-spec-{slug}.md
```

The agent re-reads the file and asks for final confirmation: "I will create [N] tasks on ClickUp. Confirm? (yes/no)"

## Phase 3: EXECUTE

For each row of the approval file, in order:

1. **Create the Epic task** in the Epic list (`<list-id-epic>`):
   ```
   clickup_create_task(
     name: "Feature Title",
     list_id: "<list-id-epic>",
     markdown_description: "...",
     priority: "high",
     tags: ["from-companyos", "spec:{slug}"],
     workspace_id: "<workspace-id>"
   )
   ```
   Save the resulting task ID.

2. **Create the Feature task** in the Feature list (`<list-id-feature>`):
   ```
   clickup_create_task(
     name: "User Story 1",
     list_id: "<list-id-feature>",
     markdown_description: "## Description\n...\n\n## Acceptance Criteria\n...",
     status: "Backlog",
     priority: "high",
     tags: ["from-companyos", "spec:{slug}"],
     workspace_id: "<workspace-id>"
   )
   ```
   Save the task ID. **Status is always `Backlog`** — the move to To Do happens only during weekly planning.

3. **Link the Feature task to the Epic** with a dependency:
   ```
   clickup_add_task_link(task_id: "{feature_task_id}", links_to: "{epic_task_id}", workspace_id: "<workspace-id>")
   ```

4. **Create subtasks** (if needed) as children of the Feature task:
   ```
   clickup_create_task(
     name: "AC: ...",
     list_id: "<list-id-feature>",
     parent: "{feature_task_id}",
     priority: "normal",
     workspace_id: "<workspace-id>"
   )
   ```

### Execution log

Print each action to screen:
```
✓ CREATED Epic: abc123 — "Feature Title" (list: Epic)
✓ CREATED Task: def456 — "User Story 1" (list: Feature)
✓ LINKED: def456 → abc123
✓ CREATED Subtask: ghi789 — "AC: The user can..." (parent: def456)
✗ FAILED Subtask: "AC: The system..." — Error: 400 Bad Request
```

### Post-execution

1. Move the file from `clickup-pending/` to `company/prodotto/clickup-done/`
2. Append a final status to the file:
   ```
   ## Execution result
   Execution date: YYYY-MM-DD HH:MM
   Tasks created: N/M
   Epic task ID: abc123
   ```
3. Update the original spec by adding to the frontmatter: `clickup-epic: "[{epic_id}](https://app.clickup.com/t/{epic_id})"` — the field MUST contain the ID and the direct link to the epic on ClickUp. The epic lives in the Epics list (<list-id-epic>) of the Product Roadmap board, and is linked to the Feature tasks via a dependency of type `blocking` (Feature blocks Epic).
4. **Update the spec's "Implementation Status" section** with the created tasks:
   - For each task created, add or update the row in the Implementation Status table
   - Fields: Deliverable (task name), Status (`Not Started`), Owner (assignee if present), ClickUp Ref (task ID with link), Notes
   - If the Implementation Status section does not exist in the spec, create it following the template in `os/agents/product/templates/prd.md`
5. **Publish/update the spec on ClickUp Docs**:
   - Every spec has a **dedicated Doc** in the "Product Specs" Folder (ID: `<folder-id-specs>`)
   - The Doc name MUST be the spec title (e.g. `PRD — Assessment Report: Gap Analysis & Remediation Plan`), NOT a generic name
   - If the spec does not yet have a Doc (empty `clickup-doc:` field in the frontmatter) → create it with `clickup_create_document` (name = spec title, parent = `{"id": "<folder-id-specs>", "type": "5"}`, visibility = `PUBLIC`, create_page = `true`), then update the page with the markdown content without frontmatter
   - If the spec already has a Doc (`clickup-doc:` in the frontmatter) → update the existing page with `clickup_update_document_page` (full content replace)
   - Update the spec frontmatter with `clickup-doc: "[{doc_id}](https://app.clickup.com/<workspace-id>/v/dc/{doc_id})"`
   - This link is the one that goes in the References section of the ClickUp tasks, so the dev clicks and lands on the spec
6. Commit: `[pm] clickup: sync-spec {nome-spec} → Epic abc123 + N tasks`

### Bidirectional Spec ↔ ClickUp alignment rule

Every time an agent interacts with ClickUp tasks linked to a spec (sync-spec, update-tasks, read-board), it MUST keep the **Implementation Status** section of the source spec aligned:

- **Task creation** (sync-spec) → adds a row in Implementation Status with `Not Started`
- **Status change on ClickUp** (update-tasks) → updates the Status column in the spec (`Not Started` → `In Progress` → `Done` → `Blocked` → `Deferred`)
- **Board read** (read-board) → if it detects misalignments between ClickUp and the spec, flags them and proposes an update
- **Task deleted or moved** → updates the row with an explanatory note
- **Spec updated in the repo** (write-spec, manual edit) → re-publishes the content to the ClickUp Doc with `clickup_update_document_page`

This rule guarantees that the spec is always an up-to-date snapshot of the implementation state, without having to open ClickUp. The ClickUp Doc is a **mirror** of the repo, not the source of truth — the repo remains the source of truth.

## Error handling

- If a Feature task fails: log the error, continue with the others, flag it in the summary
- If the Epic fails: stop everything, do not create the child tasks
- If the list is not accessible: block and ask to verify the configuration in `CLICKUP_CONFIG.md`
