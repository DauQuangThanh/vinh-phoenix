---
name: healthcare-technical-design
description: Executes implementation planning workflow for healthcare systems to generate technical design artifacts including HIPAA-compliant design documents, patient data privacy considerations, medical regulatory requirements, data models, and API contracts. Use when creating healthcare technical designs, planning medical feature implementation, designing healthcare system components, ensuring regulatory compliance in technical design, or when user mentions healthcare technical design, medical system design, HIPAA technical design, patient data design, healthcare API design, or medical data modeling.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.0"
  last_updated: "2026-02-05"
---

# Healthcare Technical Design Skill

## Overview

This skill guides you through a structured implementation planning workflow specifically for healthcare systems, creating comprehensive technical design artifacts that ensure HIPAA compliance, patient data privacy, and adherence to medical regulatory requirements. It follows a phased approach from healthcare-specific research through design to contract generation, ensuring all technical decisions are documented, compliant with healthcare standards, and aligned with medical system architecture.

## When to Use

- Planning implementation for new healthcare features or medical components
- Creating technical specifications and design documents for healthcare systems
- Designing HIPAA-compliant data models and API contracts for patient data
- Researching healthcare technical decisions and regulatory requirements
- Aligning medical feature design with existing healthcare architecture
- Documenting implementation approaches for healthcare applications
- Ensuring compliance with HIPAA, FDA, CMS, and other healthcare regulations
- When user requests "design healthcare feature", "create medical technical plan", "plan healthcare implementation", "design HIPAA-compliant API", or "design patient data system"

**Next Steps After Creating Healthcare Technical Design:**

- Use `task-management` skill to create task breakdown (tasks.md)
- Use `e2e-test-design` skill for end-to-end test planning with healthcare scenarios
- Use `coding` skill to execute implementation following healthcare coding standards
- Use `bug-analysis` skill if issues are discovered during development
- Use `healthcare-requirements-specification` skill if requirements need refinement

## Prerequisites

**Required:**

- Healthcare feature specification or requirements document available (preferably created with healthcare-requirements-specification skill)
- Templates provided with this skill (in `templates/` directory)
- Git repository with feature branch (format: `N-feature-name`, e.g., `1-patient-portal`)
- Feature directory at `specs/N-feature-name/` with `spec.md` file
- Compliance framework document (`docs/compliance-framework.md`) for HIPAA and regulatory requirements

**Optional (workspace-level enhancements):**

- `docs/healthcare-ground-rules.md` - Healthcare project constraints and standards
- `docs/healthcare-architecture.md` - Healthcare architectural decisions and patterns
- `docs/healthcare-standards.md` - Medical data standards and interoperability requirements

**Important:** Healthcare technical design must be done on a feature branch. The design artifacts will be created in `specs/N-feature-name/` directory and must comply with healthcare regulations.

## Instructions

### Step 0: Healthcare Specification and Compliance Verification

**⚠️ IMPORTANT: Always request healthcare specification documents and verify compliance requirements before starting technical design.**

1. **Request healthcare specification documents:**
   - Ask the user to provide healthcare feature specifications, medical requirements documents, or clinical workflows
   - Request any relevant healthcare documentation: feature specs, HIPAA requirements, clinical workflows, regulatory constraints, or medical design specifications
   - If no formal documentation exists, ask the user to describe:
     - The healthcare feature or medical component to be designed
     - Patient workflows and clinical interactions
     - Protected Health Information (PHI) handling requirements
     - HIPAA Security Rule and Privacy Rule compliance needs
     - Integration with Electronic Health Records (EHR) systems
     - Medical device or FDA-regulated software requirements
     - Patient safety and clinical decision support needs

2. **Verify healthcare compliance framework exists:**
   - Check if `docs/compliance-framework.md` exists (for HIPAA, FDA, CMS requirements)
   - Check if `docs/healthcare-standards.md` exists (for medical data standards)
   - If missing, note that design may need additional healthcare compliance guidance

3. **Review and confirm understanding:**
   - Summarize the healthcare requirements back to the user
   - Clarify any ambiguities or missing medical details
   - Confirm the scope and expected healthcare technical design deliverables
   - Identify what needs to be designed (PHI data models, HIPAA-compliant APIs, medical workflows)

4. **Only proceed to Step 1 after:**
   - Healthcare specification documents are provided and reviewed
   - Compliance requirements are clearly understood
   - User confirms readiness to start healthcare technical design

### Step 1: Setup and Healthcare Context Loading

1. **Create healthcare design directory structure** manually or using the following commands:

   **Manual Directory Creation:**

   ```bash
   mkdir -p specs/N-feature-name/design
   mkdir -p specs/N-feature-name/research
   mkdir -p specs/N-feature-name/compliance
   mkdir -p specs/N-feature-name/data-models
   mkdir -p specs/N-feature-name/api-contracts
   mkdir -p specs/N-feature-name/implementation
   mkdir -p specs/N-feature-name/testing
   mkdir -p specs/N-feature-name/documentation
   ```

   Replace `N-feature-name` with your actual feature branch name (e.g., `1-patient-portal`).

2. **Copy healthcare-specific templates** to the design directory:

   ```bash
   cp skills/healthcare-technical-design/templates/healthcare-design-template.md specs/N-feature-name/design/design-document.md
   cp skills/healthcare-technical-design/templates/healthcare-research-template.md specs/N-feature-name/research/research-findings.md
   cp skills/healthcare-technical-design/templates/healthcare-data-model-template.md specs/N-feature-name/data-models/data-model.md
   cp skills/healthcare-technical-design/templates/healthcare-api-contract-template.md specs/N-feature-name/api-contracts/api-contract.md
   cp skills/healthcare-technical-design/templates/healthcare-compliance-check-template.md specs/N-feature-name/compliance/compliance-checklist.md
   cp skills/healthcare-technical-design/templates/healthcare-quickstart-template.md specs/N-feature-name/implementation/quickstart-guide.md
   ```

3. **Load required healthcare context**:
   - Read healthcare feature specification/requirements from `specs/N-feature-name/spec.md`
   - Load `docs/healthcare-ground-rules.md` if exists (optional - for healthcare standards)
   - Load `docs/healthcare-architecture.md` if exists (optional - for healthcare patterns)
   - Load `docs/compliance-framework.md` (required - for HIPAA and regulatory requirements)
   - Note current git branch: `N-feature-name`

4. **Review healthcare design document template**:
   - Template copied to `specs/N-feature-name/design/design-document.md`
   - Review healthcare-specific structure and sections
   - Begin filling in feature name and basic healthcare context

### Step 2: Healthcare Technical Context Analysis

1. **Extract key healthcare information from requirements**:
   - Functional requirements (clinical workflows, patient interactions)
   - Non-functional requirements (HIPAA compliance, patient safety, performance)
   - PHI data handling and privacy requirements
   - Regulatory compliance needs (HIPAA, FDA, CMS)
   - Medical device integration requirements
   - Clinical decision support needs

2. **Document in design.md Healthcare Technical Context section**:
   - List all known healthcare technical details
   - Mark unknowns as "NEEDS CLARIFICATION"
   - Reference healthcare ground-rules that apply
   - Note healthcare architectural patterns from healthcare-architecture.md (if available)
   - Document PHI data elements and privacy requirements

3. **Evaluate against healthcare compliance framework**:
   - Check HIPAA Security Rule compliance (technical safeguards)
   - Check HIPAA Privacy Rule compliance (data usage and disclosure)
   - Document any conflicts or exceptions needed
   - Justify deviations if necessary with clinical rationale

### Step 3: Phase 0 - Healthcare Research & Regulatory Resolution

**Goal**: Resolve all NEEDS CLARIFICATION items and ensure regulatory compliance before proceeding to design

1. **Identify healthcare research tasks from Technical Context**:
   - For each NEEDS CLARIFICATION → create healthcare research question
   - For each technology choice → identify HIPAA-compliant best practices
   - For each PHI handling requirement → research privacy protection patterns
   - For each medical integration → research healthcare interoperability standards (HL7, FHIR)
   - Review healthcare-architecture.md for relevant medical decisions and patterns

2. **Conduct healthcare research and document findings**:
   - Research template copied to `specs/N-feature-name/research/research-findings.md`
   - Template structure provided in `templates/healthcare-research-template.md`
   - For each healthcare decision, document:
     - **Decision**: What was chosen for healthcare context
     - **Rationale**: Why it was chosen considering patient safety and compliance
     - **HIPAA Impact**: How it affects PHI protection and privacy
     - **Regulatory Alignment**: Compliance with FDA, CMS, or other regulations
     - **Alternatives Considered**: What else was evaluated for healthcare use
     - **Architecture Alignment**: How it aligns with existing healthcare architecture
     - **Clinical Safety**: Impact on patient safety and clinical workflows
     - **Trade-offs**: Pros and cons in healthcare context
     - **References**: Healthcare standards and regulatory sources consulted

3. **Update design.md with healthcare research outcomes**:
   - Replace all NEEDS CLARIFICATION with concrete healthcare decisions
   - Link to research.md for regulatory and clinical details

### Step 4: Phase 1 - Healthcare Data Model Design

**Prerequisites**: All NEEDS CLARIFICATION resolved in Phase 0

1. **Extract healthcare entities from requirements**:
   - Identify medical domain objects (Patient, Provider, Encounter, Medication)
   - List PHI and non-PHI attributes for each entity
   - Define relationships considering HIPAA privacy rules
   - Identify clinical state transitions and workflow states

2. **Create healthcare data model document**:
   - Data model template copied to `specs/N-feature-name/data-models/data-model.md`
   - Template structure provided in `templates/healthcare-data-model-template.md`
   - For each healthcare entity document:
     - Entity name and clinical description
     - PHI classification and privacy level
     - Fields with types, constraints, and HIPAA considerations
     - Validation rules for medical data integrity
     - Relationships to other entities (considering access controls)
     - Clinical state machine (if applicable)
     - Audit trail requirements for PHI access
   - Align with medical data models from healthcare-architecture.md (if available)

3. **Add healthcare-specific diagrams** (if helpful):
   - Entity-relationship diagrams with PHI markings
   - Clinical workflow diagrams
   - Data flow diagrams showing PHI protection
   - Audit and access control diagrams

### Step 5: Phase 1 - HIPAA-Compliant API Contract Generation

1. **Identify healthcare API endpoints from requirements**:
   - For each clinical user action → determine HIPAA-compliant endpoint
   - For each PHI data query → determine access-controlled read endpoint
   - For each medical data mutation → determine audited write endpoint
   - Consider role-based access control (RBAC) for healthcare providers

2. **Design HIPAA-compliant API contracts**:
   - API contract template copied to `specs/N-feature-name/api-contracts/api-contract.md`
   - Template structure provided in `templates/healthcare-api-contract-template.md`
   - Create additional contract files in contracts directory as needed
   - Follow healthcare interoperability standards (FHIR, HL7)
   - Include:
     - Endpoint path/operation with clinical context
     - HTTP method / FHIR resource type
     - Request schema with PHI markings
     - Response schema with privacy considerations
     - Error responses following healthcare standards
     - Authentication and authorization requirements
     - Audit logging requirements for PHI access
   - Follow API design patterns from healthcare-architecture.md (if available)

3. **Generate healthcare-standard schemas**:
   - Create FHIR resources or HL7 messages where applicable
   - Validate schema syntax against healthcare standards
   - Add clinical examples for each endpoint
   - Include privacy metadata and consent handling

### Step 6: Create Healthcare Implementation Quickstart Guide

1. **Document healthcare implementation approach**:
   - Create quickstart file at `specs/N-feature-name/implementation/quickstart-guide.md`
   - Include:
     - High-level implementation steps for healthcare context
     - HIPAA-compliant technology stack for this medical feature
     - Key files/modules to create/modify with security considerations
     - Healthcare integration points and interoperability requirements
     - PHI data handling and privacy protection strategies
     - Testing strategy including penetration testing and HIPAA validation
     - Deployment considerations for medical environments
     - Clinical safety and validation procedures

2. **Add healthcare code examples**:
   - Show HIPAA-compliant code patterns
   - Provide PHI handling and encryption examples
   - Reference healthcare design decisions from research.md
   - Include audit logging and access control examples

### Step 7: Healthcare Compliance Validation

1. **Review against healthcare compliance framework**:
   - Re-check all HIPAA Security Rule requirements (technical safeguards)
   - Re-check all HIPAA Privacy Rule requirements (data usage limitations)
   - Update Compliance Check section in design.md
   - Document any approved exceptions with clinical justification

2. **Verify healthcare completeness**:
   - All medical requirements addressed in design
   - All PHI entities have appropriate data models with privacy controls
   - All clinical actions have HIPAA-compliant API contracts
   - All NEEDS CLARIFICATION resolved with regulatory consideration
   - Healthcare architecture alignment verified (if healthcare-architecture.md exists)
   - Clinical safety and patient privacy measures documented

3. **Create healthcare summary**:
   - Update design.md Executive Summary with healthcare focus
   - List all generated artifacts with compliance status
   - Document next steps (implementation, security review, clinical validation)

### Step 8: Commit Healthcare Design Artifacts

1. **Stage all healthcare design files** (replace N-feature-name with actual feature branch name):

   ```bash
   git add specs/N-feature-name/design.md
   git add specs/N-feature-name/research/research.md
   git add specs/N-feature-name/data-model.md
   git add specs/N-feature-name/contracts/
   git add specs/N-feature-name/quickstart.md
   git add specs/N-feature-name/compliance-check.md
   ```

2. **Create commit with 'feat:' prefix**:

   ```bash
   git commit -m "feat: add HIPAA-compliant technical design for N-feature-name"
   ```

3. **Report completion**:
   - List all generated artifacts with paths
   - Confirm HIPAA compliance status
   - Confirm commit completed
   - Note current branch
   - Suggest next steps (security review, clinical validation, task breakdown)

## Examples

### Example 1: Patient Portal Authentication

**Input**:

```
Design HIPAA-compliant patient portal authentication with multi-factor authentication
```

**Process**:

1. Create design/design.md from healthcare template
2. Healthcare Technical Context identifies: PHI access controls, authentication strength, audit logging
3. Research.md documents: HIPAA authentication requirements, MFA for medical data, OAuth2 for healthcare
4. data-model.md defines: Patient entity with PHI, AuthenticationLog entity, access control relationships
5. contracts/ includes: POST /auth/patient-login, POST /auth/mfa-verify, GET /auth/patient-session
6. quickstart.md outlines: MFA implementation, PHI encryption, audit trail setup

**Output**: Complete HIPAA-compliant design package in specs/N-feature-name/ directory, committed to git

### Example 2: EHR Medication Management Integration

**Input**:

```
Integrate medication management with hospital EHR system using FHIR
```

**Process**:

1. Load compliance-framework.md for HIPAA requirements
2. Healthcare Technical Context: FHIR Medication resources, PHI in medication data, clinical safety
3. Research: FHIR medication profiles, EHR integration patterns, medication reconciliation workflows
4. Data model: Medication, Prescription, Administration entities with clinical relationships
5. Contracts: FHIR MedicationRequest, MedicationAdministration resources with privacy headers
6. Quickstart: FHIR client setup, medication safety checks, integration testing procedures

**Output**: FHIR-compliant medication management design, aligned with clinical safety standards, ready for implementation

## Edge Cases

### Missing Compliance Framework

- **Case**: Project doesn't have compliance-framework.md
- **Handling**: Stop process, require compliance framework creation first using project-ground-rules-setup skill

### PHI Data Classification Conflicts

- **Case**: Requirements conflict with PHI classification rules
- **Handling**: Document conflict in design.md, consult compliance officer, propose alternative design

### Incomplete Medical Requirements

- **Case**: Healthcare spec lacks critical clinical details
- **Handling**: Add to NEEDS CLARIFICATION, create research tasks to fill medical gaps, document clinical assumptions

### Third-Party Healthcare API Dependencies

- **Case**: Feature depends on external healthcare API (EHR, pharmacy, insurance)
- **Handling**: Research API thoroughly, document HIPAA Business Associate Agreement requirements, include fallback strategies

### Complex Clinical Workflows

- **Case**: Medical process has many clinical states and decision points
- **Handling**: Create detailed clinical workflow diagram in data-model.md, document all valid transitions, include error recovery states

## Error Handling

### Healthcare Research Incomplete

- **Error**: NEEDS CLARIFICATION items remain after healthcare research phase
- **Action**: Return to research phase, conduct deeper clinical investigation, consult medical experts if needed

### HIPAA Compliance Violation

- **Error**: Design conflicts with mandatory HIPAA requirements
- **Action**: Stop design process, document violation, revise design to comply or get regulatory approval

### Missing Healthcare Prerequisites

- **Error**: Required healthcare context files (feature spec, compliance-framework.md) not found
- **Action**: Report missing files, request user to provide or create them first

### Invalid Healthcare API Contract

- **Error**: Generated FHIR/HL7 schema has validation errors
- **Action**: Review contract structure, fix schema syntax, validate against healthcare standards

### Incomplete PHI Data Model

- **Error**: Healthcare entities missing privacy controls or audit requirements
- **Action**: Review HIPAA requirements again, add missing PHI protection details, ensure all clinical data interactions documented

## Guidelines

1. **Always use absolute paths** when referencing files
2. **ERROR and stop** if HIPAA violations cannot be justified
3. **Document all healthcare decisions** with clinical rationale in research.md
4. **Align with healthcare architecture** when healthcare-architecture.md exists
5. **Generate complete HIPAA-compliant contracts** - don't leave TODOs in medical API specifications
6. **Validate schemas** against healthcare standards before committing
7. **Use healthcare templates provided** in templates/ directory for consistency
8. **Commit with 'feat:' prefix** for healthcare design documentation
9. **Mark medical unknowns clearly** with "NEEDS CLARIFICATION" during initial analysis
10. **Resolve all clarifications** with regulatory consultation before moving to design phase

## Quality Checklist

- [ ] **Healthcare Prerequisites Met**: Feature spec exists, compliance framework available, git repo initialized, on feature branch
- [ ] **Healthcare Templates Used**: All required healthcare-specific templates copied and populated
- [ ] **Healthcare Research Complete**: All NEEDS CLARIFICATION items resolved with documented clinical decisions
- [ ] **PHI Data Models Defined**: All healthcare entities documented with PHI classification, privacy controls, and audit requirements
- [ ] **HIPAA-Compliant API Contracts**: All endpoints specified with PHI protection and access controls
- [ ] **Healthcare Compliance Verified**: Design aligns with HIPAA, FDA, and medical standards
- [ ] **Healthcare Schemas Valid**: FHIR/HL7 schemas validate against medical standards
- [ ] **PHI Protection Implemented**: All patient data handling includes appropriate privacy and security measures
- [ ] **Clinical Safety Considered**: Design includes patient safety and clinical workflow validation
- [ ] **Artifacts Committed**: All healthcare design files committed with proper commit message
- [ ] **Healthcare Review Recommended**: Consider technical-detailed-design-review skill for validation

## Tips

- **Start with Compliance**: Always verify HIPAA requirements first
- **Document PHI Carefully**: Clearly mark and protect all Protected Health Information
- **Clinical Safety First**: Design with patient safety as the primary concern
- **Reference Healthcare Standards**: Always check healthcare-architecture.md and compliance-framework.md
- **Validate Clinically**: Test designs against real clinical workflows early
- **Keep Medical Data Secure**: Implement defense-in-depth for PHI protection
- **Consider Interoperability**: Design for healthcare data exchange standards
- **Plan for Audits**: Include comprehensive audit trails for all PHI access
- **Version Healthcare APIs**: Plan for medical API evolution with backward compatibility
- **Automate Healthcare Setup**: Use the provided Python script for consistent healthcare design setup

## Additional Resources

- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/guidance/index.html) - Technical safeguards for PHI
- [HIPAA Privacy Rule](https://www.hhs.gov/hipaa/for-professionals/privacy/index.html) - PHI usage and disclosure rules
- [FHIR Specification](https://www.hl7.org/fhir/) - Healthcare interoperability standard
- [HL7 Standards](https://www.hl7.org/) - Health Level Seven data exchange standards
- [FDA Software Validation](https://www.fda.gov/medical-devices/digital-health/software-validation-medical-devices) - Medical software validation guidelines
- [Clinical Decision Support](https://www.healthit.gov/topic/safety/clinical-decision-support) - CDS implementation guidance

## Next Steps After Healthcare Design

After completing the healthcare technical design, consider these follow-up actions:

1. **Security Review**: Conduct HIPAA security assessment and penetration testing
2. **Clinical Validation**: Have medical experts review clinical workflows and safety measures
3. **Task Breakdown**: Use phoenix.taskify agent to break design into implementation tasks
4. **Checklist Creation**: Use phoenix.checklist agent to create HIPAA compliance checklist
5. **E2E Test Design**: Use phoenix.design-e2e-test agent to design healthcare end-to-end tests
6. **Implementation**: Begin implementing according to quickstart.md following healthcare coding standards
