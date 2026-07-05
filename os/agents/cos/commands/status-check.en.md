# /cos status-check — Traffic lights across all workstreams

## Purpose
Answer "how are we doing on everything?" with a traffic light per workstream and a summary.

## Input
None; optional: specific area ("product status").

## Steps
1. **Load the sources**: `prodotto` (roadmap, backlog, specs, testing), `direzione`
   (decisions, okrs), `commerciale` (PIPELINE, opportunities), `clienti` (health, onboarding),
   `compliance` (status), `vault/finance` (admin only).
2. **Assign a traffic light** to each workstream:
   - 🟢 on track · 🟡 risk identified but manageable · 🔴 stalled, needs intervention ·
     ⚫ no data in the system (the missing data IS a finding)
3. **Cover**:
   - **Product**: the quarter's epics/specs with status and test status
     (📋 plan / 🧪 in test / ✅ GO / ❌ NO-GO / ⚠️ no test plan)
   - **Decisions**: open follow-ups, passed review dates, pending decisions
   - **OKRs**: progress per KR, KRs at risk
   - **Sales/Delivery**: 🔴 deals, delayed onboarding, Critical partners
   - **Operations**: P0 actions with no owner or overdue, uncollected handoffs
4. **Executive summary**: 3-5 lines — what's on track, what needs intervention, what is stalled.

## Output format
```markdown
---
zone: direzione
tier: 🟡
type: report
---
# Status Check — {YYYY-MM-DD}

## Product    | Epic/Spec | Status | Test | Light | Notes |
## Decisions  | ID | Title | Follow-up | Light |
## OKRs       | KR | Target | Current | Light |
## Sales & Delivery | Item | Status | Light |
## Operations | Action | Owner | Deadline | Light |

## Executive summary
```

## Destination
Zone `direzione` → `briefing/status-{YYYY-MM-DD}.md`.
Commit (admin): `[cos] report: status check {YYYY-MM-DD}`.
