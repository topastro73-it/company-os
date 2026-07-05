---
zone: _os
tier: 🟡
---

# Collaborator onboarding — progressive activation

The "Company HQ" Drive starts with **only the admin** (the founder) on all zones. Each
collaborator is activated **one zone at a time**, when it is truly needed, via an
interview — there is no automatic rollout of the full matrix.

## When it gets activated

The CEO tells the admin: "onboard [name]" — or the need emerges on its own
(e.g. "{person} needs to see the pipeline"). The admin runs the interview, never assumes.

## Interview (4 questions, in order)

1. **Who are they and what is their role?** (if not already in `config/people.yaml`, create it: name, role, type
   internal/external, email — the email must match the Google account they will use)
2. **Which zones do they need to write to?** (`direzione`, `commerciale`, `clienti`, `prodotto`,
   `finance`, `compliance`, `marketing` — only those strictly necessary for the role)
3. **Which zones do they only need to read?** (often broader than the write zones — e.g. Sales
   reads `prodotto` to know what's coming, but does not write there)
4. **Which default agent will they use?** (`sales`, `delivery`, `product`, `cto`, `finance`,
   `compliance`, `marketing` — determines which zone CLAUDE.md welcomes them)

For clients (`20-Clienti/{slug}/`): access is **per folder**, not per whole zone —
also ask which specific client folders they need to follow; never give access to all of
`20-Clienti` unless the role truly requires it (e.g. Head of Sales yes, an SDR on a
specific territory no).

## Application

1. Update `config/people.yaml`: `zones_write`/`zones_read` fields (if not already correct) and
   **`onboarded: true`** (as long as it is `false`, the person stays out of the matrix — see
   the comment at the top of the file)
2. Run `osctl bootstrap --apply` (or `osctl acl-audit --fix --apply` when available):
   additive, it grants only the new permissions of the just-activated person, touches nobody
   else
3. Verify with `osctl acl-audit`: it must stay at 0 🔴 criticals
4. Commit `config/people.yaml` with message `[admin] onboard: {name} → {zones}`
5. Tell the person: install Google Drive for Desktop, sync "Company HQ",
   open Claude Code inside their zone (the published `CLAUDE.md` welcomes them on its own)

## Deactivation / role change

Same principle in reverse: Drive **does not allow removing permissions inherited** from a
broader zone, so revocation must be done **on the exact zone** where access was granted
(`osctl` calls `remove_permission` on the single folder). If someone changes role or leaves,
update `zones_write`/`zones_read` in `people.yaml`, then manually remove on Drive (or with
a future `osctl revoke` command) the access to zones no longer due — setting `onboarded:
false` is NOT enough on its own to remove access already granted, it only prevents it from
being re-granted at the next bootstrap.

## Why this way (not everything at once)

Activating the entire `acl.yaml` matrix in one go (as `osctl bootstrap --apply` does by
default) grants everyone "at target" access from day one — convenient but risky: if
the matrix has a design error (see LRN-025, the contracts case), you discover it
after access has already been given. Onboarding one person at a time, with an interview,
reduces the blast radius and forces you to verify each time that the requested access is
truly necessary.
