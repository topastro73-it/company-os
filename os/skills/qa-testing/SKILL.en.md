# QA & Testing Skill

Skill to support the CTO in planning and managing testing.
Generates test plans, test cases, test reports from existing PRDs and specs.
Does not run tests automatically — prepares everything so the team can run them.

## Multi-user context (customize for your product)

> ⚠️ Adapt the user levels to your product. Example with 3 levels — if the product is multi-role, tests must cover all of them:

```
Role A — Administrator/Partner   → management, dashboard, configuration
Role B — Operator                → demos, onboarding, daily operations
Role C — End user                → dashboard, reports, alerts
```

Every feature must be tested from the perspective of all impacted users.

## Available commands

### `/qa test-plan [spec]`
Generates a complete test plan from a PRD.

**Process**:
1. Read the PRD from `company/prodotto/specs/prd-{slug}.md`
2. Extract all user stories and acceptance criteria
3. Generate structured test plan:

```markdown
# Test Plan: {Feature Name}

**PRD**: company/prodotto/specs/prd-{slug}.md
**Version**: 1.0
**Date**: {YYYY-MM-DD}
**Owner**: CTO / QA

## Scope
- **In scope**: [what we test]
- **Out of scope**: [what we do NOT test in this cycle]
- **Environments**: [staging / pre-prod / prod]

## Test Strategy
- **Functional testing**: all user flows from the user stories
- **Edge case testing**: invalid inputs, limits, edge cases
- **Integration testing**: interactions with other modules/services
- **Security testing**: authentication, authorization, input sanitization
- **Performance testing**: [if applicable — load, response time]
- **Regression testing**: existing features that could be impacted

## Required resources
- **Test data**: [required datasets — fake records, test CSVs, etc.]
- **Test accounts**: [required roles — one account for each user level]
- **Environments**: [staging configured with X]
- **Tools**: [Postman, Cypress, manual, etc.]

## Acceptance criteria for release
- [ ] All critical test cases passed
- [ ] No open P0/P1 bugs
- [ ] Regression tests passed
- [ ] Performance within defined limits
- [ ] Security check completed

## Timeline
| Phase | Estimated duration | Who |
|------|---------------|-----|
| Test data preparation | [time] | [who] |
| Functional test execution | [time] | [who] |
| Fixing found bugs | [time] | [who] |
| Re-test after fix | [time] | [who] |
| Regression test | [time] | [who] |
| Sign-off | [time] | CTO |
```

**Output**: `company/prodotto/testing/test-plan-{slug}.md`

---

### `/qa test-cases [spec]`
Generates detailed test cases from a PRD.

**Process**:
1. Read the PRD and the acceptance criteria
2. For each acceptance criterion generate 1+ test cases
3. For each user story add: happy path, sad path, edge case
4. For each impacted user level: specific tests

**Test case format**:

```markdown
# Test Cases: {Feature Name}

**PRD**: company/prodotto/specs/prd-{slug}.md
**Total test cases**: {N}
**Critical**: {N} | **High**: {N} | **Medium**: {N} | **Low**: {N}

---

## TC-001: {Descriptive title}

- **User Story**: US-{N}
- **Priority**: Critical / High / Medium / Low
- **User level**: Role A / Role B / Role C
- **Type**: Functional / Edge case / Security / Performance
- **Pre-conditions**: [required initial state]
- **Test data**: [specific data required]

| Step | Action | Input | Expected result |
|------|--------|-------|-----------------|
| 1 | [what to do] | [with which data] | [what should happen] |
| 2 | [what to do] | [with which data] | [what should happen] |
| 3 | [what to do] | [with which data] | [what should happen] |

- **Post-conditions**: [expected final state]
- **Notes**: [additional info, known workarounds, etc.]

---

## TC-002: {Title — negative case}

- **User Story**: US-{N}
- **Priority**: High
- **User level**: Role A
- **Type**: Edge case
- **Pre-conditions**: [initial state]

| Step | Action | Input | Expected result |
|------|--------|-------|-----------------|
| 1 | [action with invalid input] | [wrong data] | [appropriate error message] |
| 2 | [verify] | | [no corrupted data] |

---

## TC-003: {Title — security}
...
```

Classify each test case by priority:
- **Critical**: if it fails, the feature cannot go to production
- **High**: core functionality, must pass
- **Medium**: secondary functionality, can be worked around
- **Low**: nice-to-have, cosmetic

**Output**: `company/prodotto/testing/test-cases-{slug}.md`

---

### `/qa test-cases-api [endpoint]`
Generates test cases specific to API endpoints.

**Process**:
1. Identify the endpoint (URL, method, parameters, auth)
2. Generate test cases for:
   - **Happy path**: valid request → correct response
   - **Input validation**: missing fields, wrong types, out-of-range values
   - **Authentication**: without token, expired token, wrong token
   - **Authorization**: user without permissions, wrong role
   - **Rate limiting**: too many requests
   - **Edge cases**: empty payload, huge payload, special characters, SQL injection, XSS

**Format**:
```markdown
## API: {METHOD} {endpoint}

### TC-API-001: Happy path
- **Request**:
  - Method: POST
  - Headers: Authorization: Bearer {valid_token}
  - Body: {valid json}
- **Expected Response**:
  - Status: 200
  - Body: {expected structure}

### TC-API-002: Missing required field
- **Request**: body without "name" field
- **Expected**: 400 Bad Request, message "name is required"

### TC-API-003: Invalid token
- **Request**: Authorization: Bearer invalid_token
- **Expected**: 401 Unauthorized

### TC-API-004: User without permissions
- **Request**: valid token but role with reduced privileges (Role C) on admin endpoint
- **Expected**: 403 Forbidden
```

**Output**: `company/prodotto/testing/test-cases-api-{endpoint-slug}.md`

---

### `/qa regression-suite`
Generates or updates the regression test suite.

**Process**:
1. Read all shipped features from `company/prodotto/changelog.md`
2. For each critical feature: 2-3 core test cases verifying it still works
3. Organize by area: authentication, Role A dashboard, operational module (Role B), end-user dashboard (Role C), core APIs
4. The regression suite is incremental — it grows with each release

**Output**: `company/prodotto/testing/test-plan-master-regression.md` (existing file — incremental update, do not create a new `regression-suite.md`)

---

### `/qa test-report [spec] [cycle]`
Generates a report of the results of a test cycle.

**Process**:
1. Ask the CTO/team for the results: for each test case, passed/failed/blocked
2. Generate report:

```markdown
# Test Report: {Feature Name} — Cycle {N}

**Date**: {YYYY-MM-DD}
**Tester**: [who executed]
**Build/Version**: [tested version]

## Summary

| Status | Count | % |
|-------|-------|---|
| ✅ Passed | {N} | —% |
| ❌ Failed | {N} | —% |
| ⏸️ Blocked | {N} | —% |
| ⭕ Not executed | {N} | —% |
| **Total** | **{N}** | **100%** |

## Verdict: GO / NO-GO / CONDITIONAL

Rationale: [why yes/no/conditional]

## Bugs found

| ID | Title | Severity | Test case | Status |
|----|--------|----------|-----------|--------|
| BUG-001 | [title] | P0/P1/P2/P3 | TC-{N} | Open / Fix in progress / Resolved |

## Failed tests — detail

### TC-{N}: {Title}
- **Expected result**: [what should have happened]
- **Actual result**: [what happened]
- **Screenshot/log**: [reference]
- **Linked bug**: BUG-{N}

## Blocked tests — reason
- TC-{N}: blocked by [reason — environment, data, blocking bug]

## Recommendations
1. [what to do before the next cycle]
2. [residual risks if we go to production]

## Sign-off
- [ ] CTO approves the release
- [ ] All P0/P1 bugs resolved
- [ ] Regression passed
```

**Output**: `company/prodotto/testing/test-report-{slug}-cycle{N}.md`

---

### `/qa security-test [feature]`
Generates a security testing checklist for a feature.

**Process**:
1. Identify the feature's attack surfaces
2. Generate checklist by category:

```markdown
# Security Test Checklist: {Feature}

## Authentication
- [ ] Endpoint accessible without authentication → must fail with 401
- [ ] Expired token → must fail with 401
- [ ] Another user's token → must fail with 403

## Authorization
- [ ] End user accesses another end user's data → must fail
- [ ] Role B (operator) accesses admin dashboard → must fail
- [ ] Privilege escalation via request manipulation → must fail

## Input Validation
- [ ] SQL injection in text fields → must be sanitized
- [ ] XSS (Cross-Site Scripting) → must be sanitized
- [ ] Path traversal in file uploads → must be blocked
- [ ] Input larger than the limit → must be rejected with an error

## Data
- [ ] PII visible only to the authorized user
- [ ] Data in transit encrypted (HTTPS)
- [ ] Sensitive data not in logs
- [ ] One tenant/partner's data not visible to another tenant/partner

## API
- [ ] Rate limiting active
- [ ] CORS configured correctly
- [ ] No debug endpoint exposed
- [ ] Correct API versioning
```

**Output**: `company/prodotto/testing/security-test-{slug}.md`

---

### `/qa smoke-test [release]`
Generates a smoke test checklist for a release.

**Process**:
1. Identify the product's core functionality (the kind that, if broken, is a P0)
2. Generate quick checklist (max 15-20 checks, executable in 30 minutes):

```markdown
# Smoke Test: Release {version}

**Estimated time**: 30 minutes
**Environment**: [staging/production]
**Date**: {YYYY-MM-DD}
**Tester**: [who]

## Login & Auth
- [ ] Role A login (admin/partner) works
- [ ] Role B login (operator) works
- [ ] Role C login (end user) works
- [ ] Logout works
- [ ] Password reset works

## Core — Role A (admin/partner)
- [ ] Admin dashboard loads
- [ ] List of managed entities visible
- [ ] Creating a new entity works

## Core — Role B (operational module)
- [ ] Main operational flow works
- [ ] Output/report generated
- [ ] Export downloadable

## Core — Role C (end user)
- [ ] End-user dashboard loads
- [ ] Main metrics visible
- [ ] Alerts visible

## API
- [ ] Health check endpoint: 200 OK
- [ ] Core endpoint: responds in <2s

## Result
- [ ] All checks passed → GO
- [ ] Failed checks: [list] → BLOCK RELEASE
```

**Output**: `company/prodotto/testing/smoke-test-{version}.md`

---

### `/qa test-data [spec]`
Generates a specification of the required test data.

**Process**:
1. Read the PRD and the test cases
2. Identify all data required to run the tests:
   - Test accounts for each role
   - Datasets (fake records, test CSVs, sample data)
   - Configurations (tenant/partner setup, active products)
   - Edge case data (malformed CSVs, names with special characters, etc.)
3. Propose how to create them (script, manual, fixture)

**Output**: `company/prodotto/testing/test-data-{slug}.md`

---

## Structure in the repo

```
company/prodotto/testing/
├── test-plan-{slug}.md            # Test plan per feature
├── test-cases-{slug}.md           # Detailed test cases
├── test-cases-api-{slug}.md       # API test cases
├── test-report-{slug}-cycle{N}.md # Results report
├── security-test-{slug}.md        # Security checklist
├── smoke-test-{version}.md        # Smoke test per release
├── test-data-{slug}.md            # Test data specification
└── test-plan-master-regression.md # Regression suite (incremental)
```

## Workflow: from PRD to tested release

```
1. PM writes PRD             → company/prodotto/specs/prd-{slug}.md
2. CTO does tech review      → estimates, risks, architecture
3. /qa test-plan             → generates test plan from the PRD
4. /qa test-cases            → generates detailed test cases
5. /qa test-data             → specifies required data
6. Dev implements            → development
7. /qa smoke-test            → quick checklist on staging
8. /qa security-test         → security checklist
9. Team runs tests           → manual or automated
10. /qa test-report          → report with results and verdict
11. If GO → release
12. /qa regression-suite     → update regression suite
```

## Integration in the system

### In the CTO workflow
When a spec moves to `status: in-development`:
- Suggest: "Do you want to generate the test plan and the test cases?"
- The test plan is created BEFORE development finishes

### In the PM workflow
When a spec moves to `status: shipped`:
- Verify: "Is there a test report with a GO verdict?"
- If not: flag — it should not be shipped without tests

### In the CEO Decision Cadence — Weekly
- "Specs in development without a test plan: [list]"
- "[N] open P0/P1 bugs"

### In the Chief of Staff — product-plan
Show a "Test status" column for each spec in `in-development`:
- 📋 Test plan created
- 🧪 In testing
- ✅ Test passed (GO)
- ❌ Test failed (NO-GO)
- ⚠️ No test plan

### ClickUp integration
Bugs found during testing can be created as tasks in ClickUp:
- Space/List: see `config/integrations.yaml` (ClickUp) → Bug list
- With a reference to the test case that found them

## Rules

- **NEVER** release without at least the smoke test
- **ALWAYS** generate test cases from the PRD, not from memory
- **ALWAYS** include negative tests and edge cases, not just the happy path
- **ALWAYS** document the results, even if everything passes
- Security tests are mandatory for features touching auth, data, APIs
- The regression suite grows with each release — do not restart it from scratch
- Bugs found in testing go to ClickUp with priority and a link to the test case
