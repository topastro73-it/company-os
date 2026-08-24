# Changelog — CompanyOS

Every change to system files (`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`) requires
an entry here in the same commit. Categories: `feat` / `change` / `fix` / `breaking` / `refactor`.
Semver. After merging a system change → `osctl publish` to distribute it to Drive.

## [0.4.0] — feat: pre-publication sanitization + agent-slug validation

A pre-publication audit showed the export's sanitization was **lexical, not semantic**: it removed
the proper nouns it had a list for, and stopped there. What remained was not a secret, but it was
enough to reconstruct the source company.

- fix(privacy): removed `toni@dna.fi` from `os/protocols/external-writes.md` (+ `.en.md`). It was a
  **working email address of a real person** at a telco customer, with their name and a reference
  to a deal artifact. Third-party personal data, in a public repo.
- fix(privacy): the 6 `CYB-123`/`CYB-456` tickets → `TASK-…`. `CYB-` is the source instance's
  ClickUp prefix: a short but searchable fingerprint of that workspace.
- fix(privacy): the source instance's vertical (ISP Tier-2 / MSP / Telco / TIC, NIS2 as the demand
  driver) was hardcoded across 22 file pairs. It is now parameterized on `config/company.yaml`,
  following the pattern `os/agents/AGENTS.md` already used. NIS2 survives as *an example* of a
  regulatory driver, not as the reader's driver.
- fix(privacy): removed the first-person industry claims ("we sell cybersecurity", "we are B2B2B",
  "SMB scan data"). A generic template cannot tell the reader what market they are in. The
  operational guidance is preserved, rewritten as conditionals pointing at
  `zones/_root/context/COMPANY.md`.
- fix(convention): the 24 examples using `[cfo]` and `[pm]` → `[finance]` and `[product]`. Neither
  agent **exists in this roster**: they belonged to the source instance, and they taught adopters
  to break the commit convention of the repo they are writing in.
- feat(audit): `scripts/audit/convention-check.py` — the guardrail that would have caught the line
  above. It derives the roster from `os/agents/*/` (no hand-maintained list) and validates every
  `[slug]` in commit examples. **Blocking in CI.**
- fix(privacy): removed references to `DEC-005` and to an internal audit dated 2026-07-03, both
  events of the source company cited in paths that do not exist here.

## [0.3.0] — feat: IT/EN parity becomes a mechanical guardrail

The bilingual layer existed with nothing verifying that it held. A translation could be missing,
orphaned, or describing behaviour that no longer exists, and nothing said so. In a public
template that is the worst kind of defect, because it breaks nothing: the English-speaking user
simply reads the wrong instructions.

- feat(audit): `scripts/audit/i18n-parity.py` — checks three defects: **MISSING** (Italian base
  file with no variant), **ORPHAN** (variant with no base file), **STALE** (base modified after
  its translation). Freshness is measured on the last commit timestamp, not on mtime, which says
  nothing after a clone. It also reads uncommitted files, so it tells the truth about the working
  tree. Allowlist in `scripts/audit/i18n-parity-allow.txt` for files already in English
  (`README.md`, the writing skill references) and folder READMEs.
- feat(ci): `.github/workflows/audit.yml` — the check is **blocking**, alongside secret-scan and
  link-lint. It needs `fetch-depth: 0`, already present.
- feat(i18n): added `CLAUDE.en.md`. The kernel, the single most important file in the repo, was
  the only Italian system file without an English variant: with `language: en` an adopter
  silently received the kernel in Italian. Pairs are now 142 and the check is green.
- fix(agents): `os/agents/admin/commands/export-template.md` — the export claimed a "mechanical"
  derivation from the private instance, but a blind copy of `os/` **would delete the `.en.md`
  layer**, which lives only here and not in the source instance. Step 2 now states the export is
  a **merge**: base files are overwritten, variants are never deleted, and a variant whose base
  changed must be retranslated **before** the push. Step 4 verifies it with
  `i18n-parity.py --strict`.
- fix(cleanup): removed `os/skills/gmail/commands/test.md`, which contained only the word "test".
- fix(privacy): `CLAUDE.md` used a real customer of the source instance as the example in the
  commit format → replaced with `{customer}`.
- Ritual guardrails updated (close + session-rituals, IT and EN) to include the check.

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
