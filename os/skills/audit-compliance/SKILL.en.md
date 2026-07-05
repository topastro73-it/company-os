# Audit & Compliance Skill

Skill to manage company compliance, certification readiness,
and continuous auditing of the company's security posture.

## Why it is critical

> ⚠️ Adapt frameworks and priorities to your industry. Example for a company selling B2B digital services:

If you are not compliant and certified:
1. Enterprise customers do not choose you (procurement requires certifications)
2. You lose credibility with end customers
3. You risk direct sanctions (frameworks like NIS2 may apply to you as a digital service provider)

Compliance is not a cost — it is a **sales prerequisite** in many B2B markets.

## Frameworks covered

> Framework examples. Fill in `Priorità` and `Status target` with your company's real situation — do not declare a "certified" status without evidence and an accredited auditor.

| Framework | Why it may be needed | Priority | Target status |
|-----------|---------------|----------|--------------|
| **NIS2** | EU legal obligation for many sectors | [to be defined] | [to be defined] |
| **GDPR** | Processing of personal data of EU subjects | [to be defined] | [to be defined] |
| **ISO 27001** | Often required in enterprise procurement | [to be defined] | [to be defined] |
| **ISO 9001** | Process quality | [to be defined] | [to be defined] |
| **ISO 27017** | Cloud security | [to be defined] | [to be defined] |
| **ISO 27018** | PII in the cloud | [to be defined] | [to be defined] |
| **SOC 2 Type II** | Enterprise credibility and US/UK markets | [to be defined] | [to be defined] |
| **Cyber Essentials** | UK market | [to be defined] | [to be defined] |

---

## Available commands

### `/audit compliance-status`
Dashboard of compliance status across all frameworks.

**Process**:
1. Read `company/compliance/status.md` for the current status
2. For each active framework: how many requirements mapped, how many satisfied, how many gaps
3. Generate dashboard with traffic lights

**Output format**:
```markdown
# Compliance Dashboard — {date}

## Overview
| Framework | Requirements | Satisfied | Gaps | Compliance % | Status |
|-----------|----------|------------|-----|-------------|--------|
| NIS2 | 45 | 38 | 7 | 84% | yellow |
| GDPR | 30 | 28 | 2 | 93% | green |
| ISO 27001 | 114 | 67 | 47 | 59% | red |
| SOC 2 | 64 | 30 | 34 | 47% | red |

## Critical gaps (blocking certification)
1. [Gap] — Framework: [which] — Effort: [S/M/L] — Owner: [role]

## Important gaps (to resolve by [date])
1. [Gap] — Framework: [which] — Effort: [S/M/L]

## Next milestones
- [Date]: [milestone]

## Recommendations
1. [Priority action]
```

**Output**: `company/compliance/reports/compliance-status-{date}.md`

---

### `/audit gap-analysis [framework]`
Detailed gap analysis for a specific framework.

**Process**:
1. Load the framework's requirements from `company/compliance/frameworks/`
2. For each requirement: status (compliant / partial / non-compliant / N/A)
3. For each gap: what is missing, effort to close it, owner, priority
4. Generate remediation roadmap

**Output**: `company/compliance/reports/gap-analysis-{framework}-{date}.md`

---

### `/audit nis2-readiness`
Specific NIS2 readiness check — often the most critical for a digital service provider.

**Process**:
1. Verify the 10 key NIS2 requirements:
   - [ ] Risk management policy documented and approved by management
   - [ ] Incident response plan with 24h/72h notification
   - [ ] Business continuity and disaster recovery plan tested
   - [ ] Supply chain security (vendor assessment)
   - [ ] Vulnerability management and patching policy
   - [ ] Cryptography and encryption policy
   - [ ] Access control and authentication (MFA)
   - [ ] Network security and monitoring
   - [ ] Cybersecurity training for management and employees
   - [ ] Documented periodic audits and testing
2. For each requirement: status, available evidence, gap
3. Assess: are we ready for an audit? If not, what is missing?
4. Timeline to reach readiness

**Output**: `company/compliance/reports/nis2-readiness-{date}.md`

---

### `/audit gdpr-check`
GDPR compliance check.

**Process**:
1. Verify key requirements:
   - [ ] Record of processing activities up to date
   - [ ] Privacy policy and cookie policy up to date
   - [ ] DPAs signed with all processors
   - [ ] Process to handle data subject rights requests (DSAR)
   - [ ] DPIA for high-risk processing
   - [ ] DPO appointed (if necessary)
   - [ ] Data breach notification within 72h procedure
   - [ ] Privacy by design integrated into development
   - [ ] Employee privacy training
   - [ ] Extra-EU transfers handled (SCC, adequacy)
2. Gaps and remediation plan
3. Disclaimer: validate with DPO/lawyer

**Output**: `company/compliance/reports/gdpr-check-{date}.md`

---

### `/audit iso27001-roadmap`
Generates a roadmap for maintaining/renewing ISO 27001 certification.

**Process**:
1. Map the 93 controls of Annex A (ISO 27001:2022)
2. For each control: current status, gap, effort
3. Identify: what we already have, what is missing, what is partial
4. Generate roadmap:
   - Phase 1: ISMS review (policy, scope, risk assessment)
   - Phase 2: Controls update
   - Phase 3: Internal audit
   - Phase 4: External surveillance/renewal audit
5. Timeline and estimated budget

**Output**: `company/compliance/reports/iso27001-roadmap-{date}.md`

---

### `/audit soc2-readiness`
Assesses readiness for SOC 2 Type II.

**Process**:
1. Verify the 5 Trust Service Criteria:
   - Security (mandatory)
   - Availability
   - Processing Integrity
   - Confidentiality
   - Privacy
2. For each criterion: controls in place, gaps, evidence
3. Estimate: timeline for Type I (point-in-time) and Type II (observation period)

**Output**: `company/compliance/reports/soc2-readiness-{date}.md`

---

### `/audit policy-review`
Reviews all company policies for completeness and freshness.

**Process**:
1. Inventory policies in `company/compliance/policies/`:
   - Information Security Policy
   - Acceptable Use Policy
   - Incident Response Policy
   - Business Continuity Policy
   - Data Classification Policy
   - Access Control Policy
   - Encryption Policy
   - Vendor Management Policy
   - Change Management Policy
   - HR Security Policy (onboarding/offboarding)
2. For each policy: does it exist? Is it up to date? Is it approved? Is it communicated?
3. Identify missing or stale policies
4. Propose a creation/update plan

**Output**: `company/compliance/reports/policy-review-{date}.md`

---

### `/audit evidence-check`
Verifies that compliance evidence is collected and up to date.

**Process**:
1. For each active framework, verify the required evidence:
   - System logs and monitoring
   - Vulnerability scan reports
   - Employee training records
   - Management approval minutes
   - Previous audit reports
   - Disaster recovery tests
   - Incident registers
   - Vendor assessments
2. For each piece of evidence: does it exist? Is it up to date? Is it archived correctly?
3. Alert for missing or expired evidence

**Output**: `company/compliance/reports/evidence-check-{date}.md`

---

### `/audit vendor-assessment [vendor]`
Assessment of a vendor's security posture.

**Process**:
1. Vendor questionnaire: certifications, policies, incident history, DPA
2. Risk rating: Critical / High / Medium / Low
3. Recommendation: approve / approve with conditions / reject
4. DPA needed? Specific clauses?

**Output**: `company/compliance/vendors/{vendor}.md`

---

## Structure in the repo

```
company/compliance/
├── status.md                        # Compliance status dashboard
├── frameworks/
│   ├── nis2-requirements.md         # Mapped NIS2 requirements
│   ├── gdpr-requirements.md         # Mapped GDPR requirements
│   ├── iso27001-controls.md         # Mapped ISO 27001 controls
│   └── soc2-criteria.md             # Mapped SOC 2 criteria
├── policies/
│   ├── information-security.md
│   ├── incident-response.md
│   ├── business-continuity.md
│   ├── access-control.md
│   ├── encryption.md
│   ├── vendor-management.md
│   ├── data-classification.md
│   ├── acceptable-use.md
│   ├── change-management.md
│   └── hr-security.md
├── vendors/
│   └── {vendor-slug}.md             # Vendor assessments
├── audits/
│   └── {date}-{type}.md             # Audit records
└── evidence/
    └── README.md                    # Where to find the evidence
```

---

## Integration into decision workflows

### In the CEO Decision Cadence

**Daily**:
- If there is a compliance deadline in the next 7 days → alert
- If an audit is scheduled in the next 30 days → preparation reminder

**Weekly**:
- "Policy review: [N] policies not updated for 6+ months"
- "Evidence: [N] pieces of evidence missing for [framework]"

**Monthly**:
- "Compliance dashboard: NIS2 [N]%, GDPR [N]%, ISO27001 [N]%"
- "Next certification milestone: [what] — [date] — are we ready?"
- "Vendor assessment: [N] vendors not assessed for 12+ months"

### In the PM workflow

**When the PM writes a PRD** (`/product write-spec`):
- Additional step: "Does this feature impact compliance?"
- Check: does it process personal data? Does it change the security architecture? Does it require a DPIA?
- If yes: flag in the spec frontmatter: `compliance-impact: [NIS2/GDPR/ISO27001]`
- Automatic handoff → `/audit` for impact assessment

### In the CTO workflow

**When the CTO does a tech-decision or architecture-review**:
- Additional step: "Does this decision impact compliance?"
- Check: does it change encryption, access control, logging, data flow?
- If yes: document the impact in the ADR and notify the audit skill
- Verify: does the new architecture maintain the mapped ISO27001 controls?

### In the Legal workflow

**When Legal reviews contracts**:
- Automatic check: does the contract include DPA clauses if it processes personal data?
- Check: has the vendor been evaluated with a vendor assessment?
- If not: flag → `/audit vendor-assessment [vendor]` before signing

### In the HR workflow

**When HR handles onboarding/offboarding**:
- Onboarding: verify that the new employee completes security training
- Offboarding: verify access revocation, NDA in place
- Tracking: training records for compliance evidence

### In the Marketing workflow

**When Marketing creates compliance content (e.g. NIS2) for customers**:
- Cross-check: "Are we ourselves compliant with what we are recommending?"
- If not: flag — we cannot recommend something we do not do ourselves

### In the Sales workflow

**When Sales responds to enterprise RFPs/procurement**:
- Automatically load: available certifications, policies, SOC2 report
- Identify gaps: "The customer requires ISO27001 and we don't have it yet — how do we respond?"
- Propose: an honest answer with a certification roadmap

### In the Chief of Staff workflow

**In daily-briefing and weekly-digest**:
- Include a "Compliance" section if there are alerts or deadlines
- In the product-plan: highlight specs with `compliance-impact`
- In the startup-snapshot: include compliance % in the section

---

## Recommended audit cadence

| Activity | Frequency | Owner | Command |
|----------|----------|-------|---------|
| Compliance status dashboard | Monthly | CoS/Legal | `/audit compliance-status` |
| Policy review | Quarterly | Legal | `/audit policy-review` |
| Evidence check | Quarterly | Legal/CTO | `/audit evidence-check` |
| Vendor assessment | Annually per vendor | Legal | `/audit vendor-assessment` |
| NIS2 readiness | Quarterly | Legal/CTO | `/audit nis2-readiness` |
| GDPR check | Every 6 months | Legal | `/audit gdpr-check` |
| Penetration test | Annually | CTO (external) | Manual |
| DR test | Every 6 months | CTO | Manual |
| Security training | Annually | HR | Manual |

---

## Rules

- **ALWAYS** disclaimer: "This analysis is an internal assessment. Formal certifications require an accredited auditor."
- **NEVER** declare compliance without documented evidence
- **ALWAYS** link every gap to a concrete action with owner and deadline
- Compliance is a continuous process, not a one-shot project
- If you sell compliance to your customers, you MUST be more compliant than they are
- Every spec with compliance impact must be flagged in the frontmatter
