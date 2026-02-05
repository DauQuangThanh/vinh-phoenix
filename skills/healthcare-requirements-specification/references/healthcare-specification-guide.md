# Healthcare Specification Guide

This guide provides detailed guidance for writing high-quality healthcare feature specifications that are compliant with regulatory requirements and focused on patient safety and clinical outcomes.

## Healthcare Specification Principles

### 1. Patient-Centered Design
Healthcare specifications must prioritize patient safety, clinical outcomes, and user experience for healthcare stakeholders (patients, clinicians, administrators).

### 2. Regulatory Compliance First
All healthcare features must comply with HIPAA, FDA regulations, and other applicable healthcare laws. Compliance requirements should be identified early and integrated into all aspects of the specification.

### 3. Clinical Workflow Focus
Specifications should describe clinical processes and workflows, not just technical features. Understanding how clinicians work is essential for successful healthcare software.

## Regulatory Considerations

### HIPAA Privacy Rule
- **Minimum Necessary**: Only access the minimum amount of PHI required for the clinical purpose
- **Patient Consent**: Obtain proper authorization before sharing PHI
- **Business Associate Agreements**: Ensure all vendors comply with HIPAA

### HIPAA Security Rule
- **Technical Safeguards**: Encryption, access controls, audit logging
- **Physical Safeguards**: Secure storage and disposal of medical records
- **Administrative Safeguards**: Policies, procedures, and training

### FDA Classification (if applicable)
- **Class I**: Low risk, general controls
- **Class II**: Moderate risk, special controls
- **Class III**: High risk, premarket approval

## Common Healthcare Specification Patterns

### Patient Portal Features
- Secure authentication with multi-factor authentication
- Granular consent management for data sharing
- Audit logging of all PHI access
- Emergency access procedures for clinical care

### Clinical Documentation
- Structured data entry to reduce errors
- Integration with existing EHR systems
- Real-time validation of clinical data
- Automated quality checks and alerts

### Telemedicine Features
- HIPAA-compliant video platforms
- Secure messaging with encryption
- Integration with clinical workflows
- Emergency escalation procedures

## Detailed Examples

### Example 1: Patient Portal Feature

**Input**: "Add patient portal for viewing medical records"

**Processing**:

1. Short name: `patient-portal`
2. Branch: `1-patient-portal` (no existing branches)
3. Healthcare spec created with clinical workflows, HIPAA requirements, patient scenarios
4. All validations pass including HIPAA compliance

**Output**: Ready for `/phoenix.design`

### Example 2: Telemedicine Feature Requiring Clarification

**Input**: "Add telemedicine consultation feature"

**Processing**:

1. Initial spec created with [NEEDS CLARIFICATION] for video platform choice and licensing
2. User responds with choice
3. Spec updated and re-validated with HIPAA compliance for video data

**Output**: Ready for next phase

## Validation Criteria

### Good Healthcare Specifications
- Include specific HIPAA requirements
- Define clinical workflows clearly
- Include patient safety considerations
- Have measurable clinical outcomes
- Consider integration with existing systems

### Common Issues to Avoid
- Generic "secure" requirements without specifics
- Missing clinical context or workflows
- No consideration of patient safety
- Vague compliance statements
- Technology-specific implementation details

### Examples of Good vs Bad Specifications

#### Good: Patient Record Access
"Clinicians can access patient records with role-based permissions. All access is logged with timestamp, user ID, and purpose. Patients can view their own records but cannot modify them."

#### Bad: Generic Security
"The system should be secure and HIPAA compliant."

#### Good: Clinical Alert
"When a patient's vital signs fall outside normal ranges, the system alerts the care team within 30 seconds and logs the alert in the patient's record."

#### Bad: Vague Alert
"The system should alert users when something is wrong."

## Guidelines

### Focus on Clinical Value and Regulatory Compliance

Healthcare specifications should describe clinical needs, patient safety, and regulatory requirements, not implementation details.

**DO:**

- "Clinicians can access patient records with role-based permissions. All access is logged with timestamp, user ID, and purpose. Patients can view their own records but cannot modify them."
- "System supports 99.9% uptime for critical care monitoring"
- "PHI data is encrypted at rest and in transit"
- "Patient consent is required before sharing medical data"

**DON'T:**

- "Use AES-256 encryption" (implementation detail)
- "Store in PostgreSQL database" (technology choice)
- "Implement with React frontend" (framework-specific)

### Healthcare Success Criteria Requirements

1. **Measurable**: Include specific clinical metrics (response time, accuracy, patient outcomes)
2. **Technology-agnostic**: No frameworks, languages, databases, or tools
3. **Patient-focused**: Outcomes from clinical and patient perspective
4. **Regulatory-compliant**: Include HIPAA and safety requirements
5. **Verifiable**: Can be tested without knowing implementation

### Reasonable Defaults and Clarification Usage in Healthcare

**Reasonable Healthcare Defaults** (don't ask about these):

- HIPAA compliance requirements, data encryption standards
- Patient data retention periods, audit logging
- Standard clinical workflows, emergency procedures

**Use [NEEDS CLARIFICATION] only when**:

- Impact on patient safety or regulatory compliance
- Multiple valid interpretations with different clinical implications
- Fundamental clinical workflow differences
- **Limit**: Maximum 3 clarification markers per healthcare feature

## Quality Checklist Application

Use this checklist to validate healthcare specifications:

- [ ] HIPAA Privacy Rule explicitly addressed
- [ ] HIPAA Security Rule requirements specified
- [ ] Patient safety risks identified and mitigated
- [ ] Clinical workflows clearly defined
- [ ] Success criteria include clinical outcomes
- [ ] Integration requirements specified
- [ ] Edge cases for medical emergencies covered
- [ ] Data retention and disposal procedures defined

## Iteration Strategy

If validation fails, prioritize fixes in this order:

1. **Patient Safety**: Address any safety concerns first
2. **Regulatory Compliance**: Fix HIPAA and other regulatory issues
3. **Clinical Workflow**: Ensure clinical processes are properly supported
4. **Technical Details**: Address remaining technical and usability issues

Maximum 3 iterations allowed. If still failing after 3 iterations, involve clinical stakeholders for review.

## Edge Cases

### Case 1: Branch Already Exists

Find highest existing number and increment. Document relationship in spec.

### Case 2: Empty or Vague Description

Ask clarifying questions about what the healthcare feature should do, who will use it (patients, providers, admins), and what clinical problem it solves.

### Case 3: High-Risk Medical Feature

Require additional safety reviews and clinical validation before proceeding.

### Case 4: Script Execution Fails

Check error output, resolve common issues, or create branch/directories manually.

### Case 5: Too Many Clarification Markers

Prioritize by patient safety and regulatory compliance, keep top 3, make informed guesses for rest. Document assumptions.

## Detailed Specification Creation Process

### Step 5: Create Healthcare Specification

Follow this execution flow to create the healthcare specification:

1. **Parse User Description**
   - Extract from user input
   - If empty, return error: "No healthcare feature description provided"

2. **Extract Healthcare Key Concepts**
   - Identify: healthcare actors (patients, providers, administrators), actions, medical data, compliance constraints
   - Document in appropriate spec sections

3. **Handle Unclear Aspects**
   - **Make informed guesses** based on context, healthcare standards, and regulatory requirements
   - **Only mark with [NEEDS CLARIFICATION: specific question]** if:
     - Choice significantly impacts patient safety or regulatory compliance
     - Multiple reasonable interpretations exist with different compliance implications
     - No reasonable default exists in healthcare context
   - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
   - **Priority**: patient safety > regulatory compliance > HIPAA/privacy > user experience > technical details

4. **Fill Healthcare Scenarios & Testing**
   - Define clinical workflows and user flows
   - Create acceptance scenarios covering normal and edge cases
   - If no clear healthcare workflow, return error: "Cannot determine clinical workflows"

5. **Generate Healthcare Functional Requirements**
   - Each requirement must be testable and HIPAA-compliant
   - Use reasonable healthcare defaults for unspecified details
   - Document assumptions in Assumptions section
   - Include patient safety and data privacy requirements

6. **Define Success Criteria**
   - Create measurable, technology-agnostic outcomes
   - Include quantitative metrics (response time, uptime, data accuracy)
   - Include qualitative measures (patient satisfaction, clinical outcomes)
   - Include regulatory compliance metrics
   - Each criterion must be verifiable without implementation details

7. **Identify Key Healthcare Entities** (if medical data involved)
   - Patient demographics, medical records, PHI data
   - Clinical workflows, care coordination
   - Regulatory reporting requirements

The script creates the initial healthcare spec file from `templates/healthcare-spec-template.md`. Now enhance it:

1. The template is already copied to SPEC_FILE by the script
2. Replace placeholders with concrete healthcare details from feature description
3. Preserve section order and headings
4. Ensure consistency with healthcare-architecture.md, healthcare-standards.md, and compliance-framework.md (if they exist in workspace)
5. Fill in all mandatory sections with healthcare focus
6. Preserve section order and headings
7. Ensure consistency with healthcare-architecture.md, healthcare-standards.md

**Healthcare Section Requirements:**

- **Mandatory sections**: Must be completed for every healthcare feature
- **Optional sections**: Include only when relevant
- **When section doesn't apply**: Remove it entirely (don't leave as "N/A")</content>
<parameter name="filePath">/Users/thanhdq.coe/97-vinh-phoenix/vinh-phoenix/skills/healthcare-requirements-specification/references/healthcare-specification-guide.md