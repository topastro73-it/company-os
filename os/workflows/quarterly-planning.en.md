# Workflow: Quarterly Planning

Coordinated quarterly planning. Timeline: ~10 business days.

## Phase 1 — Strategic direction (Day 1-2) · CEO
- **Input**: OKRs and strategy of the closing quarter (`00-Direzione/`), KPIs, recent wiki
- **Action**: review of the previous quarter, OKR scoring, draft of new OKRs
- **Output**: `00-Direzione/okrs/YYYY-QN.md` (draft) + directional decisions in
  `00-Direzione/decisions/` (`os/protocols/decisions.md`)
- **Handoff → Product + CTO**: OKR draft shared

## Phase 2 — Roadmap proposal (Day 3-5) · Product
- **Input**: OKR draft, current backlog and roadmap (`30-Prodotto/`)
- **Action**: spec status check (`spec-lifecycle.md`), roadmap review, RICE
  re-prioritization of the backlog in light of the new OKRs
- **Output**: quarterly roadmap proposal in `30-Prodotto/roadmap/`
- **Handoff → CTO**: proposed roadmap, with open feasibility points marked

## Phase 3 — Tech feasibility (Day 5-7) · CTO
- **Input**: proposed roadmap
- **Action**: architecture review if decisions are needed (ADR), share of tech debt to
  include, estimates, risks, dependencies
- **Output**: annotations on the roadmap (estimates/risks) + any ADRs in `30-Prodotto/`
- **Handoff → Sales**: technically validated roadmap

## Phase 4 — Sales alignment (Day 7-8) · Sales
- **Input**: validated roadmap, pipeline (`10-Commerciale/`)
- **Action**: feature ↔ deal mapping in the pipeline; gap analysis: is something missing to
  close deals in progress? Is a different order needed?
- **Output**: alignment note in `10-Commerciale/` with specific requests
- **Handoff → Product**: final adjustments to the roadmap (motivated by the deals)

## Phase 5 — GTM planning (Day 8-10) · Marketing
- **Input**: final roadmap
- **Action**: content plan for the quarter; launch plan for each major feature
- **Output**: content calendar and launch plans in `60-Marketing/`

## Closure · CEO
- **Action**: finalized OKRs (`00-Direzione/okrs/YYYY-QN.md`, final status); investor
  update with the quarterly plan (`00-Direzione/investor-updates/`, `render: gdoc`)
- **Exit criterion**: final OKRs + roadmap + content plan all in their respective zones,
  snapshot at close versioning them in git

## Rules
- No phase skips the previous one: a roadmap without CTO feasibility does not go to Sales
- Dates promised to clients/investors go out ONLY after Phase 3 (never without the CTO)
