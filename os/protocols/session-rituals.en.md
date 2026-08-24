# Session rituals — start and close

Two rituals, two variants: **admin** (the founder, session on the git repo) and **collaborator**
(session in their own Drive zone). The ritual belongs to the entry agent: `ceo` for the admin,
the zone's default agent for collaborators (`config/people.yaml`).

## START

### 1. Identify the person
- **Admin (repo)**: `git config user.email` → match in `config/people.yaml`
- **Collaborator (Drive)**: the zone the session runs in + the zone `CLAUDE.md`
  determine role and default agent; if ambiguous, ask once and that's it
- Greet with the **role** (e.g. "Hi {person} — Head of Sales") and enter the primary agent

### 2. Align the state
- **Admin**: `git fetch` + pull (retrieves nightly snapshots and merged changes);
  if osctl is available, check that the latest snapshot is no older than 24h
- **Collaborator**: check that Google Drive for Desktop is in sync (`_OS/` files present);
  if the zone is not reachable → graceful degradation (`zones-and-permissions.md` §7)

### 3. "Where we left off"
Extract from the last wiki session (`system/wiki/sessions/`, for collaborators the published
copy if available) and from the zone's state files:
- decisions taken, open questions, promises — with **alerts on overdue ones**
- **aging**: opportunities/tasks stuck beyond threshold in the person's zone
- **deadlines**: upcoming deadlines relevant to the role (scadenzario, review dates, follow-ups)
- **health**: outcome of the last `/system health` and acl-audit (admin only) — if 🔴, fix it first

**Stale session detector** (admin only): if the last session shows work but no wiki
page (close skipped), propose a wiki recovery from logs/commits/decisions BEFORE today's briefing.

**Cadence freshness check** (admin only, the mirror image): if the most recent wiki page is more than
**5 days ahead** of the most recent date in the cadence log, the log is stale, meaning work was done
and closed without recording the cadence. Flag it in one line and offer to realign the current dates
(never backfill the lost history unless explicitly asked). The two checks cover the two directions of
the same drift: the first a session without a wiki, the second a wiki without a cadence entry.

### 4. Load the minimum context
Shared context (`zones/_root/context/` or `_OS/context/`) once per session;
active learnings in memory (apply-loop, `memory.md` §3). Then get to work.

If the person immediately invokes a specific agent: quick check (max 1 urgent alert) and go.

## CLOSE

### Collaborator (Drive zone)
1. **Save the memory**: propose the business data that emerged and is not yet persisted
   (`memory.md` §1) → zone files
2. Session output in the right folder of the zone (no orphan files on the desktop)
3. Cross-zone requests formalized (e.g. spec request in `30-Prodotto/richieste/`)
4. Done: no commit — the **nightly snapshot** versions the collaborator's work

### Admin (repo) — full sequence
1. **Memory**: unpersisted business data → propose saving in the zone/snapshot files
2. **Wiki session**: generate `system/wiki/sessions/YYYY-MM-DD-{slug}.md` (English,
   pseudonymized — `memory.md` §2); reconcile promises/questions from recent sessions
   (done → closed, open → carried forward); update touched entity pages and `index.md`
3. **Cadence log**: update `direzione/ceo-cadence.md` (date of the cadence you ran + an entry in the
   answers log). As mandatory as step 2, and for the same reason: it is the one moment of the day the
   CEO always invokes. drive_master zone → write on Drive, never on the `company/direzione/` snapshot;
   if Drive is unreachable, say so in the summary
4. **Learnings**: propose max 2 candidates; check unpromoted candidates from the last
   30 days (anti-drift); increment `Applied:` for LRNs used in the session
5. **Snapshot**: `osctl snapshot` (Drive → `company/` + `vault/`) so the commit includes the
   real operational state; osctl absent → flag it and continue
6. **Commit & push**: `git add -A` → commit `[ceo] close: YYYY-MM-DD` → `git fetch` →
   if the remote is ahead, `git merge origin/main --no-edit` → `git push origin main`
   - Never `git reset --hard`, never `push --force`
   - Unresolvable conflicts → `CONFLICTS.md` file with details and notification
   - Repo already clean → declare it and stop
7. **Health check**: `scripts/audit/` (secret-scan, link-lint, i18n-parity, frontmatter-check) +
   `osctl acl-audit`; outcome in the summary. If a system change was merged during the
   session → verify the publish was done (`changelog.md`)
8. **Final summary**: commit SHA, files touched, push/snapshot/health outcome, open promises

## Common rules

- The close is not optional: without a close there is no wiki, counters stall, promises hang —
  the next start detects it and proposes the recovery
- **A mandatory write does not live inside a long interaction**: if a write is mandatory (wiki,
  cadence log, counters), anchor it to the close, not to an intermediate step of the briefing. The
  start re-checks it, it does not replace it
- Never ask the same thing twice in the same ritual; max 1 urgent question if the
  person is in a hurry
- Everything the ritual writes respects zones and tiers (`zones-and-permissions.md`)
