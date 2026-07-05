# Customer Success Skill

Monitoraggio salute partner, prevenzione churn, espansione account. Usata da CEO, Sales, Chief of Staff.

## Health Score Model

Ogni partner ha un **Health Score** (0–100) calcolato su 5 indicatori pesati:

| # | Indicatore | Peso | Fonte dati | Come si misura |
|---|-----------|------|-----------|----------------|
| 1 | **PMI Onboarded** | 25% | Piattaforma | N. PMI registrate vs target contrattuale. Score: (actual / target) * 100, cap 100 |
| 2 | **PMI Attive** (30gg) | 25% | Piattaforma | PMI con almeno 1 scan o login negli ultimi 30 giorni. Score: (attive / onboarded) * 100 |
| 3 | **Churn PMI** (trimestre) | 20% | Piattaforma | % PMI perse nel trimestre. Score: max(0, 100 - churn% * 10). Churn 0% = 100, Churn 10% = 0 |
| 4 | **Engagement Venditori** | 15% | CRM/Piattaforma | N. proposte generate + report inviati nel mese. Score: 0 se nessuna attivita, 50 se sporadica, 100 se regolare |
| 5 | **NPS / Soddisfazione** | 15% | Survey / Feedback | Ultimo NPS score normalizzato 0–100. Se non disponibile: stima da ticket supporto e sentiment |

### Fasce Health Score

| Fascia | Score | Significato | Azione |
|--------|-------|-------------|--------|
| **Healthy** | 80–100 | Partner attivo, PMI in crescita | Expansion play — upsell tier o servizi |
| **Stable** | 60–79 | Funziona ma non cresce | Engagement boost — training, co-marketing |
| **At Risk** | 40–59 | Segnali di disengagement | Intervento proattivo — call con Sales + PM |
| **Critical** | 0–39 | Churn imminente | Escalation CEO — rescue plan entro 7 giorni |

### Formula

```
Health Score = (PMI_Onboarded * 0.25) + (PMI_Attive * 0.25) + (Churn_Score * 0.20) + (Engagement * 0.15) + (NPS * 0.15)
```

---

## Comandi

| Comando | Descrizione | Output |
|---------|------------|--------|
| `partner-health` | Calcola health score per un partner specifico o per tutti | Report con score, trend, alert |
| `partner-review` | Review trimestrale di un partner con raccomandazioni | Documento in `20-Clienti/{slug}/report/partner-review-{partner}-{date}.md` |
| `churn-analysis` | Analisi churn con pattern e cause | Report in `company/direzione/reports/churn-analysis-{date}.md` |
| `partner-qbr` | Genera QBR (Quarterly Business Review) deck per partner | Documento in `20-Clienti/{slug}/report/qbr-{partner}-{quarter}.md` |
| `expansion-plan` | Piano di espansione per partner healthy/stable | Piano in `20-Clienti/{slug}/report/expansion-{partner}-{date}.md` |
| `alert-check` | Scansiona tutti i partner per alert critici | Lista alert con azioni suggerite |

---

## Comando: partner-health

### Input
- Partner slug (opzionale — se omesso, tutti i partner)

### Processo
1. Leggi scheda partner da `20-Clienti/{slug}/overview.md`
2. Calcola ogni indicatore con i dati disponibili
3. Calcola health score complessivo
4. Confronta con score precedente per trend
5. Genera alert se score < 60 o drop > 15 punti

### Output format
```
## Partner Health — {nome partner}

| Indicatore | Score | Dettaglio |
|-----------|-------|-----------|
| PMI Onboarded | 85 | 34/40 target |
| PMI Attive | 70 | 24/34 attive 30gg |
| Churn PMI | 90 | 1% trimestre |
| Engagement Venditori | 60 | 8 proposte/mese (sporadico) |
| NPS | 75 | Ultimo NPS: 45 |

**Health Score: 77/100 — Stable**
Trend: ↓ da 82 (ultimo check)

### Raccomandazioni
1. Engagement venditori in calo → schedulare training session
2. ...
```

---

## Comando: partner-review

### Input
- Partner slug

### Processo
1. Esegui `partner-health` per il partner
2. Analizza storico metriche (ultimi 3 mesi)
3. Identifica pattern e trend
4. Genera raccomandazioni concrete con owner e deadline

### Output
File `20-Clienti/{slug}/report/partner-review-{partner}-{YYYY-MM-DD}.md` con:
- Executive summary (3 righe)
- Health score + trend
- Metriche dettagliate con storico
- Rischi identificati
- Piano d'azione (max 5 azioni, ciascuna con owner e deadline)
- Handoff suggerito (Sales per expansion, PM per feature request, CEO per escalation)

---

## Comando: churn-analysis

### Processo
1. Scansiona tutti i partner con health score < 60
2. Identifica pattern comuni (basso onboarding, scarso engagement, etc.)
3. Calcola churn rate complessivo e per segmento
4. Genera root cause analysis

### Output
File `company/direzione/reports/churn-analysis-{YYYY-MM-DD}.md`

---

## Comando: partner-qbr

### Input
- Partner slug
- Quarter (es. Q1-2026)

### Processo
1. Raccogli tutte le metriche del quarter
2. Genera executive summary
3. Prepara talking points per la call
4. Suggerisci expansion opportunities

### Output
File `20-Clienti/{slug}/report/qbr-{partner}-{quarter}.md` con:
- Risultati del quarter (metriche vs target)
- Wins e highlights
- Aree di miglioramento
- Piano per il prossimo quarter
- Expansion opportunity (se health > 70)

---

## Comando: expansion-plan

### Input
- Partner slug

### Prerequisito
- Health score >= 60 (Stable o Healthy)

### Processo
1. Analizza tier attuale e utilizzo feature
2. Identifica gap tra tier attuale e potenziale
3. Calcola revenue potenziale da upgrade
4. Genera piano con timeline e azioni

### Output
File `20-Clienti/{slug}/report/expansion-{partner}-{YYYY-MM-DD}.md`

---

## Comando: alert-check

### Processo
1. Scansiona `20-Clienti/*/overview.md`
2. Per ogni partner, calcola health score (quick mode — dati disponibili)
3. Genera alert per:
   - Score < 40 → **CRITICAL**
   - Score drop > 15 punti in 30 giorni → **WARNING**
   - PMI attive < 30% delle onboarded → **LOW ENGAGEMENT**
   - Nessuna attivita venditori in 30+ giorni → **DORMANT**
   - Contratto in scadenza entro 60 giorni → **RENEWAL**
4. **Aging trattative** — scansiona `company/commerciale/opportunities/*.md` (skill `os/skills/opportunity-management/SKILL.md`, sezione 3) e genera alert per:
   - `last-activity` > 21gg, o blocker `severity: high` aperto, o next-step scaduto > 14gg → **STALLED 🔴**
   - 14–20gg fermi, o `status-flag: blocked` da > 7gg → **AGING 🟠**
   - Opportunità open **senza `owner-sales`** → **NO-OWNER** (priorità: weighted alto)

### Output format
```
## Partner Alerts — {data}

| Partner | Score | Alert | Azione suggerita |
|---------|-------|-------|-----------------|
| partner-a | 35 | CRITICAL | Rescue call entro 7gg — escalation CEO |
| partner-b | 72→55 | WARNING | Call Sales entro 14gg |
| partner-c | — | DORMANT | Nessuna attivita da 45gg — ricontattare |

## Opportunity Aging — {data}

| Opportunità | Account | Stage | Weighted | Aging | Alert | Blocco / azione |
|-------------|---------|-------|----------|-------|-------|------------------|
| acme-pilot | Acme | negotiation | €72k | 🔴 | NO-OWNER | Assegnare owner — deal più avanzato scoperto |
| acme-channel | Acme | discovery | € — | 🔴 | STALLED | NDA fermo 24gg — ping owner-sales |
```

---

## Integrazione CEO Cadence

### Giornaliero
- `alert-check` automatico: se ci sono alert CRITICAL, vengono inclusi nel check giornaliero al CEO

### Settimanale
- Summary health score di tutti i partner attivi
- Partner con score in calo significativo

### Mensile
- QBR reminder per partner con review schedulata nel mese
- Churn analysis del mese precedente
- Expansion opportunities identificate

---

## Dove vivono i dati

| Dato | Path |
|------|------|
| Schede partner | `20-Clienti/{slug}/overview.md` |
| Template scheda | `20-Clienti/TEMPLATE.md` |
| Report review | `20-Clienti/{slug}/report/partner-review-*.md` |
| Report churn | `company/direzione/reports/churn-analysis-*.md` |
| Report QBR | `20-Clienti/{slug}/report/qbr-*.md` |
| Piani espansione | `20-Clienti/{slug}/report/expansion-*.md` |
| Segmenti clienti | `company/commerciale/segments.md` |
| KPI | `company/direzione/metrics/kpis.md` |
