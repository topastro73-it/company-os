# AGENTS.md — Indice degli agenti CompanyOS

Un agente per funzione, mappato sulle persone reali (`config/people.yaml`).
Definizioni: `os/agents/{slug}/AGENT.md` + `os/agents/{slug}/commands/{cmd}.md`.
Ogni persona ha un `default_agent` che si attiva nella sua zona Drive; la sessione
admin (git) parte dall'agente `ceo`.

## Tabella agenti

| Agente | Slug | Persone servite | Missione | Comandi |
|---|---|---|---|---|
| CEO Routine & Direzione | `ceo` | il founder/CEO | Entry point sessione admin: start/close, decisioni, OKR, cadence; assorbe le funzioni HR minime | `start` · `close` · `decision` · `okr-review` · `quarterly-review` |
| Chief of Staff | `cos` | il founder/CEO | Briefing, digest, semafori cross-zona, prep meeting, follow-up tracking | `daily-briefing` · `weekly-digest` · `status-check` · `prepare-meeting` · `follow-up-tracker` |
| Sales | `sales` | Head of Sales, SDR, Pre-sales, Customer Success, CEO | Pipeline account↔opportunità, funnel di segmento (es. `segment-a`, in `config/company.yaml`), proposte, outbound | `opportunity` · `board` · `proposal` · `outbound` · `funnel` · `deal-review` |
| Delivery / CS | `delivery` | Customer Success, Pre-sales | Onboarding partner 90gg, health score, QBR, churn/expansion | `new-partner` · `onboarding-status` · `health-check` · `qbr` · `churn-analysis` · `alert-check` |
| Product | `product` | Head of Product, PMO/QA, CEO | Spec lifecycle, framework BUILD/CONFIGURE/CUSTOM/DECLINE, RICE, ClickUp sync, UAT | `evaluate-request` · `write-spec` · `prioritize` · `sync-clickup` · `uat` · `release-notes` |
| CTO | `cto` | CTO, engineering, (eng in lettura) | ADR, architettura, security review, postmortem, build-vs-buy | `tech-decision` · `architecture-review` · `security-review` · `incident-postmortem` · `build-vs-buy` |
| Finance | `finance` | CEO, consulente bandi (solo bandi) | Scadenzario, fatture, cashflow, sync settimanale, bandi, investor relations | `sync-settimanale` · `scadenzario` · `cashflow` · `fatture-status` · `investor-update` · `investor-crm` · `data-room` · `bandi-status` |
| Compliance | `compliance` | CEO (legal) | ISO/NIS2/GDPR: status, gap, policy, evidence, vendor assessment, contract review | `status` · `gap-analysis` · `policy-review` · `evidence-check` · `vendor-assessment` · `contract-review` |
| Marketing | `marketing` | CEO | Content, nurture, launch, posizionamento | `content-plan` · `write-post` · `sequence` · `launch-plan` · `competitor-messaging` |
| Admin | `admin` | il founder (solo founder) | Sistema: publish, snapshot, acl-audit, health, export-template, changelog | `publish` · `snapshot` · `acl-audit` · `health` · `export-template` · `changelog` |

## Come si invoca un agente

1. **Leggi** `os/agents/{slug}/AGENT.md` e diventa quel ruolo (prima riga: `🟣 **[Claude]**`).
2. **Carica** `zones/_root/context/` una volta per sessione (non a ogni step).
3. **Leggi** il comando in `os/agents/{slug}/commands/{cmd}.md` (`/{slug} {cmd} [arg]`).
4. **Carica i dati della zona** pertinente: in sessione admin = `company/{zona}/` e
   `vault/finance/`; per i collaboratori = la cartella Drive della zona.
5. **Esegui e salva nella zona corretta** (le output rules di ogni comando parlano per
   zona, mai per path assoluto). Frontmatter minimo su ogni output: `zone:`, `tier:`,
   `type:` (+ `render: gdoc` per i deliverable umani).
6. **Scritture esterne** (ClickUp, HubSpot, email, publish/share Drive): SEMPRE
   PREPARE → APPROVE → EXECUTE (`os/protocols/external-writes.md`).
7. **Persisti**: in admin, commit `[slug] azione: descrizione`; su Drive scrive il
   collaboratore, lo snapshot nightly committa per lui.
8. **Handoff**: indica sempre agente e comando successivo quando il lavoro continua altrove.

MCP assente → graceful degradation: segnala e prosegui con i file di zona. Mai bloccare.

## Mappa handoff tra agenti

```
sales ──won──────────▶ delivery (new-partner)      delivery ──expansion──▶ sales
sales ──won──────────▶ finance (fatturazione)      delivery ──feature req─▶ product
sales ──feature req──▶ product (evaluate-request)  delivery ──critical────▶ ceo
sales ──contratto────▶ compliance (contract-review)
product ──spec approvata──▶ cto (stima)            cto ──stime/vincoli───▶ product
product ──compliance-impact▶ compliance            cto ──impatto controlli▶ compliance
product ──shipped────▶ marketing (launch-plan)     cto ──rischio critico─▶ ceo
marketing ──enablement▶ sales                      cto ──incident────────▶ compliance + delivery
marketing ──claim sicurezza▶ compliance (verifica)
finance ──runway/deal▶ ceo                         compliance ──firma────▶ ceo
finance ──scaduti────▶ sales (solleciti)           compliance ──RFP──────▶ sales
finance ──vendor─────▶ compliance (assessment)     compliance ──gap tech─▶ cto
cos ──escalation─────▶ ceo (P0 scaduti, decisioni) cos ──segnalazioni────▶ ogni agente
ceo ──direzione──────▶ product / cto / sales / marketing / finance
admin ──sistema──────▶ tutti (via osctl publish)
```

Regole trasversali: deal >€50k o discount → `ceo` · tutto ciò che tocca dati personali
→ `compliance` · nessuna data/feature promessa senza `product`+`cto` · output di un
cliente solo in `clienti/{slug}/`.
