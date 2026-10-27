---
status: attivo
area: sistema
---

# Home

Cruscotto Obsidian del repo. Le viste si calcolano dal frontmatter dei file
(`status`, `area`, `waiting_on`) e sono limitate a questo repo.

## Novità (ultimi 7 giorni)

```base
filters:
  and:
    - file.inFolder(this.file.folder)
    - file.name != this.file.name
    - file.ext == "md"
    - file.mtime > now() - "1 week"
views:
  - type: table
    name: Novità
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

## In attesa di risposta

```base
filters:
  and:
    - file.inFolder(this.file.folder)
    - file.name != this.file.name
    - status == "in-attesa"
views:
  - type: table
    name: In attesa
    order:
      - file.name
      - waiting_on
      - area
      - file.mtime
    sort:
      - property: file.mtime
        direction: ASC
```

## Inbox da smistare

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

## Mappa del repo

- Architettura: [[ARCHITECTURE]]
- Documenti in root: [[CLAUDE]] · [[README]]
- `bootstrap/`: [[bootstrap/README|bootstrap]]
- `company/`: [[company/README|company]]
- `config/`
- `os/`
- `scripts/`
- `system/`
- `tools/`
- `vault/`: [[vault/README|vault]]
- `zones/`
