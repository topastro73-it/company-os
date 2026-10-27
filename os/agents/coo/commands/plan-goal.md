# /coo plan-goal — Intento e piano a ondate di un goal

## Scopo
Trasformare l'intento dell'owner umano in un goal del ledger e, solo dopo la registrazione dei
criteri, in un piano a ondate di work order.

## Input
- Intento dell'owner (chat o decisione in `direzione/decisions/`), owner `human:<slug>`, scadenza
- Per la fase piano: CRITERIA del goal già committati (hash del commit)

## Passi
**Fase A — intento** (nessun piano):
1. Assegna l'id `G-NNN` (successivo nel ledger) e lo slug.
2. Scrivi `goals/G-NNN-slug/GOAL.md`: intento verificabile, `owner: human:<slug>`, `due`,
   ruoli coinvolti, contributor umani con la loro sottozona.
3. Scrivi `CONTEXT.md`: fonti osservabili (path di zona, MCP in lettura), vincoli, fuori scope.
4. Nessuna cifra: soglie e importi restano nella zona finance, nel ledger solo ref.
5. Handoff a `/controller criteria`. **Ti fermi qui** finché i CRITERIA non sono committati.

**Fase B — piano** (solo con CRITERIA committati):
6. Scrivi `PLAN.md` con `criteria-commit: <hash>`, ondate numerate, totale WO previsto ≤ 15,
   checkpoint umano previsto (al più dopo 3 ondate). Le ondate successive alla prima si delineano.
7. Scrivi i WO dell'ondata 1 in `wo/WO-NNN.md` (formato in `os/protocols/collaboration.md`):
   servizio a catalogo offerto dal destinatario, `inputs` come ref, `criteria` come C-id esistenti.
8. Esegui `ledger-check --drive`, copia i file nello snapshot, esegui `ledger-check`.

## Formato output
Frontmatter GOAL: `zone: direzione`, `tier: 🟡`, `type: goal`, `id`, `owner`, `due`, `status`.
Frontmatter PLAN: `type: plan`, `goal`, `criteria-commit`. WO: campi del protocollo.

## Destinazione
Zona `direzione`, sottozona `ops` (mount Drive in admin) → `goals/G-NNN-slug/`, `wo/`.

## Handoff
Fase A → `controller` (`criteria`). Fase B → `/coo dispatch`.
