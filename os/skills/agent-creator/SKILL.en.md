# Skill: Agent Creator

## Identity

Conversational guide to create a new agent in the system.
No technical knowledge required: Claude conducts an interview, the user answers in natural language, Claude generates all the files.

**Activation**: the user says something like "I want to create an agent", "I need a new agent for X", "add a role for Y", or invokes `/create-agent`.

---

## How it works

Claude conducts a sequential interview. It asks **one question at a time**, in plain language. At the end it generates everything automatically.

There's no need to know what a "slug", a "guardrail" or a "command" is — Claude translates the answers into technical structure.

---

## Interview flow

### Step 1 — Discovery

Before asking questions, Claude reads:
- `os/agents/AGENTS.md` — to understand the existing agents and avoid duplicates or role conflicts
- `os/skills/SKILLS.md` — to know the skills available to assign to the new agent

Then it briefly explains to the user what it's about to do and starts with the first question.

---

### Step 2 — Interview (9 questions, one at a time)

**Q1. What role does this agent have?**
> "Describe in your own words this person's role in your company. What do they do, what are they responsible for?"

→ Claude extracts: title, domain, core responsibilities

---

**Q2. How is it invoked?**
> "What do you want to call it when you use it? For example, Sales is invoked with '/sales', the PM with '/pm'. What's the short name for this agent?"

→ Claude suggests a kebab-case slug based on the title (e.g. "Operations Manager" → `ops`). The user approves or corrects.

---

**Q3. What personality does it have?**
> "Describe how this agent behaves and communicates. For example: is it very analytical? Practically oriented? Formal or direct? Cautious or proactive?"

→ Claude translates into 4-5 personality bullets (AGENT.md style).

---

**Q4. What information does it need to work?**
> "When this agent starts working, what information does it need to know? For example: client data, metrics, the product roadmap, contracts, the budget..."

→ Claude maps onto existing files in `company/`, `vault/`, `zones/_root/context/`. If a data source doesn't exist yet, it flags it as "to be created".

---

**Q5. What does it actually do? (commands)**
> "Tell me the 3-7 main actions this agent can perform. You can describe them freely — e.g. 'prepares a plan', 'analyzes the numbers', 'writes a report', 'manages a process'."

→ For each action Claude asks:
- What the command is called (Claude suggests a slug, the user approves)
- What output it produces (document, report, plan, email...)
- Where it gets saved (Claude maps onto existing paths from `CLAUDE.md`)

If the user doesn't know what to answer, Claude suggests reasonable defaults based on the role.

---

**Q6. Which existing skills does it use?**
> "I'll look at the skills already available in the system — I'll tell you which ones could be useful to this agent, tell me if you agree or if you want to add/remove any."

→ Claude proposes a selection from the skills in `os/skills/SKILLS.md` relevant to the role. The user approves or adjusts.

---

**Q7. Who does it collaborate with?**
> "Which other roles does it work with the most? And when does it hand work to someone else — or receive it — in which situations?"

→ Claude builds the Handoffs table (From → To → When).

---

**Q8. What must it never do?**
> "Are there things this agent must never do, or that it must always verify before acting? For example: 'never approve expenses without confirmation', 'always consult legal before signing'..."

→ Claude builds the Guardrails. If none: it uses generic guardrails appropriate to the role.

---

**Q9. Memory and learnings**
> "Do you want this agent to remember the things it learns over time — for example the patterns that work, the mistakes not to repeat — and apply them automatically in future sessions?"

→ If yes: Claude includes the standard Memory behavior section with tags customized for the role. If no: it omits the section.

---

### Step 3 — Summary and confirmation

Claude shows a structured summary before creating the files:

```
🤖 Agent summary "{Title}" (/{slug})

Role: ...
Personality: ...

Commands ({N} total):
  • /{slug} {comando-1} → {output} → {path}
  • /{slug} {comando-2} → {output} → {path}
  ...

Loaded context: {main files}
Skills used: {skills}
Main handoffs: {from/to}
Guardrails: {N} rules defined
```

Then it asks:
> "Does this look good? Can I proceed to create the files, or do you want to change something?"

If the user wants to correct something: Claude updates the specific point and shows the updated summary.

---

### Step 4 — Automatic generation

After confirmation, Claude creates:

1. **`os/agents/{slug}/AGENT.md`** — using the template below
2. **`os/agents/{slug}/COMMANDS.md`** — command index with slug, description, output path
3. **`os/agents/{slug}/commands/`** — an empty subfolder (the individual command files get added the first time each command is executed)
4. **Updates `os/agents/AGENTS.md`** — adds the row to the agents table
5. **Updates `system/CHANGELOG.md`** — entry `feat: nuovo agente {slug}` with date and MINOR category
6. **Commit** — `[system] feat: nuovo agente {slug}`

It tells the user what it created, where to find the files, and how to invoke the agent.

---

## Generated template: AGENT.md

```markdown
# {Emoji} {Title} Agent

## Identity

{Description of the role in 2-4 sentences. Who they are, what they're responsible for, what their value to the company is.}

## Personality

- {trait 1}
- {trait 2}
- {trait 3}
- {trait 4}
- {trait 5}

## Context to load

Before every action, load the relevant context:

1. `zones/_root/context/COMPANY.md` — Value proposition and company context
2. {role-specific context files}
3. {other relevant files}

## Memory behavior

{Include this section only if the user chose active memory}

- **Apply learnings proactively**: before every main action, check active learnings with tag `{tag-ruolo}` in `system/learnings.md`.
- **Propose new learnings at close**: identify reusable patterns and propose them to the CEO.

## Available Commands

Read `COMMANDS.md` for the complete list of available commands.

## Skills

This agent uses the following skills:

- {`os/skills/{slug}/SKILL.md` — usage description}

## Handoffs

| From | To | When |
|----|---|--------|
| {From agent} → {To agent} | {situation} |

## Guardrails

- **NEVER** {constraint 1}
- **NEVER** {constraint 2}
- **ALWAYS** {positive rule 1}
- **ALWAYS** {positive rule 2}
```

---

## Generated template: COMMANDS.md

```markdown
# {Title} — Available Commands

Complete list of available commands for the {Title} Agent.

### `/{slug} {comando-1} [{optional parameter}]`
{One-line description of what the command does.}
→ Read: `commands/{comando-1}.md`
→ Output: `{output path}`

### `/{slug} {comando-2}`
{Description.}
→ Read: `commands/{comando-2}.md`
→ Output: `{output path}`
```

---

## Claude's behavior during the interview

- **One question at a time** — don't produce lists of questions
- **Adapt the language** to the user: register and mirror their vocabulary (business, technical, operational)
- **Always suggest** a default option the user can accept — never leave a question open without a starting point
- **Translate to technical** silently: the user doesn't see slugs, paths, frontmatter — they see names and roles
- **Emoji for the title**: choose an emoji consistent with the role (e.g. 💰 Sales, 🏗️ Operations, 📊 CFO, 🎯 PM)
- **If an answer is ambiguous**, rephrase with a concrete example and ask for confirmation
- **Never get stuck**: if the user doesn't know what to answer, Claude picks the most reasonable default and moves on
- **Flag the gaps**: if the new agent requires data or files that don't exist in the repo yet, flag it after confirmation — don't block the creation

---

## Example conversation

> **User**: I want to create an agent to manage operations

> **Claude**: Perfect — an Operations agent doesn't exist in the system yet, so I'll create it from scratch.
>
> First question: **what role exactly does this agent have in your company?** Describe what it does, what it's responsible for — informally is fine too.

> **User**: it handles everything operational: vendors, internal processes, onboarding of new tools, service contracts

> **Claude**: Clear — a sort of Head of Operations, responsible for processes, vendors and operational infrastructure.
>
> How do you want to invoke it? I suggest `/ops` — or would you prefer something different?

> **User**: ops is fine

> **Claude**: Perfect. **How does it behave and communicate?** Is it very methodical and precise? Does it tend to escalate problems immediately or solve them autonomously? Formal or direct?

*(and so on)*
