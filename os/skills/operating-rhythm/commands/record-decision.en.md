---
status: attivo
area: sistema
---

# Command: record-decision

## Trigger
"record that we decided…" / "registra che abbiamo deciso…", "log this decision" / "segna questa decisione", "we decided that…" / "abbiamo deciso che…".

## Purpose
Record a decision that came up in conversation or in a meeting, so the company can find it again.
For a decision still to be made, with options and a recommendation, there is `/ceo decision`.
Sources and rules in `../SKILL.md`.

## Process
1. **Pin it down** in one sentence: *what* was decided. Then ask for what is missing:
   - **who decided** (person from `config/people.yaml`, or "the team");
   - **why** (in the person's words — never invent it);
   - originating **account / project** and **meeting** (path of the minutes, if any);
   - **review date** or deadline, if the decision contains one.
2. **Isn't it already recorded?** — search `company/direzione/decisions/` and the "Decisioni" (decisions) tables
   of recent minutes. If an identical or contrary one exists, say so: decisions are immutable,
   a new one **supersedes** it by citing it.
3. **Who can make it** — `os/org/decision-rights.yaml`: if the person doesn't have the right,
   record it as `**Stato**: Proposta` (it ends up in the decision-maker's `approvals`).
4. Show the file as it will be written and wait for "ok".
5. Write `company/direzione/decisions/YYYY-MM-DD-{slug}.md` according to `TEMPLATE.md` (Data, Agente,
   Stato, Review Date, Contesto, Decisione, Conseguenze (date, agent, status, review date, context, decision, consequences); the options only if they were discussed).
   If it supersedes a previous decision, note it in both. Link the originating minutes.
6. If the decision brings work, update the account's `next-step` or propose a task via
   `clickup-pending/`. Commit `[{agente}] decision: {slug}`.

## Rules
Only real decisions: not opinions, not open questions. Never PII or 🔴 data in the text.
