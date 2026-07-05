# CompanyOS — Architecture

> Blueprint of the AI company operating system.
> This document is the architectural source of truth. Version: 2.0.0

## 1. Founding principle: two planes

A system that simulates permissions with markdown conventions (🔴🟡🟢 tiers in frontmatter)
doesn't actually enforce anything. CompanyOS separates **brain** and **body**:

| Plane | Where it lives | Master | Who writes | Enforcement |
|---|---|---|---|---|
| **System** (agents, protocols, guardrails, templates, config) | Git repo `company-os` | **Git** | Admin only (the founder) | Branch protection + CI |
| **Operational** (clients, pipeline, deliverables, finance, compliance) | Company Google Drive | **Drive** | Whoever has ACL on the folder | **Native Drive permissions** |

Collaborators **never touch git**. Each one works with their own Claude Code **inside the
company Drive folder** (Google Drive for Desktop). System files (zone CLAUDE.md, agents,
protocols) arrive on Drive **read-only** via publish from git: the collaborator's Claude
loads them as context but cannot alter them. Operational outputs go into the right folder
(e.g. the client folder) and **the permissions are Drive's**: whoever has no access to the
folder does not see those outputs. Period.

## 2. Zones

Every file belongs to a zone. A zone = one top-level Drive folder + one ACL + one
sync direction. Full map in `config/acl.yaml`.

| Zone | Drive | Writes | Reads | Sync |
|---|---|---|---|---|
| `_os` (system) | `_OS/` + `CLAUDE.md` per zone | admin via git | everyone | git → Drive (publish) |
| `direzione` | `00-Direzione/` | CEO | CEO, board | Drive-master, snapshot → git |
| `commerciale` | `10-Commerciale/` | sales team, CEO | sales team + CEO + CoS | Drive-master, snapshot → git |
| `clienti` | `20-Clienti/{slug}/` | **per-folder** (whoever handles that client) | per-folder | Drive-master, snapshot → git |
| `prodotto` | `30-Prodotto/` | product team, CTO, CEO | all internals | Drive-master, snapshot → git |
| `finance` | `40-Finance/` | CEO, grants consultant | CEO + finance; accountant only on `per-commercialista/` | Drive-master, snapshot → **vault** |
| `compliance` | `50-Compliance/` | CEO, legal | internals; external auditor only on `evidence/` | Drive-master, snapshot → git |
| `marketing` | `60-Marketing/` | marketing, CEO | all internals | Drive-master, snapshot → git |
| `shared` | `90-Condivisi/` | admin | everyone (internals + selected externals) | git → Drive (publish) |
| `contratti` | `70-Contratti-Riservati/{slug}/` | CEO | CEO + Head of Sales | Drive-master, snapshot → **vault** |

Rules:
- **Client folder** (`20-Clienti/{slug}/`): contains ALL *operational* outputs relating to
  that client (proposals, reports, QBRs, assessments). The folder's ACL IS the permission.
- **Signed contracts: a separate zone, not a subfolder.** Google Drive inherits permissions only
  downward (whoever has access to a folder inherits it in every subfolder; there is no native
  way to "restrict" a subfolder below the parent's level). A `contratti/` subfolder inside
  `20-Clienti/{slug}/` would therefore be visible to anyone working on that client (delivery, CS),
  not just CEO+Sales. That is why contracts live in the **`contratti`** zone
  (`70-Contratti-Riservati/{slug}/`), top-level and isolated — nobody with broader access
  above it. In the client folder only a pointer remains (`contratti/README.md`).
- **Privacy tiers** 🔴🟡🟢 stay in the frontmatter as a *classification* (for external publishing,
  PII redaction, secret-scan), but *access* is decided by the zone/Drive ACL.
- 🔴 RESTRICTED in git lives only in `vault/` (separate private repo via submodule, or a directory
  present only on the admin's clone).

## 3. Per-zone identity: published CLAUDE.md files

Every Drive zone receives from git its own `CLAUDE.md` (read-only) that configures the Claude Code
of whoever works there:

- **who you are here**: which default agent (e.g. in `10-Commerciale/` → Sales agent)
- **what you can read**: the accessible zones and the shared context (`_OS/context/`)
- **where you write**: the zone's output rules (e.g. client output → `20-Clienti/{slug}/`)
- **what you don't do**: no changes to `_OS/` files, no 🔴 data outside the zone, escalation to the CEO
- **how you ask**: handoffs and cross-zone requests (e.g. "we need a spec" → request in
  `30-Prodotto/richieste/`)

The root of the company folder has the kernel-lite `CLAUDE.md` (company identity, glossary,
common rules); the zones add the role profile. Sources in `zones/` in the repo.

## 4. Sync engine: `osctl`

Python CLI in `tools/osctl/` (requires a Google service account or admin OAuth). Commands:

- `osctl bootstrap` — creates the Drive tree from `config/acl.yaml`, sets the ACLs, writes the
  obtained folder IDs into `config/acl.yaml` (idempotent).
- `osctl publish` — git → Drive: system (`zones/`, selected `os/`, `company/` seed) to the
  zones; `.md` deliverables with `render: gdoc` frontmatter are also **converted to Google Docs**.
- `osctl snapshot` — Drive → git: downloads the Drive-master zones into `company/` (and `vault/`
  for finance) and commits. Run nightly (GitHub Action with service account) or by the admin's
  `/close`. Git thus remains **full versioning and backup** of the operational zones too.
- `osctl acl-audit` — reads the real permissions via the Drive API and compares them with
  `config/acl.yaml`: flags drift (extra/missing person, client folder without owner). Part of
  `/system health`.

Direction per zone = `sync:` in `acl.yaml`. Never two-way on the same file: every file has a single
master. Conflict = the master wins, the rest is a copy.

## 5. Frictionless markdown reader

Three levels, from the most universal:

1. **Automatic Google Doc**: every deliverable for humans (report, proposal, QBR, investor update)
   is ALSO published as a Google Doc in the same folder (conversion at publish time).
   Anyone with Drive access opens it, reads and comments — desktop and mobile, zero install.
2. **Standalone HTML viewer** (`tools/viewer/viewer.html`, published in `_OS/`): a single
   self-contained file; opened in Chrome/Edge from the synced Drive folder, it asks you to select
   the company folder and browses/renders all `.md` files with index, search and zone badges.
   For those working in the desktop folder.
3. **Claude Code**: whoever has their own Claude in the zone reads and queries everything in chat.

## 6. Agents

One agent per function, mapped onto real people (`config/people.yaml`). Definitions in
`os/agents/{slug}/AGENT.md` + `commands/`.

| Agent | Slug | People served | Mission |
|---|---|---|---|
| CEO Routine | `ceo` | the founder (admin) | Admin session entry point: start/close, decisions, OKRs, cadence |
| Chief of Staff | `cos` | the founder (admin) | Briefings, digests, cross-zone tracking, meeting prep |
| Sales | `sales` | sales team | Pipeline (accounts+opportunities), funnel, proposals, outbound |
| Delivery / CS | `delivery` | Customer Success | 90-day partner onboarding, health score, QBRs, churn/expansion |
| Product | `product` | product team | Spec lifecycle, RICE backlog, ClickUp sync, UAT/QA |
| CTO | `cto` | engineering | Technical decisions, ADRs, architecture, security review |
| Finance | `finance` | CEO, grants consultant | Invoicing, payment schedule, cashflow, grants, investor relations |
| Compliance | `compliance` | CEO (legal) | ISO/NIS2, policy register, evidence, vendor assessment, contracts |
| Marketing | `marketing` | marketing | Content, outbound sequences, launches, positioning |
| Admin | `admin` | the founder (admin) | System changes, changelog, template propagation, ACLs |

Meta-skills `agent-creator` and `skill-creator` to extend without code (admin only).

## 7. Three-layer memory (inherited and maintained)

| Layer | Where | What |
|---|---|---|
| **State** | operational zones (Drive) + snapshot in `company/` | The current facts: pipeline, health, deadlines |
| **History** | `system/wiki/` (git) | The why: sessions, entities, narrative |
| **Rules** | `system/learnings.md` (git) | Learned LRN-XXX, with apply-loop |

## 8. Mechanical guardrails

- `scripts/audit/secret-scan.sh` — tokens/keys/IBAN/🔴 files outside their zone: **CI + pre-commit** (inherited, extended to `vault/`).
- `scripts/audit/link-lint.py` — paths cited in system files exist.
- `scripts/audit/frontmatter-check.py` — zone+tier declared on every operational file.
- `osctl acl-audit` — Drive permission drift vs the matrix.
- `.github/workflows/audit.yml` — everything in CI on push/PR; nightly snapshot.
- Human-in-the-loop: writes to external systems (ClickUp, HubSpot, Drive publish, email)
  always PREPARE → APPROVE → EXECUTE (`os/protocols/external-writes.md`).

## 9. Integrations

Config in `config/integrations.yaml` (variable names only, never values).
ClickUp (product execution), HubSpot (CRM mirror of the pipeline, repo/Drive master),
Gmail and Calendar (context), invoicing + bank + payments + ERP (finance),
Google Drive (operational plane). Graceful degradation: MCP missing → continue with files, flag it.

## 10. `company-os` template and private instances

Everything company-specific lives ONLY in: `config/*.yaml`, `company/`, `vault/`,
`zones/*/context/` and in the data referenced by agents via config. Deriving the template is
mechanical: empty `config/` (keep `*.example.yaml`), `company/`, `vault/`; the agents,
protocols, osctl, viewer and guardrails are already generic. An `/admin export-template`
command produces the clean `company-os` repo with an automatic leak-scan.
