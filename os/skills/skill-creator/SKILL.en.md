# Skill: Skill Creator

## Identity

Conversational guide to create a new skill in the system.
No technical knowledge required: Claude conducts an interview, the user answers in natural language, Claude generates all the files.

**Activation**: the user says something like "I want to create a skill", "I need a new skill", "add a skill for X", or invokes `/create-skill`.

---

## How it works

Claude conducts a sequential interview. It asks **one question at a time**, in plain language. At the end it generates everything automatically.

There's no need to know what a "slug", a "path" or a "command" is — Claude translates the answers into technical structure.

---

## Interview flow

### Step 1 — Discovery

Before asking questions, Claude reads:
- `os/skills/SKILLS.md` — to understand the existing skills and avoid duplicates
- `os/agents/AGENTS.md` — to know the agents available as owners

Then it briefly explains to the user what it's about to do and starts with the first question.

---

### Step 2 — Interview (7 questions, one at a time)

**Q1. What is this skill for?**
> "Describe in your own words what this skill should do. The form doesn't matter — even a paragraph is fine."

→ Claude extracts: purpose, key verbs, domain

---

**Q2. Who mainly uses it?**
> "Who in your company will use this skill? (e.g. the founder, the sales team, whoever manages clients, whoever handles finance...)"

→ Claude maps onto existing agents in `os/agents/`. If the user names an unmapped role, Claude asks to confirm the closest agent.

---

**Q3. What does it actually do?**
> "Tell me the 2-5 main actions this skill must be able to perform. Examples: 'prepare a report', 'send an email', 'calculate a score', 'generate a document'."

→ Claude creates the command list. For each action, it asks:
- What it's called (Claude suggests a slug name, the user approves or corrects)
- What output it produces (document, report, data, email...)

If the user doesn't know what to answer to "what does it produce", Claude suggests the most natural output for that action.

---

**Q4. Does it need external data or tools?**
> "To do these things, does the skill need to access something specific? (e.g. a CRM, an Excel sheet, an API, another existing skill, data in a folder...)"

→ Claude identifies dependencies. If none: it moves on.

---

**Q5. Where should the results be saved?**
> "When the skill produces something, where do you want to find it? (e.g. in a documents folder, in a reports section, in a client's profile...)"

→ Claude maps onto existing paths from `CLAUDE.md` (output rules table). If the path doesn't exist, it proposes creating it or using a similar one.

---

**Q6. Are there important rules or constraints?**
> "Is there anything this skill must never do, or any rule it must always respect? (e.g. 'never send emails without approval', 'always use template X', 'don't touch production data')"

→ If none: it moves on.

---

**Q7. Skill type**
Claude assesses on its own, based on the answers, whether it's an **operational** skill (has executable commands, integration with systems) or a **context** skill (framework, guides, background). It shows its assessment and asks for confirmation:

> "Based on what you've told me, this looks like an **operational** skill — it has commands that produce concrete outputs. Do you confirm, or is it more of a reference guide/framework?"

---

### Step 3 — Summary and confirmation

Claude shows a structured summary of everything before creating the files:

```
📋 Skill summary "{Name}"

Purpose: ...
Type: operational / context
Owner: ...
Used by: ...

Commands:
  • {comando-1} → {output} → saved in {path}
  • {comando-2} → {output} → saved in {path}

Dependencies: ...
Rules: ...
```

Then it asks:
> "Does this look good? Can I proceed to create the files, or do you want to change something?"

If the user wants to correct something: Claude updates the specific point and shows the updated summary.

---

### Step 4 — Automatic generation

After confirmation, Claude creates:

1. **`os/skills/{slug}/SKILL.md`** — using the template below
2. **Updates `os/skills/SKILLS.md`** — adds the row to the correct table (operational or context)
3. **Updates `system/CHANGELOG.md`** — entry `feat: nuova skill {nome}` with date and MINOR category
4. **Commit** — `[system] feat: nuova skill {slug}`

It tells the user what it created, where to find the files, and how to invoke the skill.

---

## Generated template: operational skill

```markdown
# Skill: {Name}

## Identity

{Purpose in 2-3 sentences, clear language}
Used by: {agents}.

---

## Commands

| Command | Description | Output |
|---------|------------|--------|
| `{comando}` | {what it does} | {what it produces} — saved in `{path}` |

---

## Command: {comando}

### Input
- {required, optional parameters}

### Process
1. {step 1}
2. {step 2}
3. ...

### Output
{output description + destination path}

---

## Rules
{constraints and rules that emerged in the interview — omit the section if empty}

## Dependencies
{other skills, MCP tools, APIs — omit the section if empty}
```

---

## Generated template: context skill

```markdown
# Skill: {Name}

{Purpose in 2-3 sentences. When to use it and why.}
Used by: {agents} as background to inform decisions on {domain}.

---

## {Section 1 — main framework/concept}

{content}

---

## {Section 2}

{content}

---

## When to apply it

{specific situations in which this skill is relevant}
```

---

## Claude's behavior during the interview

- **One question at a time** — don't produce lists of questions
- **Adapt the language** to the user: if they use technical terms, Claude can use them; if they speak in operational/business terms, Claude stays in that register
- **Always suggest** a default option the user can accept or modify — never leave the user facing an open question without a starting point
- **Translate to technical** silently: the user doesn't see slugs, paths, frontmatter — they only see names and concepts
- **If an answer is ambiguous**, rephrase with an example and ask for confirmation: "Do you mean the command produces a file to open, or does it update existing data?"
- **Never get stuck** on a question: if the user doesn't know what to answer, Claude picks the most reasonable default and moves on

---

## Example conversation

> **User**: I want to create a skill to manage user interviews

> **Claude**: Perfect. I see there isn't a skill for this yet, so I'll create it from scratch.
>
> First question: **what exactly is this skill for?** Describe what it should do — informally is perfectly fine.

> **User**: when we do interviews with clients or potential clients, I want a place to collect the results, extract the main themes, and understand what comes up recurrently

> **Claude**: Clear. Who in your company will mainly use this skill — you as founder, someone from the product team, the sales team, or everyone?

> **User**: mostly me and whoever manages the product

> **Claude**: Perfect, I'll associate it with you (CEO) and the PM.
>
> Next question: **what should it do concretely?** Tell me the main actions — you can list or describe them however you like. For example: "collect the data from an interview", "produce a summary report", "find recurring themes"...

*(and so on)*
