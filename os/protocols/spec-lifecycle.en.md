# Spec lifecycle

Every spec lives in the `prodotto` zone (`30-Prodotto/specs/`, snapshot `company/prodotto/specs/`)
with YAML frontmatter: `status`, `last-updated`, `zone: prodotto`, `tier`, and optionally
`clickup-epic:`, `compliance-impact:`. The Product agent keeps `specs/INDEX.md` up to date.

## States

```
draft → evaluated → approved → in-development → shipped
             ↘ declined (final)     ↘ deferred (with review-date) → comes back
                                    ↘ superseded (replaced by a new spec, linked)
```

| State | Meaning |
|---|---|
| `draft` | Initial draft |
| `evaluated` | Business/technical evaluation completed (BUILD/CONFIGURE/CUSTOM/DECLINE) |
| `approved` | Approved for development |
| `in-development` | In progress (ClickUp Epic open) |
| `shipped` | Released and verified (final) |
| `declined` | Rejected, with reason (final) |
| `deferred` | Postponed, with mandatory `review-date` |
| `superseded` | Replaced by a later spec; frontmatter `superseded-by:` (final) |

Every state change updates frontmatter + INDEX.md. Creating/updating linked ClickUp
tasks always follows `external-writes.md` (PREPARE → APPROVE → EXECUTE).

## `in-development` rule

On the transition to `in-development` the agent MUST propose:
> "Do you want me to generate the test plan and the test cases?"

The test plan must be created **before** development finishes, in `30-Prodotto/testing/`
(`test-plan-{slug}.md`, `test-case-{slug}.md`).

## `shipped` rule

A spec moves to `shipped` **only when both** conditions are true:
- (a) ALL tasks of the associated ClickUp Epic are in `Released` state (`Done`/`Tested` is not enough)
- (b) a **UAT test report with a GO verdict** exists in `30-Prodotto/testing/test-report-{slug}-cycle{N}.md`

Verify both before updating the status. If ClickUp is not available, do not mark
`shipped`: flag it and defer to the next session with MCP active.

## `spec-reconciliation` rule

Before marking `shipped`, the agent MUST re-read the Epic's tasks and comments to check
whether changes emerged during development compared to the original spec: modified scope,
adjusted ACs, features removed/added, behaviors different from what was written.

If there are divergences → update the PRD with the real data **before** setting `status: shipped`.
The finished PRD describes the product **as it was built**, not as it was planned.

## Status check — before every product activity

Before any product activity (evaluate-request, write-spec, prioritize-backlog,
roadmap-review, sprint-planning, status-check, product-plan, weekly-digest):

1. **Scan** `specs/INDEX.md` + the `status` / `last-updated` frontmatter of every spec
2. **Identify the stale ones** with these thresholds:

| Status | Stale after |
|---|---|
| `draft` | 7 days |
| `evaluated` / `approved` | 14 days |
| `in-development` | 30 days |
| `deferred` | at the `review-date` |
| `shipped` / `declined` / `superseded` | never (final) |

3. **If there are stale specs**, ask BEFORE proceeding:

> 📋 **Spec Status Check** — confirm the status of these specs:
>
> | Spec | Status | Since | Update? |
> |---|---|---|---|
> | prd-xyz.md | approved | 2026-06-15 | → in-development? shipped? deferred? |

4. **Update** frontmatter (`status`, `last-updated`, `last-status-check`) and INDEX.md
5. **Proceed** with the original work

Exceptions (skip the check): already done in the last 4 hours in the same session; no stale
spec; non-product activity.
