---
name: architecture-design-review
description: Reviews system architecture documentation for completeness, consistency, and quality. Validates C4 model diagrams, architecture decisions (ADRs), quality attributes, deployment design, and alignment with requirements. Use when reviewing architecture documents, validating architectural decisions, assessing architecture quality, or when user mentions architecture review, ADR validation, C4 model check, or architecture assessment.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "2.0.0"
  last_updated: "2026-02-02"
---

# Architecture Design Review Skill

## Overview

This skill performs comprehensive reviews of system architecture documentation (`architecture.md`) to ensure completeness, consistency, and quality. It validates all aspects of the architecture including stakeholder concerns, quality attributes, C4 model diagrams, architecture decisions (ADRs), deployment design, and alignment with requirements and ground rules.

**Key Concept: Progressive Disclosure**
- **Tier 1** (Always loaded): Metadata (name + description) for discovery
- **Tier 2** (On activation): This SKILL.md with instructions
- **Tier 3** (On demand): templates/, scripts/

## When to Use

- Reviewing completed architecture documentation
- Validating architectural decisions before implementation
- Assessing architecture quality and identifying gaps
- Ensuring architecture aligns with requirements and constraints
- Checking C4 model diagram completeness and correctness
- Validating ADRs (Architecture Decision Records)
- User mentions: "review architecture", "validate ADRs", "check C4 diagrams", "architecture assessment"

## Prerequisites

- **Architecture documentation**: `docs/architecture.md`, `docs/adr/*.md` (Optional)
- **Supporting documents**: `docs/ground-rules.md`, `specs/*/spec.md` (Optional)
- **Tools**: Python 3.8+

## Instructions

### Step 1: Validate Architecture Documentation

Run the validation script to verify architecture files exist and identify related documents:

```bash
python3 skills/architecture-design-review/scripts/validate_architecture.py --json
```

Parse the JSON output to identify:
- `architecture_file`: Path to architecture.md
- `available_docs`: List of available supporting documents
- `adr_count`: Number of ADR files found

### Step 2: Load Context

Read the architecture documentation and available supporting documents.

1. **Load structure**: Read `docs/architecture.md` to identify sections, diagrams, and TODOs.
2. **Load support**: If available, read `docs/ground-rules.md`, `specs/*/spec.md`, and `docs/adr/*.md`.

### Step 3: Execute Architecture Review

Perform comprehensive review following the template structure in `templates/architecture-review-template.md`.

#### Review Checklist

- [ ] **Document Completeness**: Are Executive Summary, Stakeholders, Architectural Drivers present?
- [ ] **System Context (C4 Level 1)**: Is the system boundary defined?
- [ ] **Container View (C4 Level 2)**: Are containers and technology choices identified?
- [ ] **Component View (C4 Level 3)**: Are critical components documented?
- [ ] **Deployment View**: Is the infrastructure defined?
- [ ] **Architecture Decisions (ADRs)**: Are major decisions documented?
- [ ] **Quality Attributes**: Are strategies mapped to requirements?
- [ ] **Risks**: Are risks and debt identified with mitigation?

#### Generate Report

Create a report using the structure from `templates/architecture-review-template.md` and save it to `docs/architecture-review-report.md` (or output to user).

### Step 4: Validate Alignment

- **Requirements**: does the architecture support the features in `specs/`?
- **Constraints**: does it follow `docs/ground-rules.md`?
- **Consistency**: do diagrams match the text?

## Examples

**Example 1: Full Review**
> "Review the architecture and check for any missing components."

1. Agent runs `python3 skills/architecture-design-review/scripts/validate_architecture.py`.
2. Agent reads `docs/architecture.md`.
3. Agent checks for C4 diagrams and required sections.
4. Agent generates a report highlighting missing "Risks" section.

**Example 2: ADR Check**
> "Validate our architecture decisions."

1. Agent runs validation script to find ADRs.
2. Agent reads `docs/adr/*.md`.
3. Agent checks if decisions use the standard format (Title, Status, Context, Decision, Consequences).
