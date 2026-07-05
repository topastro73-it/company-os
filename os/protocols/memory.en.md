# Memory — three-layer memory

| Layer | Where | Answers |
|---|---|---|
| **State** | operational zones (Drive) + snapshot `company/` / `vault/` | "What's the situation?" |
| **History** | `system/wiki/` (git) | "How did we get here? Why this way?" |
| **Rules** | `system/learnings.md` (git) | "What have we learned that's worth remembering?" |

The three layers stay separate: never duplicate state in the wiki, never put narrative in the state files.

## 1. Persistent memory — intercept and propose

During every conversation, intercept the concrete business data that emerges and propose
saving it in the right zone file. **Always ask before saving**, a single grouped question
at the end of the reply, indicating the destination file:

```
💾 Data to save:
- June MRR: €X → company/direzione/metrics/kpis.md
- DNA: pilot annex signed → 20-Clienti/dna/note.md
Save everything, pick which, or no?
```

| Data type | Destination (zone) |
|---|---|
| Metric / KPI | `direzione` → metrics/kpis.md |
| Decision taken | `direzione` → decisions/YYYY-MM-DD-slug.md (see `decisions.md`) |
| Client/partner info | `clienti` → `20-Clienti/{slug}/` |
| Deal / opportunity | `commerciale` → pipeline/opportunities |
| Strategy / OKR change | `direzione` → strategy |
| Pricing | `commerciale` (price list) / `finance` if 🔴 |
| Deadline, cost, invoice | `finance` → scadenzario / costs (🔴, vault) |
| Spec/feature status | `prodotto` → specs + roadmap |
| Team / people | `config/people.yaml` (via admin) |
| Competitor | `commerciale` → battlecards |

Rules: do not ask for hypotheses/explorations/data already saved; if "save everything" → save and
confirm with a file list; if "no" → do not insist. **Critical exception (LRN-018)**: corrections
to financial obligations (deadline cancelled, amount changed) are persisted **immediately**, not
at close — stale state regenerates the wrong data in later sessions.

## 2. Wiki — the history (`system/wiki/`)

Captures the **why**: decisions, reasoning, open questions, promises. It is not a transcript.

Structure (detail in `system/wiki/README.md`):
- `sessions/{YYYY-MM-DD}-{slug}.md` — one page per session, generated **at close** (never invented during)
- `entities/clients/{slug}.md` — only the client's narrative timeline; the **state** (stage,
  value, owner, blockers) lives in the `commerciale`/`clienti` zone — the entity page links, does not duplicate
- `entities/features/{slug}.md`, `entities/decisions/{slug}.md`, `entities/concepts/{slug}.md`
- `index.md` — last 20 sessions + entity pages

Rules:
- All wiki files in **English**
- Extract from the real flow of the conversation, not generic summaries
- Entity pages grow by accumulation (timeline), they are not overwritten
- Promises past their deadline → URGENT items in the next briefing
- **Pseudonymization**: end clients as initials + role; never IBAN/tax codes/compensation (see
  `zones-and-permissions.md` §6)

## 3. Learnings — the rules (`system/learnings.md`)

The wiki says "on 3/15 {client} slowed down and it was enablement"; the learning says "when a
partner slows down, check the sales training first". Format:

```markdown
### LRN-XXX: Title
- **Rule**: When [situation], [what to do].
- **Source**: Session YYYY-MM-DD — [[session-slug]]
- **Applied**: N times (contexts)
- **Tags**: tag1, tag2
- **Status**: active | archived
```

**When to propose**: at close, max 2 generalizable patterns per session. The human approves,
edits or discards — never save without confirmation. Abstract rules, never personalized on the
client's name.

**Apply-loop**:
- At start the session loads the active LRNs; at the beginning of an agent command load
  the domain's ones (tags: sales, product, finance, compliance, …)
- When a task matches a learning: intervene proactively —
  `⚡ From past experience (LRN-XXX): "{rule}". I suggest {action}.` Max 1 per intervention.
- **Every application increments `Applied: N times`** in the session's commit. Without the
  counter the apply-loop is inert; the health check flags 🔴 if ≥60% of active LRNs are at 0.
- Obsolete learnings → `Status: archived` with reason, never deleted.

**Anti-drift (unpromoted candidates)**: proposing is not enough — an explicit decision is required.
At start and at close, scan the wiki sessions of the last 30 days: every candidate
(`## Proposed learning`) must be either promoted (LRN in `learnings.md` or note
`→ promoted as LRN-XXX`) or discarded (`→ discarded {date}`). Hanging candidates are
re-flagged until decided.
