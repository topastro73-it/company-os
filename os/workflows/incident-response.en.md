# Workflow: Incident Response

Outage or technical/security incident on the platform.

## 1. Detect & assess (CTO)
- **Trigger**: outage, degradation, security alert, client report
- **Action**: classify severity — **P0** (down / data breach) · **P1** (degraded) ·
  **P2** (minor impact); assess impact: how many partners/end-customers, which features
- **Output**: incident record `30-Prodotto/incidents/{YYYY-MM-DD}-{slug}.md`
  (severity, timeline, impact, owner)
- **Handoff → CEO**: immediate for P0/P1; P2 can proceed straight to phase 3

## 2. Communicate (CEO + Marketing)
- **P0/P1 action**: immediate communication to impacted clients (drafts via
  `os/protocols/external-writes.md` — in P0 the approval is prioritized, not skipped);
  status page; internal notification to the team
- **If personal data is involved**: activate Compliance immediately (GDPR 72h notification
  assessment / NIS2 obligations toward Telco partners) — do not wait for resolution
- **Output**: communications tracked in the impacted clients' folders
  (`20-Clienti/{slug}/`)

## 3. Resolve (CTO)
- **Action**: fix and deploy; verify observed resolution (not just a successful deploy)
- **Output**: incident record updated with the resolution timeline
- **Exit criterion**: service verified working + confirmation on sample clients

## 4. Post-mortem (CTO)
- **When**: within 5 business days for P0/P1
- **Action**: **blameless** post-mortem — what happened, why, what prevents it;
  action items with owner and deadline
- **Output**: post-mortem section in the incident record; preventive actions → backlog
  `30-Prodotto/`; if a security incident → evidence in `50-Compliance/evidence/`
- **Handoff → CEO + Sales/Delivery**: post-mortem ready

## 5. Follow-up (CEO + Sales/Delivery)
- **Action**: closing communication to impacted clients; if significant impact →
  personal call with top clients; update health scores in the `clienti` zone
- **Learning**: generalizable pattern → propose LRN-XXX (`os/protocols/memory.md` §3)

## Rules
- P0: the incident record is opened BEFORE starting the fix (30 seconds, not a report)
- Never downplay in communications: facts, impact, ETA, next update
- Post-mortem action items always have an owner and a deadline — without them, it's not closed
