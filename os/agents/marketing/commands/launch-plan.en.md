# /marketing launch-plan — Feature launch plan

## Purpose
Turn a shipped feature into demand and adoption, with effort proportional to its weight.

## Input
- Feature (with release notes in zone `prodotto`) · actual availability date

## Steps
1. Load the PRD and the release notes (`prodotto/releases/`) — only what is **shipped**
   with UAT GO gets launched; verify the benefit for the 3 levels (Partner, Seller, SMB).
2. **Classify the launch**:
   - **Tier 1** (major): blog post + partner email + social + sales enablement + webinar/demo
   - **Tier 2** (notable): blog post + email + changelog
   - **Tier 3** (minor): changelog and note in the partner release notes
3. **Message**: benefit before the feature; tailored per audience (the partner wants
   revenue, the SMB wants simple protection).
4. **Timeline**: pre-launch (assets ready, sales brief) → launch day (publications,
   sends) → post-launch (follow-up, feedback collection at 2 weeks).
5. **Success metrics**: adoption (partners active on the feature), traffic/leads, feedback.
6. Enablement assets → zone `commerciale` (where Sales finds them); sends and publications
   → PREPARE → APPROVE → EXECUTE.

## Output format
```markdown
---
zone: marketing
tier: 🟡
type: launch-plan
feature: {slug}
launch-tier: {1|2|3}
---
# Launch Plan — {feature}

## Classification and rationale   ## Message per audience
## Assets to produce | Asset | Owner | Deadline | Status |
## Timeline (pre / day / post)
## Success metrics
```

## Destination
Zone `marketing` → `content/launch-{feature}.md`.
Commit (admin): `[marketing] launch: {feature}`.

## Handoff
Enablement → `sales` · communication to active partners → `delivery` · collected feedback
→ `product`.
