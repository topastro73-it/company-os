# /admin setup — Initial interview: from cloned repo to configured instance

## Purpose
Take a person who is **not necessarily technical** from "I cloned the repo" to "the system knows who
we are, who works here and with which tools". It is step 0 of `bootstrap/README.md`: everything else
(Shared Drive, ACLs, snapshot) comes afterwards and assumes this is done.

## Input
None. It triggers when `config/company.yaml` does not exist, or on explicit request.

---

## How to run it (non-negotiable rules)

These rules matter more than the content of the questions. A badly run interview makes people
abandon the setup, and an abandoned setup leaves a system that lies about itself.

1. **One question at a time.** Never a questionnaire. Wait for the answer before the next one.
2. **No jargon without a translation.** The person answering may not know what a service account,
   an ACL or an MCP is. If a term is needed, explain it in half a line *when you use it*, not before.
3. **"I don't know" is always a valid answer**, and it has to be offered explicitly. Record
   `to confirm` and move on. Never insist twice on the same question.
4. **Write as you go**, not at the end. After each phase, save what you have collected. If the
   session is interrupted, whoever comes back picks up where they left off and repeats nothing.
5. **Propose, don't ask into the void.** When a choice is needed, offer the options the system
   already supports (§3) instead of leaving the field open. "What accounting tool do you use?" is a
   hard question; "do you use Fatture in Cloud, another one, or nothing for now?" is an easy one.
6. **Don't ask what you can work out.** Repo name, operating system, whether `git` is there, time
   zone: read them. Ask for confirmation only if the deduction matters.
7. **No secrets in chat.** Tokens, passwords and keys are not dictated: they go in `.env` or in the
   keychain. You only write the *name* of the variable in `config/integrations.yaml`. If someone
   pastes a secret in chat, say so immediately and ask them to rotate it.
8. **Never block.** Anything left unresolved becomes a line in the final recap (§6), not a wall.

---

## Phase 0 — Language

The very first question, before generating any file (`os/protocols/language.md` §1):

> 🌐 In che lingua vuoi lavorare? / Which language do you want to work in? [italiano / english]

Write `config/company.yaml → language` by copying `config/company.example.yaml`. From here on, the
whole interview and every generated file use that language.

## Phase 1 — Who you are

Five questions, in this order. After each one, write the field.

| # | Question | Where it lands |
|---|---------|--------------|
| 1 | What is the company called? | `company.yaml → name` |
| 2 | In one line: what do you do, and for whom? | `company.yaml → one_liner` + `zones/_root/context/COMPANY.md` |
| 3 | Do you sell to businesses, to consumers, or both? And do you go through resellers/partners? | `company.yaml → positioning.model` |
| 4 | What are your two or three main types of customer? (your own names for them, not standard categories) | `company.yaml → segments` |
| 5 | Is there a regulated sector that constrains you? (e.g. healthcare, finance, security; or none) | `zones/_root/context/COMPANY.md` |

On number 4: these are the labels that will show up all through the sales pipeline. If they don't
have them yet, `segment-a`, `segment-b` is fine: they can be renamed later — and tell them so.

## Phase 2 — Who works here

> 👥 Who will use the system besides you? For each one I need a name, a work email and what they
> look after. If you're on your own for now, that's perfectly fine: we add people when they arrive.

For each person write a line in `config/people.yaml` (from `people.example.yaml`), mapping "what
they look after" onto a zone and a default agent. Don't ask "which zone": work it out and show the
mapping for confirmation at the end of the phase.

⚠️ **The email is mandatory** if the person will need access to the folders: without it, `osctl`
skips them when it sets the permissions. If they don't know it, mark `to confirm` and remember it
in the recap.

Close the phase by showing the person → zone → agent table and asking a single "is this right?".

## Phase 3 — What tools you work with

This is the phase that decides how useful the system will be on day one. Run it **category by
category**, each time proposing what the template already brings. Always phrase it like this:

> Do you use {category}? [{supported option} / another one / not yet]

If they answer with something we support, **turn it on** (write the section in
`config/integrations.yaml`, say which environment variable is needed and where to put it, and point
to the script or the skill that is already there). If they answer "another one", record the name and
say honestly that the integration isn't there but that this is the place to add it. If "not yet",
just skip it.

| Category | Question | If yes, what you turn on | What we already bring |
|---|---|---|---|
| **Business bank account** | Do you use Qonto, another bank, or nothing to connect? | `integrations.yaml → banca` | `scripts/integrations/bank-qonto.sh` + `bank_qonto_sync.py` (read-only, balances and transactions) · skill `qonto` |
| **Invoicing / ERP** | How do you issue invoices? Fatture in Cloud, another accounting tool, your accountant? | `integrations.yaml → fatturazione` | skills `fatture-in-cloud`, `erp`, `financial-import` |
| **Recurring payments** | Do you take payments through Stripe or something similar? | `integrations.yaml → stripe` | skill `stripe` (MRR, churn, payout reconciliation) |
| **CRM** | Where do you keep your deals today? HubSpot, a spreadsheet, your head? | `integrations.yaml → hubspot` | skill `opportunity-management`: **the pipeline lives in the repo**, the external CRM is optional and acts as a mirror |
| **Tasks / projects** | Do you use ClickUp, Jira, Asana, Trello, something else? | `integrations.yaml → clickup` | skill `clickup` (epics, tasks, docs) |
| **Email** | What does your work email run on? Google Workspace, Microsoft, something else? | `integrations.yaml → gmail` | skill `gmail` (context, read-only; drafts only after approval) |
| **Shared documents** | Where do the company's files live today? | `config/acl.yaml` | it is the system's operational plane: see Phase 4 |
| **Compliance** | Do you have certifications underway, or asked for by customers? (ISO 27001, SOC 2, GDPR, NIS2, none) | `zones/_root/context/COMPANY.md` | agent `compliance`, skill `audit-compliance` |

Close the phase with: *"Anything we haven't connected can be added at any time, just tell me. There
is no need to redo the setup."*

## Phase 4 — The operational plane (Google Drive)

This is where the technical level goes up, and that has to be said first:

> The system keeps the "brain" part here in the repo and the "operational" part in a shared Drive
> folder, where each person only sees what concerns them. Creating it takes two things that whoever
> runs your IT usually does: a Shared Drive and a technical access for the system.
> Do you want me to walk you through it step by step now, or would you rather I prepare the
> instructions to pass on to whoever looks after that?

- **"Walk me through it"** → follow `bootstrap/README.md` §1-§3 one step at a time, waiting for
  confirmation at each step. Don't paste three commands together.
- **"I'll prepare the instructions"** → generate a file in `local/` with steps §1-§2 and the exact
  list of what you need back (Shared Drive ID, service account email, where they saved the key).
  Then close the setup: the rest happens when that information arrives.

In both cases you **don't need** to have finished this phase to use the system on the repo: say so,
and propose Phase 5.

## Phase 5 — Check

Run these and comment on each in one line, translated into language people can understand:

```bash
python3 tools/osctl/osctl.py status
python3 scripts/audit/link-lint.py
python3 scripts/audit/system-health.py
```

If `status` flags people without an email, report it here, not before.

## Phase 6 — Recap and next step

Always close with this block, even if the interview was interrupted halfway through:

```
✅ Configured
   Company: {name} · language: {it|en} · {N} people · {N} integrations connected

⏳ Still open (does not block using the system)
   • {what} — {who/how}

▶️ Next step
   {the single next step, one only}
```

Then commit: `[admin] setup: instance configured — {company name}`.

⚠️ `config/*.yaml` is gitignored by choice (it holds your data): the commit only covers what ended
up in `zones/_root/context/`. Say so, otherwise it looks like the work has been lost.

---

## Resuming an interrupted setup

When a session opens, if `config/company.yaml` exists but is incomplete (empty fields or
`to confirm`), don't start again from scratch:

> The setup had reached {phase}. Shall we pick up from there? There are {N} things left to close.

## Guardrails

- **Never invent** a piece of information that wasn't given. An empty field is better than a
  plausible, false one: every agent will read this file as the truth.
- **Never ask for a secret in chat** (§7 of the rules on how to run the interview).
- **Never launch `osctl bootstrap --apply`** without having shown the dry-run first and got a yes.
- If the interview goes past ~15 minutes, offer a break yourself: "the rest can wait, the system is
  already usable".

## Destination
`config/company.yaml`, `config/people.yaml`, `config/integrations.yaml` (gitignored),
`zones/_root/context/COMPANY.md`. No report.
