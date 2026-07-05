# Skills — Index

Skill curate, riscritte per la struttura a zone di CompanyOS
(`company/{zona}`, `vault/`, `20-Clienti/{slug}`; config integrazioni in `config/integrations.yaml`).
Due categorie:

- **Skill operative**: comandi eseguibili e/o integrazione con sistemi esterni
- **Skill di contesto**: framework e guide lette come background per informare le decisioni

Agenti di riferimento: vedi `ARCHITECTURE.md` §6 (`ceo`, `cos`, `sales`, `delivery`, `product`, `cto`, `finance`, `compliance`, `marketing`, `admin`).

## Skill operative

| Skill | Path | Usata da | Una riga |
|-------|------|----------|----------|
| **Opportunity Management** | `os/skills/opportunity-management/SKILL.md` | Sales (owner), CoS, CEO, Finance | Modello account↔opportunità, stage HubSpot-aligned, aging, board `PIPELINE.md`, drill-down deal |
| **Partner Onboarding** | `os/skills/partner-onboarding/SKILL.md` | Delivery (owner), Sales, Product | Onboarding partner 90 giorni: fasi, milestone, scheda cliente in `20-Clienti/{slug}/` |
| **Customer Success** | `os/skills/customer-success/SKILL.md` | Delivery (owner), Sales, CEO, CoS | Health score, churn prevention, QBR ed expansion plan per cliente |
| **Outbound & ABM** | `os/skills/outbound-abm/SKILL.md` | Sales (owner), Marketing, CEO | Campagne outbound account-based: targeting, sequenze, touchpoint value-first |
| **Business Analysis** | `os/skills/business-analysis/SKILL.md` | Product (owner), CEO, CoS | Analisi funzionale interattiva: AS-IS/TO-BE, process map, data model, gap analysis, functional spec |
| **QA & Testing** | `os/skills/qa-testing/SKILL.md` | CTO (owner), Product | Test plan, test case, test report, smoke/security test in `company/prodotto/testing/` |
| **ClickUp** | `os/skills/clickup/SKILL.md` | Product, CTO, CoS | Sync spec/roadmap/azioni con ClickUp — sempre PREPARE → APPROVE → EXECUTE via `clickup-pending/` |
| **Gmail** | `os/skills/gmail/SKILL.md` | Tutti gli agenti | Email come contesto (scan, ricerca thread) — mai dati sensibili fuori zona |
| **Fatture in Cloud** | `os/skills/fatture-in-cloud/SKILL.md` | Finance (owner), CEO, CoS | Sync fatture emesse, aging crediti, cashflow → `vault/finance/` |
| **Qonto** | `os/skills/qonto/SKILL.md` | Finance (owner), CEO, CoS | Saldi, transazioni e riconciliazione bancaria → `vault/finance/` |
| **Stripe** | `os/skills/stripe/SKILL.md` | Finance (owner), CEO, Sales | Pagamenti, subscription, payout; cross-ref clienti Stripe ↔ `20-Clienti/` |
| **ERP** | `os/skills/erp/SKILL.md` | Finance (owner), CEO, CoS | Pipe dati live ERP (fatturazione, cashflow, KPI) via MCP/REST |
| **Financial Import** | `os/skills/financial-import/SKILL.md` | Finance (owner), CEO, CoS | Metodologia parsing export JSON statico: formule MRR/burn/runway e regole specifiche dell'azienda |
| **Admin & Controllo** | `os/skills/admin-controllo/SKILL.md` | Finance (owner), CEO | Controllo di gestione startup italiana: cashflow, costi ricorrenti, adempimenti, incentivi |
| **Audit & Compliance** | `os/skills/audit-compliance/SKILL.md` | Compliance (owner), CTO, CEO, Sales | NIS2, GDPR, ISO27001: status, gap analysis, policy review, vendor assessment |
| **Investor Relations** | `os/skills/investor-relations/SKILL.md` | Finance (owner), CEO, Compliance | Investor update, pitch prep, data room readiness, cap table narrative |
| **Skill Creator** | `os/skills/skill-creator/SKILL.md` | Admin (owner) — richieste da tutti | Intervista conversazionale per creare nuove skill senza conoscenze tecniche |
| **Agent Creator** | `os/skills/agent-creator/SKILL.md` | Admin (owner) — richieste da tutti | Intervista conversazionale per creare nuovi agenti senza conoscenze tecniche |

## Skill di contesto

| Skill | Path | Usata da | Una riga |
|-------|------|----------|----------|
| **Pricing** | `os/skills/pricing/SKILL.md` | Product, Finance, Sales | Tiers dell'azienda, bundling, packaging, quotazioni (`20-Clienti/{slug}/proposte/quote-*`) |
| **Presentations** | `os/skills/presentations/SKILL.md` | CEO, Finance, Marketing, Sales | Deck con brand kit (`brand/company-theme.js`): pitch, board, proposte — pptx come build on-demand |
| **Spreadsheets** | `os/skills/spreadsheets/SKILL.md` | Finance, Product, Sales | Template e convenzioni per modelli finanziari e dashboard xlsx |
| **Writing** | `os/skills/writing/SKILL.md` | Marketing, CEO, Sales | Tone of voice, strutture, anti-slop (`references/`) per contenuti e copy |

## Regole d'uso

1. **Leggi** il `SKILL.md` della skill prima di eseguire un suo comando; carica i file di supporto solo se servono.
2. **Output nella zona giusta**: rispetta le destinazioni indicate dalla skill (zona Drive-master o `vault/`).
3. **Scritture esterne** (ClickUp, HubSpot, email, Drive publish): sempre PREPARE → APPROVE → EXECUTE (`os/protocols/external-writes.md`).
4. **Credenziali**: mai valori nel repo — i nomi delle variabili sono censiti in `config/integrations.yaml`.
5. **Skill interne prima dei plugin generici**: hanno il contesto dell'azienda (ICP, pricing, partner model).
