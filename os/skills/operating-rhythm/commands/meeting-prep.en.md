---
status: attivo
area: sistema
---

# Command: meeting-prep

## Trigger
"prep me for the call with…" / "preparami la call con…", "meeting brief" / "brief per il meeting", "who's in the meeting" / "chi c'è alla riunione", or before a meeting
in a scheduled run.

## Purpose
Prepare the person for a meeting: who is there, which account or project is discussed, what was
promised last time and whether it was done, what to close today. For a brief with a slotted agenda
and possible outcomes there is `/cos prepare-meeting`. Sources and rules in `../SKILL.md`.

## Process
1. **Find the meeting** — the one the person names, from Calendar (title, time, attendees).
   Several candidates → ask which one. Never guess.
2. **Attendees** — internal from `config/people.yaml` (role); external from the account card and
   from the "Partecipanti" (participants) tables of previous minutes. Unknown: say so.
3. **Account / project** — `company/clienti/{slug}/overview.md`, opportunities with
   `account: {slug}` (stage, `next-step`, `blockers`), or the `P-NNN` project.
4. **Last time** — the most recent minutes with the same account or the same people: decisions,
   commitments, "Promesse fatte a terzi" (promises made to third parties). Always also search the transcripts from the configured sources
   (`../SKILL.md` § Meeting transcripts, keyword = account or attendees): a more recent meeting
   not yet imported counts, and must be flagged ("transcript of dd/mm without minutes").
5. **Promises kept?** — for each commitment: status in the minutes, later updates
   (opportunity, newer minutes, `git log`), linked ClickUp tasks. ✓ done / ✗ open / ? not verifiable.
6. **Decisions and rules in force** — decisions in `company/direzione/decisions/` and channel/pricing
   rules that touch the account (e.g. what can be shown, what not to promise).
7. **Latest emails** (gmail skill) — latest threads with the attendees and what is awaiting a reply.

## Output
**Who** (one line each) · **What it's about** (account, stage, what is needed) · **Last time**
(date, decisions, commitments ✓/✗) · **Latest emails** · **Watch out** (rules and open risks) ·
**To close today** (2–4 points to push). Readable in two minutes, every fact with its path.

## Destination
On request: `company/commerciale/meeting-prep/YYYY-MM-DD-{slug}-brief.md` (prospect) or
`company/clienti/{slug}/report/YYYY-MM-DD-{slug}-brief.md` (client), frontmatter
`status: attivo`, `area`, `zone`, `tier`, `account`, `date`.
