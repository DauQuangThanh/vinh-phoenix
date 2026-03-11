---
name: healthcare-task-management
description: Generates HIPAA-aware, dependency-ordered tasks.md files from healthcare design artifacts (spec.md, design.md, compliance-framework.md). Organizes implementation tasks by user story with HIPAA-specific phases for PHI handling, audit logging, encryption, and compliance verification. Use when breaking down healthcare features into tasks, creating HIPAA-compliant implementation plans, or when user mentions healthcare tasks, HIPAA implementation plan, medical feature decomposition, or patient data task breakdown.
metadata:
  author: Dau Quang Thanh
  version: "1.0.0"
  last-updated: "2026-03-11"
license: MIT
---

# Healthcare Task Management Skill

## Overview

This skill generates comprehensive implementation task lists (`tasks.md`) from healthcare design artifacts. It extends the generic `task-management` skill with HIPAA-specific phases, ensuring every task breakdown includes mandatory compliance tasks for PHI handling, audit logging, encryption, access controls, and regulatory verification.

## When to Use

- Breaking down healthcare feature specifications into HIPAA-compliant implementation tasks
- Creating implementation roadmaps for medical applications or patient-facing systems
- Generating task lists that explicitly cover PHI protection, audit trails, and consent management
- Planning healthcare feature development with regulatory compliance baked in
- User mentions: "healthcare tasks", "HIPAA implementation plan", "patient data task breakdown", "medical feature decomposition"

**Use this skill instead of generic `task-management` when:**
- The feature handles Protected Health Information (PHI)
- The project is subject to HIPAA, HITECH, FDA, or CMS regulations
- The feature integrates with EHR/EMR systems
- Patient safety or clinical decision support is involved

## Prerequisites

- **Design artifacts in feature directory**:
  - `design.md` (tech stack, libraries, PHI data flows, security controls) — **Required**
  - `spec.md` (user stories with priorities) — **Required**
  - `data-model.md` (entities, PHI fields, retention policies) — Optional
  - `contracts/` (API endpoints, HL7/FHIR schemas) — Optional
  - `research.md` (regulatory decisions) — Optional
  - `quickstart.md` (test scenarios) — Optional
- **Product-level documentation**:
  - `docs/compliance-framework.md` (HIPAA, FDA, CMS requirements) — **Required**
  - `docs/healthcare-ground-rules.md` or `docs/ground-rules.md` — Strongly recommended
  - `docs/healthcare-architecture.md` or `docs/architecture.md` — Optional
  - `docs/e2e-test-plan.md` — Optional (informs test task generation)
- **Tools**: Python 3.6+ for running prerequisite checks

## Instructions

### Step 0: Healthcare Design and Compliance Verification

**⚠️ IMPORTANT: Verify healthcare design artifacts and compliance framework before generating tasks.**

1. **Confirm required documents exist:**
   - `design.md` with PHI data flows, encryption requirements, access control patterns
   - `spec.md` with user stories and HIPAA compliance acceptance criteria
   - `docs/compliance-framework.md` with applicable regulations (HIPAA, HITECH, FDA, CMS)

2. **Check for optional but important documents:**
   - `data-model.md` identifying PHI fields and retention policies
   - `contracts/` with HL7/FHIR API schemas
   - `docs/healthcare-ground-rules.md` for healthcare-specific constraints

3. **Review HIPAA compliance requirements from compliance-framework.md:**
   - Identify which HIPAA safeguards apply (Administrative, Physical, Technical)
   - Note PHI types handled (ePHI, paper PHI, verbal PHI)
   - Identify audit logging requirements
   - Note encryption-at-rest and in-transit requirements
   - Check minimum necessary access principle applications

4. **Only proceed after:**
   - `design.md` and `spec.md` confirmed as complete and reviewed
   - `docs/compliance-framework.md` loaded and applicable rules identified
   - User confirms readiness to generate task breakdown

### Step 1: Check Prerequisites and Get Feature Directory

Run the prerequisite check script to identify the feature directory and available design documents:

```bash
python3 skills/healthcare-task-management/scripts/check-prerequisites.py --json
```

Parse the output to extract:

- `FEATURE_DIR`: Absolute path to feature directory
- `AVAILABLE_DOCS`: List of available design documents
- `COMPLIANCE_FRAMEWORK`: Path to compliance-framework.md (if found)

### Step 2: Load Healthcare Design Documents

Read design artifacts from `FEATURE_DIR` in this order:

1. **docs/compliance-framework.md** (Required — highest authority):
   - Extract applicable HIPAA Technical Safeguards
   - Extract PHI handling requirements
   - Extract audit logging standards
   - Extract encryption requirements (AES-256 at rest, TLS 1.2+ in transit)
   - Extract access control requirements (RBAC, minimum necessary)
   - Extract breach notification requirements

2. **docs/healthcare-ground-rules.md** or **docs/ground-rules.md** (If exists):
   - Extract mandatory project constraints (MUST/SHOULD rules)
   - Note healthcare-specific compliance requirements

3. **design.md** (Required):
   - Extract tech stack and libraries
   - Extract PHI data flows and storage patterns
   - Extract security controls and encryption implementation
   - Extract architectural decisions and patterns

4. **spec.md** (Required):
   - Extract user stories with priorities (P1, P2, P3...)
   - Extract acceptance criteria including HIPAA compliance criteria
   - Note PHI access patterns per user story

5. **docs/architecture.md** or **docs/healthcare-architecture.md** (If exists):
   - Extract architectural patterns
   - Extract deployment and security requirements
   - Extract relevant ADRs for implementation

6. **data-model.md** (If exists):
   - Extract entities and relationships
   - Identify PHI fields requiring encryption and access controls
   - Note data retention and deletion requirements

7. **contracts/** directory (If exists):
   - List all API contract files (HL7, FHIR, REST)
   - Map endpoints to user stories
   - Note authentication/authorization requirements per endpoint

8. **docs/e2e-test-plan.md** (If exists):
   - Extract healthcare E2E test scenarios for each user story
   - Include test implementation tasks with HIPAA validation
   - Map test scenarios to user stories

### Step 3: Generate Healthcare Tasks

Create tasks.md following the healthcare phase structure:

#### Phase Organization

**Phase 1: Setup (Project Initialization)**

- Project structure creation
- Dependency installation with healthcare library versions locked
- Security configuration (secrets management, key management setup)
- Healthcare compliance configuration (audit logger, consent service stubs)

**Phase 2: Foundational (Blocking Healthcare Prerequisites)**

- PHI encryption utilities (field-level encryption, key rotation)
- HIPAA audit logging infrastructure (every PHI access/modification must be logged)
- Authentication and RBAC authorization framework
- Consent management foundation
- MUST complete before any user story — these are non-negotiable HIPAA safeguards

**Phase 3+: User Story Phases (In Priority Order)**

Each user story phase follows this order:
1. Tests (if TDD requested)
2. PHI-aware models/entities (encrypted fields, access tracking)
3. Services/business logic with audit logging hooks
4. Endpoints/UI with authorization checks
5. Integration with EHR/FHIR systems (if applicable)
6. Consent verification per operation

**Final Phase: Compliance Verification & Polish**

- HIPAA Technical Safeguard audit
- Penetration testing preparation (PHI access controls)
- Business Associate Agreement (BAA) documentation tasks
- Breach response procedure documentation
- Security documentation and compliance sign-off

#### Task Format (CRITICAL — Same as task-management)

Every task MUST follow this exact format:

```
- [ ] [TaskID] [P?] [Story?] Action verb + specific component + in precise/file/path.ext
```

**Healthcare-Specific Task Examples:**

- ✅ `- [ ] T004 Implement FieldEncryption utility for PHI fields using AES-256-GCM in src/utils/phi-encryption.ts`
- ✅ `- [ ] T007 Create AuditLogger service that records all PHI access with user/timestamp in src/services/audit-logger.ts`
- ✅ `- [ ] T012 [P] [US1] Create Patient model with encrypted SSN/DOB fields per data-model.md in src/models/patient.ts`
- ✅ `- [ ] T015 [US1] Add HIPAA minimum-necessary access check to GET /patients/:id in src/api/patients.ts`
- ✅ `- [ ] T032 Verify all PHI fields encrypted at rest — audit all Patient, Record, Appointment models`
- ❌ `- [ ] T012 [US1] Create Patient model` (missing encryption requirement, file path, specifics)

#### Mandatory HIPAA Tasks to Include

The following tasks MUST be present in every healthcare feature task breakdown. Insert them in the appropriate phase:

**Foundational Phase (always):**
- Implement PHI field-level encryption utility
- Create HIPAA audit log service (logs: who, what, when, why for every PHI access)
- Implement RBAC authorization middleware
- Create consent management service

**Per User Story (if PHI is accessed):**
- Add audit log call before/after PHI access in service layer
- Verify minimum-necessary principle enforced on each endpoint
- Test that unauthorized roles cannot access PHI

**Final Phase (always):**
- Audit all PHI fields for encryption compliance
- Verify audit log completeness (all PHI access paths covered)
- Test breach detection and notification flow
- Document data flow for BAA compliance

### Step 4: Use the Healthcare Template

Use `templates/healthcare-tasks-template.md` as the structure. Fill in:

1. **Feature name** and PHI types handled
2. **All phases** including mandatory HIPAA phases
3. **Compliance notes** for each phase
4. **Dependencies section** showing story completion order
5. **HIPAA compliance checklist** integrated into task phases

### Step 5: Generate and Commit

1. Write tasks.md to the feature directory
2. Validate AI implementation readiness (same as task-management skill)
3. **Additionally validate HIPAA completeness:**
   - [ ] PHI encryption tasks present in Foundational phase
   - [ ] Audit logging tasks present in Foundational phase
   - [ ] RBAC/authorization tasks in all user story phases that access PHI
   - [ ] Consent verification tasks where applicable
   - [ ] Compliance verification tasks in Final phase
4. Generate commit message: `docs: add HIPAA-compliant implementation tasks for [feature-name]`
5. Commit the tasks.md file

### Step 6: Report Summary

Provide a summary including:

- Path to generated tasks.md
- Total task count (including HIPAA-mandatory tasks)
- PHI types handled (identified from data-model.md)
- HIPAA safeguards covered (list Technical Safeguards addressed)
- Compliance risk items (tasks where HIPAA compliance is critical)
- Suggested MVP scope

## Edge Cases

- **Missing compliance-framework.md**: Stop and ask user to create it — HIPAA tasks cannot be generated without knowing which regulations apply
- **No PHI in the feature**: Note this explicitly, still include audit logging for access tracking as best practice, skip encryption tasks
- **EHR integration**: Add HL7/FHIR-specific tasks in the appropriate user story phase; map to SMART on FHIR if applicable
- **Multi-tenancy with PHI isolation**: Add tenant-scoping tasks to Foundational phase to ensure PHI cannot cross tenant boundaries

## Error Handling

- **Script execution fails**: Report exact error, check working directory and script permissions
- **Missing design artifacts**: List what's missing and what's required vs optional
- **compliance-framework.md not found**: Halt and request creation — cannot generate HIPAA-aware tasks without it
- **PHI fields not identified in data-model.md**: Ask user to explicitly identify which fields contain PHI before proceeding

## Scripts

### Python Script (Cross-Platform)

```bash
python3 skills/healthcare-task-management/scripts/check-prerequisites.py [--json]
```

**Features:**
- Color-coded output for human-readable mode
- JSON output with `--json` flag
- Searches standard locations for feature directories
- Validates required and optional healthcare design documents
- Checks for compliance-framework.md

### Script Output Format

```json
{
  "success": true,
  "feature_dir": "/path/to/specs/feature-name",
  "available_docs": ["design.md", "spec.md", "data-model.md"],
  "missing_required": [],
  "compliance_framework": "/path/to/docs/compliance-framework.md",
  "warning": null
}
```

## Templates

- `templates/healthcare-tasks-template.md`: Structure for HIPAA-aware tasks.md with mandatory compliance phases

## Guidelines

1. **HIPAA First**: Every task breakdown must include the mandatory PHI protection tasks
2. **PHI Identification**: Explicitly identify PHI fields before generating tasks — never assume
3. **Audit Everything**: Every PHI access path must have an audit logging task
4. **Minimum Necessary**: Every endpoint/service accessing PHI needs a minimum-necessary check task
5. **Compliance Verification**: Final phase must include a HIPAA compliance audit task
6. **Reference Framework**: All HIPAA tasks should reference `docs/compliance-framework.md`
7. **No PHI in Logs**: Add a task to verify no PHI appears in application logs (except audit logs)
8. **Encryption Keys**: Include key management tasks if new PHI encryption is introduced

## Related Skills

**Healthcare workflow (use in order):**
1. `healthcare-requirements-specification` → Creates spec.md
2. `healthcare-technical-design` → Creates design.md
3. **`healthcare-task-management`** → Creates tasks.md (this skill)
4. `healthcare-coding` → Implements from tasks.md
5. `code-review` → Validates implementation quality and HIPAA compliance

**Supporting skills:**
- `project-consistency-analysis` — Validate consistency across healthcare artifacts
- `e2e-test-design` — Create E2E test plan with healthcare scenarios before running this skill

## Quality Checklist

- [ ] `docs/compliance-framework.md` loaded and HIPAA rules extracted
- [ ] All PHI types identified from data-model.md
- [ ] Foundational phase includes PHI encryption, audit logging, RBAC tasks
- [ ] Every user story phase accessing PHI has audit log tasks
- [ ] Minimum-necessary access checks included per PHI endpoint
- [ ] Final phase includes HIPAA compliance verification tasks
- [ ] All tasks have sequential IDs, file paths, and action verbs
- [ ] User story tasks have [US#] labels
- [ ] tasks.md committed with `docs:` prefix
