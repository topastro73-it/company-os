# /controller verify — Verifica plan-blind sulle fonti

## Scopo
Stabilire per ogni criterio PASS, FAIL o non ancora osservabile, con una prova riproducibile
presa dalle fonti, non dal racconto degli agenti.

## Input
- Il prompt del subagente contiene **solo** i path di `GOAL.md`, `CRITERIA.md` e la lista delle
  fonti osservabili (dal CONTEXT). Niente PLAN, `wo/`, WAVE, note di consegna.

## Passi
1. Gira in un **subagente fresco**. Prima verifica la sessione: se `vault/finance/` non esiste
   rifiuta ("verifica 🔴 solo in sessione admin").
2. Per ogni `### C<n>`: esegui l'Observe sulle fonti (file di zona, MCP in sola lettura).
   MCP assente o fonte mancante → "non verificabile" (mai PASS).
3. Esito: PASS | FAIL | non ancora osservabile | non verificabile, con la prova (path, query,
   data di lettura) che un altro può rifare.
4. **Dettaglio** (numeri, estratti, calcoli) nella zona finance: `verify/G-NNN-verify-YYYY-MM-DD.md`.
5. **Ledger**: `VERIFY.md` con solo esito per criterio e ref al dettaglio. Non cita WO né il piano.
6. `ledger-check --drive`, copia nello snapshot, `ledger-check`.

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: verify
goal: G-NNN
---
| Criterio | Esito | Prova (ref) |
```

## Destinazione
Ledger: zona `direzione`, sottozona `ops` → `goals/G-NNN-slug/VERIFY.md`.
Dettaglio: zona `finance` (in admin `vault/finance/verify/`).

## Handoff
→ `coo` (`checkpoint`); → `ceo` se un criterio critico è FAIL.
