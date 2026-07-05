# Workflow: Quarterly Planning

Pianificazione trimestrale coordinata. Timeline: ~10 giorni lavorativi.

## Fase 1 — Strategic direction (Day 1-2) · CEO
- **Input**: OKR e strategia del trimestre chiuso (`00-Direzione/`), KPI, wiki recente
- **Azione**: review del trimestre precedente, scoring OKR, draft nuovi OKR
- **Output**: `00-Direzione/okrs/YYYY-QN.md` (draft) + decisioni direzionali in
  `00-Direzione/decisions/` (`os/protocols/decisions.md`)
- **Handoff → Product + CTO**: OKR draft condivisi

## Fase 2 — Roadmap proposal (Day 3-5) · Product
- **Input**: OKR draft, backlog e roadmap correnti (`30-Prodotto/`)
- **Azione**: status check spec (`spec-lifecycle.md`), roadmap review, ri-prioritizzazione
  RICE del backlog alla luce dei nuovi OKR
- **Output**: proposta roadmap trimestrale in `30-Prodotto/roadmap/`
- **Handoff → CTO**: roadmap proposta, con punti aperti di feasibility marcati

## Fase 3 — Tech feasibility (Day 5-7) · CTO
- **Input**: roadmap proposta
- **Azione**: architecture review se servono decisioni (ADR), quota di tech debt da
  includere, stime, rischi, dipendenze
- **Output**: annotazioni su roadmap (stime/rischi) + eventuali ADR in `30-Prodotto/`
- **Handoff → Sales**: roadmap tecnicamente validata

## Fase 4 — Sales alignment (Day 7-8) · Sales
- **Input**: roadmap validata, pipeline (`10-Commerciale/`)
- **Azione**: mapping feature ↔ deal in pipeline; gap analysis: manca qualcosa per
  chiudere deal in corso? Serve ordine diverso?
- **Output**: nota di allineamento in `10-Commerciale/` con richieste puntuali
- **Handoff → Product**: aggiustamenti finali sulla roadmap (motivati dai deal)

## Fase 5 — GTM planning (Day 8-10) · Marketing
- **Input**: roadmap finale
- **Azione**: content plan del trimestre; launch plan per ogni feature major
- **Output**: calendario contenuti e piani launch in `60-Marketing/`

## Chiusura · CEO
- **Azione**: OKR finalizzati (`00-Direzione/okrs/YYYY-QN.md`, status final); investor
  update con il piano trimestrale (`00-Direzione/investor-updates/`, `render: gdoc`)
- **Criterio di uscita**: OKR finali + roadmap + content plan tutti nelle rispettive zone,
  snapshot al close che li versiona in git

## Regole
- Nessuna fase salta la precedente: la roadmap senza feasibility CTO non passa a Sales
- Le date promesse a clienti/investitori escono SOLO dopo la Fase 3 (mai senza CTO)
