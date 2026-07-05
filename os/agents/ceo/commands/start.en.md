# /ceo start — Admin session opening

## Purpose
Open the CEO's day: context rebuilt, alerts highlighted, 3 clear priorities.

## Input
None (implicit: first interaction of the admin session).

## Steps
1. **Stale session check**: if the last session in `direzione/ceo-cadence.md` has no
   page in `system/wiki/sessions/`, propose recovery (full / stub / skip-and-log) BEFORE the briefing.
2. **Cadence**: determine from `direzione/ceo-cadence.md` whether daily / weekly / monthly applies.
3. **Where we left off**: last wiki page → decisions, open questions, expired promises (3-5 lines).
4. **Learnings**: load `system/learnings.md`, apply proactively during the session.
5. **Alert scan** (from the zone snapshots; if stale, flag it and suggest `osctl snapshot`):
   - `vault/finance/`: tax deadlines ≤3 days, invoices overdue 30+ days
   - `commerciale` zone: 🔴/🟠 opportunities (aging, read-only), deals without owner
   - `clienti` zone: Critical/At-Risk partners (health score), delayed onboarding
   - `compliance` zone: deadlines ≤7 days, audits ≤30 days, missing evidence
   - `prodotto` zone: stale specs, decisions awaiting the CEO
6. **Compose the briefing** (format below) and **ask the questions** of the active cadence.
7. **Record the answers** in `direzione/ceo-cadence.md` and update the touched zone files.
8. Close with: "what do you want to do today?" → handoff to the requested agent.

## Output format (in chat, not a file)
```
🟣 **[Claude]**
Good morning {name}. Here is your day.

QUICK STATUS — pending decisions: N · overdue follow-ups: N · partner alerts: N ·
🔴 deals: N · tax deadlines 3 days: N · invoices overdue 30+ days: N

URGENT (answer NOW)
1. [what] — [1 line of context] — [options A/B/C]

YOUR 3 PRIORITIES FOR TODAY
1. [priority] — why: [reason]

ONE QUESTION FOR YOU
[the most important question nobody is asking you]
```
The weekly cadence adds: last week's review, spec status, admin & finance,
stale metrics, priorities for the week. The monthly adds: results retrospective,
not-done, risks (OKRs, partners, runway), 3 strategic questions.

## Destination
`direzione` zone — updates to `ceo-cadence.md` and `ceo-routine.md`. No report file.
