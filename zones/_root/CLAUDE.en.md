# CLAUDE.md — Company HQ (kernel)

> Published from git, read-only. Loaded by the Claude Code of every collaborator
> working in the company Drive folder. Do not modify it: changes are made only
> in the system repo, via the admin.

## Who we are

{company} — description, mission, business model and flywheel in `_OS/context/COMPANY.md`.
Load it at the start of the session: it is the source of truth on who we are, what we do and for whom.

## First line of every reply

`🟣 **[Claude]**` — always, before any content. No exceptions.

## The zone system

This Drive folder is the company's **operational master**. Every top-level folder is a
**zone** with its own Drive ACL: **the permissions are Drive's**. If you can write in
a folder, you can work there; if you can't see it, it's not your business. The system adds no
permission layers of its own and you must not bypass them.

| Folder | Zone | Who works there |
|---|---|---|
| `_OS/` | System (read-only) | everyone reads, nobody writes |
| `00-Direzione/` | Strategy, OKRs, decisions, board | CEO |
| `10-Commerciale/` | Pipeline, opportunities, proposals | sales team |
| `20-Clienti/{slug}/` | Everything concerning that client | whoever follows that client |
| `30-Prodotto/` | Roadmap, backlog, specs, testing | product team |
| `40-Finance/` | Finance, grants (🔴 RESTRICTED) | CEO, finance |
| `50-Compliance/` | ISO/NIS2, policies, evidence | CEO, legal |
| `60-Marketing/` | Content, sequences, brand | marketing |
| `90-Condivisi/` | Approved material for everyone | everyone reads |

Every zone has its own `CLAUDE.md` telling you who you are there, where you write and what not to do.

## Where to find things

- **Company context** → `_OS/context/` (COMPANY, GLOSSARY, PRINCIPLES, TEAM) — load it
  once at the start of the session, not at every step
- **Agents** (operational roles: sales, delivery, product, finance…) → `_OS/agents/`
- **Protocols** (external-writes, memory, spec lifecycle…) → `_OS/protocols/`

## Common non-negotiable rules

1. **Client output only in its folder**: everything concerning a client (proposal,
   report, QBR, assessment) lives ONLY in `20-Clienti/{slug}/`. Never elsewhere, never duplicated.
2. **Never modify `_OS/` files**: they are published from git. If something is wrong or missing,
   flag it to the CEO — do not fix it in place.
3. **Never 🔴 RESTRICTED data outside `40-Finance/` and `70-Contratti-Riservati/`**: signed
   contracts, IBANs, tax codes/VAT numbers, non-public financials, compensation. Never in briefings, chat, commits or other zones.
4. **External writes** (ClickUp, HubSpot, email, shares to third parties): always
   PREPARE → APPROVE → EXECUTE (`_OS/protocols/external-writes.md`). Prepare the file,
   get it approved by a human, only then execute.
5. **Cross-zone requests via `richieste/` folders**: if you need something from a zone
   where you don't write (e.g. a spec from product), write the request in
   `{zona}/richieste/` — do not bypass the ACLs by asking for files around.
6. **Escalation to the CEO**: pricing, contractual commitments, product deadlines, waivers of
   these rules → do not decide on your own, escalate to the CEO.
7. **Never promise without validating**: no dates without the CTO, no features without Product,
   no compliance statements without evidence.

## Working style

Decision-oriented (clear recommendations, not just analysis), traceable (every output is a file
in the right zone), coordinated (explicit handoffs: who does what after you).
