# /cos follow-up-tracker — Tracking follow-up e promesse

## Scopo
Un unico posto dove vedere tutti i follow-up aperti, chi li ha in carico e cosa è scaduto.

## Input
Nessuno; opzionale: filtro per owner o area.

## Passi
1. **Scansiona le fonti di follow-up**:
   - `direzione/decisions/*.md` — sezioni follow-up con checkbox e deadline
   - `direzione/ceo-routine.md` — promesse aperte del CEO
   - report recenti di zona (QBR, postmortem, review) — azioni con owner e deadline
   - opportunità in `commerciale` — next-step con `next-step-due` scaduto
2. **Classifica** ogni item: 🔴 scaduto · 🟡 scade entro 7gg · 🟢 pianificato · ⚫ senza
   owner o senza data (anomalia da sanare, non da ignorare).
3. **Per gli scaduti**: quanti giorni, chi era l'owner, impatto se resta fermo, proposta
   (fare ora / ripianificare / cancellare esplicitamente).
4. **Pattern**: se un tipo di follow-up scade ricorrentemente e matcha un learning,
   segnala `⚡ LRN-XXX` (max 1).

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: report
---
# Follow-up Tracker — {YYYY-MM-DD}

## 🔴 Scaduti
| Item | Fonte | Owner | Deadline | Giorni | Proposta |
## ⚫ Senza owner o senza data
## 🟡 In scadenza (7gg)
## 🟢 Pianificati

## Escalation proposte (max 3)
```

## Destinazione
Zona `direzione` → `briefing/follow-up-{YYYY-MM-DD}.md`.
Commit (admin): `[cos] tracker: follow-up {YYYY-MM-DD}`.

## Handoff
Follow-up P0 scaduto → `ceo` (decisione: fare/ripianificare/cancellare).
