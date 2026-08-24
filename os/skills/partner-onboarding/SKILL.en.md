# Partner Onboarding Skill

Structured 90-day process from signed contract to first revenue. Used by Sales, PM, Chief of Staff.

## Overview

Onboarding a new partner follows 4 phases over 12 weeks. The goal is to take the partner from signature to **first revenue generated through the platform** as quickly and predictably as possible.

```
Week      1-2    3-4       5-8        9-12
          SETUP → ENABLEMENT → LAUNCH → OPTIMIZE
```

---

## Phase 1: SETUP (Week 1–2)

**Goal**: Platform configured, partner team with access, first SMBs loaded.

| # | Task | Owner | Success Criteria | Deadline |
|---|------|-------|-----------------|----------|
| 1.1 | Kickoff call with partner (alignment on expectations, timeline, KPIs) — use `90-Condivisi/template-deliverable/company-poc-kickoff.pptx` as the reference asset if the partner requested a guided PoC pre-signature | Sales | Meeting held, notes in CRM | Day 1 |
| 1.2 | White-label tenant creation (branding, logo, colors, domain) | CTO/Engineering | Tenant live with partner branding | Day 3 |
| 1.3 | Partner user configuration (admin + sales reps) | CTO/Engineering | All users created and active | Day 5 |
| 1.4 | Import first 5-10 pilot SMBs | Partner + PM | SMBs loaded, first scan completed | Day 7 |
| 1.5 | Partner service catalog configuration | PM | Catalog mapped to remediation | Day 10 |
| 1.6 | End-to-end test: scan → report → proposal | PM + Partner | Full flow working | Day 14 |

### Phase deliverables
- White-label tenant live
- At least 5 pilot SMBs with completed scan
- Service catalog configured

---

## Phase 2: ENABLEMENT (Week 3–4)

**Goal**: Partner's sales team trained and autonomous in using the platform.

| # | Task | Owner | Success Criteria | Deadline |
|---|------|-------|-----------------|----------|
| 2.1 | Sales rep training: how to use the platform to sell | Sales + PM | Training completed, quiz passed | Week 3 |
| 2.2 | Technical training: interpreting scans and reports | PM/Pre-sales | Technical team autonomous | Week 3 |
| 2.3 | Co-branded material creation (pitch deck, one-pager) | Marketing + Partner | Material approved by the partner | Week 3 |
| 2.4 | Sales role-play sessions (common objections) | Sales | At least 2 sessions completed | Week 4 |
| 2.5 | Lead gen campaign setup (email templates, landing) | Marketing + Partner | Campaign ready to launch | Week 4 |
| 2.6 | Target definition: list of 20-50 SMBs to contact | Partner + Sales | List validated and prioritized | Week 4 |

### Phase deliverables
- Sales team trained and certified
- Co-branded material ready
- Initial pipeline of 20-50 target SMBs

---

## Phase 3: LAUNCH (Week 5–8)

**Goal**: First real sales, active pipeline, partner autonomous in the sales cycle.

| # | Task | Owner | Success Criteria | Deadline |
|---|------|-------|-----------------|----------|
| 3.1 | Outbound campaign launch on the SMB list | Partner + Sales | Campaign live, first replies | Week 5 |
| 3.2 | First 10+ free assessments sent | Partner | 10 SMBs with report received | Week 6 |
| 3.3 | Assessment follow-up → first sales meeting | Partner + Sales | At least 3 meetings booked | Week 6-7 |
| 3.4 | First commercial proposal sent | Partner | 1+ proposal sent via the platform | Week 7 |
| 3.5 | First deal closed (even a small one) | Partner | Revenue > 0 from the platform | Week 8 |
| 3.6 | Mid-launch review: what works, what doesn't | Sales + PM + Partner | Corrective actions identified | Week 6 |

### Phase deliverables
- First revenue generated
- Active pipeline with 5+ opportunities
- Partner autonomous in the assess → propose → close cycle

---

## Phase 4: OPTIMIZE (Week 9–12)

**Goal**: Sustainable growth, consolidated processes, health score > 70.

| # | Task | Owner | Success Criteria | Deadline |
|---|------|-------|-----------------|----------|
| 4.1 | Assessment → deal conversion rate analysis | PM + Sales | Report with insights and actions | Week 9 |
| 4.2 | Service catalog optimization (based on real data) | PM + Partner | Catalog updated with top sellers | Week 10 |
| 4.3 | Continuous monitoring setup for active SMBs | PM/Engineering | Partner dashboard live | Week 10 |
| 4.4 | First internal QBR (90-day review) | Sales + PM | QBR completed, Q+1 plan | Week 12 |
| 4.5 | Health score check and baseline | CoS/Sales | Health score calculated and recorded | Week 12 |
| 4.6 | Upsell evaluation: tier upgrade or additional services | Sales | Recommendation with timeline | Week 12 |

### Phase deliverables
- Health score baseline recorded (target > 70)
- Next quarter plan defined
- Decision point: expand, maintain, or intervene

---

## Commands

| Command | Description | Output |
|---------|-------------|--------|
| `new-partner` | Initializes onboarding for a new partner | Creates partner record + tracking checklist |
| `status` | Shows onboarding status of a partner (or all) | Report with current phase and completion |
| `checklist` | Shows the detailed checklist of the current phase | Task list with status and owner |

---

## Command: new-partner

### Input
- Partner name
- Type (e.g. `segment-a` / `segment-b` / `segment-c` — the real segments live in `config/company.yaml`)
- Contract tier (see `config/company.yaml` → `pricing.tiers`, e.g. Starter / Professional / Scale / Enterprise)
- Contract signature date
- Main contact (name, role, email)

### Process
1. Create file `20-Clienti/{slug}/overview.md` from the template
2. Fill in initial data
3. Set phase = SETUP, start date = signature date
4. Generate phase 1 checklist with calculated deadlines
5. Handoff: notify Sales + PM for kickoff

### Output
- Partner file created in `20-Clienti/{slug}/overview.md`
- Commit: `[sales] onboarding: new partner {name} — setup phase started`

---

## Command: status

### Input
- Partner slug (optional — if omitted, all)

### Output format
```
## Onboarding Status — {date}

| Partner | Phase | Week | Completion | Next milestone | Alert |
|---------|-------|------|-----------|----------------|-------|
| Partner A | LAUNCH | 6/12 | 75% | First deal (week 8) | - |
| Partner B | SETUP | 2/12 | 40% | First scan (day 7) | Task 1.4 late |
```

---

## Command: checklist

### Input
- Partner slug
- Phase (optional — default: current phase)

### Output
Phase checklist with the status of each task:
```
## SETUP Checklist — Partner A (Week 1/2)

- [x] 1.1 Kickoff call — completed 2026-03-01
- [x] 1.2 White-label tenant — completed 2026-03-03
- [ ] 1.3 User configuration — in progress (deadline: 2026-03-05)
- [ ] 1.4 Pilot SMB import — not started (deadline: 2026-03-07)
- [ ] 1.5 Service catalog — not started (deadline: 2026-03-10)
- [ ] 1.6 End-to-end test — not started (deadline: 2026-03-14)

Completion: 33% | On track: Yes
```

---

## Where the data lives

| Data | Path |
|------|------|
| Partner records | `20-Clienti/{slug}/overview.md` |
| Record template | `20-Clienti/TEMPLATE.md` |
| Customer segments | `company/commerciale/segments.md` |
| **PoC kickoff deck** (pre-signature asset — standard for activating a prospect's guided PoC) | `90-Condivisi/template-deliverable/company-poc-kickoff.pptx` (source: `gen_poc_kickoff_deck.py`) |
| **PoC restitution deck** (example: {cliente}, reference for delivering post-PoC results) | `20-Clienti/acme/report/` ({cliente} PoC restitution deck — historical asset to republish) |
