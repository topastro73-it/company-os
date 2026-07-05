# /finance scadenzario — Tax and administrative deadlines

## Purpose
No tax/corporate deadline left uncovered: what is due, when, who handles it.

## Input
None; optional: horizon (default 30 days + quarter).

## Steps
1. Read `finance/scadenzario.md` (source of truth — if not up to date, flag it:
   the system must not pretend to know).
2. Classify by urgency:
   - 🔴 **overdue, not completed** (at the top, always)
   - 🟡 next 7 days · 🟢 next 30 days · next quarter (visibility)
3. For each deadline: date, type (F24, VAT, INPS, financial statements, chamber of commerce fee, beneficial
   owner, innovative-startup requirements…), estimated amount, owner (us / accountant).
4. **Advance notice**: flag monthly deadlines 7 days ahead, annual ones 30 days ahead; for those handled
   by the accountant, the question is "have we asked them? did they confirm?"
5. Concrete actions: "issue", "pay", "ask the firm" — never tax interpretations
   (those belong to the accountant).

## Output format
```markdown
---
zone: finance
tier: 🔴
type: scadenzario-report
---
# Payment Schedule — {YYYY-MM-DD}

## 🔴 Overdue (not completed!)
| Deadline | Date | Type | Estimated amount | Owner | Action |
## 🟡 Next 7 days
## 🟢 Next 30 days
## Next quarter (visibility only)
```

## Destination
Report in chat + status updates in `finance/scadenzario.md`.
Commit (admin): `[finance] scadenzario: check {YYYY-MM-DD}`.

## Handoff
Deadline requiring a cash decision → `ceo`; documents for the firm →
copy to `finance/per-commercialista/` (one-way showcase, via APPROVE).
