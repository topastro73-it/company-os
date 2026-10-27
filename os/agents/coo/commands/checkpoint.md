# /coo checkpoint — Decisione umana di fine ciclo

## Scopo
Preparare la sintesi per l'owner umano o il CEO, che decide se proseguire, correggere o
fermare. Il checkpoint azzera il contatore delle ondate.

## Input
- VERIFY del goal (esiti per criterio), ultimo WAVE-NN, ultimo standup

## Passi
1. Sintesi: esiti per criterio (solo ref), WO consegnati e bloccati, token consumati, budget.
2. Opzioni: prosegui (prossima ondata), correggi (cosa cambia nel piano), ferma.
3. Raccomandazione esplicita.
4. Presenta la bozza in chat. **Ti fermi e chiedi**: solo l'umano decide e firma. Mai firmare
   al suo posto. Una bozza senza firma non entra nel ledger (ledger-check la rifiuta).
5. Con la firma: scrivi `CHECKPOINT-NN.md` con `decided-by: human:<slug>`, `decided-at` e
   `decision` come dati dall'umano; `ledger-check --drive`, copia nello snapshot, `ledger-check`.

## Formato output
Frontmatter: `zone: direzione`, `tier: 🟡`, `type: checkpoint`, `goal`, `wave` (ultima ondata
coperta), `decided-by`, `decided-at`, `decision` (prosegui | correggi | ferma).

## Destinazione
Zona `direzione`, sottozona `ops` → `goals/G-NNN-slug/CHECKPOINT-NN.md`.

## Handoff
→ `ceo` (firma); dopo la firma → `/coo dispatch` o `/coo plan-goal` (correzione).
