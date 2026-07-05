---
zone: _os
tier: 🟡
---

# Language protocol

The instance's working language is **a single source of truth**: `language` in
`config/company.yaml` (`it` | `en`). It governs three things: the language of chat replies,
the **generation** language of every markdown file, and which **variant** of the system
files gets presented.

## 1. Choice at startup (setting up a new company)

On the first session of a not-yet-configured instance (`config/company.yaml` is missing
or `language` is not set), **before generating anything** ask:

> 🌐 In che lingua vuoi lavorare? / Which language do you want to work in? [italiano / english]

Write the answer to `config/company.yaml → language` (creating the file from the copy of
`company.example.yaml` if needed). From that moment on, never ask again.

## 2. What `language` governs

- **Chat replies**: always in the configured language (unless explicitly requested otherwise).
- **File generation**: every md output (reports, specs, proposals, briefings, wiki, decisions)
  is born in the configured language. Fixed exceptions, independent of the language:
  ClickUp tasks in English (`config/integrations.yaml → rules.task_language`),
  `system/wiki/` in English (memory protocol).
- **Presentation of system files**: system files have the Italian version as the
  base (`X.md`) and the English variant alongside (`X.en.md`). With `language: en`, load and
  present the `.en.md` variant when it exists (fallback: the base file); with `language: it`
  always use the base file. `osctl publish` publishes the right variant to Drive.

## 3. Changing language on the fly

The user can change language **at any time by saying so in chat** (e.g. "passa
all'inglese", "switch to Italian"). Whichever agent receives it:

1. Update `config/company.yaml → language` (config change: commit
   `[admin] config: language → {lang}`; no system changelog entry — it is not a system file)
2. Run `osctl publish` so the Drive zones receive the CLAUDE.md files and contexts in the new language
3. From then on: replies and new files in the new language. Files **already generated are not
   retranslated** retroactively (they are retranslated on demand if the user asks for a specific file)

## 4. Rules for `.en.md` variants

- A variant is created only if the base file is in Italian; if a file is already in English,
  no variant (the fallback covers it).
- Variants are **faithful translations**: same structure, same paths/zones/commands/config
  keys (never translated), same guardrails. Only the prose changes.
- Whoever modifies a system file also updates the variant in the same commit
  (link-lint does not enforce it; it is the admin's responsibility — when in doubt, regenerate the variant).
