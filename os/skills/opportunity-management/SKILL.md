# Opportunity Management Skill

Gestione del **cockpit commerciale**: modello dati account↔opportunità, pipeline stage, aging dei blocchi, board sinottico e drill-down sul singolo deal. È la **single source of truth della metodologia** commerciale: Sales, Chief of Staff e CEO Routine si rifanno a questa skill per leggere/scrivere lo stato delle trattative.

Owner primario: **Sales**. Usata da: Sales, Chief of Staff, CEO Routine, CFO (per coverage/forecast).

> Decisione di riferimento: **il repo è il source of truth della pipeline** (supera DEC-005). HubSpot resta CRM esterno opzionale; il campo `hubspot-id` mantiene il link ma non è la fonte.

---

## 1. Modello dati: Account vs Opportunità

Due oggetti distinti, un terzo generato.

| Oggetto | File | Cos'è |
|---------|------|-------|
| **Account** | `20-Clienti/{slug}/overview.md` | Il partner/azienda: anagrafica, contatti, health post-vendita, onboarding, **indice** delle sue opportunità. |
| **Opportunità** | `company/commerciale/opportunities/{opp-slug}.md` | Una singola trattativa. Un account può averne N (es. un vendor-agreement + più deal pilota congiunti). Contiene lo **stato vivo**: stage, valore, blocker, aging. |
| **Board** | `company/commerciale/PIPELINE.md` | Vista sinottica generata di tutte le opportunità. Snapshot di convenienza — la verità è il frontmatter delle opportunità. |

**Regole di relazione:**
- Ogni opportunità ha `account: {slug}` che punta all'account. Un account senza opportunità aperte è solo anagrafica/post-sale.
- Ogni opportunità ha `segment:` (es. `segment-a` | `segment-b` | `msp-mssp` | `vendor-channel` | `tic` — l'ICP reale vive in `config/company.yaml`) per la lettura per-segmento nel board (colonna + subtotali). Allineato a `company/commerciale/segments.md`.
- `opp-slug` = `{account}-{progetto|tipo}` (es. `acme-pilot`, `acme-vendor-agreement`, `acme-joint-project`).
- La narrativa di lungo periodo del partner vive in `system/wiki/entities/clients/{slug}.md` (timeline). L'account è il SoT di stato; la wiki entity è solo storia + link all'account.

Template: `company/commerciale/opportunities/TEMPLATE.md` · `20-Clienti/TEMPLATE.md`.

---

## 2. Tassonomia stage (allineata HubSpot)

| Stage | `stage` | `probability` | Significato |
|-------|---------|---------------|-------------|
| Discovery | `discovery` | 20 | Qualificazione iniziale, fit ICP, BANT in corso |
| Technical Alignment | `technical-alignment` | 30 | Allineamento tecnico / PoC / pilot scoping |
| Proposal Sent | `proposal-sent` | 40 | Proposta commerciale inviata |
| Negotiation | `negotiation` | 60 | Negoziazione termini/prezzo/legal |
| Contract Sent | `contract-sent` | 80 | Contratto inviato per firma |
| Won | `won` | 100 | Chiuso vinto |
| Lost / Dead | `lost` | 0 | Chiuso perso o morto |

`probability` è **derivata dallo stage** (non si imposta a mano). Quando si sposta lo stage si ricalcolano sempre:
```
probability = mappa[stage]
value-weighted = round(value-gross * probability / 100)
```

Per i pilot (es. deal enterprise/channel): `type: pilot` resta tipicamente in `technical-alignment` finché il pilot non produce esito; alla conversione passa a `proposal-sent`/`negotiation`.

---

## 3. Regole aging (calcolate live)

L'aging si calcola **al momento della lettura** dai campi `last-activity` e `next-step-due` — non si scrive nel file e non si fida del board (che è uno snapshot). `giorni_fermo = oggi − last-activity`.

| Fascia | Trigger | Significato |
|--------|---------|-------------|
| 🟢 OK | `giorni_fermo` ≤ 6 e nessun next-step scaduto e nessun blocker `high` | In movimento |
| 🟡 Attention | `giorni_fermo` 7–13, **oppure** `next-step-due` scaduto da ≤7gg | Da risvegliare |
| 🟠 Warning | `giorni_fermo` 14–20, oppure next-step scaduto 8–14gg, oppure `status-flag: blocked` da >7gg | Rischio reale |
| 🔴 Critical | `giorni_fermo` ≥21, oppure blocker `severity: high` aperto, oppure next-step scaduto >14gg | Intervento ora |

La fascia di un'opportunità è la **più grave** tra quelle attivate. Won/Lost sono esclusi dall'aging.

---

## 4. Comandi (esposti via Sales agent)

| Comando | Cosa fa |
|---------|---------|
| `/sales board` | (Ri)genera `company/commerciale/PIPELINE.md` scansionando tutte le opportunità. |
| `/sales opportunity [opp-slug]` | Drill-down: crea/aggiorna una trattativa, sposta stage, logga attività, apre/risolve blocker. |
| `/sales pipeline-review` | Report narrativo (velocity, conversion, forecast, coverage) letto dalle opportunità strutturate. |

### 4.1 `/sales opportunity [opp-slug]` — drill-down e aggiornamento

Operazioni supportate (in linguaggio naturale, es. "sposta acme-pilot a negotiation", "logga call di oggi", "blocca su NDA owner-sales"):

- **Crea**: nuovo file da `opportunities/TEMPLATE.md`, compila frontmatter, imposta `opened` e `last-activity` = oggi. Aggiunge la riga nell'indice Opportunità dell'account.
- **Sposta stage**: aggiorna `stage`, ricalcola `probability` e `value-weighted`, aggiorna `last-activity` = oggi, aggiunge voce in Timeline.
- **Logga attività**: aggiorna `last-activity` = oggi, aggiunge voce in Timeline interazioni (con link a feedback/sessione se esiste).
- **Blocker**: aggiunge/aggiorna/rimuove una entry in `blockers:` (what/owner/since/due/severity), imposta `status-flag: blocked` se almeno un blocker aperto; aggiorna la sezione narrativa "Blocker (dettaglio)".
- **Chiudi**: `stage: won|lost`, `status-flag: won|lost`, svuota i blocker aperti, registra esito in Timeline.

Dopo ogni modifica: ricorda di rigenerare il board (`/sales board`) o farlo automaticamente se il contesto lo richiede. Commit: `[sales] opportunity: {opp-slug} — {azione}`.

### 4.2 `/sales board` — generazione del cockpit

Scansiona `company/commerciale/opportunities/*.md` (escluso TEMPLATE), calcola aging live, e scrive `company/commerciale/PIPELINE.md` con questa struttura:

```
# Pipeline — Cockpit Commerciale (rigenerato {YYYY-MM-DD})

## Summary
- Open deal: {n} · Gross: € {somma value-gross open} · Weighted: € {somma value-weighted open}
- Coverage vs target €500k: {weighted/500000 %}
- Per stage: Discovery {n}/€{w} · Technical Alignment {n}/€{w} · ... · Won {n}/€{gross}

## 🔴🟠🟡 Bloccati & Aging   ← vista chiave, ordinata per gravità poi per giorni_fermo desc
| Fascia | Opportunità | Account | Stage | Valore | Blocco / motivo | Owner | Giorni fermo | Next step (due) |

## Per stage
{una tabella per stage, opp ordinate per valore weighted desc, ognuna linkata}

## Per owner
{raggruppamento per owner-sales: n deal, gross, weighted, # critici}
```

Commit: `[sales] board: pipeline cockpit {YYYY-MM-DD}`.

---

## 5. Integrazione con gli altri agenti

- **CEO Routine** (`/routine start`, Fase 4): oltre agli alert health partner, scansiona le opportunità e mostra i top 🔴🟠 (account, blocco, giorni, next step) nel blocco di apertura "Dove eravamo rimasti".
- **Customer Success** (`alert-check`): aggiunge gli alert aging delle opportunità a quelli di health.
- **Chief of Staff** (`daily-briefing`, `weekly-digest`): sezione "Pipeline — bloccati & aging" sourced live dalle opportunità.

---

## 6. Dove vivono i dati

| Dato | Path |
|------|------|
| Template opportunità | `company/commerciale/opportunities/TEMPLATE.md` |
| Opportunità | `company/commerciale/opportunities/{opp-slug}.md` |
| Board / cockpit | `company/commerciale/PIPELINE.md` |
| Funnel segmento target (target list consolidata, warm/nurture/cold — l'ICP reale vive in `config/company.yaml`) | `company/commerciale/isp-funnel.md` |
| Account (partner) | `20-Clienti/{slug}/overview.md` |
| Template account | `20-Clienti/TEMPLATE.md` |
| Timeline narrativa partner | `system/wiki/entities/clients/{slug}.md` |
| Feedback call | `company/commerciale/feedback/{YYYY-MM-DD}-{...}.md` |
| KPI / coverage | `company/direzione/metrics/kpis.md` |
| Decisione SoT pipeline | `decisions/2026-06-05-repo-sot-pipeline.md` (supera DEC-005) |
