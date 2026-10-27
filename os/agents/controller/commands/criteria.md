# /controller criteria — Criteri plan-blind di un goal

## Scopo
Registrare criteri falsificabili per il goal prima di qualsiasi piano, così che la verifica
non possa adattarsi al lavoro fatto.

## Input
- Solo `GOAL.md` e `CONTEXT.md` del goal, il canone, le fonti elencate nel CONTEXT
- Mai PLAN, WO o WAVE (non devono ancora esistere; se esistono, non li apri)

## Passi
1. Gira in un **subagente fresco** con nel prompt solo i path sopra.
2. Per ogni esito atteso dall'intento scrivi un criterio `### C<n> — titolo` con
   **Observe** (cosa si apre o si misura, su quale fonte) e **Fails if** (cosa lo falsifica).
3. Soglie in mesi o percentuali; gli importi stanno in un file della zona finance,
   referenziato. Nessuna cifra monetaria nel ledger.
4. Il testo non cita work order, ondate o scelte di piano.
5. **Proponi le soglie all'owner e attendi la conferma** in chat. Senza conferma il file non
   si registra.
6. Con la conferma: frontmatter `confirmed-by: human:<slug>`, `registered-at`; scrivi sul
   mount, `ledger-check --drive`, copia nello snapshot, `ledger-check`.
7. Committa **da solo**, prima di qualsiasi PLAN: l'hash è il `criteria-commit` del piano.

## Formato output
Frontmatter: `zone: direzione`, `tier: 🟡`, `type: criteria`, `goal`, `confirmed-by`,
`registered-at`. Corpo: `### C<n>` con Observe / Fails if.

## Destinazione
Zona `direzione`, sottozona `ops` → `goals/G-NNN-slug/CRITERIA.md`.

## Handoff
→ `coo` (`plan-goal`, fase piano) con l'hash del commit.
