---
status: attivo
area: sistema
---

# Command: publish-call

## Trigger
"publish this call" / "pubblica questa call", "write the minutes" / "fai la minuta", "do the recap" / "fai il recap", "follow up this meeting" / "follow up di questo meeting".

## Purpose
After a meeting, turn the transcript into **minutes** in the right zone and propagate their
effects: opportunity and account card updated, governance decisions recorded, ClickUp tasks and recap
email prepared in staging. A single draft, a single "ok". Sources and rules in `../SKILL.md`.

## 1. Find the meeting and the transcript
- The one the person names, or the most recent without minutes (see `follow-up-all`).
- Transcript: always search the configured sources first (`../SKILL.md` § Meeting transcripts),
  then pasted text. No transcript and no notes → nothing to publish: say so.
- Check relevance and that it is not already imported (same §). Transcript not relevant → stop:
  nothing is written to the repo. Mixed transcript → the minutes contain only the relevant part and
  state it in the **Pertinenza** (relevance) section (after the Metadati (metadata): "{azienda}: sì / parziale" (name from `config/company.yaml`), files touched,
  accounts without a file).

## 2. The account
- If the meeting concerns an existing account or opportunity, use it (`account:` = slug).
- Otherwise ask which account or project it belongs to, or propose one and wait for a yes. **Never
  infer it** from the title or attendees. New account → `new-project` first.

## 3. The draft (don't write yet)
Minutes in the format of the existing minutes (`type: minuta`): **Metadati** (title, date, duration,
source and link to the transcript, attendees in a Persona/Società/Ruolo table, absentees) · **Pertinenza** · **Decisioni** (decisions; only what was
actually decided, and by whom) · **Impegni / action item** (commitments / action items; #, Azione, Owner, Scadenza, Stato) ·
**Promesse fatte a terzi** (promises made to third parties) · **Numeri e fatti nuovi** (new numbers and facts) · **Rischi / incoerenze** (risks / inconsistencies; comparison with what
the repo already says) · **Dove è registrato** (where it is recorded).
Then, the effects:
- **Opportunity / account card** — `last-activity`, `next-step`, `next-step-due`, `blockers`, timeline entry.
- **Governance decisions** (prices, channel rules, contractual commitments) → file in
  `company/direzione/decisions/` via `record-decision`.
- **ClickUp tasks** — only if there is an owner who committed, a concrete deliverable, and a
  deadline or at least about an hour of work; small things stay in the commitments table.
  They go in `company/prodotto/clickup-pending/` (or the content's zone) for approval.
- **Recap email** to the attendees, 5–8 lines → `company/{zona}/mail-pending/`. Never send.
- Before closing the draft, look at the emails with the attendees after the meeting: commitments made
  by email count, with the same threshold.

Show everything as a single block and ask: "Publish?"

## 4. Publish (after "ok")
1. Write the minutes: `company/clienti/{slug}/report/YYYY-MM-DD-{slug}-minuta.md` (client/partner),
   `company/commerciale/meeting-prep/YYYY-MM-DD-{slug}-minuta.md` (prospect),
   `company/direzione/reports/YYYY-MM-DD-{slug}.md` (internal). Frontmatter: `status: fatto`,
   `area`, `zone`, `tier`, `type: minuta`, `account`, `date`, `source`.
2. Update opportunity and account card; write the approved decisions.
3. Leave the ClickUp/Gmail staging files in `status: pending`: they are executed after their
   approval (`approvals` or `/{agente} approve`).
4. Commit `[{agente}] meeting: {account} {data} — {sintesi}`; in admin remind about `osctl publish`
   (or `--only` on the files touched) to bring them back to Drive.

## 5. Report
One message: minutes saved (path), files updated, N decisions, N tasks and the recap draft
waiting for approval.

## Automatic mode
"Prepare the minutes for yesterday's meetings" / "Prepara le minute dei meeting di ieri": prepare the drafts, writing always waits for the ok.
