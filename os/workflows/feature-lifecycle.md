# Workflow: Feature Lifecycle

Da feedback commerciale a feature live e venduta.

## 1. Request (Sales)
- **Trigger**: cliente o prospect chiede una feature (call, demo, RFP)
- **Input**: conversazione, contesto deal (zona `commerciale` / cartella cliente)
- **Azione**: documenta la richiesta con contesto business (chi, perché, valore del deal,
  urgenza) in `30-Prodotto/richieste/{YYYY-MM-DD}-{slug}.md`
- **Handoff → Product**: richiesta presente in `richieste/`, con deal collegato

## 2. Evaluate (Product)
- **Input**: richiesta in `30-Prodotto/richieste/`
- **Azione**: prima esegui lo status check (`os/protocols/spec-lifecycle.md`), poi applica
  il framework BUILD / CONFIGURE / CUSTOM / DECLINE
- **Output**: `30-Prodotto/specs/evaluation-{slug}.md` (status `evaluated`)
- **Se DECLINE**: risposta motivata per Sales nella richiesta; il workflow finisce
- **Handoff → Product (spec)**: se BUILD

## 3. Spec (Product)
- **Azione**: scrivi la PRD completa; verifica impatto compliance (dati personali,
  security) → frontmatter `compliance-impact:` se rilevante
- **Output**: `30-Prodotto/specs/prd-{slug}.md` (status `draft` → `approved` dopo review)
- **Handoff → CTO**: PRD pronta per stima

## 4. Tech review (CTO)
- **Azione**: feasibility, stima effort, rischi; se decisione architetturale → ADR in zona
  `prodotto`; verifica che non rompa i controlli di sicurezza mappati in `50-Compliance/`
- **Output**: annotazioni sulla PRD (+ ADR)
- **Handoff → Product**: stima e rischi disponibili

## 5. Prioritize & build (Product)
- **Azione**: RICE score, inserimento in `30-Prodotto/backlog`; sync ClickUp via
  PREPARE → APPROVE → EXECUTE (`os/protocols/external-writes.md`); status `in-development`
  → proponi test plan (`spec-lifecycle.md`)
- **Build**: sviluppo fuori scope agenti; Product monitora l'Epic
- **Criterio di uscita**: tutti i task Epic `Released` + UAT GO → spec `shipped`
  (con spec-reconciliation)

## 6. Launch (Marketing)
- **Input**: spec `shipped`
- **Azione**: launch plan — changelog pubblico, contenuti, email
- **Output**: zona `marketing` (`60-Marketing/`); materiali 🟢 dopo redazione
- **Handoff → Sales**: enablement material pronto

## 7. Sell (Sales)
- **Azione**: aggiorna battlecard (`10-Commerciale/battlecards/`), notifica i prospect che
  l'avevano chiesta (bozze email via external-writes), aggiorna le opportunità collegate
- **Chiusura**: richiesta originale in `richieste/` marcata `shipped` con link alla spec
