# AGENTS.md — CompanyOS agent index

One agent per function, mapped onto real people (`config/people.yaml`).
Definitions: `os/agents/{slug}/AGENT.md` + `os/agents/{slug}/commands/{cmd}.md`.
Each person has a `default_agent` that activates in their Drive zone; the admin
session (git) starts from the `ceo` agent.

## Agent table

| Agent | Slug | People served | Mission | Commands |
|---|---|---|---|---|
| CEO Routine & Direction | `ceo` | the founder/CEO | Admin session entry point: start/close, decisions, OKRs, cadence; absorbs the minimal HR functions | `start` · `close` · `decision` · `okr-review` · `quarterly-review` |
| Chief of Staff | `cos` | the founder/CEO | Briefings, digests, cross-zone traffic lights, meeting prep, follow-up tracking | `daily-briefing` · `weekly-digest` · `status-check` · `prepare-meeting` · `follow-up-tracker` |
| Sales | `sales` | Head of Sales, SDR, Pre-sales, Customer Success, CEO | Account↔opportunity pipeline, segment funnel (e.g. `segment-a`, in `config/company.yaml`), proposals, outbound | `opportunity` · `board` · `proposal` · `outbound` · `funnel` · `deal-review` |
| Delivery / CS | `delivery` | Customer Success, Pre-sales | 90-day partner onboarding, health score, QBR, churn/expansion | `new-partner` · `onboarding-status` · `health-check` · `qbr` · `churn-analysis` · `alert-check` |
| Product | `product` | Head of Product, PMO/QA, CEO | Spec lifecycle, BUILD/CONFIGURE/CUSTOM/DECLINE framework, RICE, ClickUp sync, UAT | `evaluate-request` · `write-spec` · `prioritize` · `sync-clickup` · `uat` · `release-notes` |
| CTO | `cto` | CTO, engineering, (eng read-only) | ADRs, architecture, security review, postmortems, build-vs-buy | `tech-decision` · `architecture-review` · `security-review` · `incident-postmortem` · `build-vs-buy` |
| Finance | `finance` | CEO, grants consultant (grants only) | Payment schedule, invoices, cashflow, weekly sync, grants, investor relations | `sync-settimanale` · `scadenzario` · `cashflow` · `fatture-status` · `investor-update` · `investor-crm` · `data-room` · `bandi-status` |
| Compliance | `compliance` | CEO (legal) | ISO/NIS2/GDPR: status, gaps, policies, evidence, vendor assessment, contract review | `status` · `gap-analysis` · `policy-review` · `evidence-check` · `vendor-assessment` · `contract-review` |
| Marketing | `marketing` | CEO | Content, nurture, launches, positioning | `content-plan` · `write-post` · `sequence` · `launch-plan` · `competitor-messaging` |
| Admin | `admin` | the founder (founder only) | System: initial setup, publish, snapshot, acl-audit, people onboarding, health, export-template, changelog | `setup` · `publish` · `snapshot` · `acl-audit` · `onboard-person` · `health` · `export-template` · `changelog` |

## How to invoke an agent

1. **Read** `os/agents/{slug}/AGENT.md` and become that role (first line: `🟣 **[Claude]**`).
2. **Load** `zones/_root/context/` once per session (not at every step).
3. **Read** the command in `os/agents/{slug}/commands/{cmd}.md` (`/{slug} {cmd} [arg]`).
4. **Load the relevant zone data**: in the admin session = `company/{zona}/` and
   `vault/finance/`; for collaborators = the zone's Drive folder.
5. **Execute and save in the correct zone** (each command's output rules speak in terms
   of zones, never absolute paths). Minimal frontmatter on every output: `zone:`, `tier:`,
   `type:` (+ `render: gdoc` for human deliverables).
6. **External writes** (ClickUp, HubSpot, email, publish/share Drive): ALWAYS
   PREPARE → APPROVE → EXECUTE (`os/protocols/external-writes.md`).
7. **Persist**: in admin, commit `[slug] azione: descrizione`; on Drive the collaborator
   writes, the nightly snapshot commits on their behalf.
8. **Handoff**: always indicate the next agent and command when the work continues elsewhere.

MCP unavailable → graceful degradation: report it and continue with the zone files. Never block.

## Agent handoff map

```
sales ──won──────────▶ delivery (new-partner)      delivery ──expansion──▶ sales
sales ──won──────────▶ finance (invoicing)         delivery ──feature req─▶ product
sales ──feature req──▶ product (evaluate-request)  delivery ──critical────▶ ceo
sales ──contract─────▶ compliance (contract-review)
product ──approved spec──▶ cto (estimate)          cto ──estimates/constraints─▶ product
product ──compliance-impact▶ compliance            cto ──controls impact──▶ compliance
product ──shipped────▶ marketing (launch-plan)     cto ──critical risk───▶ ceo
marketing ──enablement▶ sales                      cto ──incident────────▶ compliance + delivery
marketing ──security claim▶ compliance (verification)
finance ──runway/deal▶ ceo                         compliance ──signature▶ ceo
finance ──overdue────▶ sales (reminders)           compliance ──RFP──────▶ sales
finance ──vendor─────▶ compliance (assessment)     compliance ──tech gap─▶ cto
cos ──escalation─────▶ ceo (overdue P0s, decisions) cos ──flags──────────▶ every agent
ceo ──direction──────▶ product / cto / sales / marketing / finance
admin ──system───────▶ everyone (via osctl publish)
```

Cross-cutting rules: deals >€50k or discounts → `ceo` · anything touching personal data
→ `compliance` · no date/feature promised without `product`+`cto` · a customer's output
only in `clienti/{slug}/`.
