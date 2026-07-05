# /delivery new-partner — Partner onboarding kickoff

## Purpose
Turn a won deal into a tracked 90-day onboarding, from day 1.

## Input
- Partner name · type (Telco Tier-1 / regional ISP / MSP-MSSP) · contract tier
- Signature date · main contact (name, role, email) · contractual SMB target

## Steps
1. Verify the handoff from Sales: `won` opportunity in the `commerciale` zone (link it).
2. Create the `clienti/{slug}/` folder (if admin: ask `admin`/osctl to create the
   Drive folder with per-folder ACL and the client's owner assigned).
3. Create the **partner card** (format below) with phase = SETUP, start = signature date.
4. Generate the **onboarding checklist** with the 4 phases and deadlines computed from signature:
   SETUP (kickoff d.1, tenant d.3, users d.5, first SMBs d.7, catalog d.10, e2e test d.14) →
   ENABLEMENT (training, co-branded material, list of 20-50 target SMBs) →
   LAUNCH (campaign, 10+ assessments, first proposal, first deal wk.8) →
   OPTIMIZE (conversion analysis, 90d QBR, health baseline).
5. Notify: kickoff call to schedule (Sales + Delivery), tenant setup → `cto`.

## Output format (partner card)
```markdown
---
zone: clienti/{slug}
tier: 🟡
type: partner
partner-type: isp-tier2
contract-tier: engage
signed: YYYY-MM-DD
onboarding-phase: setup
health-score: null        # baseline at day 90
owner-delivery: {person}
target-pmi: 40
---
# {Partner Name}
## Contacts  ## Contract (ref. clienti/{slug}/contratti/ 🔴)
## 90d onboarding — checklist by phase (tasks, owner, deadline, status)
## Timeline  ## Notes
```

## Destination
`clienti/{slug}` zone → `scheda-partner.md` + `onboarding-checklist.md`.
Commit (admin): `[delivery] onboarding: new partner {name} — setup started`.

## Handoff
`cto` (white-label tenant) · `sales` (joint kickoff) · `finance` (first invoice).
