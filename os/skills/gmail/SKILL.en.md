# Skill: Gmail Reading

## Purpose

Provide all agents with contextual access to company email via Gmail MCP.
Emails are **context only** — they are not archived in the repo, not forwarded in full, and must not put sensitive data into public documents.

## When each agent uses it

| Agent | Primary use | Typical queries |
|--------|---------------|---------------|
| **Chief of Staff** | Daily briefing, unanswered emails, escalations | `is:unread newer_than:1d`, `is:unread older_than:2d -label:sent` |
| **CEO** | Emails from investors, board, strategic partners | `from:investor OR from:vc newer_than:7d`, `subject:term sheet OR subject:follow-up` |
| **PM** | Feature requests from customers, bug reports, feedback | `from:customer subject:feature OR subject:request newer_than:14d`, `label:feedback` |
| **CTO** | System alerts, incidents, emails from infrastructure vendors | `subject:alert OR subject:incident OR subject:downtime newer_than:1d`, `from:pagerduty OR from:aws` |
| **Sales** | Replies to proposals, prospect follow-ups, deal emails | `subject:proposal OR subject:quote newer_than:7d`, `from:[prospect-domain]` |
| **CFO** | Invoices, wire transfers, emails from the bank and the accountant | `subject:fattura OR subject:invoice newer_than:30d`, `from:commercialista OR from:banca` |
| **Legal** | Contracts, NDAs, legal emails | `subject:contratto OR subject:NDA OR subject:agreement newer_than:30d`, `label:legal` |
| **HR** | Candidates, interviews, job offers | `subject:candidatura OR subject:application newer_than:14d`, `label:recruiting` |
| **Marketing** | Press inquiries, partnerships, co-marketing requests | `subject:press OR subject:partnership newer_than:14d` |

## Useful Gmail queries for all agents

```
# Urgent unread emails
is:unread is:important newer_than:1d

# Emails unanswered for more than 48h (needs attention)
is:unread older_than:2d -from:me -label:newsletter

# Emails from a specific domain
from:@dominio.com newer_than:30d

# Ongoing threads (unresolved)
is:unread label:inbox -label:automated

# Search by specific topic
subject:"[topic]" OR body:"[keyword]" newer_than:14d
```

## Security rules (MANDATORY)

1. **Never archive emails in the repo** — Emails are temporary context, not company documents.
2. **Summaries only, never full text** — When using an email's content in a document, write a synthesis; never quote verbatim.
3. **Never put sensitive data in public files** — Amounts, personal data, NDA/contract contents must not go into zones readable by everyone (`company/prodotto/`, `company/marketing/`, shared zones); 🔴 data stays in `vault/` / `company/finance/`.
4. **Never put email bodies in commits** — Commit messages describe the action; they do not quote emails.
5. **PII (candidates, employees)** — Never outside private conversations with HR.
6. **Credentials and tokens** — If an email contains passwords, tokens, or reset links, do not copy them anywhere.

## How to invoke

```
# Load the Gmail MCP tool before every operation
# Use gmail_search_messages to search
# Use gmail_read_thread to read a specific thread
# Synthesize the content, do not copy it

Example:
- gmail_search_messages(query="from:cliente@example.com newer_than:7d")
- Read the relevant threads with gmail_read_thread
- Extract only: sender, date, topic, action required (yes/no), urgency
```

## Structured output

When using email as context, always use this format:

```
**Email from [name/role]** — [date]
Topic: [one line]
Action required: [yes/no — if yes, what]
Urgency: [high/medium/low]
```

## Integration with commands

- `email-scan.md` — CoS: daily scan for the briefing
- `email-context.md` — All agents: email context on a specific topic
