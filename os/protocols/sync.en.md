# Sync — file lifecycle between git and Drive

Two planes, two masters: the **system** lives in git, the **operational** lives on Drive.
`osctl` (in `tools/osctl/`) moves files in the direction declared by `sync:` in `config/acl.yaml`.

## 1. A single master per file

Every file has **one master only**. Never two-way on the same file.

| Direction | Zones | Master | The other side is |
|---|---|---|---|
| `git_to_drive` (publish) | `_os`, `shared` | git | read-only copy on Drive |
| `drive_master` (snapshot) | direzione, commerciale, clienti, prodotto, finance, compliance, marketing | Drive | versioned snapshot in `company/` (finance → `vault/`) |

In an admin session you may edit the `company/` snapshot **only** if the file is git-master
or if right afterwards you republish the change to the Drive master; otherwise edit on Drive.

## 2. Publish (git → Drive)

`osctl publish` distributes the system to the Drive zones:
- `zones/` → the zone `CLAUDE.md` files and context (`_OS/`, root, `90-Condivisi/`)
- selected `os/` (agents, protocols, templates) → `_OS/`
- `tools/viewer/viewer.html` → `_OS/`
- initial `company/` seeds at bootstrap

**When**: mandatory after every merge of a system change (see
`os/protocols/changelog.md`); the collaborator always works on the latest published version.
On Drive these files are **read-only**: nobody edits them there — changes go through git.

## 3. Snapshot (Drive → git)

`osctl snapshot` downloads the Drive-master zones and commits:
- standard zones → `company/{zona}/` (e.g. `10-Commerciale/` → `company/commerciale/`)
- `40-Finance/` → `vault/finance/` (the admin's private repo, never in the main repo)
- commit: `[snapshot] drive: YYYY-MM-DD`

**When**:
- **Nightly** — GitHub Action with service account (backup and full versioning of the operational plane too)
- **At the admin `/close`** — so the session closes with the real state of the zones

Git remains the versioning and the backup of everything, but for the Drive-master zones it is a **copy**, not the master.

## 4. Conflicts — the master wins

If the same file turns out modified on both sides:
1. **The zone's master wins** (Drive for the operational zones, git for `_os`/`shared`)
2. The losing version is not thrown away: save it as `{nome}.conflict-YYYY-MM-DD.md`
   next to the snapshot and flag it to the admin in the sync summary
3. Never an automatic merge between the two sides: whoever wrote on the wrong side re-applies by hand on the master

Prevention: never edit the snapshot of a Drive-master zone unless you can immediately
carry the change back to Drive.

## 5. Google Doc conversion

Deliverables for humans are published **also** as a Google Doc in the same folder,
so anyone with Drive access can open and comment on them without installing anything. The conversion
triggers on publish when:
- the frontmatter has `render: gdoc`, **or**
- the frontmatter `type:` is among the defaults of `config/acl.yaml` →
  `publish.gdoc_default_for: [report, proposta, qbr, investor-update]`

Rules:
- the `.md` remains the **source of truth**; the Google Doc is a regenerable artifact
- substantive edits received as comments on the Doc → carried back to the `.md`, then re-rendered
- the regenerated Doc **overwrites** the previous one (same file, same ID: links don't break)

## 6. If osctl is not available

Missing MCP/network/credentials do not block the work:
1. **Work on the files** you have (`company/` snapshot for the admin, local Drive folder for collaborators)
2. Flag: "osctl unavailable — local changes ready, sync on restore"
3. System changes stay in git and get published at the first usable `osctl publish`
4. On restore: first `snapshot` (align the state), then `publish` (distribute the system)
5. No manual operation on Drive that simulates the sync (risk of a double master)
