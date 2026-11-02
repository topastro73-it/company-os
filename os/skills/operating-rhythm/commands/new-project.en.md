---
status: attivo
area: sistema
---

# Command: new-project

## Trigger
"open the project…" / "apri il progetto…", "new client" / "nuovo cliente", "new opportunity" / "nuova opportunità", "create an internal project" / "crea un progetto interno".

## Purpose
Create the right file, from its template, in the right zone — step by step, with confirmation before
writing. Sources and rules in `../SKILL.md`.

## Steps
0. **Don't create duplicates** — search by name and slug in `company/clienti/`,
   `company/commerciale/opportunities/` and `company/direzione/projects/INDEX.md`.
1. **What is it** — ask whether it needs:
   - **account** (client or partner) → `company/clienti/{slug}/overview.md` from `company/clienti/TEMPLATE.md`;
   - **opportunity** (a deal) → `company/commerciale/opportunities/{opp-slug}.md` from
     `TEMPLATE.md` in the same folder, with `account:` pointing to the account;
   - **internal project** → `company/direzione/projects/P-NNN-{slug}.md` with the next free number,
     plus the row in `INDEX.md`.
2. **Collect** the template's mandatory fields (name, kebab-case slug, owner from
   `config/people.yaml`, type/segment, initial stage or status, next-step with deadline). Never
   invent values: unknown fields stay empty with a comment. Show everything again and ask "ok?".
3. **Write** the file with complete frontmatter (`zone`, `tier`, `status`, `area`), then the indexes
   (the zone's `INDEX.md`, `PIPELINE.md` for an opportunity).
4. **Optional** — ClickUp list or initial tasks via `clickup-pending/`; HubSpot record via
   `hubspot-pending/`. Both wait for approval.
5. Commit `[{agente}] opportunity|delivery|admin: nuovo {tipo} {slug}`; in admin remind about the publish.
