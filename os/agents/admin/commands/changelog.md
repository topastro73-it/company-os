# /admin changelog — Registro modifiche di sistema

## Scopo
Ogni modifica al sistema è tracciata e versionata: `system/CHANGELOG.md` è la storia
del cervello. Nessuna modifica a `os/`, `zones/`, `config/`, `tools/`, `CLAUDE.md`
entra senza entry **nello stesso commit**.

## Input
- Descrizione della modifica · categoria: `feat` | `change` | `fix` | `breaking` | `refactor`
- File toccati (se non deducibili dallo staging)

## Passi
1. Determina la **versione**: `breaking` → incrementa minor (x.Y.0); feat/change/fix/
   refactor → incrementa patch (x.y.Z). La versione corrente è in testa al CHANGELOG.
2. Scrivi l'entry (formato sotto): cosa cambia, perché, impatto per chi usa il sistema
   (quale zona/agente se ne accorge), eventuale azione richiesta (es. "serve publish").
3. `breaking`: documenta anche il percorso di rollback (commit precedente + cosa
   ripubblicare su Drive).
4. Verifica che l'entry e la modifica siano **nello stesso commit**
   (`[admin] system: {descrizione}` — o il commit dell'agente che ha fatto la modifica).
5. Ricorda il passo successivo: `/admin publish` per distribuire, se la modifica tocca
   file che vivono anche su Drive.

## Formato output (entry)
```markdown
## [x.y.z] — YYYY-MM-DD
### {feat|change|fix|breaking|refactor}
- **{area}**: {cosa è cambiato e perché}
  - Impatto: {chi/cosa se ne accorge}
  - Azione: {publish richiesto? migrazione? niente}
  - Rollback (se breaking): {come}
```

## Destinazione
`system/CHANGELOG.md` (git). Commit insieme alla modifica descritta.

## Guardrail specifici
- Entry senza modifica o modifica senza entry = incoerenza → `/admin health` la segnala
- Il CHANGELOG non contiene mai dati di business — descrive il sistema, non i contenuti
