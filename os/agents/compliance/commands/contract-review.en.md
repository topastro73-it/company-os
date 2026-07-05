# /compliance contract-review — Contract analysis or draft

## Purpose
Review (or draft) a contract identifying risks and missing clauses.
Drafts and analysis, never a definitive legal opinion.

## Input
- Type: partnership/reseller, SaaS agreement, NDA, DPA, supplier
- Counterparty · the text (if review) or the key terms (if draft)

## Steps
1. Load previous contracts with the same counterparty (`clienti/{slug}/contratti/` if partner —
   restricted ACL) and the standard templates; consistency with clauses already negotiated.
2. **Review checklist**:
   - clear subject matter and consideration · term, renewal, termination · SLAs and penalties ·
     limitation of liability (cap, exclusions) · IP (who owns what) ·
     confidentiality · governing law and jurisdiction
   - **personal data processed? → DPA mandatory**, attached or referenced; does the supplier
     have a valid vendor assessment? If not → **blocking flag**, assessment before signing
   - white-label/tenant clauses for partner contracts (branding, liability towards SMBs)
3. **Red flags** by severity: blocking / to negotiate / acceptable with note.
4. Proposed amendment for every red flag (alternative text ready to use).
5. **Thresholds**: value >€50k or non-standard clauses → recommend external legal review,
   always. Signing is ONLY for the CEO.

## Output format
```markdown
---
zone: compliance
tier: 🟡
type: contract-review
counterparty: {slug}
---
# Contract Review — {tipo} — {controparte} — {data}

## Summary and recommendation (signable? under what conditions?)
## Red flags | Clause | Severity | Risk | Proposal |
## DPA and vendor assessment check
## Next steps

> Internal draft/analysis. Have a lawyer validate it before use.
```

## Destination
Analysis: `compliance` zone → `audits/contract-{controparte}-{YYYY-MM-DD}.md`.
The signed contract (🔴) goes ONLY in `clienti/{slug}/contratti/` or `vault/`.
Commit (admin): `[compliance] contract: review {controparte}`.

## Handoff
Signing → `ceo` · outcome to the deal owner → `sales` · missing supplier DPA →
`/compliance vendor-assessment`.
