# Changelog — CompanyOS

Every change to system files (`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`) requires
an entry here in the same commit. Categories: `feat` / `change` / `fix` / `breaking` / `refactor`.
Semver. After merging a system change → `osctl publish` to distribute it to Drive.

## [0.2.1] — fix: the cadence-log write moves from `start` to `close`

- fix(agents): `os/agents/ceo/commands/close.md` — new step 3 **Cadence log**, as mandatory as the
  session wiki. Previously the update to `direzione/ceo-cadence.md` was specified **only** in step 7 of
  `/ceo start`, i.e. in the middle of the briefing: if the session moved on to something else, the
  write was silently skipped and the cadence log became a false source of truth for every later
  session that read it. Steps 3-9 renumbered to 4-10.
- fix(agents): `os/agents/ceo/commands/start.md` — new step 2 **Cadence freshness check**, the mirror
  image of the stale session detector: if the most recent wiki page is more than 5 days ahead of the
  cadence log, the log is stale and realignment is offered. Step 1 catches the session without a wiki,
  step 2 the wiki without a cadence entry. Steps 2-8 renumbered to 3-9; step 8 (former 7) now states it
  is no longer the only write point.
- fix(protocols): `os/protocols/session-rituals.md` — the same two insertions in the admin ritual
  (START and CLOSE), plus a common rule: a mandatory write does not live inside a long interaction.
- `.en.md` variants updated in parallel for all three files.
- **Zone note**: `direzione` is `drive_master`, so the cadence log is written **on Drive**, never on the
  `company/direzione/` snapshot (kernel rule §5). The new steps say so explicitly.
- Requires `osctl publish` to distribute to Drive.

## [0.2.0] — feat: bilingual IT/EN + language protocol

- feat(protocols): `os/protocols/language.md` — language chosen in the initial interview
  (`config/company.yaml → language`); governs replies, md generation and which variant of
  the system files is presented/published; switchable at any time in chat
- feat(i18n): English `.en.md` variant next to every system file (agents, skills,
  protocols, workflows, zones, context, bootstrap, ARCHITECTURE, system) — 142 files
- feat(osctl): `Config.language` + variant selection in publish (with `en` system files
  go to Drive in English); fallback to `*.example.yaml` on a fresh clone
- feat(docs): `README.md` in English (primary) + `README.it.md`
- fix: `system/system/wiki` path typo in opportunity-management

## [0.1.0] — initial template — feat: CompanyOS

AI company operating system, reusable public template.

- Two-plane architecture: git repo = master of the system (agents, protocols, guardrails,
  config); Google Drive = operational master with native per-zone ACLs.
- 10 agents (ceo, cos, sales, delivery, product, cto, finance, compliance, marketing, admin),
  curated skills, protocols, workflows.
- `osctl`: bootstrap / publish / snapshot / acl-audit (git ↔ Drive).
- Standalone markdown viewer; mechanical guardrails (secret-scan, link-lint, frontmatter, health)
  in CI and pre-commit.
- Progressive collaborator onboarding (one zone at a time, via interview).
