# /admin onboard-person — Progressive activation of a collaborator

## Purpose
Activate a person's Drive access one zone at a time, via interview — not the whole
`acl.yaml` matrix in one shot. Full protocol: `os/protocols/onboarding-collaborator.md`.

## Input
Name of the person (new or already in `config/people.yaml` with `onboarded: false`).

## Steps
1. **Interview** (4 questions, in order — do not assume):
   - Who they are, what role they have, type (internal/external), email of the Google account they will use
   - Which zones do they need to **write** to? (only those necessary for the role)
   - Which zones do they need to **read only**?
   - Which **default agent**? (`sales`, `delivery`, `product`, `cto`, `finance`,
     `compliance`, `marketing`)
   - If they touch `clienti`: which specific client folders they follow (never the whole zone
     without a reason)
2. Update `config/people.yaml`: create/update the entry, set `zones_write`/`zones_read`
   consistent with the answers, then **`onboarded: true`**
3. Run `osctl bootstrap --apply` (additive: it grants only this person's new
   permissions, it does not touch the others)
4. Verify `osctl acl-audit`: it must stay at 0 🔴 criticals
5. Commit: `[admin] onboard: {name} → {zone(s)}`
6. Handoff to the person: install Google Drive for Desktop, sync "Company HQ",
   open Claude Code inside their own zone (the published `CLAUDE.md` welcomes them by itself)

## Output format
```markdown
## Onboarding — {name}
Role: {role} · Agent: {agent} · Write zones: {zones} · Read zones: {zones}
Assigned client folders: {slug, slug...} (if applicable)

✓ config/people.yaml updated (onboarded: true)
✓ osctl bootstrap --apply executed
✓ osctl acl-audit: 0 criticals
```

## Destination
Commit on `config/people.yaml`. No separate file — the state is the config itself.
