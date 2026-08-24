# /sales opportunity — Drill-down e aggiornamento trattativa

## Scopo
Creare o aggiornare una singola opportunità: stage, attività, blocker, chiusura.

## Input
- `opp-slug` (= `{account}-{progetto}`) o istruzione in linguaggio naturale
  (es. "sposta acme-pilot a negotiation", "logga call di oggi", "blocca su NDA owner M.R.")

## Passi
1. **Crea**: nuovo file da template opportunità; compila frontmatter (`account`, `segment`
   ∈ segment-a | segment-b | segment-c | channel | other, `stage`, `value-gross`,
   `owner-sales`, `opened` e `last-activity` = oggi). I segmenti reali della tua azienda
   sono dichiarati in `config/company.yaml`: usa quelle chiavi, non i placeholder.
   Aggiungi la riga nell'indice opportunità dell'account (`commerciale/accounts/{slug}.md`).
2. **Sposta stage**: aggiorna `stage`, **ricalcola** `probability` (mappa stage) e
   `value-weighted`; `last-activity` = oggi; voce in Timeline.
3. **Logga attività**: `last-activity` = oggi + voce in Timeline (chi, cosa, esito, next step).
4. **Blocker**: aggiungi/risolvi entry in `blockers:` (what/owner/since/due/severity);
   `status-flag: blocked` se almeno un blocker aperto.
5. **Chiudi**: `stage: won|lost`, svuota blocker aperti, registra esito in Timeline.
   Se **won** → handoff `delivery` (new-partner) e `finance` (fatturazione).
6. Dopo ogni modifica: rigenera il board (`/sales board`) o segnala che è stale.

## Formato output (frontmatter opportunità)
```yaml
---
zone: commerciale
tier: 🟡
type: opportunity
account: {slug}
segment: segment-a
stage: negotiation          # probability DERIVATA: 20/30/40/60/80/100/0
probability: 60
value-gross: 48000
value-weighted: 28800
owner-sales: {persona}
opened: YYYY-MM-DD
last-activity: YYYY-MM-DD
next-step: "…"
next-step-due: YYYY-MM-DD
blockers: []
hubspot-id: ""
---
```

## Destinazione
Zona `commerciale` → `opportunities/{opp-slug}.md`.
Commit (admin): `[sales] opportunity: {opp-slug} — {azione}`.
