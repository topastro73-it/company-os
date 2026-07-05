# /product release-notes — Note di rilascio

## Scopo
Documentare cosa è uscito: versione interna completa + versione comunicabile ai partner.

## Input
- Release/versione · spec incluse (shipped in questo rilascio)

## Passi
1. Verifica i prerequisiti per ogni spec inclusa: UAT con verdetto **GO** e epic ClickUp
   Released. Manca qualcosa → la spec non entra nelle note (e non è shipped).
2. **Spec-reconciliation**: confronta la PRD con quanto realmente costruito (task e
   commenti epic); se divergono, aggiorna prima la PRD, poi scrivi le note.
3. **Versione interna**: cosa è cambiato, per quale livello utente (Partner / Venditore /
   PMI), migrazioni o azioni richieste, known issues, link a spec e UAT.
4. **Versione partner** (linguaggio non tecnico): beneficio prima della feature, cosa
   devono fare (se qualcosa), screenshot/asset se disponibili. Mai promesse su ciò che
   verrà — solo ciò che è shipped.
5. Aggiorna `prodotto/specs/INDEX.md` (status shipped) e la roadmap.

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: release-notes
release: {vX.Y}
date: YYYY-MM-DD
---
# Release {vX.Y} — {data}

## Novità (per livello utente)
| Feature | Livello | Spec | UAT |
## Azioni richieste   ## Known issues

---
## Versione partner (comunicabile)
{testo pronto per invio/pubblicazione}
```

## Destinazione
Zona `prodotto` → `releases/release-{vX.Y}.md`.
Commit (admin): `[product] release: {vX.Y}`.

## Handoff
Feature Tier 1/2 → `marketing` (`/marketing launch-plan`) · comunicazione ai partner →
`delivery` (invio gated PREPARE→APPROVE→EXECUTE).
