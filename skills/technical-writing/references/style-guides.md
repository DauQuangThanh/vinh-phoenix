# Technical Documentation Style Guides

A curated list of industry-standard style guides and resources for technical writing.

## Major Style Guides

### Google Developer Documentation Style Guide

**URL:** <https://developers.google.com/style>

**Coverage:**

- General principles and tone
- Grammar and mechanics
- Formatting and organization
- API documentation
- UI text and error messages

**Key Principles:**

- Be conversational and friendly
- Use second person ("you")
- Use present tense
- Use active voice
- Be concise

**Best For:** Developer-focused documentation, API docs, technical tutorials

### Microsoft Writing Style Guide

**URL:** <https://learn.microsoft.com/en-us/style-guide/welcome/>

**Coverage:**

- Voice and tone
- Grammar and usage
- Formatting and layout
- Accessibility
- Global communications

**Key Principles:**

- Warm and relaxed
- Crisp and clear
- Ready to lend a hand
- Technically accurate

**Best For:** Software documentation, user guides, Microsoft ecosystem

### GitLab Documentation Style Guide

**URL:** <https://docs.gitlab.com/ee/development/documentation/styleguide/>

**Coverage:**

- Language and word choice
- Documentation structure
- Markdown guidelines
- Screenshots and images
- API documentation

**Key Principles:**

- Clear and direct
- Inclusive language
- Task-oriented
- Version-specific

**Best For:** Open-source projects, DevOps documentation

### Red Hat Style Guide (Supplementary)

**URL:** <https://redhat-documentation.github.io/supplementary-style-guide/>

**Coverage:**

- Terminology
- Grammar conventions
- Formatting
- Product-specific guidance

**Key Principles:**

- Consistency
- Clarity
- Accessibility
- Technical accuracy

**Best For:** Enterprise software documentation, technical manuals

## Specialized Guides

### The Chicago Manual of Style (General Reference)

**Type:** Book / Subscription website

**Coverage:**

- Comprehensive grammar rules
- Citation styles
- Punctuation
- Editing guidelines

**Best For:** General writing reference, formal documentation

### Apple Style Guide

**URL:** Available through Apple Style Guide App

**Coverage:**

- Apple product terminology
- UI text guidelines
- Localization
- Accessibility

**Best For:** macOS/iOS documentation, Apple ecosystem

### DigitalOcean Technical Writing Guidelines

**URL:** <https://www.digitalocean.com/community/tutorials>

**Coverage:**

- Tutorial structure
- Code formatting
- Writing for developers
- Practical examples

**Best For:** Developer tutorials, how-to guides, technical education

## Domain-Specific Resources

### API Documentation

**Swagger/OpenAPI Style Guide**

- URL: <https://swagger.io/docs/specification/>
- Focus: REST API specification and documentation

**Write the Docs - API Documentation**

- URL: <https://www.writethedocs.org/guide/api/>
- Focus: Best practices for API documentation

### Accessibility

**Web Content Accessibility Guidelines (WCAG)**

- URL: <https://www.w3.org/WAI/WCAG21/quickref/>
- Focus: Making documentation accessible

**A11Y Style Guide**

- URL: <https://a11y-style-guide.com/>
- Focus: Accessible writing patterns

### Markdown

**Markdown Guide**

- URL: <https://www.markdownguide.org/>
- Focus: Markdown syntax and best practices

**CommonMark Spec**

- URL: <https://commonmark.org/>
- Focus: Standard Markdown specification

## Quick Reference Guides

### Word Choice

| ❌ Avoid | ✅ Use | Reason |
|---------|--------|--------|
| Simply, just, easy | [Omit or be specific] | Patronizing, assumes difficulty |
| Please | [Omit in instructions] | Unnecessary in technical steps |
| Click here | [Descriptive link text] | Not accessible |
| He/she | They | Gender-neutral |
| Blacklist/whitelist | Blocklist/allowlist | Inclusive language |
| Master/slave | Primary/replica | Inclusive language |
| Guys | Everyone, folks, team | Gender-neutral |

### Tense and Voice

| Situation | Tense | Example |
|-----------|-------|---------|
| Instructions | Present/Imperative | "Click the button" |
| Feature descriptions | Present | "The system sends an email" |
| Past events | Past | "The request was sent" |
| Future capabilities | Future | "Version 2.0 will include..." |

**Prefer Active Voice:**

- ❌ Passive: "The file is uploaded by the user"
- ✅ Active: "The user uploads the file"
- ✅ Better: "Upload the file"

### Capitalization

**Follow these conventions:**

| Item | Style | Example |
|------|-------|---------|
| Headings | Title case or sentence case | "Quick Start Guide" or "Quick start guide" |
| UI elements | Match the UI exactly | Click **Save** (if button says "Save") |
| File names | As written | `config.json` |
| Code | As written in code | `myFunction()` |
| Products | Title case | "GitHub Copilot" |
| Features | Sentence case | "Code completion" |

### Punctuation

**Lists:**

- Capitalize first word
- End with period if complete sentences
- No period if fragments
- Be consistent within list

**Serial comma:**

- Use Oxford comma: "red, white, and blue"
- Prevents ambiguity

**Contractions:**

- Generally acceptable in informal docs
- Avoid in formal technical specifications
- Be consistent

### Formatting

**Code:**

- Use backticks for inline code: `variable`
- Use code blocks for multi-line code
- Specify language for syntax highlighting
- Test all code examples

**Lists:**

- Use bullet points for unordered items
- Use numbers for sequential steps
- Keep items parallel in structure
- Limit nesting to 2-3 levels

**Emphasis:**

- **Bold** for UI elements and emphasis
- *Italic* for introducing new terms
- `Code formatting` for code elements
- Don't overuse emphasis

## Tools and Linters

### Vale

**URL:** <https://vale.sh/>

**Description:** Extensible style guide linter

**Usage:**

```bash
# Install
brew install vale

# Check files
vale README.md

# Use with specific style
vale --config=.vale.ini docs/
```

**Benefits:**

- Enforce style guide rules automatically
- Integrate with CI/CD
- Support for multiple style guides
- Custom rule creation

### markdownlint

**URL:** <https://github.com/DavidAnson/markdownlint>

**Description:** Markdown style checker and linter

**Usage:**

```bash
# Install
npm install -g markdownlint-cli

# Check files
markdownlint "**/*.md"

# Fix automatically
markdownlint "**/*.md" --fix
```

**Benefits:**

- Consistent Markdown formatting
- Catch common mistakes
- Configurable rules

### write-good

**URL:** <https://github.com/btford/write-good>

**Description:** Naive linter for English prose

**Usage:**

```bash
# Install
npm install -g write-good

# Check file
write-good README.md
```

**Checks for:**

- Passive voice
- Weasel words
- Duplicate words
- Clichés

### alex

**URL:** <https://alexjs.com/>

**Description:** Catch insensitive, inconsiderate writing

**Usage:**

```bash
# Install
npm install -g alex

# Check files
alex docs/
```

**Checks for:**

- Gender-biased language
- Racial bias
- Ableist language
- Other insensitive terms

### textlint

**URL:** <https://textlint.github.io/>

**Description:** Pluggable linting tool for text and Markdown

**Usage:**

```bash
# Install
npm install -g textlint

# With plugins
npm install -g textlint-rule-terminology

# Check files
textlint README.md
```

## Building Your Style Guide

### Start Simple

1. **Choose a base:**
   - Adopt an existing guide (Google, Microsoft)
   - Customize as needed
   - Document differences

2. **Focus on consistency:**
   - Terminology
   - Formatting
   - Tone

3. **Make it accessible:**
   - Central location
   - Easy to search
   - Examples included

### Essential Sections

**Minimum style guide should include:**

1. **Voice and Tone**
   - Target audience
   - Formality level
   - Perspective (1st, 2nd, 3rd person)

2. **Word Choice**
   - Preferred terms
   - Terms to avoid
   - Product-specific terminology

3. **Formatting**
   - Headings
   - Code blocks
   - Lists
   - Links

4. **Grammar**
   - Tense preferences
   - Active vs passive voice
   - Capitalization rules

5. **Structure**
   - Document templates
   - Required sections
   - Organization

### Example Style Guide Template

```markdown
# [Your Company] Documentation Style Guide

## Voice and Tone

Write in a friendly, professional tone. Use second person ("you") to address readers.

❌ One should ensure proper configuration
✅ Ensure you configure it properly

## Terminology

### Preferred Terms

| Use | Don't Use |
|-----|-----------|
| sign in | log in, login |
| username | user name |
| email | e-mail, Email |

### Product Names

- [Product Name] (capitalized, not "product name")
- [Feature Name] (Title Case for features)

## Formatting

### Code

Inline code: Use `backticks` for:
- Command names: `npm install`
- File names: `package.json`
- Variable names: `userId`

Code blocks: Use for multi-line code:
```javascript
// Always specify language
const example = 'like this';
```

### Links

Use descriptive link text:

- ❌ Click this link
- ✅ Read the [installation guide](link)

### Lists

- Start with capital letter
- No period for fragments
- Period for complete sentences.
- Parallel structure

## Document Structure

### Required Sections

All docs must include:

1. Title (H1)
2. Brief description
3. Target audience/prerequisites
4. Main content
5. Next steps (if applicable)

### Optional Sections

- Examples
- Troubleshooting
- FAQs
- Additional resources

## Examples

[Include examples of well-written docs]

## Changelog

Track changes to this guide:

- 2026-01-29: Initial version

```

## CI/CD Integration

Automate style guide enforcement:

**GitHub Actions example:**
```yaml
name: Lint Documentation

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Lint Markdown
        uses: nosborn/github-action-markdown-cli@v3.2.0
        with:
          files: "**/*.md"
      
      - name: Check Style
        run: |
          npm install -g vale
          vale --config=.vale.ini docs/
```

## Resources

### Communities

- **Write the Docs:** <https://www.writethedocs.org/>
- **Technical Writing Slack:** Various communities
- **Stack Overflow Documentation:** Q&A for docs

### Books

- **"Docs for Developers"** by Jared Bhatti et al.
- **"The Product is Docs"** by Christopher Gales
- **"Every Page is Page One"** by Mark Baker
- **"Modern Technical Writing"** by Andrew Etter

### Courses

- **Google Technical Writing Courses:** Free online courses
- **Write the Docs - Documentation Guide:** Comprehensive online resource
- **LinkedIn Learning:** Various technical writing courses

### Newsletters

- **Technical Writing World:** Regular updates
- **I'd Rather Be Writing:** Blog and resources

## Summary

**To create effective documentation:**

1. Choose or create a style guide
2. Focus on consistency
3. Use linting tools
4. Train your team
5. Review and update regularly
6. Integrate into workflow

**Remember:**

- Perfect style is less important than consistency
- Adapt style guides to your needs
- Automate enforcement where possible
- Style guides evolve with your project
