---
status: attivo
area: sistema
---

# Home

Obsidian dashboard for the repo. The views are computed from the files' frontmatter
(`status`, `area`, `waiting_on`) and are limited to this repo.

## What's new (last 7 days)

```base
filters:
  and:
    - file.inFolder(this.file.folder)
    - file.name != this.file.name
    - file.ext == "md"
    - file.mtime > now() - "1 week"
views:
  - type: table
    name: What's new
    order:
      - file.name
      - file.folder
      - status
      - file.mtime
    sort:
      - property: file.mtime
        direction: DESC
    limit: 20
```

## Waiting for a reply

```base
filters:
  and:
    - file.inFolder(this.file.folder)
    - file.name != this.file.name
    - status == "in-attesa"
views:
  - type: table
    name: Waiting
    order:
      - file.name
      - waiting_on
      - area
      - file.mtime
    sort:
      - property: file.mtime
        direction: ASC
```

## Inbox to sort

```base
filters:
  and:
    - file.inFolder(this.file.folder)
    - file.name != this.file.name
    - file.ext == "md"
    - file.path.contains("/inbox/")
views:
  - type: table
    name: Inbox
    order:
      - file.name
      - file.folder
      - status
      - file.mtime
    sort:
      - property: file.mtime
        direction: ASC
```

## Repo map

- Architecture: [[ARCHITECTURE]]
- Root documents: [[CLAUDE]] · [[README]]
- `bootstrap/`: [[bootstrap/README|bootstrap]]
- `company/`: [[company/README|company]]
- `config/`
- `os/`
- `scripts/`
- `system/`
- `tools/`
- `vault/`: [[vault/README|vault]]
- `zones/`
