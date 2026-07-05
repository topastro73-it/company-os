# Changelog di sistema

Ogni modifica ai file di sistema — `os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/` —
richiede una entry in `system/CHANGELOG.md` **nello stesso commit** della modifica.
Nessuna entry, nessun merge: il repo git è il master del sistema e il changelog è la sua storia.

## Categorie

| Categoria | Quando |
|---|---|
| `feat` | Nuovo agente, skill, protocollo, comando, workflow, tool |
| `change` | Comportamento modificato in un componente esistente |
| `fix` | Correzione a un comando, regola o guardrail |
| `breaking` | Componente rimosso o regola incompatibile col comportamento precedente |
| `refactor` | Riorganizzazione strutturale senza cambio di comportamento |

## Formato entry

```markdown
## [X.Y.Z] — YYYY-MM-DD — {categoria}: {sintesi}
- {categoria}({area}): descrizione — es. feat(agents): nuovo comando delivery/qbr
- fix(protocols): soglia stale spec draft 7→10 giorni
```

Più modifiche nello stesso commit → una sola versione, più righe.

## Versioning (semver)

- **MAJOR** per `breaking`
- **MINOR** per `feat`
- **PATCH** per `change` / `fix` / `refactor`

Versione corrente: la prima entry di `system/CHANGELOG.md` (verifica con
`git tag --sort=-v:refname | head -1` se i tag sono allineati).

## Checkpoint

Dopo cambi MINOR o MAJOR, proponi all'admin un checkpoint: git tag `vX.Y.Z` sul commit
della modifica. I tag sono i punti di rollback.

## Rollback

Il rollback a un tag precedente ripristina **solo i file di sistema**
(`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`, `system/learnings.md`) — **mai** i dati
operativi (`company/`, `vault/`, `system/wiki/`): quelli hanno il proprio master (Drive) e
la propria storia. Dopo un rollback: entry `change` nel changelog ("rollback a vX.Y.Z, motivo")
e publish immediato.

## Publish obbligatorio dopo merge

Una modifica di sistema mergiata su `main` **non è attiva finché non è pubblicata**: i
collaboratori leggono i file `_OS/` su Drive, non il repo. Quindi, dopo ogni merge che tocca
i path di sistema:

1. `osctl publish` — distribuisce `zones/` e `os/` aggiornati sulle zone Drive (read-only)
2. Verifica nel summary di publish che i file modificati risultino aggiornati
3. Se osctl non è disponibile → segnala che la modifica è "mergiata ma non distribuita" e
   ripeti il publish alla prima occasione (vedi `sync.md` §6)

La CI (`.github/workflows/audit.yml`) verifica su ogni PR che i commit che toccano i path di
sistema contengano anche una modifica a `system/CHANGELOG.md`.
