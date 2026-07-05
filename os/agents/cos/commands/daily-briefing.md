# /cos daily-briefing — Briefing del giorno

## Scopo
Dare al CEO in 2 minuti: cosa è cambiato, cosa richiede attenzione oggi, stato pipeline.

## Input
Nessuno. Trigger: "briefing di oggi", "cosa devo sapere?".

## Passi
1. **Cadence check**: se in sessione admin e scatta un ritmo (`direzione/ceo-cadence.md`),
   lascia che `/ceo start` faccia le domande PRIMA del briefing; altrimenti procedi.
2. **Novità ultime 24-48h**: in admin `git log --since="48 hours ago"`; su Drive i file
   modificati di recente nelle zone leggibili. Raggruppa per agente/area.
3. **Segnali che richiedono il CEO**:
   - follow-up con scadenza oggi/domani (da `direzione/decisions/` e report di zona)
   - decisioni aperte senza owner o senza data · handoff non raccolti
4. **Pipeline — bloccati & aging** (live dai frontmatter di `commerciale/opportunities/`):
   top 🔴🟠 con account, stage, blocco, owner, giorni fermi, next step. Evidenzia deal
   senza owner e weighted alto bloccato. Board stale >3gg → suggerisci `/sales board`.
5. **Partner alert** (zona `clienti`): health Critical/At-Risk, onboarding in ritardo.
6. **Finance flash** (`vault/finance/`, solo admin): scadenze ≤3gg, fatture scadute 30+gg.
7. **Compliance** (solo se c'è qualcosa): scadenze ≤7gg, evidenze mancanti, audit vicini.
8. **Priorità oggi**: 3-5 azioni, ognuna con contesto in 1 riga e tempo stimato.

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: briefing
---
# Briefing — {YYYY-MM-DD}

## Cosa è cambiato          ## Richiede la tua attenzione oggi
## Pipeline — bloccati & aging (tabella 🔴🟠)
## Partner alert            ## Finance flash
## Compliance (se presente) ## Priorità oggi (3-5, con owner)
```
Ogni dato cita la fonte (file di zona).

## Destinazione
Zona `direzione` → `briefing/daily-{YYYY-MM-DD}.md`. Consegna anche in chat.
Commit (admin): `[cos] briefing: {YYYY-MM-DD}`.
