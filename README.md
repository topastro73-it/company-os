# CompanyOS

🇮🇹 [Versione italiana](README.it.md)

An AI-driven company operating system — a reusable template.

**The principle**: two planes. This git repo is the **brain** (agents, protocols, guardrails,
config) and only the admin changes it. The **body** is the company's Google Drive folder:
that's where the founder and collaborators work — each with their own Claude Code inside
their own zone — and permissions are **native Drive ACLs**, not conventions.

→ Full architecture: [ARCHITECTURE.md](ARCHITECTURE.md) ([EN](ARCHITECTURE.en.md))
→ Initial setup (language, Drive, service account, people): [bootstrap/README.md](bootstrap/README.md) ([EN](bootstrap/README.en.md))

## Language

On the first session the system asks your **working language** (Italian/English) and stores it
in `config/company.yaml → language`: it governs chat replies, the language every generated
markdown file is written in, and which variant of the system files is presented (Italian base
files, `.en.md` English variants). You can switch at any time just by saying so in chat.
Details: `os/protocols/language.md`.

## Repo map

| Path | What |
|---|---|
| `CLAUDE.md` | Kernel for admin sessions (this repo) |
| `os/agents/` · `os/skills/` · `os/workflows/` · `os/protocols/` | The system: per-function agents, skills, cross-agent workflows, protocols (every file has an English `.en.md` variant) |
| `zones/` | Per-zone Drive CLAUDE.md + shared context (published read-only) |
| `config/` | Instance parameters (`*.example.yaml` to copy and fill in) |
| `company/` | Versioned snapshot of the operational Drive zones (Drive is the master) |
| `vault/` | 🔴 finance & legal & contracts — admin only |
| `tools/osctl/` | git ↔ Drive sync engine (bootstrap, publish, snapshot, acl-audit) |
| `tools/viewer/` | Standalone markdown reader for people working in the Drive folder |
| `scripts/audit/` | Mechanical guardrails (secret-scan, link-lint, frontmatter, health) — in CI and pre-commit |
| `system/` | CHANGELOG, learnings (LRN-XXX), wiki |

## Day to day

- **Admin**: session in this repo → `/ceo start` … `/ceo close` (snapshot, wiki, push).
  System changes → changelog in the same commit → `osctl publish`.
- **Collaborator**: opens Claude Code inside their Drive folder (e.g. `10-Commerciale/`):
  the zone CLAUDE.md configures it automatically. They can only write where their ACL
  allows; activation is progressive, one zone at a time
  (`os/protocols/onboarding-collaborator.md`).
- **Reading without Claude**: deliverables are also published as Google Docs;
  the viewer (`_OS/viewer.html`) browses every `.md` in the company folder.

## How to instantiate

1. Clone this repo (private) for your company
2. Open Claude Code at the repo root and run `/admin setup`: the initial interview asks for
   language, company identity, people and tools → it fills in `config/*.yaml` from the
   `*.example.yaml` files
3. Follow [bootstrap/README.md](bootstrap/README.md): Shared Drive, service account,
   `osctl bootstrap`, progressive onboarding of your people

## Template

A private instance fills `config/`, `company/`, `vault/`, `zones/*/context/` with its own
data; `/admin export-template` regenerates this template from an instance (config and data
emptied, automatic leak-scan).
