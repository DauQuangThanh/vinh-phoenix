---
name: code-review
description: Reviews implemented code against specifications, architecture, and standards. Validates test coverage, checks compliance with design patterns, verifies checklist completion, and assesses code simplicity, maintainability, and readability. Generates comprehensive review reports with actionable feedback. Use when reviewing code, validating implementation quality, checking standards compliance, or when user mentions code review, review implementation, validate code, or check quality.
metadata:
  author: Dau Quang Thanh
  version: "2.1"
  last_updated: "2026-02-07"
license: MIT
---

# Code Review Skill

## Overview

This skill performs comprehensive code reviews by analyzing implemented code against specifications, design documents, architectural patterns, and coding standards. It validates test coverage, checks quality checklist completion, assesses code simplicity, maintainability, and readability, and generates detailed review reports with actionable feedback.

## When to Use

- Reviewing implemented code
- Validating implementation against `spec.md` and `design.md`
- Checking compliance with coding standards (e.g. `docs/standards.md`)
- Verifying test coverage and quality
- When user mentions: "review code", "validate implementation", "check code quality", "run code review"

## Prerequisites

- **Required documents in feature directory**:
  - Implementation code files
  - `spec.md` - Feature requirements and acceptance criteria
  - `design.md` - Technical design and architecture
- **Product-level documentation** (Optional but recommended):
  - `docs/architecture.md`
  - `docs/standards.md`
- **Python 3.8+** for running the prerequisite check script.

## Instructions

### Step 1: Check Prerequisites and Discover Implementation

Run the prerequisite check script to discover implementation artifacts and missing documents.

```bash
python3 skills/code-review/scripts/check-prerequisites.py
```

The script will output a JSON summary. Parse it to identify:

- `missing_docs`: If any required documents (`spec.md`, `design.md`) are missing, **stop and ask the user to provide them**.
- `implementation_files`: The list of source files to review.
- `test_files`: The list of test files available.
- `checklist_status`: Availability of quality checklists.

### Step 2: Load Review Context

Read all available documents identified in Step 1 to build a complete review context.

#### Required Context

1. **Read `spec.md`**: Extract acceptance criteria, user stories, and constraints.
2. **Read `design.md`**: Understand the intended architecture, data models, and API contracts.

#### Product Standards

If `docs/standards.md` or `docs/architecture.md` exist, read them to understand the broader coding conventions and patterns.

### Step 3: Perform Code Review

Analyze the `implementation_files` one by one or in logical groups. Compare them against:

1. **Requirements**: Does it fulfill `spec.md` criteria?
2. **Design**: Does it follow `design.md` structure?
3. **Quality**: Are variable names clear? Is logic simple? Is error handling robust?
4. **Tests**: Do `test_files` cover the main paths and edge cases?

### Step 4: Generate Report

Create a review report using the template `skills/code-review/templates/review-report.md`.
Fill in:

- **Summary**: High-level assessment.
- **Findings**: Issues categorized by severity (Critical, Major, Minor).
- **Verification**: Status of tests and checklists.
- **Recommendations**: Actionable steps to fix issues.

Save the report as `review-report.md` in the current directory (or update existing).

- Extract performance strategies

1. **docs/standards.md** (Optional):
   - Extract UI naming conventions
   - Extract code naming conventions
   - Extract file structure standards
   - Extract API design standards
   - Extract database naming conventions
   - Extract testing standards
   - Extract Git commit conventions
   - Extract documentation standards
   - Extract code quality metrics

#### Supporting Documents (If Available)

1. **tasks.md** (Optional):
   - Extract completed tasks list
   - Verify all tasks marked as [X]
   - Identify any incomplete tasks

2. **data-model.md** (Optional):
   - Extract entity definitions
   - Extract relationships and constraints

3. **contracts/** (Optional):
   - Extract API specifications
   - Extract endpoint definitions
   - Extract request/response schemas

4. **checklists/** (Optional):
   - Extract quality checklist items
   - Verify completion status

### Step 3: Review Implementation Against Specifications

Systematically review the code against requirements. See [references/review-criteria.md](references/review-criteria.md) for complete checklists covering:

- **Functional Requirements**: User stories, acceptance criteria, features, edge cases
- **Non-Functional Requirements**: Performance, security, scalability, maintainability
- **API Contract Validation**: Endpoints, schemas, HTTP methods, status codes
- **Data Model Validation**: Entities, relationships, constraints, indexes

### Step 4: Architecture Alignment Review (If architecture.md exists)

Verify implementation follows architectural guidelines. See [references/review-criteria.md](references/review-criteria.md) for complete checklists covering:

- **Architectural Patterns**: Design patterns, architectural styles, component boundaries
- **Component Organization**: Directory structure, module dependencies, cross-cutting concerns
- **Technology Stack Compliance**: Libraries, versions, ADRs
- **Quality Attributes**: Performance, security, scalability, observability

### Step 5: Standards Compliance Review (If standards.md exists)

Check code against coding standards. See [references/review-criteria.md](references/review-criteria.md) for complete checklists covering:

- **Naming Conventions**: UI, code, database naming
- **File and Directory Structure**: Organization, hierarchy, consistency
- **API Design Standards**: RESTful conventions, versioning, error handling
- **Code Quality Standards**: Complexity, DRY, error handling, logging
- **Testing Standards**: Organization, coverage, isolation
- **Git Commit Standards**: Conventions, prefixes, atomicity
- **Documentation Standards**: Code docs, API docs, inline comments

### Step 6: Test Coverage and Quality Review

Analyze test implementation and coverage. See [references/review-criteria.md](references/review-criteria.md) for complete checklists covering:

- **Test Presence**: Unit, integration, contract, E2E tests
- **Test Quality**: Readability, naming, AAA pattern, isolation
- **Coverage Metrics**: Line coverage, branch coverage, critical paths
- **Test Execution**: Pass rate, determinism, performance

### Step 7: Quality Checklist Validation (If checklists exist)

Verify all quality checklists are complete:

**Checklist Validation Process:**

1. **Scan all checklist files** in `FEATURE_DIR/checklists/`:
   - Count total items: Lines matching `- [ ]` or `- [X]` or `- [x]`
   - Count completed: Lines matching `- [X]` or `- [x]`
   - Count incomplete: Lines matching `- [ ]`

2. **Create status table**:

   ```text
   | Checklist    | Total | Completed | Incomplete | Status |
   |--------------|-------|-----------|------------|--------|
   | ux.md        | 12    | 12        | 0          | ✓ PASS |
   | test.md      | 10    | 10        | 0          | ✓ PASS |
   | security.md  | 8     | 8         | 0          | ✓ PASS |
   | performance.md | 6   | 5         | 1          | ✗ FAIL |
   ```

3. **Determine overall status**:
   - **PASS**: All checklists have 0 incomplete items
   - **FAIL**: One or more checklists have incomplete items

4. **Review incomplete items**:
   - List specific incomplete checklist items
   - Assess impact of incomplete items
   - Recommend completion or document exceptions

### Step 8: Code Quality Analysis

Perform detailed code quality assessment. See [references/review-criteria.md](references/review-criteria.md) for complete checklists covering:

- **Code Simplicity**: Clear logic flow, no unnecessary complexity, straightforward solutions
- **Code Readability**: Clear naming conventions, appropriate comments, consistent formatting
- **Code Maintainability**: Well-structured code, follows patterns, easy to modify and extend
- **Code Structure**: Single responsibility, proper abstraction, appropriate coupling and cohesion
- **Error Handling**: Error catching, meaningful messages, proper propagation, resource cleanup
- **Security**: Input validation, authentication, authorization, encryption
- **Performance**: Bottlenecks, efficient queries, caching, optimal algorithms

Review severity levels are defined in [references/review-criteria.md](references/review-criteria.md).

### Step 9: Generate Review Report

Create comprehensive review using `templates/review-report.md`:

**Report Contents**:

- **Executive Summary**: Overall assessment and key findings
- **Specification Compliance**: Requirements met vs missing
- **Architecture Alignment**: Patterns followed, ADRs respected
- **Standards Compliance**: Naming, structure, API design, testing
- **Test Coverage**: Metrics and quality assessment
- **Checklist Status**: Completion status and incomplete items
- **Code Quality**: Structure, security, performance, maintainability
- **Issues Found**: Critical, major, minor issues with severity
- **Recommendations**: Actionable improvements prioritized
- **Approval Status**: Approved / Approved with conditions / Changes required

Save report to `FEATURE_DIR/code-review-report.md`

### Step 10: Report Summary

Provide concise summary including:

- Overall review status (Approved / Conditional / Changes Required)
- Total issues found (Critical: X, Major: Y, Minor: Z)
- Specification compliance (X% complete)
- Architecture alignment (Pass/Fail)
- Standards compliance (Pass/Fail)
- Test coverage (X%)
- Checklist status (All passed / Some incomplete)
- Path to detailed review report
- Key recommendations (top 3-5)

## Additional Resources

- [references/review-criteria.md](references/review-criteria.md) - Complete review checklists and severity classifications
- `templates/review-report.md` - Structure for comprehensive review reports
- `templates/review-checklist.md` - Checklist template for manual review tracking

## Review Severity Classification

See [references/review-criteria.md](references/review-criteria.md) for complete severity level definitions:

- **Critical**: Security vulnerabilities, data corruption, complete failures
- **Major**: Incomplete requirements, performance issues, missing tests
- **Minor**: Style inconsistencies, minor violations, optimization opportunities
- **Informational**: Suggestions, alternative approaches, best practices

## Examples

### Example 1: Comprehensive Review with All Documents

**Input:**

```bash
python3 skills/code-review/scripts/check-prerequisites.py
```

**Output:**

```json
{
  "feature_dir": "/path/to/specs/feature-name",
  "available_docs": ["spec.md", "design.md", "tasks.md", "checklists/ux.md"],
  "missing_docs": [],
  "implementation_files": ["src/feature.ts", "src/feature-service.ts", "src/types.ts"],
  "test_files": ["tests/feature.test.ts", "tests/feature-service.test.ts"],
  "checklist_status": "Found: checklists/ux.md"
}
```

**Review Process:**

1. Load all documents (spec, design, architecture, standards)
2. Review 3 implementation files against specifications
3. Validate 2 test files for coverage and quality
4. Check architecture alignment with docs/architecture.md
5. Verify standards compliance with docs/standards.md
6. Validate checklist completion
7. Generate comprehensive review report
8. Report: "Approved - All checks passed, 2 minor suggestions"

### Example 2: Review with Incomplete Checklists

**Checklist Status:**

```text
| Checklist       | Total | Completed | Incomplete | Status |
|-----------------|-------|-----------|------------|--------|
| ux.md           | 12    | 12        | 0          | ✓ PASS |
| security.md     | 8     | 6         | 2          | ✗ FAIL |
| performance.md  | 6     | 6         | 0          | ✓ PASS |
```

**Incomplete Items:**

- security.md: Input validation for file uploads
- security.md: Rate limiting for API endpoints

**Review Process:**

1. Identify incomplete security checklist items
2. Assess impact: Critical security issues
3. Review code for actual implementation status
4. Generate report with Critical severity issues
5. Report: "Changes Required - 2 critical security items incomplete"

## Edge Cases

- **Missing spec.md or design.md**: Cannot perform comprehensive review, report error
- **No implementation files found**: Verify FEATURE_DIR, check if implementation started
- **No test files found**: Report as Major issue, recommend adding tests
- **Malformed checklists**: Attempt to parse, report parsing issues
- **Architecture.md or standards.md missing**: Skip those checks, note in report
- **Test coverage tool unavailable**: Perform manual coverage assessment from test files
- **Conflicting standards**: Prioritize standards.md over architecture.md, note conflicts

## Error Handling

- **Script execution fails**: Report exact error, check working directory and permissions
- **Invalid JSON from script**: Parse as text and extract paths manually
- **Missing required documents**: List missing documents and halt review
- **Cannot read implementation files**: Report access issues, suggest checking permissions
- **Test execution fails**: Report failed tests, include error logs, mark as Critical
- **Checklist parsing errors**: Report malformed checklists, attempt best-effort parsing

## Scripts

This skill includes cross-platform scripts for checking review prerequisites:

### Bash Script (Unia cross-platform Python script for checking review prerequisites

### Prerequisite Check Script

```bash
python3 skills/code-review/scripts/check-prerequisites.py
```

**Features:**

- Locates feature directory and documentation.
- Discovers implementation files and test files.
- Validates checklist existence.
- Checks for product-level documentation (architecture.md, standards.md).
- Outputs JSON for easy parsing.

**Output Format:**

The script outputs JSON with:

- `feature_dir`: Path to feature directory.
- `available_docs`: List of found documents.
- `missing_docs`: List of expected but missing documents.
- `implementation_files`: List of source code files.
- `test_files`: List of test files.
- `checklist_status`: Summary string of found checklists.

- `templates/review-report.md`: Structure for comprehensive code review reports
- `templates/review-checklist.md`: Checklist template for manual review tracking

## Guidelines

1. **Be Thorough**: Review all aspects systematically
2. **Be Objective**: Focus on facts, not opinions
3. **Be Constructive**: Provide actionable feedback
4. **Be Specific**: Reference exact files, lines, and issues
5. **Prioritize Issues**: Use severity levels consistently
6. **Explain Rationale**: Why something is an issue
7. **Suggest Solutions**: How to fix issues
8. **Acknowledge Good Work**: Note well-implemented sections
9. **Consider Context**: Understand project constraints
10. **Document Exceptions**: Note approved deviations from standards

## Success Criteria

A code review is complete when:

- [ ] All required documents reviewed
- [ ] Implementation verified against specifications
- [ ] Architecture alignment checked (if architecture.md exists)
- [ ] Standards compliance verified (if standards.md exists)
- [ ] Test coverage assessed
- [ ] Checklists validated (if checklists exist)
- [ ] Code quality analyzed
- [ ] Issues categorized by severity
- [ ] Review report generated with recommendations
- [ ] Approval status determined and documented
