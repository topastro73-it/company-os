# Outbound & ABM Execution Skill

Execution of Account-Based Marketing campaigns and personalized outbound sequences. Used by Sales, Marketing, CEO.

## Principles

1. **Extreme personalization**: every message must look hand-written for that specific prospect. Zero generic templates. Research the company, the role, the trigger events before writing
2. **Trigger events first**: don't reach out cold — wait for (or look for) a trigger: NIS2 deadline, breach in the sector, CEO change, headcount growth, new funding round, industry event
3. **CEO brand on LinkedIn = channel #1**: the founder sharing genuine insights generates more pipeline than any traditional outbound campaign. Every sequence includes a LinkedIn layer
4. **Value-first, pitch-last**: the first 3 touchpoints deliver value (insights, data, content). The proposal comes only after credibility has been established
5. **Coordinated multi-channel**: LinkedIn + email + events + referrals. Never a single channel
6. **Persistence without spam**: 8 touchpoints in 8 weeks, then monthly nurture. Never more than 1 touch/week in the active sequence
7. **Human voice, no AI slop**: every email/message passes the anti-slop quick-check before sending. No filler ("Hope you're doing well"), no passive voice, no em-dashes, no vague statements. See [`os/skills/writing/SKILL.md`](../writing/SKILL.md#anti-ai-slop-rules) (rules) and [`os/skills/writing/references/`](../writing/references/) (EN detail + examples)

---

## Commands

| Command | Description | Output |
|---------|-------------|--------|
| `sequence` | 8-week outreach sequence for a specific account | Plan in `company/commerciale/sequences/` |
| `email-template` | Personalized email template for a specific type | File in `company/commerciale/email-templates/` |
| `linkedin-sequence` | Complete LinkedIn plan (connection + messages + content) | Plan in `company/commerciale/sequences/` |
| `tracking` | Status of all active sequences | Report |
| `nurture-plan` | Nurture plan for unconverted prospects | Plan in `company/commerciale/sequences/` |

---

## Command: sequence

### Input
- Target company name
- Contact (name, role, LinkedIn URL if available)
- Partner type (e.g. `segment-a` / `segment-b` / MSP-MSSP — the real ICP lives in `config/company.yaml`)
- Trigger event (why now? what happened?)
- Referral available? (who can introduce us)

### 8-week sequence structure

| Week | Channel | Touchpoint type | Goal |
|------|---------|-----------------|------|
| 1 | LinkedIn | **Warm-up**: engage with the prospect's content (like, comment, share) | Visibility, familiarity |
| 2 | LinkedIn | **Connection request**: personalized, NO pitch, reference to the trigger event | Connection accepted |
| 3 | Email | **First touch**: pure value — insight, data point, report relevant to their sector | Open + click |
| 4 | LinkedIn | **Value message**: share relevant CEO content (post, article, case study) | Engagement, reply |
| 5 | Email | **Social proof**: similar case (partner of the same segment/size), concrete results | Credibility, interest |
| 6 | LinkedIn + Email | **Soft proposal**: "We're working with [someone like you] on [problem]. Interested in seeing how?" | Meeting request |
| 7 | Email | **Direct follow-up**: "Did you get a chance to see my message? How about 15 min" | Reply, meeting |
| 8 | LinkedIn | **Nurture hook**: high-value content + "If it's not the right time, no problem — I'll stay in touch" | Door open for nurture |

### Output format
```markdown
# Outbound Sequence — {company}

## Target
- Company: {name}
- Contact: {name}, {role}
- Type: {segment — e.g. segment-a/segment-b/MSP}
- Trigger event: {description}
- Referral: {name or "None — cold outreach"}

## Timeline

### Week 1 — LinkedIn Warm-up
**Action**: [Specific action with the prospect's post/content to engage with]
**Message**: —
**Goal**: Show up in the feed, build familiarity

### Week 2 — Connection Request
**Channel**: LinkedIn
**Message**:
> Hi {name}, I saw your [post/talk/article] on [topic]. I work in our sector for {partner type} and I'd love to connect — {trigger event reference}. {CEO signature}

**Goal**: Connection accepted

### Week 3 — First Touch (Email)
**Subject**: {personalized subject — max 6 words, no clickbait}
**Body**:
> [Max 150 words. Open with the trigger event. Share 1 relevant data point/insight. Close with a link to a useful resource. ZERO pitch.]

**CTA**: Link to report/content

[... weeks 4-8 ...]

## Required content
| Week | Content | Exists? | Path / Action |
|------|---------|---------|---------------|
| 3 | Sector report {type} | Yes/No | {path or "Create with /marketing"} |
| 5 | Case study {segment} | Yes/No | {path or "Create"} |

## Tracking metrics
| Week | Channel | Action | Status | Reply |
|------|---------|--------|--------|-------|
| 1 | LinkedIn | Warm-up | — | — |
| 2 | LinkedIn | Connection | — | — |
[...]
```

Save to: `company/commerciale/sequences/sequence-{company-slug}-{YYYY-MM-DD}.md`
Commit: `[sales] outbound: sequence for {company}`

---

## Command: email-template

### Input
- Template type (see list below)
- Context: for whom, which trigger, which segment

### 9 Template Types

| # | Type | When to use it | Tone |
|---|------|----------------|------|
| 1 | `cold-intro` | First contact without a referral | Curious, humble, immediate value |
| 2 | `value-share` | Sharing an insight/data point/report | Generous, expert, zero pitch |
| 3 | `case-study` | Social proof with a concrete result | Concrete, numbers, credible |
| 4 | `roi-model` | Showing the economic return | Analytical, personalized, provocative |
| 5 | `meeting-request` | Asking for a call | Direct, respectful of time, specific |
| 6 | `follow-up` | After a touchpoint with no reply | Short, adds value, not pushy |
| 7 | `post-event` | After meeting at an event | Personal, specific reference, fast |
| 8 | `referral-ask` | Asking for an introduction | Contextual, easy to say yes |
| 9 | `trigger-event` | Reacting to an event (breach, NIS2, funding) | Timely, empathetic, useful |

### Rules for every template
- **Max 150 words** in the body
- **1 single CTA** (clear, specific, low friction)
- **Subject**: max 6 words, no emoji, no clickbait, no all-caps
- **Opening**: never "Hope you're doing well", never "My name is X and I do Y". Open with the prospect, not with yourself
- **Personalization**: at least 1 prospect-specific element (company, role, event, post)
- **Signature**: name + role + 1 line of context ("We help [partner type] achieve [result]")
- **Anti-slop check**: before saving, go through the Quick Checks in [`os/skills/writing/SKILL.md`](../writing/SKILL.md#anti-ai-slop-rules). Cut adverbs (`really`, `just`, `simply`), passive voice, em-dashes, throat-clearing openers ("Here's the thing"), binary contrasts ("not X, it's Y"), false agency ("the decision emerges")

### Output format
```markdown
# Email Template: {type}

## Context
- For: {segment/role}
- Trigger: {specific event}
- Goal: {what the recipient should do}

## Template

**Subject**: {subject}

**Body**:
> {Max 150 words}

**CTA**: {specific action}

## Variants
- Variant A (more direct): [...]
- Variant B (softer): [...]

## Personalization notes
- Replace [{field}] with prospect-specific data
- If a referral is available, open with "{referral name} suggested I write to you"
```

Save to: `company/commerciale/email-templates/{tipo}-{contesto}-{YYYY-MM-DD}.md`
Commit: `[marketing] template: {type} email for {context}`

---

## Command: linkedin-sequence

### Input
- Target profile (name, role, company)
- Duration (default: 4 weeks)

### Process
1. **Connection strategy**: personalized message for the request
2. **Messaging sequence**: 3-4 direct messages post-connection
3. **Content plan**: which CEO posts to make visible / comment on / share
4. **Engagement plan**: how to interact with the prospect's content

### Output format
```markdown
# LinkedIn Sequence — {name}, {company}

## Connection Request
> {Message — max 300 characters}

## Post-Connection Messages
### Day 2 (after acceptance)
> {Thank-you message + open question — NO pitch}

### Day 7
> {Value: share an insight or content}

### Day 14
> {Social proof + soft ask}

### Day 21
> {Direct meeting request}

## CEO Content Plan
| Week | Post to publish | Goal |
|------|-----------------|------|
| 1 | {Topic relevant to the prospect} | Visibility in the feed |
| 2 | {Case study or data point} | Credibility |
| 3 | {Opinion on an industry trend} | Thought leadership |

## Engagement Plan
- Like: every prospect post
- Comment: 1-2 substantial comments/week on the prospect's content or their network's
- Share: share 1 piece of prospect content with a CEO comment
```

Save to: `company/commerciale/sequences/linkedin-{slug}-{YYYY-MM-DD}.md`
Commit: `[marketing] outbound: LinkedIn sequence for {name}`

---

## Command: tracking

### Process
1. Scan `company/commerciale/sequences/*.md`
2. For each sequence, read the "Tracking metrics" table
3. Generate an aggregate report

### Output format
```
## Outbound Tracking — {date}

### Active sequences
| Account | Contact | Week | Last touch | Reply | Next step |
|---------|---------|------|------------|-------|-----------|
| {company} | {name} | 4/8 | Value email | Opened, no reply | Case study week 5 |

### Summary
- Active sequences: {N}
- Replies received: {N} ({%})
- Meetings booked: {N}
- In nurture: {N}

### Required actions
1. {Account}: {action}
```

---

## Command: nurture-plan

### Input
- List of prospects who did not reply to the active sequence

### Process
1. For each unconverted prospect:
   - 1 touch per month (alternating email and LinkedIn)
   - Value content (never a pitch)
   - Monitor trigger events to reactivate the sequence
2. Generate a 6-month plan

### Output format
```markdown
# Nurture Plan — {date}

## Prospects in nurture
| Prospect | Company | Last interaction | Non-conversion reason |
|----------|---------|------------------|-----------------------|
| {name} | {company} | {date} | {reason} |

## Monthly plan
### Month 1
| Prospect | Channel | Content | Triggers to monitor |
|----------|---------|---------|---------------------|
| {name} | Email | Q1 cybersecurity report | NIS2 deadline, sector breach |

### Month 2
[...]

## Reactivation rules
- Relevant trigger event → restart from sequence week 3
- Positive reply → hand off to Sales for direct follow-up
- Explicit opt-out → remove from nurture
```

Save to: `company/commerciale/sequences/nurture-{YYYY-MM-DD}.md`
Commit: `[marketing] nurture: updated nurture plan`

---

## CEO Cadence Integration

### Weekly
- **Outbound tracking**: summary of active sequences, replies, meetings booked during the week
- Alert if no sequence is active or no touchpoint happened during the week

### Monthly
- Full outbound pipeline review
- Nurture plan refresh
- Content gaps for sequences (content needed but missing)

---

## Where the data lives

| Data | Path |
|------|------|
| Outbound sequences | `company/commerciale/sequences/sequence-*.md` |
| LinkedIn sequences | `company/commerciale/sequences/linkedin-*.md` |
| Email templates | `company/commerciale/email-templates/*.md` |
| Nurture plans | `company/commerciale/sequences/nurture-*.md` |
| Content index (for `reuse`) | `company/marketing/content-index.md` |
| Partners (for personalization) | `20-Clienti/*/overview.md` |
| Segments (for targeting) | `company/commerciale/segments.md` |
| **PoC kickoff deck** (standard asset to activate a new prospect after a qualification meeting) | `90-Condivisi/template-deliverable/company-poc-kickoff.pptx` (source: `gen_poc_kickoff_deck.py`) |
