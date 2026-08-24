# ClickUp Skill

Integration with ClickUp via MCP (Model Context Protocol). Available to agents: PM, CTO, Chief of Staff.

## Global ClickUp rules

### Task language

All ClickUp tasks (title, description, acceptance criteria, DoD) must be written **always in English**. No exceptions. Even if the source spec is in Italian, the ClickUp task is in English.

### Verify spec + epic before writing/rewriting a task

Before creating or rewriting any task, the agent MUST:

1. **Read the source spec** (`company/prodotto/specs/prd-{slug}.md`) to extract the correct data — do not trust the existing text in the task
2. **Read the epic** (on ClickUp or in the repo) to understand the overall context and the relationships between tasks
3. **Verify the data cited** — if the task mentions rules, mappings, domains, thresholds, compare them against the source spec to make sure they are correct and up to date
4. **Never invent data** — if a piece of information is not in the spec, do not include it in the task. Flag the gap to the PM

This rule prevents tasks that copy stale or incorrect information from previous versions.

### How to find a task's epic

Epics live in the **Epics** list (<list-id-epic>) in the **Product Roadmap** board (Folder <folder-id-roadmap>). Feature tasks are linked to the epic via a **dependency of type `blocking`** (Feature blocks Epic). To find a task's epic:

1. Read the task's `dependencies` field
2. The task with `type: 1` (blocking) that lives in the Epics list is the parent epic
3. Alternatively: the spec frontmatter has the `clickup-epic:` field with the ID and direct link

**Spec frontmatter**: every spec MUST have `clickup-epic:` in its frontmatter with the format `"[{epic_id}](https://app.clickup.com/t/{epic_id})"`. The old `jira-epic:` field is no longer used (migrated in April 2026).

### ClickUp Docs — Product Specs

Product specs are published as **individual ClickUp Docs** inside the **"Product Specs"** Folder:

```yaml
folder_id: "<folder-id-specs>"
folder_name: "Product Specs"
location: Space Product Engineering (<space-id>) → Product Specs (<folder-id-specs>)
```

**Naming convention**: each Doc has the explanatory name of the spec (e.g. `PRD — Assessment Report: Gap Analysis & Remediation Plan`), NOT a generic name. The Doc name MUST match the spec's `# ...` title.

**Structure**:
```
Product Engineering (Space)
├── Product Specs (Folder <folder-id-specs>)
│   ├── Doc: "PRD — Assessment Report: Gap Analysis & Remediation Plan"
│   ├── Doc: "PRD — AI Sales Assistant"
│   ├── Doc: "PRD — Offer Generation"
│   └── ...
├── Delivery Board (Folder)
└── Product Roadmap (Folder)
```

- **One Doc per spec** — the Doc name is the spec title
- **The repo is the source of truth** — the ClickUp Doc is a mirror. Edits are made in the repo, then re-published to the Doc
- **Every spec has `clickup-doc:`** in its frontmatter with the doc ID and direct link
- **ClickUp tasks link to the spec** in the References section with the link to the Doc (not to GitHub)
- **Sync**: when a spec is created or updated (sync-spec, write-spec), the Doc is created or updated automatically

---

## Semi-automatic flow: PREPARE → APPROVE → EXECUTE

Every write operation on ClickUp follows 3 mandatory phases:

### Phase 1: PREPARE

The agent analyzes the input (PRD, roadmap, backlog) and generates an **approval file** in `company/prodotto/clickup-pending/YYYY-MM-DD-{comando}.md` with the complete list of proposed actions:

```markdown
# ClickUp Sync — Approval required
Date: YYYY-MM-DD
Command: sync-spec | sync-roadmap | update-tasks

## Proposed actions

| # | Type | Summary | Details |
|---|------|---------|---------|
| 1 | CREATE Task | "Task Name" | List: Feature, Priority: High, Tags: from-companyos |
| 2 | CREATE Subtask | "Subtask Name" | Parent: #1, Assignee: — |
| 3 | UPDATE Task | TASK-123 | Status: In Progress → Done |

## Confirmation

Review the actions above, then run: `/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-{comando}.md`
To cancel: delete the file or do not run the approve command.
```

### Phase 2: APPROVE

The user reviews the approval file and confirms explicitly. The agent **never executes actions on ClickUp without explicit approval** (exception: read-only commands such as `read-board`).

Approval invocation:
```
/product clickup approve company/prodotto/clickup-pending/YYYY-MM-DD-{comando}.md
```

### Phase 3: EXECUTE

The agent executes the approved actions by calling the ClickUp MCP tools. Every action is logged. When done, the approval file is moved to `company/prodotto/clickup-done/`.

---

## Workspace and Structure

> The real IDs (workspace, space, folder, list) live in `config/integrations.yaml` (clickup section). The `<...>` placeholders below must be replaced with those values.

```yaml
workspace_id: "<workspace-id>"
workspace_name: <workspace-name>
space_name: Product Engineering
space_id: "<space-id>"
```

### "Product Engineering" Space hierarchy

```
Product Engineering (Space <space-id>)
├── Delivery Board (Folder <folder-id-delivery>)
│   ├── Feature (List <list-id-feature>)      ← feature/development tasks
│   ├── Bug (List <list-id-bug>)          ← bug reports
│   ├── Tech-debt (List <list-id-techdebt>)    ← technical debt
│   ├── Bug submission form (List <list-id-bugform>)
│   └── War Room (List <list-id-warroom>)     ← urgencies/incidents
├── Product Roadmap (Folder <folder-id-roadmap>)
│   ├── Epic (List <list-id-epic>)         ← roadmap epics
│   └── Release Planning (List <list-id-release>)
└── 01 - Internal Projects (List <list-id-internal>)
```

---

## Standard tags

Every task created by the system carries the **`from-companyos`** tag for traceability. This tag is **always mandatory, no exceptions**.

Additional tags:
- `spec:{slug}` — linked to a specific PRD

**Explicit rule**: never add quarter tags (e.g. `Q1-2026`, `Q2-2026`). Time-related information goes in the task description, not in tags.

---

## Issue type → ClickUp List mapping

| Startup OS | ClickUp List | Notes |
|-----------|-------------|------|
| Feature / Initiative (Epic) | Product Roadmap → Epic (`<list-id-epic>`) | Parent task, groups subtasks |
| User Story / Feature task | Delivery Board → Feature (`<list-id-feature>`) | Development task |
| Bug / Defect | Delivery Board → Bug (`<list-id-bug>`) | Bug report |
| Technical task / Tech debt | Delivery Board → Tech-debt (`<list-id-techdebt>`) | No direct user value |
| Release | Product Roadmap → Release Planning (`<list-id-release>`) | Release planning |

## Epic: status and priority

The Epic list uses **4 operational statuses**: `NOW`, `NEXT`, `LATER`, `RELEASED`.

**`shipped` rule for specs**: a spec in `company/prodotto/specs/` can be marked `shipped` **only when ALL tasks of the associated Epic are in `Released` status** on ClickUp. It is not enough for them to be `Done` or `Tested`. Before updating the frontmatter `status: shipped`, verify the status of every Epic task via `clickup_filter_tasks` or `clickup_get_task`.

**`spec-reconciliation` rule**: before marking a spec as `shipped`, the agent must read the Epic's tasks and comments (via `clickup_get_task` + `clickup_get_task_comments` for each task) and verify whether changes emerged during development compared to the original specifications. Examples of divergences to detect: modified ACs, features removed or reduced in scope, behaviors different from what was written, new exceptions or edge cases handled differently. If there are divergences, update the PRD before setting `status: shipped`. The finished PRD must describe the product as it was built, not as it was planned.

**Epic creation rule**: every new Epic is ALWAYS created with status **`ON HOLD`**. The priority is set based on the Customer Backward classification:

| Classification | ClickUp Priority | Initial ClickUp Status |
|----------------|-----------------|------------------------|
| Now | `urgent` | `NOW` |
| Next | `high` | `NEXT` |
| Later | `normal` | `LATER` |

## Priority mapping (Feature / Bug / Tech-debt)

| Startup OS | ClickUp Priority |
|-----------|-----------------|
| P0 - Critical | `urgent` |
| P1 - High | `high` |
| P2 - Medium | `normal` |
| P3 - Low | `low` |

## Delivery Board — Feature list statuses and workflow

### Feature list statuses

| Status | Managed by | Meaning |
|-------|----------------|-------------|
| `Backlog` | PM / system | **Main reservoir of all work to be done.** Every task created by the system enters here. |
| `To Do` | PM (weekly planning) | Tasks selected from the Backlog for the current sprint/week, ready for dev pickup. |
| `In Progress` | Dev | Tasks actively being worked on. |
| `In Review` | Dev / PM | PR open or in QA. |
| `Done` | Dev / PM | Completed and verified. |
| `Idea` | CEO (manual use) | **CEO manual use only.** The system never writes to this status. |

### Fundamental rule for task creation

**Every task created by the system (sync-spec, sync-roadmap, update-tasks) is ALWAYS created with status `Backlog`.**

Never create tasks in `To Do`, `Idea` or other statuses. The Backlog is the only entry point for automatically generated tasks.

### Weekly flow

```
BACKLOG (all available work)
    ↓ weekly planning — PM selects by priority
TO DO (current sprint — ready for dev pickup)
    ↓ dev picks up the task
IN PROGRESS → IN REVIEW → DONE
```

### Pickup rule for the Dev Team

Devs pick up tasks from **To Do** in priority order:

**urgent → high → normal → low**

For equal priority, pick the task with the tag of the most critical epic (check the epic status on Product Roadmap: NOW > NEXT > LATER).

### Operational meaning of priorities

| Priority | Meaning | When to use |
|----------|-------------|--------------|
| `urgent` | Blocks a release or a live customer | Critical bugs, P0 fixes, hotfixes |
| `high` | Core feature of the sprint goal | Main tasks of NOW epics |
| `normal` | Important but not blocking | Secondary tasks, edge cases, infra |
| `low` | Nice-to-have | Minor UI, polish, non-urgent tech debt |

### Rule for the PM

Every task that enters **To Do** MUST have a priority assigned. No task in To Do with null priority.

---

## Available MCP tools

### Active MCP servers

**Two** ClickUp servers are available. Use the first one by default:

| Server | Tool prefix | State | When to use it |
|--------|-------------|-------|---------------|
| **claude.ai ClickUp** (remote, OAuth) | `mcp__claude_ai_ClickUp__*` | ✅ Default | Always, as long as it works |
| `clickup` (local, @taazkareem) | `mcp__clickup__*` | Fallback | Only if the remote one is down or you need a tool the remote one does not offer |

> ⚠️ The remote server **does not detect the default workspace** when the user has multiple workspaces. You must pass `workspace_id: "<workspace-id>"` (the company) **on every call**, even on read-only tools. Without this parameter the call fails with `Multiple workspaces available`.

### Reading (read-only, no approval required)

| Tool | Use |
|------|-----|
| `clickup_search` | Search tasks, docs, any asset in the workspace |
| `clickup_get_task` | Details of a single task (supports custom ID) |
| `clickup_filter_tasks` | Filter tasks by tag, list, status, assignee, dates |
| `clickup_get_workspace_hierarchy` | Space/folder/list structure |
| `clickup_get_task_comments` | Comments of a task |
| `clickup_get_custom_fields` | Available custom fields |

### Writing (ALWAYS with approval)

| Tool | Use |
|------|-----|
| `clickup_create_task` | Create a task in a list (requires `name` + `list_id`) |
| `clickup_update_task` | Update fields of an existing task |
| `clickup_create_task_comment` | Add a comment to a task |
| `clickup_add_tag_to_task` | Add a tag to a task |
| `clickup_add_task_dependency` | Set a dependency between tasks |
| `clickup_move_task` | Move a task to another list |

### Notes on tool usage

- **workspace_id**: ALWAYS pass `"<workspace-id>"` (the company) as a parameter — mandatory on the remote server, ignored by the local server but harmless
- **list_id**: use the IDs from the hierarchy above to create tasks in the correct list
- **assignees**: use `clickup_resolve_assignees` to convert names/emails into user IDs
- **tags**: tags must already exist in the space; use `from-companyos` + `spec:{slug}`
- **subtask**: use the `parent` parameter with the parent task ID to create subtasks
- **dependency Feature → Epic**: when creating Feature tasks linked to an Epic, ALWAYS add a dependency of type `blocking` (Feature blocks Epic) using `clickup_add_task_dependency` with `task_id` = feature, `depends_on` = epic, `type` = "blocking". This creates the "Block" relationship visible in ClickUp.
- **descriptions**: ALWAYS use `markdown_description` (not `description`) with real markdown. Do NOT use escaped `\n` — use real newlines in the parameter. Required formatting:
  - Section headings with `##` (e.g. `## Description`, `## Acceptance Criteria`)
  - Important text in **bold** with `**text**`
  - Bullet lists with `-`
  - Acceptance criteria as checkboxes with `- [ ]`
  - `---` separator between the Description and Acceptance Criteria sections
- **self-consistency**: every task description (Epic, Feature, Subtask) must be **completely self-sufficient**. The dev who picks up the task must not have to look up the PRD, ask the PM, or read other documents. The description must include: product context (why this feature exists), the problem it solves, the expected behavior, all the detailed acceptance criteria. The link to the spec is an optional reference, not a substitute for context.

---

## Task Readiness Checklist (pass/fail)

**A task is "ready" only if ALL of the checks below pass. If even one fails, the task stays in backlog/refinement and cannot be approved.**

### Three cardinal rules

1. **2-minute rule** — If a dev reads the task for 2 minutes and does not know what to do → task must be redone.
2. **Self-consistency** — The task must be sufficient on its own. The dev MAY consult the spec/epic for deeper detail, but does NOT NEED them to understand what to build.
3. **Zero architecture** — Never include technical solutions, software architecture, DB names, endpoints, stack. The tech side is the responsibility of the architect/engineer, who is a different person outside this system. Functional requirements only.

### Full checklist

#### 1) Identity and traceability
- [ ] Clear, specific, outcome-oriented title (not vague)
- [ ] Linked to the Epic via "Dependencies"
- [ ] Linked to the spec (doc + section, if possible)
- [ ] Tags `from-companyos` + `spec:{slug}` present

#### 2) Ownership and accountability
- [ ] Exactly one accountable owner (no "team" as assignee)
- [ ] If there are contributors, they are in comments/collaborators, not co-owners
- [ ] Acceptance owner/reviewer defined (who confirms the "done")

#### 3) Problem and intent clarity
- [ ] **Why** this task exists (business/product reason)
- [ ] **Expected outcome** in one sentence
- [ ] **Explicit scope** — what is included
- [ ] **Explicit out of scope** — what is excluded

#### 4) Execution clarity
- [ ] Actionable implementation description (the dev can start without guessing)
- [ ] Dependencies listed (services, teams, prior tasks, data, infra) — described functionally
- [ ] Constraints listed (compliance, UX, performance, deadline)
- [ ] Blockers known at creation time documented

#### 5) Definition of Done (DoD) quality
- [ ] Explicit, testable, observable DoD
- [ ] Validation method defined (test/review/demo/query/screenshot)
- [ ] Required evidence defined (PR, CI run, screenshot, doc update)
- [ ] Done criteria avoid vague wording ("implemented", "fixed", "completed")
- [ ] DoD proportional to task type (feature/bug/refactor/discovery)

#### 6) Test and verification requirements
- [ ] Required test level declared (unit/integration/e2e/manual)
- [ ] Acceptance checks listed
- [ ] Regression expectation declared (what must NOT break)
- [ ] Relevant edge cases documented

#### 7) Operational planning fields
- [ ] Priority set
- [ ] Due date only if meaningful (not arbitrary)

#### 8) Workflow policy checks
- [ ] No duplicate of an existing active/planned task
- [ ] Naming follows the team convention

### Minimum "Ready" (mandatory minimum set)

A task is ready when it has **at least**: an outcome-oriented title, a why, scope / out of scope, an owner, epic + spec links, a testable DoD checklist, dependencies/constraints, priority, validation/evidence expectations.

---

## Available commands

| Command | File | Access |
|---------|------|---------|
| sync-spec | `os/skills/clickup/commands/sync-spec.md` | PM, CTO |
| sync-roadmap | `os/skills/clickup/commands/sync-roadmap.md` | PM, CTO |
| read-board | `os/skills/clickup/commands/read-board.md` | All |
| update-tasks | `os/skills/clickup/commands/update-tasks.md` | PM, CTO, CoS |
| sync-ceo-actions | `os/skills/clickup/commands/sync-ceo-actions.md` | CoS |

## Configuration

See `config/integrations.yaml (sezione clickup)` for the full setup.
