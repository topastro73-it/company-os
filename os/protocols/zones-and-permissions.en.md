# Zones and permissions

The access model has two orthogonal components:
- **Zone** = *where the file lives* and *who sees it* → decided by the Drive ACL (`config/acl.yaml`)
- **Tier** 🔴🟡🟢 = *how sensitive the content is* → decides external publishing, PII redaction, secret-scan

## 1. Every file has a zone

Every operational file declares its zone in the frontmatter:

```yaml
---
zone: clienti          # _os | direzione | commerciale | clienti | prodotto | finance | compliance | marketing | shared
tier: 🟡               # 🔴 restricted | 🟡 internal (default) | 🟢 public
---
```

`scripts/audit/frontmatter-check.py` verifies that every operational file declares zone and tier.
A file without `zone:` is treated as belonging to the zone of the folder it lives in;
a file without `tier:` is 🟡 INTERNAL by default.

## 2. Access is decided by the Drive ACL

The system **has no permission layer of its own**: who can read/write a file is
determined by the ACL of the zone's Drive folder, per the matrix in `config/acl.yaml`.
If a person has no access to the folder, they don't see those files — nothing else is needed.
`osctl acl-audit` compares the real permissions with the matrix and flags drift.

Operational consequences for the agent:
- Write every output **only in the relevant zone** (never a client's output outside `20-Clienti/{slug}/`)
- Do not copy content from a restricted zone to a broader one (e.g. from `40-Finance/` to `30-Prodotto/`)
- Never bypass the ACL "for convenience" (e.g. duplicating a contract in `90-Condivisi/`)

## 3. Per-folder ACL on 20-Clienti

`20-Clienti/` has `per_folder_acl: true`: each client folder `20-Clienti/{slug}/` has its
own ACL — only those following that client see it (owner + assigned team). When creating
a new client folder:
1. Apply the zone's default ACL (`write:` in `acl.yaml`)
2. Assign an explicit **owner** (the person following the client)
3. Restrict to those involved only; `osctl acl-audit` flags client folders without an owner

## 4. Restricted subzones (only when they ADD access, never when they remove it)

Google Drive inherits permissions only downward: whoever has access to a folder inherits it
in every subfolder, and there is no native way to restrict it further down.
A "restricted subzone" in `acl.yaml` works **only** if it adds extra people compared to
the parent folder (which may have no access at all, e.g. finance); you cannot use it to
*remove* access from those who already have it above.

| Subzone | Path | Access | Content |
|---|---|---|---|
| Accountant | `40-Finance/per-commercialista/` | write: the founder · read: + accounting firm | One-way showcase for the tax firm |
| Grants | `40-Finance/bandi/` | the founder + grants consultant | Grant reporting, project documents |
| Audit evidence | `50-Compliance/evidence/` | write: the founder · read: internals + auditor | Evidence for the certification body |

These work because the parent zone (`finance`, `compliance`) is already more restricted than
those added deeper: nobody loses permissions, only an extra reader is added.

**Client contracts**: NOT a subzone of `20-Clienti/{slug}/` — whoever works on the client
(delivery, CS) already has broader access than the parent folder, so you cannot restrict
below it. It lives in the separate, top-level zone `contratti` (`70-Contratti-Riservati/{slug}/`,
write: the founder · read: the founder, Head of Sales). Only `contratti/README.md` with the pointer
stays in the client folder. General rule: if a restriction is tighter than the parent zone, it needs a
separate top-level zone, not a subfolder.

## 5. Tiers 🔴🟡🟢 — what the classification is for

The tier does NOT decide who accesses (that's the ACL): it decides **what may leave** and **how**.

| Tier | Typical content | Rules |
|---|---|---|
| 🔴 RESTRICTED | Signed contracts, cap table, IBAN, tax codes/VAT numbers, non-public financials, compensation | Lives only in `40-Finance/`, `70-Contratti-Riservati/`, and in git only in `vault/`. Never published, never cited in wiki/learnings/commits/briefings |
| 🟡 INTERNAL | Pipeline, unpublished metrics, roadmap, partner notes, decisions | Default. Publish to third parties only after PII redaction |
| 🟢 PUBLIC | Blog, public battlecards, authorized case studies, onboarding material | Publishable anywhere |

The tier feeds three mechanisms: (a) the **external publish** gate (never 🔴, 🟡 only redacted),
(b) **PII redaction** before anything leaves, (c) `secret-scan.sh` which blocks in CI/pre-commit
tokens, IBANs and 🔴 files outside the allowed destinations.

## 6. PII rules

- **Never** IBANs, tax codes, VAT numbers, card numbers, personal phone numbers, compensation/salaries in:
  `system/wiki/`, `system/learnings.md`, commit messages, briefings, PR titles
- **End clients** (our partners' clients) in wiki and learnings: **initials + role**
  (e.g. "M. Rossi, CISO Acme"), unless there is a dedicated entity page in `system/wiki/entities/clients/{slug}.md`
- Learnings: **abstract** rules ("when a partner slows down…"), never personalized on the name
- Screenshots with client UI: redact/blur before saving outside the client folder

## 7. Graceful degradation — zone not accessible

If a zone is not reachable (Drive not mounted, ACL missing, vault not present on the clone):
1. **Flag** immediately which zone is missing and what you won't be able to do
2. **Continue** with what you have: snapshots in `company/` (for the admin), files of the current zone
3. **Never block** the work waiting for the zone; do not invent the missing data
4. If the output belongs in the missing zone, save it in local staging and flag:
   "zone X unavailable — file ready, I'll move it on restore"
5. Vault not mounted → agents on 🔴 data degrade: they answer only with available 🟡 data
