# /admin health — System health

## Purpose
A single traffic light on the mechanical health of the system. Run at `/ceo close` (summary)
and on-demand (full). Green is not optional: red = stop and fix.

## Input
- None; optional: `--quick` (blocking checks only)

## Steps
1. **Executable guardrails** (`scripts/audit/`):
   - `secret-scan.sh` — tokens/keys/IBANs/🔴 files outside the allowed destinations
   - `link-lint.py` — paths cited in system files exist
   - `frontmatter-check.py` — `zone:` + `tier:` declared on operational files
2. **ACL**: `osctl acl-audit` (Drive permission drift) — see `/admin acl-audit`.
3. **Sync freshness**: last snapshot (did the nightly run? how old is `company/`?),
   pending publishes (system changes committed but not distributed).
4. **Repo hygiene**: `.env` never committed (`git log --all -- .env` empty), branch = main,
   CI green on the last push, changelog aligned with the latest system change.
5. **Protocol/memory freshness**: learnings without review for too long, wiki sessions
   missing relative to the cadence.
6. Compose the report: every check → 🟢/🟡/🔴 with an action if not green.

## Output format
```markdown
## System Health — {YYYY-MM-DD}

| Check | Result | Detail / action |
|---|---|---|
| secret-scan | 🟢 | — |
| link-lint | 🟡 | 2 missing paths → fix or allowlist |
| acl-audit | 🟢 | — |
| snapshot freshness | 🟢 | last: yesterday 02:00 |
| pending publishes | 🟡 | 3 files → /admin publish |
| … | | |

Verdict: 🟢/🟡/🔴 — {1-line summary}
```

## Destination
Report in chat; if 🔴: `system/audits/health-{YYYY-MM-DD}.md` + explicit block
("do not close the session until…"). Commit only if fixes were applied.
