# Command: email-context

## Agent
All agents

## Trigger
When an agent needs email context on a specific topic before acting.

Invocation examples:
- "search Acme Corp's emails about the proposal"
- "find the feedback emails about feature X"
- "was there anything via email about yesterday's incident?"
- "search for emails from [candidate] about the interview"

## Purpose

Provide inline email context to any agent **without generating files**.
The output is temporary context for the current conversation and is not committed.

## Process

### Step 1 — Receive the topic

The agent specifies:
- **Topic**: what it is about (e.g. "Acme Corp proposal", "bulk import feature", "database incident")
- **Sender or domain** (optional): if searching for email from a specific person or company
- **Time window** (optional, default: 30 days)

### Step 2 — Build the Gmail query

Compose the query based on the context:

```
# For a generic topic
subject:"[keyword]" OR body:"[keyword]" newer_than:30d

# For a specific sender
from:[email-o-dominio] newer_than:30d

# For a combination
from:[dominio] subject:"[keyword]" newer_than:14d

# For open threads on a topic
subject:"[keyword]" is:unread

# For sent emails (to see whether we already replied)
from:me subject:"[keyword]" newer_than:30d
```

### Step 3 — Read the relevant threads

For each email found, read the thread with `gmail_read_thread`.
Priority: most recent threads and threads with multiple exchanges (a sign of an active conversation).

### Step 4 — Synthesize the context

Return a structured synthesis:

```markdown
**Email context — [topic]**

Threads found: N (last 30 days)

**[Date] — [Sender] → [Recipient]**
Subject: [subject]
Summary: [1-2 lines on what it says]
Status: [awaiting reply / replied / resolved]

[repeat for each relevant thread]

**Takeaway**
- [What is relevant for the agent's current action]
- [Any commitments made via email not yet reflected in the repo]
- [Open actions emerging from the thread]
```

## Security rules

- Never copy the full text of the email — summaries only
- If the email contains amounts, contract terms, personal data: describe them generically ("there is a commercial proposal", "a contract was shared") without reporting the values
- This command does not generate files — the context stays in the conversation
- If the context is relevant to a decision, the agent integrates it into the document being produced, not the email itself

## Usage examples by agent

**PM**
```
email-context topic="feature bulk import" from="@cliente.com" days=60
```
→ Context for writing a spec based on real feedback

**Sales**
```
email-context topic="proposta Enterprise" from="acme.com" days=14
```
→ Understand where the deal stands before doing a follow-up

**CTO**
```
email-context topic="incident database" days=7
```
→ Check whether there were reports via email before writing the post-mortem

**CFO**
```
email-context topic="fattura Q1" from="fornitore.com" days=90
```
→ Check invoice status before the quarterly close

**Legal**
```
email-context topic="NDA Acme" from="legal@acme.com" days=30
```
→ Find the latest draft exchanged before finalizing

**HR**
```
email-context topic="colloquio" from="candidato@email.com" days=14
```
→ Retrieve interview context before making an offer
