# 🔥 Vinh Phoenix

## *Reusable Agent Skills for Structured Software Development*

**A curated library of 18 production-ready skills that empower AI coding assistants to deliver quality software through structured workflows.**

---

## 💡 What is Vinh Phoenix?

**Vinh Phoenix is a skills library that transforms how AI coding assistants approach software development.**

Instead of ad-hoc interactions, Phoenix provides battle-tested skills that guide AI assistants through structured workflows:

- **Requirements Skills** - Capture and clarify what to build
- **Architecture Skills** - Design systems and understand codebases
- **Planning Skills** - Create detailed implementation roadmaps
- **Standards Skills** - Establish and maintain code quality
- **Implementation Skills** - Write and review code systematically
- **Testing Skills** - Design comprehensive test strategies
- **Integration Skills** - Connect with project management tools

The **Phoenix CLI** installs these skills into your projects, making them discoverable by 20+ AI coding assistants. Skills are automatically loaded when tasks match their descriptions.

> **Think of Phoenix as a professional toolkit:** Just as craftspeople have specialized tools for each task, Phoenix gives your AI assistant specialized skills for each phase of software development. The AI automatically activates relevant skills based on what you're trying to accomplish.

## 🚀 Getting Started

**New to Vinh Phoenix?** Follow these guides:

| Guide | Description |
| ------- | ------------- |
| 📦 [Installation Guide](installation.md) | Set up Phoenix CLI and prerequisites |
| ⚡ [Quick Start Guide](quickstart.md) | Build your first project in minutes |
| 🔄 [Upgrade Guide](upgrade.md) | Update to the latest version |
| 💻 [Local Development](local-development.md) | Contribute and develop locally |

### Project Workflows

**Choose your workflow based on project type:**

| Workflow | Best For | Timeline |
| ---------- | ---------- |----------|
| 🌱 [Greenfield](greenfield-workflow.md) | New applications from scratch | 2-4 weeks (MVP) |
| 🏗️ [Brownfield](brownfield-workflow.md) | Adding features to existing apps | 1-2 weeks/feature |

---

## 🎯 Available Skills

After installation, AI assistants automatically discover and use these skills based on your requests:

### Architecture: Agent Skills Standard

Vinh Phoenix uses the [Agent Skills format](https://agentskills.io) - an open standard for giving AI agents new capabilities:

**How It Works:**

1. **Discovery** - At startup, agents load name and description of each skill
2. **Activation** - When your task matches a skill's description, the AI loads full instructions
3. **Execution** - The AI follows instructions, using templates and scripts as needed

**What Gets Installed:**

- 18 skill modules in agent-specific folders (`.github/skills/`, `.claude/skills/`, etc.)
- Each skill has SKILL.md (instructions), templates, scripts (bash & PowerShell)
- Skills like `requirements-specification`, `technical-detailed-design`, `coding`, etc.

This architecture enables:

- ✅ Progressive disclosure - Skills load context only when needed
- ✅ Multi-agent support - 20+ AI assistants use the same skills format
- ✅ Easy updates - Upgrade all skills with `phoenix init --here --force`

### Core Workflow Skills

Follow this complete workflow for Spec-Driven Development:

| Skill | When the AI Uses It |
| --------- | ---------- |
| `project-ground-rules-setup` | When you ask to establish project principles |
| `context-assessment` | When you need to analyze an existing codebase |
| `requirements-specification` | When you describe what you want to build |
| `requirements-specification-review` | When you ask to clarify requirements |
| `architecture-design` | When you request system architecture documentation |
| `coding-standards` | When you need coding standards documented |
| `technical-detailed-design` | When you specify tech stack and implementation |
| `task-management` | When you ask to break down work into tasks |
| `project-consistency-analysis` | When you request plan validation |
| `coding` | When you ask to implement according to plan |

### Product-Level Skills

Run these once per product for end-to-end testing:

| Skill | When the AI Uses It |
| --------- | ---------- |
| `e2e-test-design` | When you request end-to-end test specifications |

### Enhancement Skills

Additional commands for project management and integration:

| Skill | When the AI Uses It |
| --------- | ---------- |
| `tasks-to-github-issues` | When you ask to convert tasks to GitHub issues |
| `tasks-to-azure-devops` | When you ask to convert tasks to Azure DevOps items |
| `git-commit` | When committing changes |
| `code-review` | When you request code quality review |

---

## 🧩 The Skills Library

Phoenix includes **18 modular skills**, each containing templates, scripts, and documentation. These skills work across 20+ AI agents:

<details>
<summary><strong>View All Skills</strong></summary>

| Skill | When Used | Purpose |
| ------- | -------- | --------- |
| `requirements-specification` | Requirements gathering | Capture feature requirements from natural language |
| `requirements-specification-review` | Requirements clarification | Structured clarification through questioning |
| `technical-detailed-design` | Technical planning | Create detailed implementation plans |
| `technical-detailed-design-review` | Plan validation | Validate design consistency and coverage |
| `task-management` | Task breakdown | Break down plans into actionable tasks |
| `coding` | Implementation | Execute implementation tasks systematically |
| `code-review` | Quality assurance | Review code quality and standards |
| `architecture-design` | System design | Design system architecture with C4 diagrams |
| `architecture-design-review` | Architecture validation | Review architecture decisions |
| `coding-standards` | Standards definition | Establish coding conventions |
| `e2e-test-design` | Test planning | Design end-to-end test specifications |
| `project-ground-rules-setup` | Project setup | Define project principles |
| `context-assessment` | Codebase analysis | Analyze existing codebase patterns |
| `project-consistency-analysis` | Validation | Cross-artifact consistency checks |
| `tasks-to-github-issues` | Integration | Sync tasks with GitHub Issues |
| `tasks-to-azure-devops` | Integration | Sync tasks with Azure DevOps |
| `git-commit` | Version control | Generate semantic commit messages |
| `nextjs-mockup` / `nuxtjs-mockup` | Prototyping | Generate framework-specific mockups |

**Each skill is self-contained** with templates and scripts (bash & PowerShell), installed to agent-specific folders.

</details>

---

## 🎯 Core Philosophy

Phoenix skills enable **Spec-Driven Development** - a structured approach where specifications drive implementation:

| Principle | What It Means |
| ----------- | --------------- |
| **Intent First** | Define the "*what*" and "*why*" before the "*how*" |
| **Rich Specifications** | Create detailed specs with organizational principles |
| **Step-by-Step** | Improve through multiple phases, not one-shot generation |
| **AI-Powered** | Skills guide AI to interpret specs and generate quality code |

## 🌟 When to Use Phoenix Skills

| Scenario | What You Can Do |
| ---------- | ------------------ |
| **🆕 New Projects** | <ul><li>Use all 18 skills for complete workflow</li><li>Establish architecture and standards first</li><li>Generate specs, plans, and implementations</li><li>Build production-ready applications</li></ul> |
| **🔧 Existing Projects** | <ul><li>Start with context-assessment skill</li><li>Focus on 7-9 core skills</li><li>Add features while maintaining consistency</li><li>Integrate systematically with existing code</li></ul> |
| **🔬 Exploration** | <ul><li>Use specification and design skills for prototyping</li><li>Try different solutions in parallel</li><li>Test multiple tech stacks quickly</li><li>Validate ideas before full implementation</li></ul> |

## 🔬 What We're Building

Phoenix skills are designed to support real-world development needs:

- **🔧 Tech Independence** - Skills work with any language, framework, or platform
- **🏢 Enterprise Ready** - Support organizational constraints and compliance requirements
- **👥 Developer Focused** - Flexible workflows for different development styles
- **🔄 Iterative Process** - Enable exploration, refinement, and continuous improvement

---

## 🤝 Contributing

Want to help improve Vinh Phoenix? Check our [Contributing Guide](https://github.com/dauquangthanh/vinh-phoenix/blob/main/CONTRIBUTING.md) to get started.

**Ways to contribute:**

- 🐛 Report bugs or issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit code improvements

---

## 💬 Get Help

Need assistance?

- 📖 [Support Guide](https://github.com/dauquangthanh/vinh-phoenix/blob/main/SUPPORT.md) - Common questions and solutions
- 🐛 [Open an Issue](https://github.com/dauquangthanh/vinh-phoenix/issues/new) - Report bugs or request features
- 💭 [Discussions](https://github.com/dauquangthanh/vinh-phoenix/discussions) - Ask questions and share ideas
