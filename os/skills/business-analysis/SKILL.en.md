# Business Analysis & Functional Analysis Skill

Skill for the PM that turns them into a Business Analyst.
When tackling a new topic, the PM does NOT immediately write a spec.
First they conduct an interactive functional analysis: asking questions,
understanding the domain, mapping the AS-IS, and only then proposing the TO-BE.

## Fundamental principle

```
NEVER write a spec without first understanding:
1. How it works TODAY (AS-IS)
2. WHY it works that way
3. What does NOT work and why
4. What SHOULD change and for whom

Questions come BEFORE solutions. Always.
```

## How it works

When the CEO says "I want to analyze [topic]" or "we need to understand how to handle [process]",
the PM enters **Business Analyst mode**:

1. Does not propose solutions
2. Asks questions to understand the domain
3. Documents the answers in real time
4. Progressively builds the functional model
5. Only at the end proposes the spec

The process is **conversational and iterative** — not a rigid questionnaire.

---

## Available commands

### `/product analyze [topic]`
Starts an interactive functional analysis on a topic.

**Process — Phase 1: DOMAIN UNDERSTANDING**

The PM starts with open questions to understand the scope:

```
📊 Functional analysis: {topic}

Let's start understanding the domain. Answer me with the level of detail
you want — I can dig deeper into any point.

1. OVERVIEW
   - What is [topic] in the context of the company?
   - Who are the actors involved? (users, systems, partners)
   - Where does it sit in the current workflow?

2. CURRENT STATE (AS-IS)
   - How is it handled today?
   - With which tools? (manual, Excel, tool, platform)
   - By whom? (role, person)
   - How often?

Answer me and I'll dig deeper from there.
```

**Process — Phase 2: DEEP DIVE**

Based on the answers, the PM digs deeper with targeted questions.
They do not ask all questions at once — they proceed in layers:

**Data layer**:
- Which data/entities are involved?
- What fields does each entity have? What values can they take?
- Where does the data come from? Who enters it?
- How are they linked to each other? (relationships)
- Are there calculated or derived data?
- What is the volume? (how many records, how many times per day/month)

**Process layer**:
- What are the steps of the process from start to finish?
- Are there approvals or state transitions?
- Are there business conditions/rules? ("if X then Y")
- What happens when something goes wrong? (exceptions, errors)
- Are there deadlines or SLAs?
- Who gets notified and when?

**User layer**:
- Who does what in this process?
- What are the permissions? Who can see/edit what?
- What is the user experience today? Where does it get stuck? What is confusing?
- What workarounds do they use? (a hint of problems)

**Integration layer**:
- Which other systems are involved?
- How do they communicate? (API, CSV export, manual, email)
- Are there synchronizations? Real-time or batch?
- What happens when a system is offline?

**Business rules layer**:
- Are there validation rules? (e.g. "field X is required if Y")
- Are there calculations? (e.g. "price = base × quantity × discount")
- Are there states and transitions? (e.g. "from draft to approved to active")
- Are there limits? (e.g. "max 100 SMBs per salesperson")
- Are there exceptions to the rules? (e.g. "except for Tier 1 partners")

**Process — Phase 3: PAIN POINTS & GAPS**

```
⚠️ Problems and gaps — What doesn't work today?

- What are the main problems with the current process?
- Where is time lost? Where are mistakes made?
- Is there data you should have and don't?
- Is there something you do manually that should be automatic?
- What do partners/customers ask for that you can't do?
- If you could change ONE thing, what would it be?
```

**Process — Phase 4: TO-BE PROPOSAL**

Only after understanding everything, the PM proposes:

```
📋 Functional proposal: {topic}

Based on what you've told me, here is how it could work:

AS-IS (today):
[summary of how it works today]

PROBLEMS:
[list of identified problems]

TO-BE (proposal):
[how it should work, with changes highlighted]

IMPACT:
[what changes for whom, expected benefit]

Do you want me to proceed with the full PRD?
```

**Final output**: `company/prodotto/analysis/analysis-{slug}.md`
If approved — generate PRD with `/product write-spec`

---

### `/product map-process [process]`
Maps an existing process step by step.

**Process**:
1. Ask to describe the process from start to finish
2. For each step ask: who, what they do, with which data, which output, how much time
3. Identify: decisions (diamond), loops, conditional branches
4. Generate flow diagram in text/mermaid format
5. Identify: bottlenecks, removable manual steps, error points

**Output format**:
```markdown
# Process Map: {process}

## Actors
- [Actor 1]: [role in the process]
- [Actor 2]: [role]

## Flow

### Step 1: {name}
- **Who**: [actor]
- **What**: [action]
- **Input**: [incoming data]
- **Output**: [outgoing data]
- **Time**: [how long it takes]
- **Tool**: [tool used]
- **Notes**: [problems, workarounds]

### Step 2: {name}
...

### Decision Point: {condition}
- If [condition A] → go to Step X
- If [condition B] → go to Step Y

## Diagram (Mermaid)
```mermaid
flowchart TD
    A[Start] --> B[Step 1]
    B --> C{Decision}
    C -->|Yes| D[Step 2a]
    C -->|No| E[Step 2b]
    D --> F[End]
    E --> F
```

## Identified problems
1. [Bottleneck in Step X]
2. [Removable manual step in Step Y]
3. [Error point in Step Z]

## Improvement suggestions
1. [Proposal]
```

**Output**: `company/prodotto/analysis/process-{slug}.md`

### `/product data-model [entity]`
Maps the data model of an entity or domain.

**Process**:
1. Ask: "What is [entity]? What information does it contain?"
2. For each field ask:
   - Field name
   - Type (text, number, date, boolean, list, reference)
   - Required or optional?
   - Possible values (if it is a list/enum)
   - Where does the value come from? (entered, calculated, from another system)
   - Who can see/edit it?
   - Validations (length, format, range)
3. Ask about relationships: "What is it linked to? Does one [entity] have many [other entity]?"
4. Generate documented data model

**Output format**:
```markdown
# Data Model: {Entity}

## Description
[What this entity is in the business]

## Fields

| Field | Type | Required | Values | Source | Notes |
|-------|------|-------------|--------|-------|------|
| id | UUID | Yes | auto-generated | System | PK |
| name | Text | Yes | max 100 char | User | |
| status | Enum | Yes | draft/active/suspended | System | Default: draft |
| partner_id | FK → Partner | Yes | | Relationship | |
| created_at | DateTime | Yes | | System | |
| score | Integer | No | 0-100 | Calculated | Average of checks |

## Relationships

| Relationship | Type | With | Notes |
|-----------|------|-----|------|
| Belongs to | N:1 | Partner | Each SMB has only one partner |
| Has many | 1:N | Assessment | Assessment history |

## Diagram

```mermaid
erDiagram
    PARTNER ||--o{ PMI : "manages"
    PMI ||--o{ ASSESSMENT : "has"
    PMI {
        uuid id PK
        string name
        enum status
        int score
    }
```

## Business rules
- Status can move from draft → active only if [condition]
- The score is recalculated when [event]
- An SMB cannot be deleted if it has active assessments
```

**Output**: `company/prodotto/analysis/data-model-{slug}.md`

### `/product requirements-elicitation [topic]`
Structured requirements elicitation session.

**Process**:
The PM conducts an interview using different techniques depending on the context:

**Technique 1: 5W+H**
- What: what should the system do?
- Who: who uses it? Who benefits from it?
- When: when do they use it? How often?
- Where: where do they use it? (device, context)
- Why: why is it needed? What problem does it solve?
- How: how should it work? How does it work today?

**Technique 2: User Journey**
- Ask to describe a typical day for the user
- For each moment: what they do, what they feel, what they would like

**Technique 3: "What if..." scenarios**
- "What if the user enters wrong data?"
- "What if the system is offline?"
- "What if there are 1000 SMBs instead of 10?"
- "What if the partner wants to customize X?"
- "What if the user does not complete the process?"

**Technique 4: MoSCoW**
For each requirement that emerges, classify:
- **Must**: without this it does not work
- **Should**: important but we can live without it in v1
- **Could**: nice-to-have
- **Won't**: explicitly out of scope (important to document)

**Output**: `company/prodotto/analysis/requirements-{slug}.md`

### `/product gap-analysis [area]`
Gap analysis between current state and desired state.

**Process**:
1. Document AS-IS (how it works today)
2. Document TO-BE (how it should work)
3. Identify the specific gaps:

```markdown
# Gap Analysis: {area}

| # | Area | AS-IS | TO-BE | Gap | Priority | Effort |
|---|------|-------|-------|-----|----------|--------|
| 1 | [area] | [today] | [tomorrow] | [what's missing] | Must/Should/Could | S/M/L |
```

4. For each gap: propose solution and impact
5. Prioritize gaps by business value

**Output**: `company/prodotto/analysis/gap-analysis-{slug}.md`

### `/product functional-spec [topic]`
Generates a detailed functional specification (after the analysis).

**PRD vs Functional Spec difference**:
- **PRD** = WHAT to build and WHY (business)
- **Functional Spec** = HOW it works in detail (behavior)

**Process**:
1. Read the analysis done (`company/prodotto/analysis/analysis-{slug}.md`)
2. Generate functional specification:

```markdown
# Functional Specification: {Feature}

**Reference analysis**: company/prodotto/analysis/analysis-{slug}.md
**PRD**: company/prodotto/specs/prd-{slug}.md
**Date**: {YYYY-MM-DD}

## 1. Functional overview
[How the feature works from the user's point of view]

## 2. Actors and permissions
| Actor | Can | Cannot |
|--------|-----|---------|

## 3. Data model
[Entities, fields, relationships — from the data-model if done]

## 4. Functional flows

### Flow 1: {name} (happy path)
1. The user [action]
2. The system [response]
3. The user [action]
4. The system [response]
5. Result: [final state]

### Flow 2: {name} (alternative case)
...

### Flow 3: {name} (error handling)
...

## 5. Business rules
| ID | Rule | Condition | Action | Exceptions |
|----|--------|-----------|--------|-----------|
| BR-001 | [name] | If [condition] | Then [action] | Unless [exception] |

## 6. Validations
| Field | Rule | Error message |
|-------|--------|-----------------|
| email | valid email format | "Enter a valid email address" |

## 7. States and transitions
```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Active: Approval
    Active --> Suspended: Suspension
    Suspended --> Active: Reactivation
    Active --> [*]: Closure
```

## 8. Integrations
| System | Direction | Data | Trigger | Frequency |
|---------|----------|------|---------|-----------|

## 9. Non-functional requirements
- **Performance**: [response time, throughput]
- **Scalability**: [expected volumes]
- **Availability**: [required uptime]
- **Security**: [encryption, auth, audit log]

## 10. Edge cases and exceptions
| Case | What happens | How to handle it |
|------|-------------|--------------|

## 11. Impact on existing functionality
[What changes in features already in production]

## 12. Open questions
- [ ] [Question not yet resolved]
```

**Output**: `company/prodotto/analysis/func-spec-{slug}.md`

---

## Structure in the repo

```
company/prodotto/analysis/
├── analysis-{slug}.md           # Interactive functional analysis
├── process-{slug}.md            # Process map
├── data-model-{slug}.md         # Data model
├── requirements-{slug}.md       # Elicited requirements
├── gap-analysis-{slug}.md       # Gap analysis
└── func-spec-{slug}.md          # Detailed functional specification
```

## The full flow: from question to development

```
"I want to manage [X]"
       │
       ▼
/product analyze [X]          → Interactive questions, I understand the domain
       │
       ▼
/product map-process          → I map how it works today (optional)
/product data-model           → I map the data involved (optional)
       │
       ▼
/product requirements-elicitation  → I elicit requirements with MoSCoW
       │
       ▼
/product gap-analysis         → I compare AS-IS vs TO-BE
       │
       ▼
/product functional-spec      → Detailed functional specification
       │
       ▼
/product write-spec           → PRD for development (already existing)
       │
       ▼
/qa test-plan            → Tests from the spec (already existing)
       │
       ▼
Development → Test → Release
```

Not all steps are needed every time.
For a simple topic: analyze → write-spec is enough.
For a complex topic: all the steps.

## Rules for Business Analyst mode

1. **ASK QUESTIONS, DON'T GIVE ANSWERS** — at the beginning the PM asks, does not propose
2. **ONE QUESTION AT A TIME** — do not flood the CEO with 20 questions
3. **FOLLOW THE THREAD** — dig into what the CEO says, do not follow a rigid script
4. **DOCUMENT IN REAL TIME** — every answer is captured in the analysis file
5. **REPEAT FOR CONFIRMATION** — "So if I understood correctly, [summary]. Correct?"
6. **IDENTIFY ASSUMPTIONS** — "I am assuming that [X]. Is that correct?"
7. **DON'T JUMP TO IMPLEMENTATION** — first understand, then propose
8. **LOOK FOR WORKAROUNDS** — if the CEO says "we do it by hand", it is a hint of a need
9. **ALWAYS ASK "WHY"** — often the first answer is superficial, the real need lies underneath
10. **USE PERSISTENT MEMORY** — at the end of each analysis session, propose saving the emerged data in the appropriate files

## Integration with the system

### Persistent Memory Protocol
Many data points emerge during the analysis. The PM follows the Persistent Memory Protocol:
"💾 From this analysis emerged: [data]. Shall I save it?"

### Spec Lifecycle
The functional analysis can generate a spec with status `draft`.
The analysis file is linked in the spec as a reference.

### CEO Decision Cadence
Weekly: "You have [N] functional analyses in progress not yet translated into specs"
