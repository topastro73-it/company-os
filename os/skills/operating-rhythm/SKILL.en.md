---
status: attivo
area: sistema
---

# Skill: Operating Rhythm

## Purpose

A person's daily working rhythm on the repo: their day, meeting preparation and recap,
decisions, approvals, the state of an account or project, what others are doing.
Everything is read and written **in the zone files** (`company/`, `vault/` admin only) and in the
company systems listed in `config/integrations.yaml`: no external context backend.

Nine commands, in `commands/`:

| Command | Typical triggers | Writes? |
|---|---|---|
| `my-day` | "what's my day" / "com'è la mia giornata", "what do I have today" / "cosa ho oggi", "catch me up" / "aggiornami" | no |
| `meeting-prep` | "prep me for the call with…" / "preparami la call con…", "meeting brief" / "brief per il meeting", "who's in the meeting" / "chi c'è alla riunione" | brief in zone |
| `publish-call` | "publish this call" / "pubblica questa call", "write the minutes" / "fai la minuta", "do the recap" / "fai il recap" | minutes + linked files; ClickUp/Gmail via staging |
| `follow-up-all` | "follow up my meetings" / "segui i miei meeting", "clear the follow-ups" / "smaltisci i follow-up" | via `publish-call` |
| `approvals` | "what do I need to approve" / "cosa devo approvare", "approval queue" / "coda approvazioni" | executes what you approve |
| `project-pulse` | "how is {account} going" / "come va {account}", "status of {opportunity/project}" / "stato di {opportunità/progetto}", "update the status" / "aggiorna lo stato" | status update |
| `new-project` | "open the project…" / "apri il progetto…", "new client" / "nuovo cliente", "new opportunity" / "nuova opportunità" | new file from template |
| `record-decision` | "record that we decided…" / "registra che abbiamo deciso…", "log this decision" / "segna questa decisione" | `direzione/decisions/` |
| `team-radar` | "what is {person} doing" / "cosa sta facendo {persona}", "what happened this week" / "cosa è successo questa settimana" | no |

Agents: CoS (owner), CEO, Sales, Delivery, Product. The CoS commands remain the company view
(`/cos daily-briefing`, `prepare-meeting`, `follow-up-tracker`, `status-check`, `weekly-digest`);
this skill is the **person's** view and the meeting → minutes → commitments cycle.

## Where the data lives

| What | Where |
|---|---|
| People, roles, email | `config/people.yaml` (short key, `name`, `role`, `emails`, `default_agent`) |
| Client/partner accounts | `company/clienti/{slug}/overview.md` (frontmatter `status`, `owner-sales`, `owner-pm`, `health-score`) |
| Opportunities | `company/commerciale/opportunities/{opp-slug}.md` (`account`, `stage`, `owner-sales`, `next-step`, `next-step-due`, `blockers`, `last-activity`) · board `PIPELINE.md` |
| Internal projects | `company/direzione/projects/P-NNN-*.md` (register `INDEX.md`) · goals and WOs in `company/direzione/ops/` |
| Meetings held | minutes with frontmatter `type: minuta`, `account`, `date`, `source`: `company/clienti/{slug}/report/`, `company/commerciale/meeting-prep/`, `company/direzione/reports/` |
| Transcripts | the sources in `config/integrations.yaml → meeting_transcripts.sources`, always (§ Meeting transcripts) · pasted text |
| Upcoming meetings | Google Calendar connector; without it, the calendar "has not been verified" |
| Decisions | `company/direzione/decisions/YYYY-MM-DD-slug.md` (immutable, superseded by a new one) · "Decisioni" (decisions) table in the minutes |
| Commitments and tasks | "Impegni / action item" (commitments / action items) table in the minutes · `next-step`/`blockers` of opportunities · ClickUp (`config/integrations.yaml → clickup`) |
| Approvals | files in `company/*/*-pending/` with `status: pending` · decisions `**Stato**: Proposta` · files `status: in-attesa` with `waiting_on` |
| Email | skill `os/skills/gmail/` (read-only; drafts only via `mail-pending/`) |
| History | `git log` (admin only; collaborators work on Drive) |

## Meeting transcripts

**Every command that deals with meetings** (`my-day`, `meeting-prep`, `publish-call`, `follow-up-all`,
`project-pulse`, `team-radar`) **always searches** the transcripts, not only the minutes already
in the repo. The sources are URLs configured in `config/integrations.yaml → meeting_transcripts.sources`
(each with `url`, `provider`, `label`, `title_format`, `shared`); the relevance terms
(`include_terms`, `exclude_terms`) apply to all of them. To add or change a source, only the
config is edited. No source configured → only repo minutes and pasted text.

1. **Search** each source over the command's period (default last 14 days), reading **every
   page** of results; for an account or a person add the keyword. Depending on the
   `provider` (inferred from the host if missing):
   - `clickup` — the workspace is the number after `app.clickup.com/` in the URL: `clickup_search` with
     `asset_types: [doc]`, sorted by `created_at` desc, until `next_cursor` is exhausted. Notetaker
     Docs have no folder; the AI summary is on the first page of the Doc.
   - `drive` — the URL is a folder: list the files for the period with the Drive connector (or, in admin,
     from the `OS_DRIVE_MOUNT` mount) and read the transcript documents.
   - `url` — read the given page or feed as is; each entry is a meeting.
   The meeting date is taken from the title according to `title_format` (e.g. `MM/DD/YYYY` = US date:
   convert it to dd/mm/yyyy) or, failing that, from the creation date.
2. **Filter for relevance** — mandatory for `shared: true` sources (shared with other
   companies), recommended for all. For each transcript:
   - **relevant** if the title contains an `include_terms` entry, the name or slug of an account
     (`company/clienti/`), of an opportunity or of a `P-NNN` project, or if people from
     `config/people.yaml` other than the admin appear in the summary (the admin may also attend
     other companies' meetings: that alone is not enough);
   - **excluded** if the title contains an `exclude_terms` entry and nothing links it to the repo;
   - **doubtful** otherwise: read only the summary and decide; if still unsure, ask the user
     with a single question that lists all the doubtful ones;
   - **mixed** (other topics are discussed too): keep only the relevant part; the minutes say so
     in the "Pertinenza" (relevance) section.
3. **Already imported?** — a transcript is already in the repo if some minutes have its title in `source:`
   or its link in the body. Never import it twice: update the existing minutes.
4. **Confidentiality** — nothing from excluded meetings is copied into the repo, nor into reports or commits:
   at most the count ("N meetings of other companies excluded"). Never quote their content or people.
5. **Source in the minutes** — `source: "{label} — {original title}"` and the link to the transcript
   in the Metadati (metadata).

Source unreachable → its transcripts "have not been verified": say so, and continue with
the other sources and with the repo minutes.

## Who "I" am

In an admin session "I" is `config/people.yaml → admin`. Otherwise the person is recognised
by the email they work with (`people.*.emails`); if in doubt, ask. "My" files are those where
the person is owner (`owner-sales`, `owner-pm`, `Owner` in tables, `to:`/`from:` of WOs) or
participant ("Partecipanti" (participants) table in the minutes).

## Dates

Today = system date, Europe/Rome time zone. "This week" = Monday–Sunday. Every date shown
carries the label past / today / upcoming relative to today.

## Writes

- **Repo files** (minutes, opportunities, account cards, decisions, briefs): draft in chat → "ok" →
  write in the correct zone, with frontmatter `status`/`area` and `zone`/`tier` where the zone
  requires it (`zones/{zona}/CLAUDE.md`). The `company/` zones are Drive-master: in admin they are edited
  only if you then publish (CLAUDE.md, rule 5). Commit `[agente] meeting|decision|…: …`.
- **External systems** (ClickUp, Gmail, HubSpot, Calendar): always PREPARE → APPROVE → EXECUTE
  (`os/protocols/external-writes.md`) with staging in `clickup-pending/`, `mail-pending/`,
  `hubspot-pending/`. ClickUp tasks follow `config/integrations.yaml → clickup.rules`
  (English, initial status, mandatory tags).
- A generic "yes" does not choose between options: if there were several options or an answer per item,
  ask which ones and act only on those.

## Rules

- Report only what a file or a tool actually says, with the path as source. An unreachable
  source (ClickUp, Calendar, Gmail) = "not verified", never "empty".
- Never invent an account, a reason, a commitment or a deadline: if the file doesn't say it, it isn't recorded.
- Privacy: never PII or 🔴 data outside `vault/` and `40-Finance/`; finance only in admin.
- Business data surfaced in chat → propose saving it to the zone file (`os/protocols/memory.md`).
