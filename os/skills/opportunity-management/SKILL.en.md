# Opportunity Management Skill

Management of the **commercial cockpit**: account↔opportunity data model, pipeline stages, blocker aging, synoptic board and drill-down on individual deals. It is the **single source of truth for the commercial methodology**: Sales, Chief of Staff and CEO Routine rely on this skill to read/write the state of deals.

Primary owner: **Sales**. Used by: Sales, Chief of Staff, CEO Routine, CFO (for coverage/forecast).

> Reference decision: **the repo is the source of truth for the pipeline**. HubSpot remains an optional external CRM; the `hubspot-id` field keeps the link but is not the source.

---

## 1. Data model: Account vs Opportunity

Two distinct objects, a third one generated.

| Object | File | What it is |
|--------|------|------------|
| **Account** | `20-Clienti/{slug}/overview.md` | The partner/company: master data, contacts, post-sale health, onboarding, **index** of its opportunities. |
| **Opportunity** | `company/commerciale/opportunities/{opp-slug}.md` | A single deal. An account can have N of them (e.g. a vendor-agreement + several joint pilot deals). Contains the **live state**: stage, value, blockers, aging. |
| **Board** | `company/commerciale/PIPELINE.md` | Generated synoptic view of all opportunities. Convenience snapshot — the truth is the opportunities' frontmatter. |

**Relationship rules:**
- Every opportunity has `account: {slug}` pointing to the account. An account with no open opportunities is just master data / post-sale.
- Every opportunity has `segment:` (e.g. `segment-a` | `segment-b` | `segment-c` | `channel` | `other` — the real segments live in `config/company.yaml`) for per-segment reading on the board (column + subtotals). Aligned with `company/commerciale/segments.md`.
- `opp-slug` = `{account}-{project|type}` (e.g. `acme-pilot`, `acme-vendor-agreement`, `acme-joint-project`).
- The partner's long-term narrative lives in `system/wiki/entities/clients/{slug}.md` (timeline). The account is the SoT for state; the wiki entity is only history + link to the account.

Templates: `company/commerciale/opportunities/TEMPLATE.md` · `20-Clienti/TEMPLATE.md`.

---

## 2. Stage taxonomy (aligned with HubSpot)

| Stage | `stage` | `probability` | Meaning |
|-------|---------|---------------|---------|
| Discovery | `discovery` | 20 | Initial qualification, ICP fit, BANT in progress |
| Technical Alignment | `technical-alignment` | 30 | Technical alignment / PoC / pilot scoping |
| Proposal Sent | `proposal-sent` | 40 | Commercial proposal sent |
| Negotiation | `negotiation` | 60 | Negotiating terms/price/legal |
| Contract Sent | `contract-sent` | 80 | Contract sent for signature |
| Won | `won` | 100 | Closed won |
| Lost / Dead | `lost` | 0 | Closed lost or dead |

`probability` is **derived from the stage** (never set manually). When the stage moves, always recalculate:
```
probability = map[stage]
value-weighted = round(value-gross * probability / 100)
```

For pilots (e.g. enterprise/channel deals): `type: pilot` typically stays in `technical-alignment` until the pilot produces an outcome; on conversion it moves to `proposal-sent`/`negotiation`.

---

## 3. Aging rules (calculated live)

Aging is calculated **at read time** from the `last-activity` and `next-step-due` fields — it is not written to the file and the board is not to be trusted (it is a snapshot). `days_idle = today − last-activity`.

| Band | Trigger | Meaning |
|------|---------|---------|
| 🟢 OK | `days_idle` ≤ 6 and no overdue next-step and no `high` blocker | Moving |
| 🟡 Attention | `days_idle` 7–13, **or** `next-step-due` overdue by ≤7 days | Needs a wake-up |
| 🟠 Warning | `days_idle` 14–20, or next-step overdue 8–14 days, or `status-flag: blocked` for >7 days | Real risk |
| 🔴 Critical | `days_idle` ≥21, or open blocker with `severity: high`, or next-step overdue >14 days | Intervene now |

An opportunity's band is the **most severe** among those triggered. Won/Lost are excluded from aging.

---

## 4. Commands (exposed via the Sales agent)

| Command | What it does |
|---------|--------------|
| `/sales board` | (Re)generates `company/commerciale/PIPELINE.md` by scanning all opportunities. |
| `/sales opportunity [opp-slug]` | Drill-down: creates/updates a deal, moves stage, logs activity, opens/resolves blockers. |
| `/sales pipeline-review` | Narrative report (velocity, conversion, forecast, coverage) read from the structured opportunities. |

### 4.1 `/sales opportunity [opp-slug]` — drill-down and update

Supported operations (in natural language, e.g. "move acme-pilot to negotiation", "log today's call", "block on NDA owner-sales"):

- **Create**: new file from `opportunities/TEMPLATE.md`, fill in frontmatter, set `opened` and `last-activity` = today. Adds the row to the account's Opportunities index.
- **Move stage**: update `stage`, recalculate `probability` and `value-weighted`, update `last-activity` = today, add an entry to the Timeline.
- **Log activity**: update `last-activity` = today, add an entry to the interactions Timeline (with a link to feedback/session if it exists).
- **Blocker**: add/update/remove an entry in `blockers:` (what/owner/since/due/severity), set `status-flag: blocked` if at least one blocker is open; update the narrative section "Blocker (dettaglio)".
- **Close**: `stage: won|lost`, `status-flag: won|lost`, clear open blockers, record the outcome in the Timeline.

After every change: remember to regenerate the board (`/sales board`) or do it automatically if the context requires it. Commit: `[sales] opportunity: {opp-slug} — {action}`.

### 4.2 `/sales board` — cockpit generation

Scans `company/commerciale/opportunities/*.md` (excluding TEMPLATE), calculates aging live, and writes `company/commerciale/PIPELINE.md` with this structure:

```
# Pipeline — Commercial Cockpit (regenerated {YYYY-MM-DD})

## Summary
- Open deals: {n} · Gross: € {sum of open value-gross} · Weighted: € {sum of open value-weighted}
- Coverage vs €500k target: {weighted/500000 %}
- Per stage: Discovery {n}/€{w} · Technical Alignment {n}/€{w} · ... · Won {n}/€{gross}

## 🔴🟠🟡 Blocked & Aging   ← key view, sorted by severity then by days idle desc
| Band | Opportunity | Account | Stage | Value | Blocker / reason | Owner | Days idle | Next step (due) |

## Per stage
{one table per stage, opps sorted by weighted value desc, each one linked}

## Per owner
{grouped by owner-sales: n deals, gross, weighted, # critical}
```

Commit: `[sales] board: pipeline cockpit {YYYY-MM-DD}`.

---

## 5. Integration with the other agents

- **CEO Routine** (`/routine start`, Phase 4): in addition to partner health alerts, scans the opportunities and shows the top 🔴🟠 (account, blocker, days, next step) in the opening block "Where we left off".
- **Customer Success** (`alert-check`): adds opportunity aging alerts to the health ones.
- **Chief of Staff** (`daily-briefing`, `weekly-digest`): "Pipeline — blocked & aging" section sourced live from the opportunities.

---

## 6. Where the data lives

| Data | Path |
|------|------|
| Opportunity template | `company/commerciale/opportunities/TEMPLATE.md` |
| Opportunities | `company/commerciale/opportunities/{opp-slug}.md` |
| Board / cockpit | `company/commerciale/PIPELINE.md` |
| Target segment funnel (consolidated target list, warm/nurture/cold — the real ICP lives in `config/company.yaml`) | `company/commerciale/target-funnel.md` |
| Account (partner) | `20-Clienti/{slug}/overview.md` |
| Account template | `20-Clienti/TEMPLATE.md` |
| Partner narrative timeline | `system/wiki/entities/clients/{slug}.md` |
| Call feedback | `company/commerciale/feedback/{YYYY-MM-DD}-{...}.md` |
| KPI / coverage | `company/direzione/metrics/kpis.md` |
| Pipeline SoT decision | `company/direzione/decisions/{YYYY-MM-DD}-repo-sot-pipeline.md` |
