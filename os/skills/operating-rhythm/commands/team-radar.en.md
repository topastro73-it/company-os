---
status: attivo
area: sistema
---

# Command: team-radar

## Trigger
"what is {person} doing" / "cosa sta facendo {persona}", "what is {person} working on" / "su cosa lavora {persona}", "what happened this week" / "cosa è successo questa settimana",
"company news" / "novità in azienda", "team update". Read-only.

## Purpose
Keep the person up to date on what others and the company are doing. For the full digest by area
(pipeline, product, finance) there is `/cos weekly-digest`. Sources and rules in `../SKILL.md`.
Respect the zones: in a non-admin session show only what the person can read
(`config/acl.yaml`), and say so if a list looks thin.

## One person
1. **Who** — `config/people.yaml` (name, role, `default_agent`); several matches → ask.
2. **Accounts and opportunities** — files where they are `owner-sales`/`owner-pm`, with stage and next-step.
3. **Projects** — `company/direzione/projects/INDEX.md` (owner or support) and WOs where they are `to:`.
4. **Meetings in the last 7 days** — minutes where they appear among the participants, plus the
   relevant transcripts from the configured sources with their name (`../SKILL.md` § Meeting transcripts), flagging those without minutes.
5. **Open commitments** — minutes rows and `blockers` with owner = the person; ClickUp tasks
   assigned (if ClickUp doesn't respond: not verified).
6. **Decisions** — where they appear as the one who decided, last 14 days.

Output: **Accounts and projects** (role, status) · **Recent meetings** · **Open commitments**
(overdue first) · **Decisions**.

## The company
1. **Decisions of the week** — new files in `company/direzione/decisions/` since Monday.
2. **Meetings** — minutes of the week and relevant transcripts from the configured sources not yet
   imported, by account; those without an account separately. Of other companies' meetings, only the count.
3. **Movement** — in admin `git log --since=<monday>` grouped by zone and agent; opportunities
   that changed stage; new or closed blockers.

Output: **Decisions of the week** · **Accounts in motion** · **Blocked / needing attention** ·
**Who held the most meetings** (optional, one line). With artifacts, one page.

## Weekly digest
Schedule it on Monday at 08:30 with the prompt **"what happened last week" / "cosa è successo la settimana scorsa"**.
