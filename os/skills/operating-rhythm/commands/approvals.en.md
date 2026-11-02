---
status: attivo
area: sistema
---

# Command: approvals

## Trigger
"what do I need to approve" / "cosa devo approvare", "approval queue" / "coda approvazioni", "what is waiting for my approval" / "cosa aspetta la mia approvazione".

## Purpose
Everything in the repo waiting for the person's ok, in a single queue: approve (execute) or reject.
Sources and rules in `../SKILL.md`; execution according to `os/protocols/external-writes.md`.

## 1. Load the queue
- **External writes** — files with `status: pending` in `company/*/clickup-pending/`,
  `hubspot-pending/`, `mail-pending/`, `publish-pending/`.
- **Proposed decisions** — `company/direzione/decisions/` with `**Stato**: Proposta`.
- **Waiting on me** — files with `status: in-attesa` and `waiting_on` = the person or their role;
  drafts marked "da approvare" (to approve) (e.g. channel rules, price lists in `proposte-bozze/`).
- The queue depends on who decides: `os/org/decision-rights.yaml`. Show only what the person
  can approve; the rest, if relevant, as "waiting on {others}".

## 2. Show it
By zone. For each item a card: what (system and actions, or title) · from whom and since when ·
age (over 7 days → "to revalidate", per the protocol) · path.
With artifacts: a page of cards numbered 1…N; otherwise a numbered list.

## 3. Decide
The person replies in one line, e.g. "approve 1, 3 · reject 2 · 4 only lines 1-2". Act only
on the items named: a generic "ok" does not approve everything.
- **Approve** — execute the file's actions in order (EXECUTE), note outcome and IDs, `status: executed`,
  move to `*-done/`. Decision: `**Stato**: Approvata`. External system unreachable: the file
  stays `approved` and is executed at the next start.
- **Approve in part** — execute only the lines indicated, note the others as not approved.
- **Reject** — `status: cancelled` with a one-line reason if the person gave one.
- **Skip** — stays as it is.

## 4. Report
"Approved N (executed N, failed N), rejected N, waiting N." Commit `[{agente}] approve: …`.

## Rules
Never approve on the person's behalf without their explicit instruction for that item.
