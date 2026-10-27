# /coo dispatch — Esecuzione di un'ondata

## Scopo
Far eseguire ai ruoli i WO di un'ondata e registrare esiti e costo.

## Input
- Goal e numero d'ondata; WO dell'ondata in stato `accepted`

## Passi
1. Controlla il budget: WO del goal ≤ 15, ondate dopo l'ultimo CHECKPOINT ≤ 3. Oltre → stop,
   `/coo checkpoint`.
2. Per ogni WO lancia un **subagente** con un brief stretto: `AGENT.md` del ruolo destinatario,
   il WO, il comando o servizio da eseguire, gli `inputs` (ref) e il path di output nella
   `output-zone`. Nessun accesso a zone fuori dal domain del ruolo (`config/acl.yaml → roles`).
3. I WO verso `human:<slug>` non si lanciano: restano `accepted` finché la persona consegna.
4. A consegna: WO → `delivered`, nota di consegna con soli ref e `tokens: <n>` (il
   `total_tokens` del subagente). Un WO che non può procedere → `blocked` con `reason`/`exit`.
5. I WO emessi dai ruoli durante l'ondata si smistano nell'ondata successiva (mai rimbalzo al
   mittente senza `routed-by: coo`).
6. Scrivi `WAVE-NN.md`: token per WO e totale, WO usati su 15, ondate dall'ultimo checkpoint.
   Solo token, mai valuta. Ogni conteggio si scrive `<n> tok` (o `tokens: <n>` nel
   frontmatter): è l'unica forma in cui `ledger-check` ammette numeri grandi nel ledger.
7. `ledger-check --drive`, copia nello snapshot, `ledger-check`.

## Formato output
`WAVE-NN.md`: frontmatter `zone: direzione`, `tier: 🟡`, `type: wave`, `goal`, `wave`; tabella
WO | ruolo | stato | token (celle nella forma `<n> tok`).

## Destinazione
Zona `direzione`, sottozona `ops` → `goals/G-NNN-slug/WAVE-NN.md` e `wo/`.

## Handoff
→ `controller` (`verify`) a fine ondata; → `/coo checkpoint` se il budget è al limite.
