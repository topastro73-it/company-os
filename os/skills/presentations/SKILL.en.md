# Presentations Skill

Framework for creating presentations. Used by CEO, Marketing, Sales, PM.

## Available Presentation Types

### 1. Pitch Deck (Investors) — Owner: CEO
Standard structure (10-12 slides):
1. **Title + One-liner**
2. **Problem** — The pain point, size of the problem
3. **Solution** — How we solve it (demo screenshot)
4. **Market** — TAM/SAM/SOM
5. **Business Model** — How we make money
6. **Traction** — Key metrics, growth, customers
7. **Competition** — Competitive map, differentiation
8. **Team** — Founders, advisors
9. **Financials** — Revenue, projections, unit economics
10. **The Ask** — How much we are raising, use of funds
11. **Vision** — Where we will be in 5 years
12. **Contact** — CTA

### 2. Product Demo Deck (Customers) — Owner: Sales + PM
Structure (8-10 slides):
1. **Title + Customer-centric hook**
2. **Their problem** (talk about THEM)
3. **How we solve it** — Solution overview
4. **Demo walkthrough** — 3-5 slides with screenshots/flow
5. **Results** — Case study, impact metrics
6. **Why us** — Differentiators
7. **Pricing overview** — Tiers and ranges
8. **Next steps** — Trial, POC, contract

### 3. Sales Proposal Deck — Owner: Sales
Structure (6-8 slides):
1. **Title + Prospect name**
2. **Your challenge** (personalized)
3. **Our solution for you** (personalized)
4. **Expected impact** (ROI, metrics)
5. **Pricing** (specific quote)
6. **Timeline** (implementation)
7. **Social proof** (similar case study)
8. **Next steps**

## How to generate the presentations

To generate a real `.pptx` file, ask Claude Code:
"Generate a .pptx presentation for [type] following the framework in `os/skills/presentations/SKILL.md`"

Claude Code can generate real PowerPoint files using the pptxgenjs library.

## Brand template (MANDATORY)

All company presentations must use the **brand template** in
`os/skills/presentations/brand/` — do NOT generate decks with pptxgenjs's default style.

- **Tokens & guidelines**: `company/marketing/brand/company-brand.md` (SSoT: colors, fonts, layout).
- **pptxgenjs module**: `os/skills/presentations/brand/company-theme.js`
  (`applyBrand()` + helpers `slideTitle / slideSection / slideContent / slideMetrics / slideClosing`).
- **How to use it**: see `os/skills/presentations/brand/README.md`.
- **Sample**: `node os/skills/presentations/brand/build-sample.js`.

Identity in brief (neutral default theme, to be customized with your brand): dark background, signature
accent **`#2563EB`** (placeholder), **system sans-serif** font, large numbers for metrics,
footer with wordmark + website + page number.

Workflow: pick the structure from the deck type (below) → map each slide to a template helper → generate the `.pptx`.

## Design Principles
- **One idea per slide** — don't overload
- **Little text** — maximum 5-6 lines per slide
- **Big numbers** — key metrics in large font
- **Consistency** — same style, fonts, colors across all slides
- **Visual > text** — screenshots, charts, diagrams whenever possible
