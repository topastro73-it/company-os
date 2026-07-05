# Skills — Index

Curated skills, rewritten for the CompanyOS zone structure
(`company/{zona}`, `vault/`, `20-Clienti/{slug}`; integration config in `config/integrations.yaml`).
Two categories:

- **Operational skills**: executable commands and/or integration with external systems
- **Context skills**: frameworks and guides read as background to inform decisions

Reference agents: see `ARCHITECTURE.md` §6 (`ceo`, `cos`, `sales`, `delivery`, `product`, `cto`, `finance`, `compliance`, `marketing`, `admin`).

## Operational skills

| Skill | Path | Used by | One line |
|-------|------|----------|----------|
| **Opportunity Management** | `os/skills/opportunity-management/SKILL.md` | Sales (owner), CoS, CEO, Finance | Account↔opportunity model, HubSpot-aligned stages, aging, `PIPELINE.md` board, deal drill-down |
| **Partner Onboarding** | `os/skills/partner-onboarding/SKILL.md` | Delivery (owner), Sales, Product | 90-day partner onboarding: phases, milestones, client record in `20-Clienti/{slug}/` |
| **Customer Success** | `os/skills/customer-success/SKILL.md` | Delivery (owner), Sales, CEO, CoS | Health score, churn prevention, QBR and expansion plan per client |
| **Outbound & ABM** | `os/skills/outbound-abm/SKILL.md` | Sales (owner), Marketing, CEO | Account-based outbound campaigns: targeting, sequences, value-first touchpoints |
| **Business Analysis** | `os/skills/business-analysis/SKILL.md` | Product (owner), CEO, CoS | Interactive functional analysis: AS-IS/TO-BE, process map, data model, gap analysis, functional spec |
| **QA & Testing** | `os/skills/qa-testing/SKILL.md` | CTO (owner), Product | Test plan, test cases, test report, smoke/security tests in `company/prodotto/testing/` |
| **ClickUp** | `os/skills/clickup/SKILL.md` | Product, CTO, CoS | Sync specs/roadmap/actions with ClickUp — always PREPARE → APPROVE → EXECUTE via `clickup-pending/` |
| **Gmail** | `os/skills/gmail/SKILL.md` | All agents | Email as context (scan, thread search) — never sensitive data outside its zone |
| **Fatture in Cloud** | `os/skills/fatture-in-cloud/SKILL.md` | Finance (owner), CEO, CoS | Sync issued invoices, receivables aging, cashflow → `vault/finance/` |
| **Qonto** | `os/skills/qonto/SKILL.md` | Finance (owner), CEO, CoS | Balances, transactions and bank reconciliation → `vault/finance/` |
| **Stripe** | `os/skills/stripe/SKILL.md` | Finance (owner), CEO, Sales | Payments, subscriptions, payouts; cross-ref Stripe customers ↔ `20-Clienti/` |
| **ERP** | `os/skills/erp/SKILL.md` | Finance (owner), CEO, CoS | Live ERP data pipe (invoicing, cashflow, KPIs) via MCP/REST |
| **Financial Import** | `os/skills/financial-import/SKILL.md` | Finance (owner), CEO, CoS | Static JSON export parsing methodology: MRR/burn/runway formulas and company-specific rules |
| **Admin & Controllo** | `os/skills/admin-controllo/SKILL.md` | Finance (owner), CEO | Italian startup management control: cashflow, recurring costs, statutory obligations, incentives |
| **Audit & Compliance** | `os/skills/audit-compliance/SKILL.md` | Compliance (owner), CTO, CEO, Sales | NIS2, GDPR, ISO27001: status, gap analysis, policy review, vendor assessment |
| **Investor Relations** | `os/skills/investor-relations/SKILL.md` | Finance (owner), CEO, Compliance | Investor updates, pitch prep, data room readiness, cap table narrative |
| **Skill Creator** | `os/skills/skill-creator/SKILL.md` | Admin (owner) — requests from everyone | Conversational interview to create new skills without technical knowledge |
| **Agent Creator** | `os/skills/agent-creator/SKILL.md` | Admin (owner) — requests from everyone | Conversational interview to create new agents without technical knowledge |

## Context skills

| Skill | Path | Used by | One line |
|-------|------|----------|----------|
| **Pricing** | `os/skills/pricing/SKILL.md` | Product, Finance, Sales | Company tiers, bundling, packaging, quotes (`20-Clienti/{slug}/proposte/quote-*`) |
| **Presentations** | `os/skills/presentations/SKILL.md` | CEO, Finance, Marketing, Sales | Decks with brand kit (`brand/company-theme.js`): pitch, board, proposals — pptx as on-demand build |
| **Spreadsheets** | `os/skills/spreadsheets/SKILL.md` | Finance, Product, Sales | Templates and conventions for financial models and xlsx dashboards |
| **Writing** | `os/skills/writing/SKILL.md` | Marketing, CEO, Sales | Tone of voice, structures, anti-slop (`references/`) for content and copy |

## Usage rules

1. **Read** the skill's `SKILL.md` before executing one of its commands; load supporting files only if needed.
2. **Output in the right zone**: respect the destinations indicated by the skill (Drive-master zone or `vault/`).
3. **External writes** (ClickUp, HubSpot, email, Drive publish): always PREPARE → APPROVE → EXECUTE (`os/protocols/external-writes.md`).
4. **Credentials**: never values in the repo — variable names are catalogued in `config/integrations.yaml`.
5. **Internal skills before generic plugins**: they carry the company's context (ICP, pricing, partner model).
