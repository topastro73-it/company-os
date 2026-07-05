# Workflow: Feature Lifecycle

From commercial feedback to a live, sold feature.

## 1. Request (Sales)
- **Trigger**: a client or prospect asks for a feature (call, demo, RFP)
- **Input**: conversation, deal context (`commerciale` zone / client folder)
- **Action**: document the request with business context (who, why, deal value,
  urgency) in `30-Prodotto/richieste/{YYYY-MM-DD}-{slug}.md`
- **Handoff → Product**: request present in `richieste/`, with linked deal

## 2. Evaluate (Product)
- **Input**: request in `30-Prodotto/richieste/`
- **Action**: first run the status check (`os/protocols/spec-lifecycle.md`), then apply
  the BUILD / CONFIGURE / CUSTOM / DECLINE framework
- **Output**: `30-Prodotto/specs/evaluation-{slug}.md` (status `evaluated`)
- **If DECLINE**: reasoned reply for Sales in the request; the workflow ends
- **Handoff → Product (spec)**: if BUILD

## 3. Spec (Product)
- **Action**: write the full PRD; check compliance impact (personal data,
  security) → frontmatter `compliance-impact:` if relevant
- **Output**: `30-Prodotto/specs/prd-{slug}.md` (status `draft` → `approved` after review)
- **Handoff → CTO**: PRD ready for estimation

## 4. Tech review (CTO)
- **Action**: feasibility, effort estimate, risks; if an architectural decision → ADR in the
  `prodotto` zone; verify it doesn't break the security controls mapped in `50-Compliance/`
- **Output**: annotations on the PRD (+ ADR)
- **Handoff → Product**: estimate and risks available

## 5. Prioritize & build (Product)
- **Action**: RICE score, insertion into `30-Prodotto/backlog`; ClickUp sync via
  PREPARE → APPROVE → EXECUTE (`os/protocols/external-writes.md`); status `in-development`
  → propose test plan (`spec-lifecycle.md`)
- **Build**: development is outside agent scope; Product monitors the Epic
- **Exit criterion**: all Epic tasks `Released` + UAT GO → spec `shipped`
  (with spec-reconciliation)

## 6. Launch (Marketing)
- **Input**: spec `shipped`
- **Action**: launch plan — public changelog, content, email
- **Output**: `marketing` zone (`60-Marketing/`); 🟢 materials after redaction
- **Handoff → Sales**: enablement material ready

## 7. Sell (Sales)
- **Action**: update battlecards (`10-Commerciale/battlecards/`), notify the prospects who
  had asked for it (email drafts via external-writes), update the linked opportunities
- **Closure**: original request in `richieste/` marked `shipped` with a link to the spec
