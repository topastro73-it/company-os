# Command: email-scan

## Trigger
Invoked automatically by `/cos daily-briefing`, or manually with "scan email", "check the inbox", "are there any important emails?"

## Purpose
Scan the last 24h of email, classify by urgency and type, and produce a structured synthesis for the briefing.

## Process

1. **Urgent scan** (highest priority)
   ```
   gmail_search_messages(query="is:unread is:important newer_than:1d")
   ```
   - Classify: action required / monitoring / informational

2. **Unanswered scan** (follow-up needed)
   ```
   gmail_search_messages(query="is:unread older_than:2d -from:me -label:newsletter -label:automated")
   ```
   - Identify threads open for 48h+ without a reply

3. **Scan by category** (context for agents)
   - Investors/board: `from:investor OR subject:"term sheet" OR subject:"follow-up" newer_than:7d`
   - Customers/partners: `from:@[partner-domain] newer_than:3d`
   - Invoices/finance: `subject:fattura OR subject:invoice newer_than:7d`
   - Legal: `subject:contratto OR subject:NDA newer_than:7d`
   - Candidates: `subject:candidatura OR subject:application newer_than:7d`

4. **For each relevant email**, read the thread with `gmail_read_thread` and extract:
   - Sender and role
   - Topic (1 line)
   - Action required (yes/no — if yes, what)
   - Urgency (high/medium/low)
   - Suggested recipient agent (CEO, PM, Sales, etc.)

5. **Identify patterns**
   - Recurring topics (same subject from multiple senders)
   - Long threads without resolution
   - Emails from key stakeholders (investors, top partners)

## Output

Format to insert into the daily-briefing:

```markdown
### Email — Last 24h

**Action required** ({N})
| From | Topic | Action | Urgency | For |
|----|-------|--------|---------|-----|
| [name] | [topic] | [what is needed] | high/medium | [agent] |

**Unanswered for 48h+** ({N})
| From | Topic | Days | Suggestion |
|----|-------|--------|-------------|
| [name] | [topic] | [N] | [reply / delegate / ignore] |

**FYI** ({N})
- [sender]: [topic, 1 line]
```

## Security rules

- **Never archive emails in the repo** — synthesis in the briefing only
- **Never quote verbatim** — always paraphrase
- **Never sensitive data** — amounts, personal data, NDA contents stay out
- **Never email bodies in commits** — the commit describes the action, it does not quote emails
