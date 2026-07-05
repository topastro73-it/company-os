# /product prioritize — Prioritizzazione backlog (RICE)

## Scopo
Riprioritizzare il backlog con un metodo difendibile, non con l'ultima voce che ha urlato.

## Input
Nessuno; opzionale: nuovi item da inserire prima dello scoring.

## Passi
1. **Spec status check**; poi carica `prodotto/backlog.md`, roadmap, OKR (`direzione`).
2. Per ogni item applica **RICE**:
   - **Reach**: quanti partner/venditori/PMI impattati (numero, per trimestre)
   - **Impact**: 3 Massive · 2 High · 1 Medium · 0.5 Low · 0.25 Minimal
   - **Confidence**: 100% / 80% / 50% (sotto il 50% l'item non è pronto per lo scoring:
     serve discovery, non priorità)
   - **Effort**: person-weeks (stima CTO se disponibile, altrimenti flag "da stimare")
   - **Score = (R × I × C) / E**
3. **Strategic fit overlay**: lo score si piega alla strategia solo esplicitamente —
   se promuovi un item oltre il suo RICE, scrivi perché.
4. Proponi 3 tier: **Must-do / Should-do / Nice-to-have**; identifica dipendenze e
   sequenza consigliata.
5. Evidenzia i delta rispetto alla prioritizzazione precedente (cosa è salito/sceso e perché).

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: backlog
last-prioritized: YYYY-MM-DD
---
# Backlog — prioritizzato {YYYY-MM-DD}

## Must-do
| Item | R | I | C | E | Score | Fit | Note |
## Should-do   ## Nice-to-have
## Delta vs precedente   ## Dipendenze e sequenza
```

## Destinazione
Zona `prodotto` → `backlog.md` (aggiornamento in place, storico nei delta).
Commit (admin): `[product] backlog: RICE re-prioritization`.

## Handoff
Top Must-do senza PRD → `/product write-spec` · effort mancanti → `cto` ·
cambio priorità rilevante per OKR → `ceo`.
