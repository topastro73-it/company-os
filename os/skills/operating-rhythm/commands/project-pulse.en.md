---
status: attivo
area: sistema
---

# Command: project-pulse

## Trigger
"how is {account} going" / "come va {account}", "status of {opportunity}" / "stato di {opportunità}", "where is P-00N at" / "a che punto è P-00N", "update the status" / "aggiorna lo stato",
"write the status" / "scrivi lo status".

## Purpose
The state of **one** account, opportunity or internal project, and its update. For the
traffic lights across all workstreams there is `/cos status-check`. Sources and rules in `../SKILL.md`.

## Read
1. **The main file** — `company/clienti/{slug}/overview.md`, the opportunity
   `company/commerciale/opportunities/{opp-slug}.md` or `company/direzione/projects/P-NNN-*.md`.
   Ambiguous name → list the candidates and ask.
2. **Linked** — opportunities with the same `account`, minutes from the last 30 days
   (`type: minuta`, `account`), decisions that mention it, WOs/goals in `company/direzione/ops/`.
   Always also search the transcripts from the configured sources with the account name (`../SKILL.md` §
   Transcript): those not imported go under **Inconsistencies** ("meeting of dd/mm without minutes").
3. **Work** — open commitments in the minutes, `next-step`/`blockers`, linked ClickUp tasks.
4. **Movement** — in admin `git log --since=<today-14>` on the account's files.

## Output
**Status** (stage/status, owner, one-line summary) · **Needed now** (`next-step` with
deadline, blockers with owner) · **Latest decisions** · **Recent meetings** (date, link to the
minutes) · **Commitments** (open / overdue) · **Inconsistencies** (e.g. `last-activity` older
than the latest minutes, overdue next-step, account without an opportunity file).

## Status update (on request, or propose it if `last-activity` is more than 7 days old)
1. Draft: the frontmatter fields to change (`stage`, `probability`, `next-step`,
   `next-step-due`, `blockers`, `last-activity`, `health-score`…) and 4–6 timeline lines (done,
   in progress, risks, next steps), only from cited sources.
2. Wait for "ok", then write. Stage change of an opportunity → also `PIPELINE.md`.
3. Commit `[{agente}] opportunity|delivery: {slug} → …`.

## Rules
Never invent progress: if nothing has moved, say so. Changes that require another role
(prices, delivery dates, features) go through their owner (CLAUDE.md, rule 7).
