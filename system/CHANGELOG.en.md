# Changelog — CompanyOS

Every change to system files (`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`) requires
an entry here in the same commit. Categories: `feat` / `change` / `fix` / `breaking` / `refactor`.
Semver. After merging a system change → `osctl publish` to distribute it to Drive.

## [0.7.0] — feat: PDF report template (A4 landscape)

- feat(presentations): `os/skills/presentations/report/` — HTML template for reports and documents
  for clients and partners (PoC, QBR, assessment): a cover and 14 sample pages, one per component
  (action titles, cards, exhibits, tables with status pills, timeline, KPIs, next steps), plus
  `render.sh`, which builds the PDF with headless Chrome and the PNG previews.
- The brand is kept out of the markup: colours in `assets/brand.css` (neutral sample values), logos in
  `assets/logo-ink.png` / `logo-white.png` ("YOUR LOGO" placeholders). The README's "Brand" section
  explains how to adapt it.
- `os/skills/SKILLS.md` index and the presentations skill updated.
- Alignment: CyberangelsOS kernel 2.10.1 ↔ company-os 0.7.0.

## [0.6.0] — feat: Org-OS, mechanical export, aligned with kernel 2.10.0

First version derived with `osctl export-template` instead of by hand: the template picks up
everything generic the source instance built from August to today.

- feat(org-os): agents working as a team on goals. New agents `coo` (orchestrator: plan in waves of
  work orders, dispatch, standup, unblock, checkpoint; reports to the CEO) and `controller`
  (plan-blind verifier: falsifiable criteria before the plan, verification against sources). Role
  charters in `os/org/roles/`, service catalog `os/org/services.yaml`, decision rights
  `os/org/decision-rights.yaml`, protocols `os/protocols/collaboration.md` (ledger, work orders,
  states, escalation, anti-loop) and `os/protocols/autonomy.md` (levels L0–L3: AI goes at most to
  `verified`, closing needs a human signature). The ledger lives in the `direzione` zone (`ops/`).
  `/ceo start` runs the COO standup on active goals.
- feat(audit): `scripts/audit/ledger-check.py` — the Org-OS ledger carries no figures, IBANs, VAT/tax
  IDs or 🔴 content, and has a valid format, resolvable WOs, 🔴 routing only to people with ACL,
  human signatures and an anti-loop budget. Blocking in pre-commit (`--staged`) and CI, with 97
  selftests and a fake ledger in `scripts/audit/fixtures/ledger/`.
- feat(osctl): `osctl export-template` — derives a public template from an instance
  (`config/export.example.yaml`). A merge, not an overwrite: `.en.md` files stay, lines marked
  `@instance` are removed, leak-scan on company, people, emails and clients taken from config, list
  of translations to do. Dry-run by default, never commits or pushes. Selftest in CI.
- feat(osctl): retry with backoff on transient Drive errors; `publish` includes `os/skills` and skips
  `node_modules`.
- feat(kernel): frontmatter rule (`status`, `area`, `waiting_on`) in `CLAUDE.md`, and `Home.md`, an
  Obsidian Bases dashboard that builds its views from it.
- feat(config): `company.example.yaml → positioning.segments`: the segments that sales and
  opportunities refer to now have a key to declare them in (the files used to point to a key the
  example did not have). `integrations.example.yaml → banca.external_accounts` for accounts the bank
  API does not cover.
- fix(skills): the Qonto skill documents the API's real limits (Open Banking accounts excluded,
  User-Agent rejected by Cloudflare with error 1010).
- fix(audit): `system-health.py` also checks the ledger and the pre-commit hook; grace period on
  learning counters after a migration.
- change(i18n): selftest fixtures in `i18n-parity-allow.txt` (test data, not documentation).
- fix(privacy): removed the source instance's vertical from the 0.4.0 changelog.
- Alignment: CyberangelsOS kernel 2.10.0 ↔ company-os 0.6.0.

## [0.5.0] — feat: MIT license, setup interview, reusable example scripts

The template promised an initial interview in five documents and implemented it in none: whoever
cloned it was asked their language and then left alone. That was the worst defect for a system that
lives on its first run.

- feat(legal): added an **MIT** `LICENSE`. Without one the default is all rights reserved: nobody
  could legally reuse the template the README invites them to reuse.
- feat(agents): `os/agents/admin/commands/setup.md` (+ `.en.md`) — the initial interview, written for
  people who are **not technical**. Six phases with binding conduct rules: one question at a time,
  "I don't know" always offered as a valid answer, no jargon without an immediate translation,
  progressive writing (an interrupted setup resumes rather than restarts), never a secret dictated
  in chat. Phase 3 scans the stack by category (bank, invoicing/ERP, payments, CRM, tasks, email,
  documents, compliance) and for each one **proposes what the template already ships** instead of
  leaving the field open. Phase 4, the only genuinely technical one, offers a way out: step-by-step
  guidance, or instructions to hand to whoever runs IT.
- feat(scripts): new `scripts/integrations/` directory with the first two **working** examples,
  `bank-qonto.sh` and `bank_qonto_sync.py` (balances and transactions, **read-only**, no
  dependencies). These are not skeletons: it is code in use in a real deployment, sanitized. The
  header is written for non-programmers. The Keychain account name is configurable and it works off
  macOS via environment variables. Bank coordinates are no longer read or printed.
- fix(skills): `os/skills/qonto/` carried **three false claims**: it pointed at non-existent scripts,
  declared a `pip install requests` dependency that is not needed, and documented a `reconcile`
  subcommand the script never implemented. All three fixed, plus the 6 command files.
- fix(agents): `os/agents/AGENTS.md` did not list `onboard-person`, which exists and is documented in
  its own agent: anyone reading the index believed the command did not exist.
- fix(audit): `scripts/audit/system-health.py` counted the format example inside the fenced code
  block as a learning, so a pristine clone showed an undeserved 🔴 — the first thing a cloner saw
  was a red light. It now strips fenced blocks and withholds judgement below 3 entries (a percentage
  over 1 sample is noise).
- fix(audit): removed three dead entries from `link-lint-allow.txt`, including the two Qonto paths
  that now exist elsewhere: they were masking a genuinely broken reference.

## [0.4.0] — feat: pre-publication sanitization + agent-slug validation

A pre-publication audit showed the export's sanitization was **lexical, not semantic**: it removed
the proper nouns it had a list for, and stopped there. What remained was not a secret, but it was
enough to reconstruct the source company.

- fix(privacy): removed a real email address from `os/protocols/external-writes.md` (+ `.en.md`). It was a
  **working email address of a real person** at a telco customer, with their name and a reference
  to a deal artifact. Third-party personal data, in a public repo.
- fix(privacy): the 6 example tickets used the source instance's real ClickUp prefix → `TASK-…`.
  A short but searchable fingerprint of that workspace.
- fix(privacy): the source instance's vertical (market segments and the regulation used as demand
  driver) was hardcoded across 22 file pairs. It is now parameterized on `config/company.yaml`,
  following the pattern `os/agents/AGENTS.md` already used. NIS2 survives as *an example* of a
  regulatory driver, not as the reader's driver.
- fix(privacy): removed the first-person industry claims ("we sell cybersecurity", "we are B2B2B",
  "SMB scan data"). A generic template cannot tell the reader what market they are in. The
  operational guidance is preserved, rewritten as conditionals pointing at
  `zones/_root/context/COMPANY.md`.
- fix(convention): 24 examples used two agent slugs inherited from the source instance →
  `[finance]` and `[product]`. Neither agent **exists in this roster**: they belonged to the source instance, and they taught adopters
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
