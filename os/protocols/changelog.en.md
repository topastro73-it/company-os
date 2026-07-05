# System changelog

Every change to system files — `os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/` —
requires an entry in `system/CHANGELOG.md` **in the same commit** as the change.
No entry, no merge: the git repo is the master of the system and the changelog is its history.

## Categories

| Category | When |
|---|---|
| `feat` | New agent, skill, protocol, command, workflow, tool |
| `change` | Modified behavior in an existing component |
| `fix` | Correction to a command, rule or guardrail |
| `breaking` | Component removed or rule incompatible with previous behavior |
| `refactor` | Structural reorganization with no behavior change |

## Entry format

```markdown
## [X.Y.Z] — YYYY-MM-DD — {category}: {summary}
- {category}({area}): description — e.g. feat(agents): new delivery/qbr command
- fix(protocols): stale draft spec threshold 7→10 days
```

Multiple changes in the same commit → a single version, multiple lines.

## Versioning (semver)

- **MAJOR** for `breaking`
- **MINOR** for `feat`
- **PATCH** for `change` / `fix` / `refactor`

Current version: the first entry of `system/CHANGELOG.md` (verify with
`git tag --sort=-v:refname | head -1` if tags are aligned).

## Checkpoints

After MINOR or MAJOR changes, propose a checkpoint to the admin: git tag `vX.Y.Z` on the
commit of the change. Tags are the rollback points.

## Rollback

Rolling back to a previous tag restores **only the system files**
(`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`, `system/learnings.md`) — **never** the
operational data (`company/`, `vault/`, `system/wiki/`): those have their own master (Drive) and
their own history. After a rollback: a `change` entry in the changelog ("rollback to vX.Y.Z, reason")
and an immediate publish.

## Mandatory publish after merge

A system change merged to `main` **is not active until it is published**: collaborators
read the `_OS/` files on Drive, not the repo. So, after every merge that touches
the system paths:

1. `osctl publish` — distributes the updated `zones/` and `os/` to the Drive zones (read-only)
2. Verify in the publish summary that the modified files show as updated
3. If osctl is not available → flag that the change is "merged but not distributed" and
   repeat the publish at the first opportunity (see `sync.md` §6)

CI (`.github/workflows/audit.yml`) checks on every PR that commits touching the system
paths also include a change to `system/CHANGELOG.md`.
