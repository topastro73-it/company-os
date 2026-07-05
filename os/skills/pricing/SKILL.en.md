# Pricing Skill

Framework for pricing decisions in B2B SaaS. Used by PM, CFO and Sales.

> **Ownership (audit 2026-07-03):** this skill is the *shared reference*. The outputs have distinct owners:
> - **CFO** `/finance pricing-model` → `vault/finance/reports/pricing-model-{date}.md` — economic model (margins, unit economics, sensitivity).
> - **PM** `/product pricing-analysis` → `company/prodotto/analysis/pricing-{slug}.md` — pricing impact of a feature/packaging.
> - **Sales** `/sales pricing-quote` → quote for a single deal.
> The **official pricing** lives in `vault/finance/pricing.md` (SSoT); the others are supporting analyses. Do not confuse the three outputs.

## B2B SaaS Pricing Principles

### Value-Based Pricing
Don't price based on costs. Price based on the value the customer gets.
Key question: "How much is solving this problem worth to the customer?"

### Pricing Architecture

#### Models
| Model | When to use it | Pros | Cons |
|-------|----------------|------|------|
| **Per-seat** | Value grows with users | Predictable, scalable | Limits adoption |
| **Usage-based** | Value proportional to usage | Aligned with value | Unpredictable for the customer |
| **Flat fee** | Simplicity is a differentiator | Easy to sell | Doesn't scale with value |
| **Tiered** | Different segments with different needs | Natural segmentation | Complexity |
| **Hybrid** | Need for predictability + upside | Balanced | More complex to communicate |

#### Packaging (Tiers)
| Tier | Target | Characteristics |
|------|--------|-----------------|
| **Starter/Basic** | SMB, self-serve | Core features, limits on volume/users |
| **Professional** | Mid-market | All features, integrations, support |
| **Enterprise** | Enterprise, high-touch | Custom, SLA, dedicated support, SSO, audit |

### Decision Framework

#### For a new feature — where do I put it?
1. **Core** (included in all tiers): if it's table stakes or if competitive differentiation requires it
2. **Tier-gated**: if the target segment is clear (e.g. SSO → Enterprise)
3. **Add-on**: if the value is independent of the tier and separately measurable
4. **Usage-based**: if the value is directly proportional to usage

#### For a pricing change
1. Analyze the impact on existing customers (grandfathering?)
2. Model the revenue impact: ACV change × conversion change × churn change
3. Test: what does the competitor do? Is our price justifiable?
4. Communicate: transparency about why the change, adequate notice

### Pricing Health Metrics
- **Average ACV**: trend and distribution
- **Average discount rate**: how much do we come down from list price? (target: <15%)
- **Tier distribution**: % of customers per tier (healthy: 60% mid, 25% starter, 15% enterprise)
- **Upgrade rate**: % of customers moving up a tier
- **Price sensitivity**: at what point does price block deals?

### Anti-Patterns
- ❌ "The competitor charges X, we charge X-20%" → race to the bottom
- ❌ "The customer says it's too expensive" → they might not be your ICP
- ❌ "Different price for every customer" → operational nightmare
- ❌ "Unlimited free tier" → attracts wrong-fit customers
- ❌ "Discount to close the deal" → without a process = slippery slope

### Where pricing data lives in the repo
- `vault/finance/pricing.md` — Current price list and tier structure
- `decisions/` — Past pricing decisions with rationale
- `company/prodotto/analysis/pricing-*.md` — Pricing analyses (by PM and CFO)
- `20-Clienti/{slug}/proposte/quote-*.md` — Quotes (by Sales)
