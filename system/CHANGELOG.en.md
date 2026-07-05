# Changelog — CompanyOS

Every change to system files (`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`) requires
an entry here in the same commit. Categories: `feat` / `change` / `fix` / `breaking` / `refactor`.
Semver. After merging a system change → `osctl publish` to distribute it to Drive.

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
