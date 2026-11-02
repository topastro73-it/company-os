---
status: attivo
area: sistema
---

# Command: my-day

## Trigger
"what's my day" / "com'è la mia giornata", "what do I have today" / "cosa ho oggi", "morning brief" / "brief del mattino", "catch me up" / "aggiornami", or a scheduled run
"run my day" / "esegui la mia giornata". Read-only.

## Purpose
One page that tells the person where they stand this morning: **their** meetings, commitments,
approvals and accounts. For the CEO's company view there is `/cos daily-briefing`.
Common sources and rules in `../SKILL.md`.

## Process (in parallel where possible)
1. **Who and when** — the person (`config/people.yaml`) and today's date.
2. **Today's meetings** — from the Calendar connector. For each one with a known account, the link to the
   account card or the opportunity and whether a brief already exists in `meeting-prep/`.
3. **Meetings without minutes** — relevant transcripts from the configured sources for the last 7 days
   (`../SKILL.md` § Meeting transcripts) not yet imported, plus Calendar events with external attendees without
   minutes (propose `follow-up-all`).
4. **My commitments** — "Impegni / action item" (commitments / action items) rows of recent minutes with owner = me and status
   not `fatto`; `next-step`/`next-step-due` and `blockers` of the opportunities I own; ClickUp
   tasks assigned to me in the company workspace (if ClickUp doesn't respond: not verified).
5. **To approve** — files `status: pending` in `company/*/*-pending/` and decisions
   `**Stato**: Proposta` that concern me or my role; files `status: in-attesa` with `waiting_on` = me.
6. **News on my accounts** — in admin `git log --since=<yesterday>` on files I own;
   new decisions in `company/direzione/decisions/`.
7. **Emails to answer** (optional, gmail skill) — up to 5 threads from people in my accounts.

## Output
First the thing that needs an action. Then, only if not empty:
**Today** (Rome time, title, account) · **Without minutes** · **To approve** (propose `approvals`) ·
**My commitments** (overdue, then today, then the rest) · **News on my accounts** ·
**Blocked** (open blockers) · **Emails to answer**. Each item with the file path.
With artifacts available: a card page with the counts in the titles.

## Every morning
A skill doesn't schedule itself: create a scheduled task on weekdays at 08:00 with the
prompt **"run my day" / "esegui la mia giornata"**.
