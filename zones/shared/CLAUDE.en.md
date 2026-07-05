# CLAUDE.md — Zone `90-Condivisi`

> Published from git, read-only. Common rules in the root CLAUDE.md and `_OS/context/`.

## What this zone is

The **internal showcase**: approved material, readable by everyone (internals + registered
externals). It arrives **only via publish from git** (admin): nobody writes here directly.
If you see it here, it is the official version and you can use it.

## What it contains

| Folder | Content |
|---|---|
| `glossario/` | Company glossary (published copy of `_OS/context/GLOSSARY.md`) |
| `onboarding/` | Onboarding guides: how the zone system works, first steps |
| `template-deliverable/` | Official templates for reports, proposals, QBRs, assessments |
| `viewer/` | HTML viewer to read the folder's `.md` files without installing anything |

## The viewer

`viewer/viewer.html` is a single self-contained file: open it in Chrome/Edge from the synced
Drive folder, select the company folder and browse all `.md` files with index,
search and zone badges. It is the simplest way to read documents without Claude Code.
Alternatively, the main deliverables are also published as Google Docs in their
folder of origin.

## How to use it

- **Templates**: when you produce a deliverable (report, proposal, QBR), ALWAYS start from
  the template in here — then save the output in the right zone (client output →
  `20-Clienti/{slug}/`), never in this folder.
- **Onboarding**: new collaborator or doubt about how the system works →
  the answer starts from `onboarding/`.

## What NOT to do

- **Never write here**: the zone is git → Drive, read-only. Material to share with
  everyone → propose it to the CEO/admin, who publishes it from git.
- Never copy here (or ask to publish) 🟡/🔴 content: the zone is also visible to
  registered externals — only approved material with no sensitive data.
- Do not modify the templates "on the fly": if a template can be improved, flag it to the admin.
