# Protocols — index

Protocols define *how* the system operates. The kernel (`CLAUDE.md`) defines the
non-negotiable rules; the operational detail lives here. Each protocol is self-contained and max 120 lines.

| Protocol | What it governs |
|---|---|
| [zones-and-permissions.md](zones-and-permissions.md) | Zones, Drive ACLs, restricted subzones, tiers 🔴🟡🟢, PII rules, graceful degradation |
| [sync.md](sync.md) | File lifecycle between git and Drive: publish, snapshot, single master, conflicts, Google Docs |
| [external-writes.md](external-writes.md) | PREPARE → APPROVE → EXECUTE for every write to external systems (ClickUp, HubSpot, Gmail, publish to third parties) |
| [memory.md](memory.md) | Three-layer memory: state in the zones, history in `system/wiki/`, rules in `system/learnings.md` |
| [spec-lifecycle.md](spec-lifecycle.md) | Product spec states, in-development/shipped rules, reconciliation, status-check |
| [decisions.md](decisions.md) | Format and lifecycle of decisions (immutable, direzione zone) |
| [changelog.md](changelog.md) | Entry in `system/CHANGELOG.md` for every system change, semver, checkpoints, rollback, publish |
| [session-rituals.md](session-rituals.md) | Start and close routines, for admin (repo) and collaborators (Drive zone) |
| [onboarding-collaborator.md](onboarding-collaborator.md) | Progressive activation (per zone, via interview) of collaborators on the operational Drive |
| [language.md](language.md) | Working language: choice at setup, md generation, `.en.md` variants, change via chat |
| [collaboration.md](collaboration.md) | Org-OS: goal ledger, work orders, states, Team Topologies modes, escalation, anti-loop, plan-blind |
| [autonomy.md](autonomy.md) | Agent autonomy levels L0–L3; AI goes at most as far as `verified`, closure only with a human sign-off |

Cross-agent workflows in `os/workflows/` (index in `os/workflows/README.md`).
In the `company-os` template, system files have English variants `.en.md` alongside (see language.md).
