<div align="center">

# 🔥 Vinh Phoenix

## *Reusable Agent Skills for Structured Software Development*

**A curated library of 18 production-ready skills that power AI coding assistants to deliver quality software through structured workflows.**

[![Release](https://github.com/dauquangthanh/vinh-phoenix/actions/workflows/release.yml/badge.svg)](https://github.com/dauquangthanh/vinh-phoenix/actions/workflows/release.yml)
[![GitHub stars](https://img.shields.io/github/stars/dauquangthanh/vinh-phoenix?style=social)](https://github.com/dauquangthanh/vinh-phoenix/stargazers)
[![License](https://img.shields.io/github/license/dauquangthanh/vinh-phoenix)](https://github.com/dauquangthanh/vinh-phoenix/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub_Pages-blue)](https://dauquangthanh.github.io/vinh-phoenix/)

</div>

---

## Table of Contents

- [🎯 What is Vinh Phoenix?](#-what-is-vinh-phoenix)
- [🧩 The Skills Library](#-the-skills-library)
- [⚡ Get Started](#-get-started)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [🔧 Phoenix CLI Reference](#-phoenix-cli-reference)
- [📚 Core Philosophy](#-core-philosophy)
- [🌟 Development Workflows](#-development-workflows)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn More](#-learn-more)
- [📋 Detailed Process](#-detailed-process)
- [🔍 Troubleshooting](#-troubleshooting)
- [👥 Maintainers](#-maintainers)
- [💬 Support](#-support)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)

## 🎯 What is Vinh Phoenix?

**Vinh Phoenix is a skills library that transforms AI coding assistants into structured development partners.**

Instead of ad-hoc prompting, Phoenix provides 18 battle-tested skills that guide AI assistants through:

- ✅ Requirements specification and clarification
- ✅ Architecture design and review
- ✅ Technical planning and implementation
- ✅ Code quality and consistency analysis
- ✅ Test design and execution
- ✅ Project management and tracking

**The Phoenix CLI** installs these skills into your project, making them instantly available to 20+ AI coding assistants. Skills are automatically discovered and used by AI models when your tasks match their descriptions.

> **Think of it like a professional toolkit:** Just as a craftsperson has specialized tools for each task, Phoenix gives your AI assistant specialized skills for each phase of software development. The AI automatically activates relevant skills based on what you're trying to accomplish.

## 🧩 The Skills Library

Phoenix includes **18 modular skills**, each containing:

- 📋 **Templates** - Structured formats for specifications, plans, and documentation
- 🔧 **Scripts** - Automation for git operations, file management, and workflows (bash & PowerShell)
- 📖 **Documentation** - Clear guidance on when and how to use each skill

### Available Skills

| Category | Skills | Purpose |
|----------|--------|----------|
| **Requirements** | `requirements-specification`<br/>`requirements-specification-review` | Define and validate what to build |
| **Architecture** | `architecture-design`<br/>`architecture-design-review`<br/>`context-assessment` | Design systems and understand existing codebases |
| **Planning** | `technical-design`<br/>`technical-design-review`<br/>`project-management` | Create implementation plans and track progress |
| **Standards** | `coding-standards`<br/>`project-ground-rules-setup`<br/>`project-consistency-analysis` | Establish and maintain quality standards |
| **Implementation** | `coding`<br/>`code-review` | Write and review code |
| **Testing** | `e2e-test-design` | Design comprehensive test suites |
| **Integration** | `tasks-to-github-issues`<br/>`tasks-to-azure-devops` | Sync with project management tools |
| **Version Control** | `git-commit` | Manage commits with semantic messages |
| **Prototyping** | `nextjs-mockup`<br/>`nuxtjs-mockup` | Generate framework-specific mockups |

**Key Benefits:**

- 🔄 **Reusable** - Each skill works across projects and frameworks
- 🤝 **Multi-agent** - Same skills power 20+ AI assistants
- 🎯 **Focused** - Each skill handles one aspect of development
- 📦 **Self-contained** - Templates and scripts embedded in each skill
- 🔧 **Cross-platform** - Both bash and PowerShell scripts included

## ⚡ Get Started

### 1. Install Phoenix CLI

The Phoenix CLI distributes skills to your projects:

**Recommended: Install once, use everywhere**

```bash
uv tool install phoenix-cli --from git+https://github.com/dauquangthanh/vinh-phoenix.git

### 2. Initialize Your Project

Install skills into your project:

```bash
phoenix init <PROJECT_NAME>
phoenix check
```

This installs all 18 skills into agent-specific folders (`.github/skills/`, `.claude/skills/`, etc.), making them discoverable by your AI assistant.

### 3. Work with Your AI Assistant

Launch your AI assistant and describe what you want to build. The AI will automatically discover and use the relevant skills:

```bash
# The AI assistant automatically activates relevant skills based on your request
"Specify a photo organizer with drag-and-drop albums"
"Design this using Next.js with TypeScript and Tailwind CSS"
"Break this down into actionable tasks"
"Implement the feature"
```

**Skills are loaded on demand** - when your task matches a skill's description, the AI reads the full instructions and follows them.

---

## 🌟 Development Workflows

Phoenix skills support both **Greenfield** (new projects) and **Brownfield** (existing projects) development:

```mermaid
flowchart LR
    Start([Project Type?])
    Start --> Greenfield[🌱 Greenfield<br/>New Project]
    Start --> Brownfield[🏗️ Brownfield<br/>Existing Project]
    
    Greenfield --> GF1[📋 Set Ground Rules<br/>Set Principles]
    GF1 --> GF2[🎯 Specify<br/>Define Features]
    GF2 --> GF3[🔍 Clarify<br/>Refine Requirements]
    GF3 --> GF4[📝 Architect<br/>System Design]
    GF4 --> GF5[📏 Standardize<br/>Coding Rules]
    GF5 --> GF6[🛠️ Design<br/>Technical Plan]
    GF6 --> GF7[📋 Taskify<br/>Break Down Tasks]
    GF7 --> GF8[⚡ Implement<br/>Build Features]
    GF8 --> GF9[✅ Test & Deploy]
    
    Brownfield --> BF1[📚 Assess Context<br/>Analyze Codebase]
    BF1 --> BF2[📋 Set Ground Rules<br/>Update Principles]
    BF2 --> BF3[🎯 Specify<br/>New Feature]
    BF3 --> BF4[🔍 Clarify<br/>Requirements]
    BF4 --> BF5[🛠️ Design<br/>Integration Plan]
    BF5 --> BF6[📋 Taskify<br/>Task Breakdown]
    BF6 --> BF7[⚡ Implement<br/>Add Feature]
    BF7 --> BF8[✅ Test & Deploy]
    
    style Greenfield fill:#90EE90
    style Brownfield fill:#87CEEB
    style GF8 fill:#FFD700
    style BF7 fill:#FFD700
```

**Greenfield** projects start with establishing principles, architecture, and standards. **Brownfield** projects begin with context assessment to understand existing patterns.

**Key Differences:**

| Aspect | 🌱 Greenfield | 🏗️ Brownfield |
|--------|--------------|---------------|
| **Starting Point** | Empty project | Existing codebase |
| **Setup Skill** | `project-ground-rules-setup` | `context-assessment` |
| **Focus** | Establish foundations first | Integrate with existing patterns |
| **Timeline** | 2-4 weeks (MVP) | 1-2 weeks per feature |
| **Flexibility** | Complete freedom in design | Must maintain consistency |
| **Skills Used** | All 18 skills available | Focus on 7-9 core skills |

---

Then use it anywhere:

```bash
phoenix init <PROJECT_NAME>
phoenix check
```

<p align="center">
  <img src="./media/vinh-phoenix.png" alt="Vinh Phoenix Installation" width="100%"/>
</p>

**Need to upgrade?** See the [Upgrade Guide](./docs/upgrade.md) or run:

```bash
uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git
```

```bash
uv tool install phoenix-cli --force --native-tls --from git+https://github.com/dauquangthanh/vinh-phoenix.git
```

<details>
<summary><strong>Alternative: Run without installing</strong></summary>

```bash
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <PROJECT_NAME>
```

```bash
uvx --native-tls --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <PROJECT_NAME>
```

**Why install?**

- ✅ Available everywhere in your terminal
- ✅ Easy to upgrade with `uv tool upgrade`
- ✅ Cleaner than shell aliases
- ✅ Better tool management

</details>

---

### Your First Project in 9 Steps

> **💡 Automatic Version Control:** All Phoenix commands automatically generate appropriate git commit messages and commit changes upon completion. Commands use semantic commit prefixes (`docs:`, `feat:`, `test:`, `chore:`) to maintain a clear project history.

#### 1️⃣ **Set Project Rules**

Launch your AI assistant in the project. Phoenix skills are now discoverable by the AI.

Ask the AI to create your project's guiding principles:

```bash
"Create project ground rules focused on code quality, testing standards, user experience consistency, and performance requirements"
```

#### 2️⃣ **Write the Specification**

Describe **what** you want to build and **why** (not the tech stack yet):

```bash
"Specify a photo organizer with albums grouped by date. 
Users can drag-and-drop albums to reorganize them. Albums show photos in a tile view. 
No nested albums allowed.
```

#### 3️⃣ **Clarify Requirements** *(Recommended)*

Ask the AI to clarify underspecified areas through structured questioning:

```bash
"Clarify the requirements, focusing on edge cases, data validation, and user experience details"
```

#### 4️⃣ **Design System Architecture** *(Optional, once per product)*

Document your system architecture:

```bash
"Create system architecture documentation with C4 diagrams, tech stack decisions, and architecture patterns"
```

#### 5️⃣ **Set Coding Standards** *(Optional, once per product)*

Create coding standards for your team:

```bash
"Define coding standards including naming conventions, file organization, and best practices"
```

#### 6️⃣ **Create Technical Design**

Now specify **how** to build it (tech stack and architecture):

```bash
"Design the technical implementation using Vite with vanilla HTML, CSS, and JavaScript. 
Keep libraries minimal. Store metadata in local SQLite. No image uploads.
```

#### 7️⃣ **Break Down Tasks**

Generate an actionable task list:

```bash
"Break this design down into actionable tasks"
```

#### 8️⃣ **Validate the Plan** *(Recommended)*

Check consistency and coverage before implementation:

```bash
"Analyze the plan for consistency and coverage"
```

#### 9️⃣ **Build It**

Execute all tasks automatically:

```bash
"Implement all the tasks according to the plan"
```

#### 🧪 **Test & Iterate**

Run your application and fix any issues. Your AI assistant will help debug.

---

**Want more details?** Read our [complete guide](./spec-driven.md).

## 🤖 Supported AI Agents

| Agent                                                     | Support | Notes                                             |
| ----------------------------------------------------------- | --------- |---------------------------------------------------|
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ | Amazon Q Developer CLI [does not support](https://github.com/aws/amazon-q-developer-cli/issues/3064) custom arguments for slash commands. |
| [Amp](https://ampcode.com/)                               | ✅ | |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview)   | ✅ |                                                   |
| [Claude Code](https://www.anthropic.com/claude-code)      | ✅ |                                                   |
| [CodeBuddy CLI](https://www.codebuddy.ai/cli)             | ✅ |                                                   |
| [Codex CLI](https://github.com/openai/codex)              | ✅ |                                                   |
| [Cursor](https://cursor.sh/)                              | ✅ |                                                   |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ |                                                   |
| [GitHub Copilot](https://code.visualstudio.com/)          | ✅ |                                                   |
| [Google Antigravity](https://ai.google.dev/)              | ✅ | IDE-based agent with slash command support |
| [IBM Bob](https://www.ibm.com/products/bob)               | ✅ | IDE-based agent with slash command support |
| [Jules](https://jules.google.com/)                        | ✅ | |
| [Kilo Code](https://github.com/Kilo-Org/kilocode)         | ✅ |                                                   |
| [opencode](https://opencode.ai/)                          | ✅ |                                                   |
| [Qoder CLI](https://qoder.ai)                             | ✅ |                                                   |
| [Qwen Code](https://github.com/QwenLM/qwen-code)          | ✅ |                                                   |
| [Roo Code](https://roocode.com/)                          | ✅ |                                                   |
| [SHAI (OVHcloud)](https://github.com/ovh/shai)            | ✅ | |
| [Windsurf](https://windsurf.com/)                         | ✅ |                                                   |

## 🔧 Phoenix CLI Reference

The `phoenix` command supports the following options:

### Commands

| Command     | Description                                                    |
| ------------- | ---------------------------------------------------------------- |
| `init`      | Initialize a new Phoenix project from the latest template      |
| `check`     | Check for installed tools (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`, `kilocode`, `auggie`, `roo`, `codebuddy`, `amp`, `shai`, `q`, `bob`, `jules`, `qoder`, `antigravity`) |
| `version`   | Display CLI version, template version, and system information  |

### `phoenix init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
| ------------------------ | ---------- |------------------------------------------------------------------------------|
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory) |
| `--ai`                 | Option   | AI assistant(s) to use. Can be a single agent or comma-separated list (e.g., `claude,gemini,copilot`). Valid options: `claude`, `gemini`, `copilot`, `cursor-agent`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, `codebuddy`, `amp`, `shai`, `q`, `bob`, `jules`, `qoder`, `antigravity`. If not specified, an interactive multi-select menu will appear |
| `--ignore-agent-tools` | Flag     | Skip checks for AI agent tools like Claude Code                             |
| `--no-git`             | Flag     | Skip git repository initialization                                          |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one   |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation) |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                 |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                            |
| `--github-token`       | Option   | GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)  |

### Examples

```bash
# Basic project initialization
phoenix init my-project

# Initialize with specific AI assistant
phoenix init my-project --ai claude

# Initialize with multiple AI assistants (comma-separated)
phoenix init my-project --ai claude,gemini,copilot

# Initialize with Cursor support
phoenix init my-project --ai cursor-agent

# Initialize with multiple agents including Windsurf and Amp
phoenix init my-project --ai windsurf,amp,claude

# Initialize with SHAI support
phoenix init my-project --ai shai

# Initialize with IBM Bob support
phoenix init my-project --ai bob

# Initialize in current directory
phoenix init . --ai copilot
# or use the --here flag
phoenix init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
phoenix init . --force --ai copilot
# or
phoenix init --here --force --ai copilot

# Skip git initialization
phoenix init my-project --ai gemini --no-git

# Enable debug output for troubleshooting
phoenix init my-project --ai claude --debug

# Use GitHub token for API requests (helpful for corporate environments)
phoenix init my-project --ai claude --github-token ghp_your_token_here

# Check system requirements
phoenix check

# Display version and system information
phoenix version
```

### Available Agent Skills

After running `phoenix init`, **18 agent skills** will be discoverable by your AI assistant, organized into categories:

- **Core Workflow Skills** - Complete development cycle from requirements to implementation
- **Product-Level Skills** - End-to-end testing (run once per product)
- **Enhancement Skills** - Project management and integration capabilities

#### How It Works: Skills-Based Architecture

**Phoenix uses the Agent Skills format** - an open standard for giving AI agents new capabilities:

- **Automatic Discovery** - At startup, agents load the name and description of each skill
- **On-Demand Activation** - When your task matches a skill's description, the AI loads full instructions
- **Progressive Disclosure** - Skills stay fast by loading context only when needed

**What gets installed:**

- 18 reusable skill modules (in `skills/`), each with its own templates and scripts
- Skills like `requirements-specification`, `technical-design`, `coding`, etc.
- Both bash and PowerShell scripts included automatically

**How agents use skills:**

1. You describe what you want to build
2. The AI identifies relevant skills based on descriptions
3. The AI loads skill instructions and follows them
4. Scripts and templates are used as needed

This modular design enables:

- **Multi-agent support** - 20+ AI assistants use the same skills format
- **Consistent workflows** - Same development process across different agents
- **Easy updates** - Upgrade all skills at once with `phoenix init --here --force`

After running `phoenix init`, your AI assistant can leverage these skills:

> **💡 Automatic Commits:** All commands automatically generate semantic commit messages and commit their changes upon completion, maintaining a clear project history without manual intervention.

#### Core Workflow Skills

Essential skills for the complete Spec-Driven Development workflow:

| Skill                  | When the AI Uses It                                                           | Auto Commit Prefix |
| -------------------------- | ----------------------------------------------------------------------- |--------------------|
| `project-ground-rules-setup`      | When you ask to create or update project principles and development guidelines | `docs:` |
| `context-assessment` | When you need to analyze an existing codebase's architecture and patterns | `docs:` |
| `requirements-specification`       | When you describe what you want to build (requirements and user stories)        | `docs:` |
| `requirements-specification-review`       | When you ask to clarify underspecified requirements through structured questioning | `docs:` |
| `architecture-design`         | When you request system architecture documentation with diagrams | `docs:` |
| `coding-standards`       | When you need coding standards and conventions documented | `docs:` |
| `technical-design`        | When you specify the tech stack and implementation approach     | `docs:` |
| `project-management`       | When you ask to break down a design into actionable tasks                     | `docs:` |
| `project-consistency-analysis`       | When you request analysis of plan consistency and coverage | `docs:` |
| `coding`     | When you ask to implement tasks according to a plan         | `feat:`, `fix:`, `test:` (context-dependent) |

#### Product-Level Skills

Skills for end-to-end testing (run once per product, not per feature):

| Skill                      | When the AI Uses It                                                           | Auto Commit Prefix |
| ------------------------------ | ----------------------------------------------------------------------- |--------------------|
| `e2e-test-design`   | When you request end-to-end test specifications for the product | `test:` |

#### Enhancement Skills

Additional skills for project management and integration:

| Skill                  | When the AI Uses It                                                           | Auto Commit Prefix |
| -------------------------- | ----------------------------------------------------------------------- |--------------------|
| `tasks-to-github-issues` | When you ask to convert tasks into GitHub issues with dependency tracking | `chore:` |
| `tasks-to-azure-devops`  | When you ask to convert tasks into Azure DevOps work items with dependencies | `chore:` |
| `git-commit` | When committing changes with semantic commit messages | varies |
| `code-review` | When you request code quality review and validation | n/a |

### Environment Variables

| Variable         | Description                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| `SPECIFY_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific feature when not using Git branches.<br/>**Must be set in the context of the agent you're working with prior to using `/phoenix.design` or follow-up commands. |

## 🎯 Why Spec-Driven Development?

Spec-Driven Development is built on these core principles:

| Principle | What It Means |
| ----------- | --------------- |
| **Intent First** | Define the "*what*" and "*why*" before the "*how*" |
| **Rich Specifications** | Create detailed specs with organizational principles and guardrails |
| **Step-by-Step Refinement** | Improve through multiple steps, not one-shot generation |
| **AI-Powered** | Use advanced AI to interpret specifications and generate implementations |

---

## 🌟 When to Use Spec-Driven Development

Vinh Phoenix supports three main development scenarios with different workflows:

### Development Workflows Overview

```mermaid
flowchart TB
    subgraph Greenfield["🌱 GREENFIELD: New Applications (2-4 weeks)"]
        direction TB
        GF1[📋 Set Ground Rules: Set Principles] --> GF2[🎯 Specify: Feature Requirements]
        GF2 --> GF3[🔍 Clarify: Refine Spec]
        GF3 --> GF4[📝 Architect: System Design]
        GF4 --> GF5[📏 Standardize: Coding Standards]
        GF5 --> GF6[🛠️ Design: Technical Plan]
        GF6 --> GF7[📋 Taskify: Break Down]
        GF7 --> GF8[⚡ Implement: Build It]
        GF8 --> GF9[✅ Test & Deploy]
    end
    
    subgraph Brownfield["🏗️ BROWNFIELD: Existing Apps (1-2 weeks/feature)"]
        direction TB
        BF1[📚 Assess Context: Analyze Codebase] --> BF2[📋 Set Ground Rules: Update Principles]
        BF2 --> BF3[🎯 Specify: New Feature]
        BF3 --> BF4[🔍 Clarify: Requirements]
        BF4 --> BF5[🛠️ Design: Integration Plan]
        BF5 --> BF6[📋 Taskify: Task List]
        BF6 --> BF7[⚡ Implement: Add Feature]
        BF7 --> BF8[✅ Test & Deploy]
    end
    
    style Greenfield fill:#E8F5E9
    style Brownfield fill:#E3F2FD
    style GF8 fill:#FFD700
    style BF7 fill:#FFD700
```

| Scenario | What You Can Do |
| ---------- | ----------------- |
| **🆕 New Projects (Greenfield)** | <ul><li>Start with high-level requirements</li><li>Establish project principles and architecture</li><li>Generate complete specifications</li><li>Plan implementation steps</li><li>Build production-ready apps with clear standards</li></ul> |
| **🔧 Existing Projects (Brownfield)** | <ul><li>Add new features systematically to existing codebases</li><li>Maintain consistency with existing patterns</li><li>Adapt the SDD process to your current architecture</li><li>Integrate new functionality smoothly</li></ul> |
| **🔬 Exploration** | <ul><li>Try different solutions in parallel</li><li>Test multiple tech stacks</li><li>Experiment with UX patterns</li><li>Rapid prototyping and validation</li></ul> |

---

## 🔬 What We're Exploring

Our experiments focus on making Spec-Driven Development work for real teams:

- **🔧 Tech Independence** - Build apps with any tech stack, proving this process works across languages and frameworks
- **🏢 Enterprise Ready** - Support organizational constraints: cloud providers, compliance requirements, design systems
- **👥 User Focused** - Build for different user needs and development styles (from exploratory coding to structured workflows)
- **🔄 Iterative & Creative** - Enable parallel exploration of solutions and robust workflows for modernization

---

## ⚙️ What You Need

Before you start, make sure you have:

- **Operating System:** Linux, macOS, or Windows
- **AI Assistant:** Any [supported agent](#-supported-ai-agents) (Claude, Gemini, Copilot, Cursor, etc.)
- **Package Manager:** [uv](https://docs.astral.sh/uv/)
- **Python:** [Version 3.11 or higher](https://www.python.org/downloads/)
- **Version Control:** [Git](https://git-scm.com/downloads)

> Having issues with an agent? [Open an issue](https://github.com/dauquangthanh/vinh-phoenix/issues/new) so we can improve it.

## 📚 Learn More

### Choose Your Workflow

```mermaid
flowchart TD
    Start{What are you<br/>building?}
    
    Start -->|Brand new application| GF[🌱 Greenfield Workflow]
    Start -->|Adding to existing app| BF[🏗️ Brownfield Workflow]
    
    GF --> GFDesc["<b>Timeline:</b> 2-4 weeks<br/><b>Steps:</b> Set Ground Rules → Specify →<br/>Architect → Standardize →<br/>Design → Taskify → Implement"]
    BF --> BFDesc["<b>Timeline:</b> 1-2 weeks/feature<br/><b>Steps:</b> Assess Context →<br/>Set Ground Rules → Specify → Design → Implement"]
    
    style GF fill:#90EE90
    style BF fill:#87CEEB
    style GFDesc fill:#E8F5E9
    style BFDesc fill:#E3F2FD
```

**Quick Links:**

- 💬 [Get Support](https://github.com/dauquangthanh/vinh-phoenix/issues/new) - Ask questions or report issues
- 📄 [View License](./LICENSE) - MIT License
- 🌟 [Star on GitHub](https://github.com/dauquangthanh/vinh-phoenix) - Support the project

---

## 📋 Detailed Process

<details>
<summary>Click to expand the detailed step-by-step walkthrough</summary>

### Project Setup

You can use the Phoenix CLI to bootstrap your project, which will bring in the required artifacts in your environment. Run:

```bash
phoenix init <project_name>
```

Or initialize in the current directory:

```bash
phoenix init .
# or use the --here flag
phoenix init --here
# Skip confirmation when the directory already has files
phoenix init . --force
# or
phoenix init --here --force

phoenix init <project_name> --ai claude
phoenix init <project_name> --ai gemini
phoenix init <project_name> --ai copilot

# Or in current directory:
phoenix init . --ai claude
phoenix init . --ai codex

# or use --here flag
phoenix init --here --ai claude
phoenix init --here --ai codex

# Force merge into a non-empty current directory
phoenix init . --force --ai claude

# or
phoenix init --here --force --ai claude
```

The CLI will check if you have Claude Code, Gemini CLI, Cursor CLI, Qwen CLI, opencode, Codex CLI, or Amazon Q Developer CLI installed. If you do not, or you prefer to get the templates without checking for the right tools, use `--ignore-agent-tools` with your command:

```bash
phoenix init <project_name> --ai claude --ignore-agent-tools
```

---

### 🌱 Greenfield Workflow (New Projects)

For new projects starting from scratch, follow these steps:

#### **STEP 1:** Establish project principles

Go to the project folder and run your AI agent. In our example, we're using `claude`.

You will know that things are configured correctly if you see the `/phoenix.set-ground-rules`, `/phoenix.specify`, `/phoenix.design`, `/phoenix.taskify`, and `/phoenix.implement` commands available.

The first step should be establishing your project's governing principles using the `/phoenix.set-ground-rules` command. This helps ensure consistent decision-making throughout all subsequent development phases:

```text
/phoenix.set-ground-rules Create principles focused on code quality, testing standards, user experience consistency, and performance requirements. Include governance for how these principles should guide technical decisions and implementation choices.
```

This step creates or updates the `docs/ground-rules.md` file with your project's foundational guidelines that the AI agent will reference during specification, planning, and implementation phases.

#### **STEP 2:** Create project specifications

With your project principles established, you can now create the functional specifications. Use the `/phoenix.specify` command and then provide the concrete requirements for the project you want to develop.

>[!IMPORTANT]
>Be as explicit as possible about *what* you are trying to build and *why*. **Do not focus on the tech stack at this point**.

An example prompt:

```text
Develop Taskify, a team productivity platform. It should allow users to create projects, add team members,
assign tasks, comment and move tasks between boards in Kanban style. In this initial phase for this feature,
let's call it "Create Taskify," let's have multiple users but the users will be declared ahead of time, predefined.
I want five users in two different categories, one product manager and four engineers. Let's create three
different sample projects. Let's have the standard Kanban columns for the status of each task, such as "To Do,"
"In Progress," "In Review," and "Done." There will be no login for this application as this is just the very
first testing thing to ensure that our basic features are set up. For each task in the UI for a task card,
you should be able to change the current status of the task between the different columns in the Kanban work board.
You should be able to leave an unlimited number of comments for a particular card. You should be able to, from that task
card, assign one of the valid users. When you first launch Taskify, it's going to give you a list of the five users to pick
from. There will be no password required. When you click on a user, you go into the main view, which displays the list of
projects. When you click on a project, you open the Kanban board for that project. You're going to see the columns.
You'll be able to drag and drop cards back and forth between different columns. You will see any cards that are
assigned to you, the currently logged in user, in a different color from all the other ones, so you can quickly
see yours. You can edit any comments that you make, but you can't edit comments that other people made. You can
delete any comments that you made, but you can't delete comments anybody else made.
```

After this prompt is entered, you should see Claude Code kick off the planning and spec drafting process. Claude Code will also trigger some of the built-in scripts to set up the repository.

Once this step is completed, you should have a new branch created (e.g., `001-create-taskify`), as well as a new specification in the `specs/001-create-taskify` directory.

The produced specification should contain a set of user stories and functional requirements, as defined in the template.

At this stage, your project folder contents should resemble the following:

```text
└── docs
    └── ground-rules.md
└── specs
   └── 001-create-taskify
       └── spec.md
```

#### **STEP 3:** Functional specification clarification (required before planning)

With the baseline specification created, you can go ahead and clarify any of the requirements that were not captured properly within the first shot attempt.

You should run the structured clarification workflow **before** creating a technical plan to reduce rework downstream.

Preferred order:

1. Use `/phoenix.clarify` (structured) – sequential, coverage-based questioning that records answers in a Clarifications section.
2. Optionally follow up with ad-hoc free-form refinement if something still feels vague.

If you intentionally want to skip clarification (e.g., spike or exploratory prototype), explicitly state that so the agent doesn't block on missing clarifications.

Example free-form refinement prompt (after `/phoenix.clarify` if still needed):

```text
For each sample project or project that you create there should be a variable number of tasks between 5 and 15
tasks for each one randomly distributed into different states of completion. Make sure that there's at least
one task in each stage of completion.
```

You should also ask Claude Code to validate the **Review & Acceptance Checklist**, checking off the things that are validated/pass the requirements, and leave the ones that are not unchecked. The following prompt can be used:

```text
Read the review and acceptance checklist, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not.
```

It's important to use the interaction with Claude Code as an opportunity to clarify and ask questions around the specification - **do not treat its first attempt as final**.

#### **STEP 4:** Generate a plan

You can now be specific about the tech stack and other technical requirements. You can use the `/phoenix.design` command that is built into the project template with a prompt like this:

```text
We are going to generate this using .NET Aspire, using Postgres as the database. The frontend should use
Blazor server with drag-and-drop task boards, real-time updates. There should be a REST API created with a projects API,
tasks API, and a notifications API.
```

The output of this step will include a number of implementation detail documents, with your directory tree resembling this:

```text
.
├── specs
│  └── 001-create-taskify
│      ├── contracts
│      │  ├── api-spec.json
│      │  └── signalr-spec.md
│      ├── data-model.md
│      ├── plan.md
│      ├── quickstart.md
│      ├── research.md
│      └── spec.md
└── docs/
    └── ground-rules.md
```

Check the `research.md` document to ensure that the right tech stack is used, based on your instructions. You can ask Claude Code to refine it if any of the components stand out, or even have it check the locally-installed version of the platform/framework you want to use (e.g., .NET).

Additionally, you might want to ask Claude Code to research details about the chosen tech stack if it's something that is rapidly changing (e.g., .NET Aspire, JS frameworks), with a prompt like this:

```text
I want you to go through the implementation plan and implementation details, looking for areas that could
benefit from additional research as .NET Aspire is a rapidly changing library. For those areas that you identify that
require further research, I want you to update the research document with additional details about the specific
versions that we are going to be using in this Taskify application and spawn parallel research tasks to clarify
any details using research from the web.
```

During this process, you might find that Claude Code gets stuck researching the wrong thing - you can help nudge it in the right direction with a prompt like this:

```text
I think we need to break this down into a series of steps. First, identify a list of tasks
that you would need to do during implementation that you're not sure of or would benefit
from further research. Write down a list of those tasks. And then for each one of these tasks,
I want you to spin up a separate research task so that the net results is we are researching
all of those very specific tasks in parallel. What I saw you doing was it looks like you were
researching .NET Aspire in general and I don't think that's gonna do much for us in this case.
That's way too untargeted research. The research needs to help you solve a specific targeted question.
```

>[!NOTE]
>Claude Code might be over-eager and add components that you did not ask for. Ask it to clarify the rationale and the source of the change.

#### **STEP 5:** Have Claude Code validate the plan

With the plan in place, you should have Claude Code run through it to make sure that there are no missing pieces. You can use a prompt like this:

```text
Now I want you to go and audit the implementation plan and the implementation detail files.
Read through it with an eye on determining whether or not there is a sequence of tasks that you need
to be doing that are obvious from reading this. Because I don't know if there's enough here. For example,
when I look at the core implementation, it would be useful to reference the appropriate places in the implementation
details where it can find the information as it walks through each step in the core implementation or in the refinement.
```

This helps refine the implementation plan and helps you avoid potential blind spots that Claude Code missed in its planning cycle. Once the initial refinement pass is complete, ask Claude Code to go through the checklist once more before you can get to the implementation.

You can also ask Claude Code (if you have the [GitHub CLI](https://docs.github.com/en/github-cli/github-cli) installed) to go ahead and create a pull request from your current branch to `main` with a detailed description, to make sure that the effort is properly tracked.

>[!NOTE]
>Before you have the agent implement it, it's also worth prompting Claude Code to cross-check the details to see if there are any over-engineered pieces (remember - it can be over-eager). If over-engineered components or decisions exist, you can ask Claude Code to resolve them. Ensure that Claude Code follows the [ground rules](base/docs/ground-rules.md) as the foundational piece that it must adhere to when establishing the plan.

#### **STEP 6:** Generate task breakdown with /phoenix.taskify

With the implementation plan validated, you can now break down the plan into specific, actionable tasks that can be executed in the correct order. Use the `/phoenix.taskify` command to automatically generate a detailed task breakdown from your implementation plan:

```text
/phoenix.taskify
```

This step creates a `tasks.md` file in your feature specification directory that contains:

- **Task breakdown organized by user story** - Each user story becomes a separate implementation phase with its own set of tasks
- **Dependency management** - Tasks are ordered to respect dependencies between components (e.g., models before services, services before endpoints)
- **Parallel execution markers** - Tasks that can run in parallel are marked with `[P]` to optimize development workflow
- **File path specifications** - Each task includes the exact file paths where implementation should occur
- **Test-driven development structure** - If tests are requested, test tasks are included and ordered to be written before implementation
- **Checkpoint validation** - Each user story phase includes checkpoints to validate independent functionality

The generated tasks.md provides a clear roadmap for the `/phoenix.implement` command, ensuring systematic implementation that maintains code quality and allows for incremental delivery of user stories.

#### **STEP 7:** Implementation

Once ready, use the `/phoenix.implement` command to execute your implementation plan:

```text
/phoenix.implement
```

The `/phoenix.implement` command will:

- Validate that all prerequisites are in place (ground-rules, spec, plan, and tasks)
- Parse the task breakdown from `tasks.md`
- Execute tasks in the correct order, respecting dependencies and parallel execution markers
- Follow the TDD approach defined in your task plan
- Provide progress updates and handle errors appropriately

>[!IMPORTANT]
>The AI agent will execute local CLI commands (such as `dotnet`, `npm`, etc.) - make sure you have the required tools installed on your machine.

Once the implementation is complete, test the application and resolve any runtime errors that may not be visible in CLI logs (e.g., browser console errors). You can copy and paste such errors back to your AI agent for resolution.

---

### 🏗️ Brownfield Workflow (Existing Projects)

For adding new features to existing codebases, follow this streamlined workflow:

#### **STEP 1:** Assess existing codebase

Start by analyzing the existing codebase to understand its architecture, patterns, and conventions:

```text
/phoenix.assess-context
```

This command performs a comprehensive analysis of your codebase and creates `docs/context-assessment.md` that documents:

- **Technology Stack** - Languages, frameworks, libraries, and tools in use
- **Project Structure** - Directory organization and architectural layers
- **Architecture Patterns** - Design patterns, component relationships, and communication patterns
- **Coding Conventions** - Naming conventions, file organization, and code quality practices
- **Data Layer** - ORM/query patterns, schema design, and data access patterns
- **API Patterns** - Endpoint structure, authentication, and integration patterns
- **Testing Strategy** - Test organization, coverage, and testing patterns
- **Build & Deployment** - Build process, environment configuration, and deployment strategy
- **Technical Health Score** - Overall assessment with strengths and improvement areas
- **Feature Integration Readiness** - Guidance for adding new features consistently

>[!NOTE]
>The context assessment serves as the foundation for all subsequent steps. It helps ensure that new features integrate seamlessly with existing patterns and maintain codebase consistency.

#### **STEP 2:** Update project principles

With the codebase context understood, update or establish project principles that align with the existing architecture:

```text
/phoenix.set-ground-rules Review the context assessment and update project principles to align with the existing codebase patterns. 
Ensure principles cover code quality standards found in the assessment, testing practices currently in use, 
and architectural decisions that should guide new feature development.
```

This step creates or updates `docs/ground-rules.md` to reflect:

- Coding standards and conventions discovered in the codebase
- Architectural patterns and design principles in use
- Testing practices and quality standards
- Integration guidelines for maintaining consistency

>[!TIP]
>The `/phoenix.set-ground-rules` command in brownfield projects should reference the context assessment to ensure principles align with existing practices rather than imposing new ones.

#### **STEP 3:** Create feature specification

With both the codebase context and updated principles established, specify the new feature you want to add:

```text
/phoenix.specify Add a user notification system that sends email alerts when tasks are assigned. 
Users can configure notification preferences (immediate, daily digest, or disabled) in their profile settings.
```

The AI agent will reference the context assessment and updated principles to ensure the specification aligns with existing patterns and architecture.

#### **STEP 4:** Clarify requirements

Use the clarification workflow to refine the specification:

```text
/phoenix.clarify
```

This ensures all edge cases and integration points with the existing system are properly defined.

#### **STEP 5:** Design integration plan

Create a technical plan that integrates with the existing architecture:

```text
/phoenix.design Follow the existing email service pattern identified in the context assessment. 
Use the current user preference storage approach. Integrate with the existing task assignment workflow.
```

The plan will reference existing components, patterns, and conventions from the context assessment.

#### **STEP 6:** Generate task breakdown

Break down the implementation into specific tasks:

```text
/phoenix.taskify
```

Tasks will be organized to integrate with existing code while maintaining consistency with established patterns.

#### **STEP 7:** Implement the feature

Execute the implementation plan:

```text
/phoenix.implement
```

The AI agent will build the feature following existing coding conventions and integration patterns identified in the context assessment and established principles.

#### **STEP 8:** Test and validate

Test the new feature in the context of the existing application. Ensure it integrates properly with existing functionality and doesn't break existing workflows.
</details>

---

## � Project Structure

After running `phoenix init`, your project will have the following structure:

```
<project-root>/
├── .<agent-folder>/       # Agent-specific folder (e.g., .claude/, .github/, .gemini/)
│   └── phoenix.*.md       # 15 Phoenix agent skills
│
├── .<agent-folder>/skills/  # Agent-specific skills (reusable capabilities)
│   ├── architecture-design/
│   │   ├── SKILL.md       # Skill documentation
│   │   ├── templates/     # Reusable templates for this skill
│   │   └── scripts/       # Automation scripts (bash & PowerShell)
│   ├── coding/
│   ├── context-assessment/
│   ├── nextjs-mockup/
│   └── ... (18 skills total for various development tasks)
│
├── docs/                  # Project documentation (created by commands)
│   ├── ground-rules.md    # Project principles (created by /phoenix.set-ground-rules)
│   ├── architecture.md    # System architecture (created by /phoenix.architect)
│   └── standards.md       # Coding standards (created by /phoenix.standardize)
│
└── specs/                 # Your feature specifications (created as you work)
    └── <feature-name>/
        ├── spec.md        # Requirements and user stories
        ├── plan.md        # Technical implementation plan
        ├── tasks.md       # Task breakdown for execution
        └── research.md    # Tech stack research notes
```

**Key Folders:**

- **`.<agent>/`** - Agent skills and configuration (`.claude/`, `.github/`, `.gemini/`, etc.)
- **`.<agent>/skills/`** - Reusable skill modules (18 total, each with templates & scripts)
- **`docs/`** - Project-level documentation (ground-rules, architecture, standards)
- **`specs/`** - Your feature specifications (grows as you build)

### 🧩 Available Skills

Phoenix includes **18 reusable skills** that power your AI assistant:

| Skill Module | Powers Command(s) | Purpose |
| -------------- | ------------------- | --------- |
| `requirements-specification` | `/phoenix.specify` | Create feature specifications from natural language |
| `requirements-specification-review` | `/phoenix.clarify` | Structured clarification workflow |
| `technical-design` | `/phoenix.design` | Generate implementation plans with tech stack |
| `technical-design-review` | `/phoenix.analyze` | Validate design consistency and coverage |
| `project-management` | `/phoenix.taskify` | Break down designs into actionable tasks |
| `coding` | `/phoenix.implement` | Execute tasks and build features |
| `architecture-design` | `/phoenix.architect` | Document system architecture (C4 diagrams) |
| `architecture-design-review` | *(validation)* | Review architecture completeness |
| `coding-standards` | `/phoenix.standardize` | Create coding conventions and standards |
| `e2e-test-design` | `/phoenix.design-e2e-test` | Design end-to-end test specifications |
| `project-ground-rules-setup` | `/phoenix.set-ground-rules` | Establish project principles |
| `context-assessment` | `/phoenix.assess-context` | Analyze existing codebases (brownfield) |
| `project-consistency-analysis` | `/phoenix.analyze` | Check cross-artifact consistency |
| `code-review` | *(quality checks)* | Code review automation |
| `git-commit` | *(auto-commits)* | Generate semantic commit messages |
| `tasks-to-github-issues` | `/phoenix.tasks-to-issues` | Sync tasks to GitHub issues |
| `tasks-to-azure-devops` | `/phoenix.tasks-to-ado` | Sync tasks to Azure DevOps |
| `nextjs-mockup` / `nuxtjs-mockup` | *(rapid prototyping)* | Generate framework-specific mockups |

**Skills are framework-agnostic** - they work with any tech stack and support 20+ AI agents through a common interface.

**Note:** Agent-specific folders (like `.github/skills/`, `.claude/skills/`) are auto-managed by the Phoenix CLI. You primarily work in `specs/` for your features.

---

## �🛠️ Troubleshooting

### Git Authentication on Linux

Having trouble with Git authentication? Install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e

# Download Git Credential Manager
echo "⬇️ Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb

# Install
echo "📦 Installing..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb

# Configure Git
echo "⚙️ Configuring Git..."
git config --global credential.helper manager

# Clean up
echo "🧹 Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb

echo "✅ Done! Git Credential Manager is ready."
```

---

## 👥 Project Team

**Maintainer:** Dau Quang Thanh ([@dauquangthanh](https://github.com/dauquangthanh))

---

## 💬 Get Help

Need assistance? We're here to help:

- 🐛 **Bug Reports:** [Open an issue](https://github.com/dauquangthanh/vinh-phoenix/issues/new)
- 💡 **Feature Requests:** [Open an issue](https://github.com/dauquangthanh/vinh-phoenix/issues/new)
- ❓ **Questions:** [Open a discussion](https://github.com/dauquangthanh/vinh-phoenix/discussions)

---

## 🙏 Credits

This project is inspired by and builds upon [Spec-Kit](https://github.com/github/spec-kit).

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

**Open source and free to use.** Contributions welcome!
