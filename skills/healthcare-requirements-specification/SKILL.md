---
name: healthcare-requirements-specification
description: Creates or updates feature specifications from natural language descriptions in healthcare domain, ensuring compliance with HIPAA, patient data privacy, and medical regulations. Use when creating healthcare features, documenting medical requirements, ensuring regulatory compliance, or when user mentions healthcare specs, medical features, patient data, or HIPAA.
metadata:
  author: Dau Quang Thanh
  version: "1.1"
  last_updated: "2026-02-05"
license: MIT
---

# Healthcare Requirements Specification

## Overview

This skill creates or updates feature specifications from natural language descriptions in the healthcare domain, generating structured documentation with testable requirements, user stories, and acceptance criteria. It validates specification quality and ensures requirements are unambiguous, compliant with healthcare regulations (HIPAA, FDA, CMS), and focused on patient safety and data privacy.

## When to Use

Use this skill when:

- Creating a new healthcare feature specification from a user description
- Converting natural language requirements into structured healthcare specifications
- Documenting medical product requirements for stakeholders
- Validating specification quality and regulatory compliance
- Ensuring requirements are testable and HIPAA-compliant
- User mentions: healthcare specs, medical features, patient data, HIPAA, clinical workflows, EHR integration

**Next Steps After Creating Specifications:**

- Use `coding-standards` skill to establish product-level coding conventions
- Use `architecture-design` skill for system architecture documentation
- Use `technical-detailed-design` skill for feature-level implementation planning

## Prerequisites

**Required Tools:**

- Git (for branch management)
- Bash or PowerShell (for running scripts)
- Python 3.6+ (recommended for cross-platform compatibility)

**Required Files:**

- `templates/healthcare-spec-template.md` and `templates/healthcare-checklist-template.md`
- Scripts in `scripts/` directory

**Optional Context Files:**

- `docs/healthcare-architecture.md`, `docs/healthcare-standards.md`, `docs/compliance-framework.md`

## Instructions

### Step 0: Ground Rules and Compliance Verification

**⚠️ IMPORTANT: Always verify ground rules and compliance requirements exist before creating healthcare feature specifications.**

1. **Check for ground rules document:**
   - Look for `docs/ground-rules.md` in the workspace
   - Ground rules define project principles, constraints, and standards
   - These are essential for creating aligned specifications

2. **Check for compliance framework:**
   - Look for `docs/compliance-framework.md` in the workspace
   - Compliance framework defines HIPAA requirements, data privacy rules, and regulatory standards
   - Critical for healthcare specifications

3. **If ground rules or compliance framework are missing:**
   - **STOP** and inform the user: "Ground rules document and/or compliance framework not found"
   - Recommend: "Please set up project ground rules and compliance framework first"
   - Ask: "Would you like me to help set up these documents before creating this specification?"
   - Wait for user decision:
     - If user wants to set up → guide them to use `project-ground-rules-setup` skill
     - If user wants to proceed anyway → ask for confirmation and document this decision
     - If unsure → explain the importance of compliance in healthcare

4. **If documents exist:**
   - Read and review `docs/ground-rules.md` and `docs/compliance-framework.md`
   - Extract key principles, HIPAA requirements, and regulatory constraints
   - Note any relevant healthcare standards or conventions
   - Use these to guide specification creation

5. **Only proceed to Step 1 after:**
   - Ground rules and compliance framework are reviewed (if they exist), OR
   - User explicitly confirms to proceed without them (with understanding of risks)

### Step 1: Extract Healthcare Feature Short Name

Analyze the healthcare feature description and generate a concise short name (2-4 words):

1. **Extract meaningful healthcare keywords** from the description
2. **Use action-noun format** when possible (e.g., "add-patient-portal", "secure-phi-access")
3. **Preserve medical terms** and acronyms (PHI, EHR, HIPAA, FDA, etc.)
4. **Keep it descriptive** but concise enough to understand at a glance

**Examples:**

- "Add patient appointment scheduling" → `patient-appointment-scheduling`
- "Implement HIPAA-compliant messaging" → `hipaa-secure-messaging`
- "Create EHR integration for labs" → `ehr-lab-integration`
- "Fix PHI data breach vulnerability" → `phi-security-fix`

### Step 2: Check for Existing Branches

Before creating a new branch, find the highest healthcare feature number for this short name:

```bash
# Fetch all remote branches
git fetch --all --prune

# Find highest number across all sources
# Remote branches
git ls-remote --heads origin | grep -E "refs/heads/[0-9]+-<short-name>$"

# Local branches
git branch | grep -E "^[* ]*[0-9]+-<short-name>$"

# Specs directories
ls -d specs/[0-9]*-<short-name> 2>/dev/null || true
```

**Determine next number:**

- Extract all numbers from all three sources
- Find the highest number N
- Use N+1 for the new branch number
- If no existing branches/directories found, start with number 1

### Step 3: Run Healthcare Feature Creation Script

Execute the appropriate script with the calculated number and short-name:

**Bash:**

```bash
<SKILL_DIR>/scripts/create-healthcare-feature.sh --json --number <N+1> --short-name "<short-name>" "<healthcare feature description>"
```

**PowerShell:**

```powershell
<SKILL_DIR>/scripts/create-healthcare-feature.ps1 -Json -Number <N+1> -ShortName "<short-name>" "<healthcare feature description>"
```

**Python 3 (Cross-platform):**

```bash
python3 <SKILL_DIR>/scripts/create-healthcare-feature.py --json --number <N+1> --short-name "<short-name>" "<healthcare feature description>"
```

Replace `<SKILL_DIR>` with the absolute path to this skill directory.

**Important Notes:**

- Only run this script once per healthcare feature
- The JSON output contains BRANCH_NAME and SPEC_FILE paths
- For single quotes in args, use escape syntax: `'I'\''m Groot'` or use double quotes: `"I'm Groot"`
- The script creates and checks out the branch (Optional)

If available in the workspace, load healthcare-specific context to ensure alignment:

1. **Read `docs/healthcare-architecture.md`** (if exists):
   - Understand healthcare technology stack (EHR systems, HL7, FHIR)
   - Review healthcare architectural patterns
   - Note compliance requirements

2. **Read `docs/healthcare-standards.md`** (if exists):
   - Understand healthcare naming conventions
   - Review healthcare coding standards
   - Note medical terminology standards

3. **Read `docs/compliance-framework.md`** (if exists):
   - Understand HIPAA requirements
   - Review data privacy rules
   - Note regulatory compliance standards

**Note**: This step is optional. The skill works independently without these files.

### Step 5: Create Healthcare Specification

Parse the healthcare feature description and create a structured specification using the healthcare spec template. For detailed guidance on specification creation, parsing requirements, handling clarifications, and filling healthcare scenarios, see [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md).

**Key Activities:**

- Parse user description and extract healthcare concepts
- Handle unclear aspects with limited clarification markers (max 3)
- Generate testable, HIPAA-compliant functional requirements
- Define measurable success criteria with clinical outcomes
- Identify key healthcare entities and regulatory requirements

The script creates the initial spec file from `templates/healthcare-spec-template.md` and enhances it with healthcare-specific details.

### Step 7: Validate Healthcare Specification Quality

Create and use a quality checklist to validate the healthcare specification. For detailed validation criteria and examples, see [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md).

#### 7a. Create Healthcare Spec Quality Checklist

Generate a checklist file at `<FEATURE_DIR>/checklists/healthcare-requirements.md`:

```markdown
# Healthcare Specification Quality Checklist: [FEATURE NAME]

**Purpose**: Validate healthcare specification completeness, quality, and compliance before proceeding to planning
**Created**: [DATE]
**Feature**: [Link to spec.md]

## Healthcare Content Quality

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on patient value and clinical outcomes
- [ ] Written for healthcare stakeholders (clinicians, administrators, patients)
- [ ] All mandatory sections completed
- [ ] HIPAA compliance requirements identified
- [ ] Patient safety considerations included

## Regulatory Compliance

- [ ] HIPAA Privacy Rule requirements addressed
- [ ] HIPAA Security Rule requirements addressed
- [ ] Patient data privacy (PHI) protections specified
- [ ] Data retention and disposal requirements defined
- [ ] Audit logging and access controls specified
- [ ] Breach notification procedures outlined

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable and include clinical outcomes
- [ ] Success criteria are technology-agnostic
- [ ] All clinical scenarios are defined
- [ ] Edge cases including medical emergencies identified
- [ ] Scope is clearly bounded with clinical constraints
- [ ] Dependencies and assumptions identified

## Patient Safety & Clinical Quality

- [ ] Patient safety requirements explicitly stated
- [ ] Clinical workflow disruptions minimized
- [ ] Error handling for medical data specified
- [ ] Backup and recovery procedures for critical data
- [ ] Integration with existing healthcare systems considered

## Feature Readiness

- [ ] All functional requirements have clear acceptance criteria
- [ ] Clinical user scenarios cover primary workflows
- [ ] Feature meets measurable clinical outcomes defined in Success Criteria
- [ ] Regulatory compliance requirements are met
- [ ] No implementation details leak into specification

## Notes

- Items marked incomplete require spec updates before next phase
- Healthcare specifications must pass compliance review before implementation
```

#### 7b. Run Validation Check

Review the healthcare spec against each checklist item. See [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md) for detailed validation criteria, common failures, and fix strategies.

#### 7c. Handle Validation Results

**If all items pass:** Mark checklist complete and proceed to final commit.

**If items fail:** Update spec to address issues, re-run validation (max 3 iterations). See [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md) for iteration strategy.

**If [NEEDS CLARIFICATION] markers remain:** Present clarification questions to user (max 3). See [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md) for question format.

#### 7d. Update Checklist

After each validation iteration, update the checklist file with current pass/fail status.

### Step 8: Commit Healthcare Specification

Generate a 'docs:' prefixed git commit message and commit:

```bash
git add <SPEC_FILE> <CHECKLIST_FILE>
git commit -m "docs: add healthcare specification for <feature-name>"
```

### Step 9: Report Completion

Report to user with:

- Branch name
- Spec file path
- Checklist results summary
- Readiness for next phase (`/phoenix.clarify`, `/phoenix.architect`, or `/phoenix.design`)

### Step 10: Quality Review (Recommended)

**After completing the healthcare specification, it's highly recommended to run a quality review:**

1. **Run the requirements-specification-review skill** to validate:
   - Completeness of all sections
   - Consistency with ground rules and healthcare architecture
   - Testability of requirements
   - Clarity and lack of ambiguity
   - Proper acceptance criteria

2. **Address any findings** from the review before proceeding to technical design

3. **If issues found**, update the specification and repeat validation

**Next Steps:**

- If review passes, proceed to architecture (if new healthcare product) or technical design (if adding feature)
- Use `architecture-design` skill for new healthcare product architecture
- Use `technical-detailed-design` skill for healthcare feature implementation planning

## Examples

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

See [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md) for detailed examples of good vs bad healthcare specifications.

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

See [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md) for detailed edge case handling.

## Guidelines

### Focus on Clinical Value and Regulatory Compliance

Healthcare specifications should describe clinical needs, patient safety, and regulatory requirements, not implementation details. See [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md) for detailed examples and comprehensive guidelines.

**Key Principles:**

- Prioritize patient safety and HIPAA compliance
- Include measurable clinical outcomes in success criteria
- Use reasonable healthcare defaults for standard requirements
- Limit clarification markers to maximum 3 per feature

## Error Handling

Common errors and resolutions:

- **"No healthcare feature description provided"**: Prompt user for description
- **"Cannot determine clinical workflows"**: Ask about users and clinical processes
- **"Compliance framework not found"**: Recommend setup, explain HIPAA requirements
- **"Template file not found"**: Check templates folder or use generic structure
- **"Script execution failed"**: Resolve git/config issues or create manually
- **"Validation failed after 3 iterations"**: Document issues, suggest manual review

## Scripts

This skill includes cross-platform scripts for healthcare feature creation:

**Python 3 (Cross-platform):**

```bash
python3 skills/healthcare-requirements-specification/scripts/create-healthcare-feature.py --number 5 --short-name "patient-portal" "Add HIPAA-compliant patient portal"
```

All scripts create Git branches, generate healthcare specs from templates, and provide JSON/human-readable output.

Optional workspace files (if available):

- `docs/architecture.md` - Healthcare technology stack and architectural patterns
- `docs/standards.md` - Healthcare naming conventions and coding standards
- `docs/compliance-framework.md` - HIPAA and regulatory compliance requirements

**Self-Contained**: This skill includes all necessary healthcare templates and scripts - no external dependencies required
**Cross-Platform**: Provides both Bash (macOS/Linux), PowerShell (Windows), and Python 3 (all platforms) scripts for maximum compatibility
**Progressive Disclosure**: Loads minimal context initially and fetches additional healthcare details only when needed
**Healthcare-Focused**: Specifications describe clinical needs, patient safety, and regulatory compliance, not implementation details
**Compliance-First**: HIPAA and regulatory validation ensures healthcare specifications are compliant before proceeding
**Patient-Centered**: All requirements and success criteria must be verifiable from a clinical/patient perspective
**Portable**: Can be used in any healthcare project - workspace-level healthcare architecture/standards files are optional enhancements

## Quality Checklist

Before considering healthcare specification complete:

- [ ] Ground rules and compliance framework reviewed
- [ ] Healthcare feature description parsed and clinical concepts extracted
- [ ] Short name and branch number validated
- [ ] Git branch and spec directory created
- [ ] Healthcare spec and checklist templates used
- [ ] Functional requirements, scenarios, and success criteria defined
- [ ] HIPAA compliance and patient safety addressed
- [ ] Quality validation completed
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Ready for requirements-specification-review skill

## Tips

1. **Compliance First**: Always check for compliance framework before creating healthcare specifications
2. **Patient Safety**: Include patient safety requirements in every healthcare specification
3. **Clinical Focus**: Prioritize clinical workflows and regulatory compliance over technical details
4. **Clarification Limits**: Keep [NEEDS CLARIFICATION] markers to maximum 3 per healthcare feature
5. **Measurable Success**: Include clinical outcomes and regulatory metrics in success criteria

## Additional Resources

- [references/healthcare-specification-guide.md](references/healthcare-specification-guide.md) - Detailed healthcare specification writing guide
- [templates/healthcare-spec-template.md](templates/healthcare-spec-template.md) - Healthcare specification template
- [templates/healthcare-checklist-template.md](templates/healthcare-checklist-template.md) - Quality validation checklist template
