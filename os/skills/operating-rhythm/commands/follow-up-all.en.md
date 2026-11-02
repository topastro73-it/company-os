---
status: attivo
area: sistema
---

# Command: follow-up-all

## Trigger
"follow up my meetings" / "segui i miei meeting", "clear the follow-ups" / "smaltisci i follow-up", "which meetings have no minutes" / "quali meeting non hanno la minuta", or a
scheduled run "prepare the minutes for yesterday's meetings" / "prepara le minute dei meeting di ieri".

## Purpose
Work through, one at a time, the person's meetings still without minutes. For promised and
overdue follow-ups (open commitments) there is `/cos follow-up-tracker`. Sources and rules in `../SKILL.md`.

## Process
1. **Find the pending meetings** — always all transcripts from the configured sources for the
   last 14 days (or the requested period), filtered for relevance and already-imported as in
   `../SKILL.md` § Meeting transcripts; plus Calendar events with external attendees that have neither transcript nor minutes.
   With no reachable source and no Calendar: say so and ask the person for the list.
2. Show the list oldest first: date, title, account (or "account to be defined"), transcript
   yes/no, relevance (yes / partial / doubtful). At the bottom a single line: "N meetings of other companies
   excluded" (no titles). Doubtful ones are asked here, together with accounts to be defined. Ask: all or only some? Accounts to be defined are asked right away, with a single
   question that lists them all.
3. For each chosen meeting, the `publish-call` procedure (draft → one "ok" → write). Short
   drafts; after the first two, if the person approves without changes, propose "ok to all the remaining ones".
4. Meeting with nothing to record (cancelled, only greetings): note it in the report, no file.
5. Final tally: minutes written N, skipped N (why), still pending N.

## Scheduled mode
Prepare the drafts for yesterday's meetings and **stop before writing**: present them as a single
list to approve.

## Rules
Never infer an account. Never assign tasks: ClickUp tasks are created in staging for approval.
