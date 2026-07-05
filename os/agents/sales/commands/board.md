# /sales board — Cockpit pipeline

## Scopo
Rigenerare la vista sinottica della pipeline. Il board è uno **snapshot di convenienza**:
la verità è nel frontmatter delle opportunità.

## Input
Nessuno.

## Passi
1. Scansiona `commerciale/opportunities/*.md` (escluso il template).
2. Per ogni opportunità open calcola **aging live** (🟢 ≤6gg · 🟡 7-13 · 🟠 14-20 · 🔴 ≥21;
   next-step scaduto e blocker alzano la fascia; vale la più grave).
3. Verifica coerenza: `probability` ≠ mappa stage → correggila (è derivata); opportunità
   senza `owner-sales` → flag NO-OWNER.
4. Calcola summary: n. open, gross, weighted, coverage vs target, subtotali per stage
   e per segment.
5. Scrivi il board.

## Formato output
```markdown
---
zone: commerciale
tier: 🟡
type: board
generated: YYYY-MM-DD
---
# Pipeline — Cockpit Commerciale (rigenerato {YYYY-MM-DD})

## Summary
- Open: {n} · Gross: €{…} · Weighted: €{…} · Coverage vs target: {…}%
- Per stage: Discovery {n}/€{w} · Technical Alignment {n}/€{w} · … · Won {n}/€{gross}
- Per segment: {subtotali}

## 🔴🟠🟡 Bloccati & Aging   ← vista chiave, per gravità poi giorni fermi desc
| Fascia | Opportunità | Account | Stage | Weighted | Blocco/motivo | Owner | Giorni | Next step (due) |

## Per stage   (una tabella per stage, opp per weighted desc, linkate)
## Per owner   (n deal, gross, weighted, n critici — evidenzia NO-OWNER)
```

## Destinazione
Zona `commerciale` → `PIPELINE.md` (sovrascrivi).
Commit (admin): `[sales] board: pipeline cockpit {YYYY-MM-DD}`.

## Handoff
Deal 🔴 con weighted alto → `deal-review`; NO-OWNER → assegnazione (Head of Sales/CEO).
