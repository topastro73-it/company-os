# /cos weekly-digest — Digest settimanale

## Scopo
Fotografia della settimana: output per area, decisioni, follow-up scaduti, outlook.

## Input
Nessuno. Trigger: "digest della settimana".

## Passi
1. **Attività della settimana**: in admin `git log --since="7 days ago"` raggruppato per
   agente; su Drive i file nuovi/modificati per zona. Aree senza attività → segnala il gap.
2. **Decisioni della settimana**: nuove entry in `direzione/decisions/` con stato e review
   date; decisioni con follow-up non ancora assegnati.
3. **Follow-up scaduti**: checkbox `[ ]` con deadline nella settimana passata → cosa era
   previsto, owner, escalation sì/no.
4. **Pipeline health** (zona `commerciale`): coverage weighted vs target, distribuzione per
   stage, movimenti di stage della settimana, top 🔴🟠 con giorni fermi, deal senza owner.
5. **Delivery & partner** (zona `clienti`): health score in movimento (↑/↓), onboarding
   status per fase, QBR in arrivo.
6. **Prodotto** (zona `prodotto`): spec stale (draft >7gg, evaluated/approved >14gg,
   in-development >30gg), UAT/test in corso, release della settimana.
7. **Compliance & finance**: alert attivi, scadenze prossima settimana (finance solo admin).
8. **Outlook**: follow-up e milestone dei prossimi 7 giorni.

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: digest
---
# Weekly Digest — settimana {inizio} → {fine}

## Output per area (tabella)      ## Decisioni prese
## Follow-up scaduti              ## Pipeline — health & aging
## Delivery & partner             ## Prodotto — spec & release
## Compliance / Finance           ## Outlook prossima settimana
```

## Destinazione
Zona `direzione` → `briefing/weekly-{YYYY-MM-DD}.md`.
Commit (admin): `[cos] digest: settimana {data}`.
