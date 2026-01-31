---
name: technical-writing
description: Creates and improves technical documentation for software projects including API docs, README files, user guides, architecture documents, and tutorials. Use when writing technical documentation, documenting code, creating user guides, or when user mentions technical writing, documentation, API docs, README, or software documentation.
metadata:
  author: Dau Quang Thanh
  version: "1.0.1"
  last-updated: "2026-01-29"
license: MIT
---

# Technical Writing for Software Development

## Overview

This skill helps create and improve technical documentation for software projects, including API documentation, README files, user guides, architecture documents, and tutorials. It provides structured guidance for writing clear, comprehensive documentation tailored to different audiences.

## When to Use

Use this skill when:

- Creating or updating README files, API docs, or user guides
- Documenting system architecture and design decisions
- Writing tutorials, release notes, or troubleshooting guides
- Developing developer onboarding or SDK documentation

## Prerequisites

- Text editor with Markdown support
- Understanding of the software/system being documented
- Access to source code (for API documentation)
- Target audience definition and style guide (if applicable)

## Instructions

### Step 1: Identify Documentation Type and Audience

**Developer-Facing:** API reference, SDK docs, contributing guidelines, architecture docs
**End-User:** Installation guides, user guides, tutorials, FAQ, release notes
**Mixed Audience:** README files, configuration guides, integration docs

See [references/software-doc-types.md](references/software-doc-types.md) for detailed information on each type.

### Step 2: Gather Information

Collect before writing:

- **Technical Details:** API endpoints, parameters, configuration, requirements, dependencies
- **Use Cases:** Common workflows, real-world examples, edge cases
- **Context:** Project purpose, audience skill level, related systems

### Step 3: Structure Your Documentation

**README:** Title → Features → Installation → Quick Start → Usage → Configuration → Contributing → License

**API:** Overview → Authentication → Endpoints (with request/response/examples) → Rate limiting → Versioning

**User Guide:** Introduction → Getting Started → Features → Advanced Topics → Troubleshooting → FAQ

**Architecture:** Overview → Diagrams → Components → Data Flow → Tech Stack → Design Decisions → Security

See templates in [templates/](templates/) for complete structures.

### Step 4: Write Clear and Concise Content

**Clarity:** Use simple language, define technical terms, avoid jargon, use active voice

**Consistency:** Follow a style guide, use consistent terminology and formatting

**Completeness:** Include all necessary information, provide context, cover edge cases

**Accuracy:** Verify details, test code examples, keep current, include versions

See [references/documentation-best-practices.md](references/documentation-best-practices.md) for comprehensive guidelines.

### Step 5: Add Code Examples

Best practices:

- **Keep Focused:** One concept per example, minimal boilerplate
- **Make Runnable:** Complete code, include imports, specify dependencies
- **Explain:** Add comments, describe what it demonstrates, highlight key points
- **Show Output:** Include expected results

```python
# Example: Calculate sum
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(f"Sum: {total}")
# Output: Sum: 15
```

### Step 6: Use Visual Aids

- **Diagrams:** Architecture, sequence, ER diagrams, component diagrams
- **Tables:** Parameters, configuration options, error codes, feature comparisons
- **Screenshots:** UI elements, expected output, configuration screens
- **Code Blocks:** With syntax highlighting and language specification

### Step 7: Organize for Scannability

- **Clear Headings:** Descriptive, hierarchical, task-based
- **Break Up Text:** Short paragraphs (3-5 sentences), bullet points, numbered steps, callouts
- **Navigation:** Table of contents, internal links, related docs links

### Step 8: Document Edge Cases and Errors

Include for each error:

- Error code/name
- When it occurs
- Possible causes
- Resolution steps
- Prevention tips

Example:

```markdown
### Error: `ConnectionTimeout`

**Description:** API request exceeds timeout limit.

**Causes:** Network issues, server overload, large payload

**Resolution:**
1. Check network connection
2. Increase timeout in config
3. Reduce payload size
4. Retry with exponential backoff
```

### Step 9: Add Configuration and Setup Details

**Installation:** Requirements, prerequisites, step-by-step process, verification

**Configuration:** All options, defaults, required vs optional, environment-specific settings

```markdown
## Installation

### Requirements
- Python 3.8+, pip, 2GB RAM

### Install
```bash
pip install mypackage
```

### Verify

```bash
mypackage --version
# Expected: mypackage 1.0.0
```

```

### Step 10: Review and Test

**Review Checklist:**

- [ ] Technical details verified
- [ ] Code examples tested
- [ ] Links functional
- [ ] Spelling/grammar checked
- [ ] Formatting consistent
- [ ] Version info accurate

**Testing:** Follow instructions yourself, have others test, run code examples

### Step 11: Maintain and Update

- Update with each release
- Document breaking changes
- Add new features, remove deprecated content
- Maintain changelog and version API docs

## Examples

See [references/complete-examples.md](references/complete-examples.md) for detailed examples including:

- README files for libraries
- API endpoint documentation
- Tutorial documents
- Error documentation
- Configuration documentation

## Edge Cases

### Case 1: Technical Terminology Varies Across Domains

**Handling:** Define terms explicitly on first use and provide a glossary for complex topics.

**Action:** Use tooltips or hover text for inline definitions, or create a dedicated glossary page.

### Case 2: Documentation for Multiple Versions

**Handling:** Maintain version-specific documentation with clear version indicators.

**Action:** Use version selectors in documentation site, include version in URLs, maintain changelog.

### Case 3: Multilingual Documentation

**Handling:** Provide translations with cultural context, not just word-for-word.

**Action:** Use localization tools, engage native speakers for review, maintain translation memory.

### Case 4: Documentation for Private/Internal APIs

**Handling:** Balance security with usability by documenting without exposing sensitive details.

**Action:** Use placeholders for sensitive values, provide sanitized examples, restrict access appropriately.

### Case 5: Rapidly Changing Codebase

**Handling:** Automate documentation generation where possible and implement review processes.

**Action:** Use docstring-based tools (Sphinx, JSDoc), integrate docs into CI/CD, assign documentation owners.

## Error Handling

### Error: Outdated Code Examples

**Issue:** Code examples no longer work with current version.

**Resolution:**
1. Test all examples against current version
2. Update examples to use current API
3. Add version badges to examples
4. Automate testing of documentation examples

### Error: Missing Context

**Issue:** Documentation assumes too much prior knowledge.

**Resolution:**
1. Define target audience explicitly
2. Add prerequisites section
3. Link to foundational concepts
4. Provide background information

### Error: Inconsistent Terminology

**Issue:** Same concept called different names throughout docs.

**Resolution:**
1. Create and maintain terminology glossary
2. Use search/replace to standardize terms
3. Document preferred terms in style guide
4. Use documentation linter to catch variations

### Error: Poor Searchability

**Issue:** Users can't find information in documentation.

**Resolution:**
1. Improve heading structure and keywords
2. Add comprehensive table of contents
3. Implement search functionality
4. Use consistent naming conventions
5. Add cross-references and "See also" sections

## Scripts

### Document Structure Validator

Validates documentation structure and completeness.

**Bash (macOS/Linux):**
```bash
./scripts/validate-docs.sh --dir ./docs --type readme
./scripts/validate-docs.sh --dir ./docs --type api
```

**PowerShell (Windows):**

```powershell
.\scripts\validate-docs.ps1 -Directory .\docs -Type readme
.\scripts\validate-docs.ps1 -Directory .\docs -Type api
```

### Documentation Generator

Generates documentation templates based on type.

**Bash (macOS/Linux):**

```bash
./scripts/generate-docs.sh --type readme --output ./README.md
./scripts/generate-docs.sh --type api --output ./docs/api.md
```

**PowerShell (Windows):**

```powershell
.\scripts\generate-docs.ps1 -Type readme -Output .\README.md
.\scripts\generate-docs.ps1 -Type api -Output .\docs\api.md
```

## Additional Resources

- [references/documentation-best-practices.md](references/documentation-best-practices.md) - Comprehensive guide to documentation standards and best practices
- [references/software-doc-types.md](references/software-doc-types.md) - Detailed explanation of different documentation types
- [references/style-guides.md](references/style-guides.md) - Links to popular documentation style guides
- [templates/readme-template.md](templates/readme-template.md) - Ready-to-use README template
- [templates/api-doc-template.md](templates/api-doc-template.md) - API documentation template
- [templates/user-guide-template.md](templates/user-guide-template.md) - User guide template
- [templates/architecture-doc-template.md](templates/architecture-doc-template.md) - Architecture documentation template

### References

- [documentation-best-practices.md](references/documentation-best-practices.md) - Standards and best practices
- [software-doc-types.md](references/software-doc-types.md) - Explanation of documentation types
- [style-guides.md](references/style-guides.md) - Popular style guides and tools
- [complete-examples.md](references/complete-examples.md) - Full documentation examples

### Templates

- [readme-template.md](templates/readme-template.md) - README template
- [api-doc-template.md](templates/api-doc-template.md) - API documentation template
- [user-guide-template.md](templates/user-guide-template.md) - User guide template
- [architecture-doc-template.md](templates/architecture-doc-template.md) - Architecture
