---
name: architecture-design
description: Creates comprehensive system architecture documentation using C4 model diagrams and ADRs. Use when designing product architecture, defining quality strategies, or when user mentions architecture design, system design, C4 diagrams, or architectural decisions.
metadata:
  author: Dau Quang Thanh
  version: "1.1.0"
  last_updated: "2026-02-02"
license: MIT
---

# Architecture Design Skill

## Overview

This skill creates comprehensive system architecture documentation for products using C4 model diagrams, Architecture Decision Records (ADRs), and quality attribute strategies. It guides product-level architecture design, documents architectural decisions, defines quality requirements, and plans deployment architecture and infrastructure.

## When to Use

- Creating comprehensive system architecture documentation for products
- Designing product-level architecture with C4 model diagrams
- Documenting architectural decisions (ADRs)
- Defining quality attribute requirements and strategies
- Planning deployment architecture and infrastructure
- When user mentions "design architecture", "system architecture", "C4 diagrams"
- Before creating feature-level implementation plans
- After creating feature specifications and ground rules

## Prerequisites

**Required Tools**:

- Python 3.8+
- Git (recommended for version control)
- File system access to project repository

**Required Files**:

- `docs/ground-rules.md` - Project principles and constraints
- Feature specifications in `specs/*/spec.md` (at least one recommended)

**Optional**:

- Existing architecture documentation to update

## Instructions

### Step 0: Specification and Requirements Gathering

**⚠️ IMPORTANT: Always request specification documents before starting architecture design.**

1. **Request specification documents:**
   - Ask the user to provide requirements specifications, feature documentation, or product requirements
   - Request any relevant documentation: PRD (Product Requirements Document), feature specs, user stories, or business requirements
   - If no formal documentation exists, ask the user to describe:
     - The product or system to be architected
     - Key features and functionalities
     - Expected users and stakeholders
     - Business goals and objectives
     - Technical constraints or preferences
     - Performance and scalability requirements
     - Security and compliance needs

2. **Verify ground rules exist:**
   - Check if `docs/ground-rules.md` exists in the project
   - If missing, recommend creating it first using the `project-ground-rules-setup` skill
   - Ground rules are essential for architecture design

3. **Review and confirm understanding:**
   - Summarize the requirements back to the user
   - Clarify any ambiguities or missing details
   - Confirm the scope and expected architecture deliverables
   - Identify what needs to be designed (new system, system enhancement, specific components)

4. **Only proceed to Step 1 after:**
   - Specification documents are provided and reviewed
   - Ground rules file exists or creation is confirmed
   - Requirements are clearly understood
   - User confirms readiness to start architecture design

### Step 1: Setup and Initialization

Run the setup script to prepare the architecture environment:

```bash
python3 <SKILL_DIR>/scripts/setup_architect.py
```

The script will:

- Detect repository root
- Create `docs/` and `docs/adr/` directories
- Copy architecture template to `docs/architecture.md`
- Find all feature specifications
- Return paths and metadata in JSON format

**Parse the JSON output** to get:

- `ARCH_DOC`: Path to the architecture document
- `DOCS_DIR`: Documentation directory
- `ADR_DIR`: Architecture Decision Records directory
- `SPECS_DIR`: Feature specifications directory
- `SPEC_COUNT`: Number of feature specs found
- `FEATURE_SPECS`: Array of spec file paths
- `PRODUCT_NAME`: Product/project name
- `GROUND_RULES`: Path to ground rules file

### Step 2: Load Existing Context

Before starting architecture design, load existing project context:

1. Read `docs/ground-rules.md` - Project principles, constraints, conventions
2. Read all feature specifications from `FEATURE_SPECS` array
3. Load the architecture template from `ARCH_DOC` path
4. Review any existing architecture documentation

### Step 3: Execute Architecture Design Workflow

Follow the architecture design phases systematically:

#### Phase 0: Architecture Analysis & Stakeholder Identification

**Goal**: Understand requirements and stakeholders

1. **Analyze feature specifications**:
   - Read all `specs/*/spec.md` files
   - Extract common patterns and requirements
   - Identify system boundaries
   - List all external integrations mentioned

2. **Identify stakeholders** from ground-rules and specs:
   - End users and their concerns
   - Development team requirements
   - Operations team needs
   - Security and compliance requirements
   - Business stakeholders

3. **Extract architectural drivers**:
   - Business goals from feature specs
   - Quality attributes (performance, scalability, security)
   - Technical constraints from ground-rules
   - Organizational constraints
   - Assumptions and dependencies

**Output**: Complete sections "Executive Summary" and "Architecture Snapshot"

#### Phase 1: System Design & C4 Model

**Goal**: Create visual architecture using C4 model

**Prerequisites**: Phase 0 complete

Create four levels of architecture diagrams using Mermaid format. See [references/c4-and-adr-guide.md](references/c4-and-adr-guide.md) for detailed C4 model guidance, diagram examples, and when to use each level.

1. **System Context (C4 Level 1)**: User types, external systems, system boundaries
2. **Container View (C4 Level 2)**: Technical containers, technology stack, communication protocols
3. **Component View (C4 Level 3)**: Component breakdown for critical containers
4. **Code View (C4 Level 4)**: Optional - directory structure, design patterns

**Output**: Complete "System Overview (C4)" section with all Mermaid diagrams

#### Phase 2: Deployment & Infrastructure Design

**Goal**: Design production deployment architecture

**Prerequisites**: Phase 1 complete

Design deployment topology, CI/CD pipeline, and disaster recovery. See [references/c4-and-adr-guide.md](references/c4-and-adr-guide.md) for deployment architecture patterns (single-region, multi-region active-passive, multi-region active-active).

1. **Deployment architecture**: Environment topology, infrastructure components, multi-AZ setup
2. **CI/CD pipeline**: Build/test/deploy stages, deployment strategy, IaC approach
3. **Disaster recovery**: Backup strategy, RTO/RPO, recovery procedures

**Output**: Complete "Deployment Summary" section

#### Phase 3: Architecture Decisions & Quality Strategies

**Goal**: Document decisions and quality attribute strategies

**Prerequisites**: Phase 2 complete

Document ADRs for major architectural choices and map quality strategies to requirements. See [references/c4-and-adr-guide.md](references/c4-and-adr-guide.md) for:

- Detailed ADR template and examples
- When to create ADRs
- Quality attribute strategies (performance, scalability, availability, security, maintainability)
- Common architecture patterns (event-driven, API gateway, CQRS, strangler fig)

1. **Document ADRs**: For each major decision, include context, decision, rationale, consequences, alternatives
2. **Map quality strategies**: Performance, scalability, availability, security, maintainability
3. **Identify risks**: Architecture risks, technical debt, open questions

**Output**: Complete "Architecture Decisions (ADR Log)", "Quality Attributes", and "Risks & Technical Debt" sections

#### Phase 4: Agent Checklist & Finalization

**Goal**: Create actionable guidance for agents and validate completeness

**Prerequisites**: Phase 3 complete

1. **Complete Agent Checklist**:
   - **Inputs**: Payloads, headers, authentication requirements
   - **Outputs**: JSON schemas, status codes, response formats
   - **Public APIs**: List endpoints with HTTP methods
   - **Events**: Event names, payload schemas, topics/queues
   - **Data Contracts**: Key tables/fields, indexes, relationships
   - **SLOs**: Latency targets, availability targets
   - **Secrets**: Secret sources, rotation policies
   - **Config**: Environment variables, feature flags
   - **Failure Modes**: Timeouts, retries, idempotency requirements
   - **Security**: Roles, scopes, token TTLs

2. **Generate supplementary documents** (if needed):
   - `docs/architecture-overview.md` - High-level summary for stakeholders
   - `docs/deployment-guide.md` - Detailed deployment instructions
   - `docs/adr/` - Individual ADR files for version control

3. **Validation**:
   - Ensure all sections are complete
   - Verify all Mermaid diagrams render correctly
   - Check that all "ACTION REQUIRED" comments are addressed
   - Validate consistency with ground-rules
   - Confirm quality targets are measurable and specific

### Step 4: Update Agent Context

After completing the architecture, update agent-specific context files:

```bash
python3 <SKILL_DIR>/scripts/update_agent_context.py [agent-type]
```

**Supported agent types**: claude, gemini, copilot, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, roo, codebuddy, amp, shai, q, bob, jules, qoder, antigravity

**Omit agent type** to update all existing agent files.

### Step 5: Commit Architecture

Create a git commit with the completed architecture:

```bash
git add docs/architecture.md docs/adr/
git commit -m "docs: add system architecture documentation"
```

### Step 6: Quality Review (Recommended)

**After completing the architecture, it's highly recommended to run a quality review:**

1. **Run the architecture-design-review skill** to validate:
   - Alignment with ground rules and project goals
   - Technical feasibility and scalability
   - Completeness of architectural decisions
   - Clarity of component descriptions
   - Proper documentation of trade-offs

2. **Address any findings** from the review before proceeding to feature specifications

3. **If issues found**, update the architecture and repeat validation

**Next Steps:**

- If review passes, proceed to create feature specifications using `requirements-specification` skill
- Use `coding-standards` skill to establish code conventions
- Use `technical-detailed-design` skill for individual feature implementation planning

## Examples

### Example 1: E-Commerce Platform Architecture

**Input**: Design architecture for e-commerce platform with 3 feature specs (user management, product catalog, checkout)

**Process**:

1. Run setup script → Get architecture template and 3 specs
2. Analyze specs → Extract: user auth, product search, payment gateway
3. Identify stakeholders → End users, admins, payment provider, analytics
4. Create C4 Context → Users, Admin, System, Stripe, Google Analytics
5. Design Containers → React SPA, Node.js API, PostgreSQL, Redis, RabbitMQ
6. Define Components → Auth service, Product service, Order service, Payment service
7. Plan deployment → AWS ECS, Multi-AZ, CloudFront CDN, RDS Multi-AZ
8. Document ADRs → Microservices (scalability), PostgreSQL (ACID), Redis (caching)
9. Define quality targets → 95% < 200ms, 99.9% uptime, PCI DSS compliance
10. Complete agent checklist → REST endpoints, JWT auth, event schemas

**Output**: Complete `docs/architecture.md` with C4 diagrams and 5 ADRs

### Example 2: SaaS Analytics Platform

**Input**: Design architecture for multi-tenant analytics platform

**Process**:

1. Run setup script → Get template, ground rules, 4 specs
2. Analyze requirements → Multi-tenancy, real-time dashboards, data export
3. Identify drivers → Performance (sub-second queries), Scalability (1M+ events/sec)
4. Create C4 diagrams → Context (users, data sources), Containers (Kafka, Druid, React)
5. Design deployment → Kubernetes on AWS EKS, horizontal pod autoscaling
6. Document ADRs → Event-driven architecture, Apache Druid (OLAP), tenant isolation
7. Define strategies → Sharding by tenant_id, columnar storage, query caching
8. Risk assessment → Data lake performance, multi-tenancy security
9. Complete checklist → GraphQL API, event schemas, SLOs (p95 < 100ms)

**Output**: Complete architecture with deployment diagrams and security model

## Key Rules

1. **Use Absolute Paths**: All file operations must use absolute paths
2. **Product-Level Scope**: Architecture goes to `docs/architecture.md` (product-level, NOT feature-level)
3. **Mermaid Diagrams Required**: All diagrams MUST use Mermaid format embedded in markdown
4. **ADRs Are Mandatory**: Every major architectural decision MUST have an ADR
5. **Measurable Targets**: Quality attribute targets must be specific and measurable (not "fast", but "95% < 200ms")
6. **Reference Specs**: Document which feature specs influenced each architectural decision
7. **Respect Ground Rules**: Ground-rules constraints MUST be respected; violations must be justified
8. **Concrete Values**: Use concrete numbers, versions, URLs (not placeholders)
9. **One Architecture Per Product**: This is product-level, not feature-level planning

## Architecture Decision Record (ADR) Format

See [references/c4-and-adr-guide.md](references/c4-and-adr-guide.md) for detailed ADR template with complete example.

## Edge Cases

### Case 1: No Feature Specifications Yet

**Handling**: Create architecture based on ground-rules and user input only. Focus on high-level system design. Update architecture after feature specs are created.

### Case 2: Updating Existing Architecture

**Handling**: Read existing `docs/architecture.md`, preserve existing ADRs, add new sections for changes. Create new ADRs for new decisions. Mark superseded ADRs appropriately.

### Case 3: Microservices vs Monolith Decision

**Handling**: Consider: team size, deployment frequency, scalability needs, organizational structure. Document decision in ADR with clear rationale. Default to monolith for small teams unless specific drivers require microservices.

## Error Handling

### Error: Template Not Found

**Action**: Script creates basic architecture file. Manually structure document using standard sections from skill documentation.

### Error: Mermaid Diagram Syntax Error

**Action**: Validate Mermaid syntax using online editor (mermaid.live). Fix syntax errors. Test rendering in markdown preview.

## Scripts

### setup_architect.py

Creates architecture environment and copies template:

```bash
python3 <SKILL_DIR>/scripts/setup_architect.py
```

**Returns**: JSON with paths (ARCH_DOC, DOCS_DIR, ADR_DIR, SPECS_DIR, SPEC_COUNT, FEATURE_SPECS, PRODUCT_NAME, GROUND_RULES)

### update_agent_context.py

Updates agent-specific context with architecture decisions:

```bash
python3 <SKILL_DIR>/scripts/update_agent_context.py [agent-type]
```

## Templates

### arch-template.md

Located at: `<SKILL_DIR>/templates/arch-template.md`

Streamlined architecture template with sections for C4 diagrams, deployment, ADRs, and quality attributes.
