# ⚡ Quick Start Guide

**Get started with Phoenix skills in your development workflow.**

---

## 🎯 What You'll Learn

This guide shows you how to:

1. Install Phoenix skills into your project
2. Use skills through slash commands in your AI assistant
3. Follow a structured development workflow

Phoenix provides **18 reusable skills** that guide your AI assistant through software development tasks.

---

## 🚀 Installation

### Step 1: Install Phoenix CLI

The CLI distributes skills to your projects:

```bash
# Create a new project
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <PROJECT_NAME>

# OR work in current directory
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init .
```

This installs all 18 skills into agent-specific folders, making them available as slash commands.

---

## 🎯 The 9-Step Workflow

Each step uses a specific skill from the library:

> **💡 Automatic Version Control:** All skills automatically generate semantic git commit messages and commit changes upon completion.

| Step | Command | Skill Used | Purpose |
| ------ | --------- |------------|----------|
| 1️⃣ | `/phoenix.set-ground-rules` | `project-ground-rules-setup` | Set project principles |
| 2️⃣ | `/phoenix.specify` | `requirements-specification` | Define requirements |
| 3️⃣ | `/phoenix.clarify` | `requirements-specification-review` | Clarify unclear areas |
| 4️⃣ | `/phoenix.architect` | `architecture-design` | Design system architecture |
| 5️⃣ | `/phoenix.standardize` | `coding-standards` | Create coding standards |
| 6️⃣ | `/phoenix.design` | `technical-detailed-design` | Create implementation plan |
| 7️⃣ | `/phoenix.taskify` | `task-management` | Break down into tasks |
| 8️⃣ | `/phoenix.analyze` | `technical-detailed-design-review` | Validate consistency |
| 9️⃣ | `/phoenix.implement` | `coding` | Build features! |

> **💡 Smart Context:** Phoenix skills automatically detect your active feature from your Git branch (like `001-feature-name`).

---

## 🧩 Understanding Skills

**Each slash command is powered by a modular skill:**

- **18 Skills Total** - Covering all phases of development
- **Self-Contained** - Each skill has templates, scripts, and documentation
- **Cross-Platform** - Both bash and PowerShell scripts included
- **Multi-Agent** - Same skills work with 20+ AI assistants

**Installed Locations:**

- `.github/skills/` for GitHub Copilot
- `.claude/skills/` for Claude Code
- `.gemini/extensions/` for Gemini CLI
- *(and 17 more agent-specific locations)*

---

## 🚀 Step-by-Step Example

### Step 1: Set Project Principles

Use the `project-ground-rules-setup` skill to establish your project's foundation:

```bash
/phoenix.set-ground-rules This project follows a "Library-First" approach. All features must be implemented as standalone libraries first. We use TDD strictly. We prefer functional programming patterns.
```

**What this does:** The skill creates `docs/ground-rules.md` with principles that guide all development decisions.

---

### Step 2: Write Requirements

Use the `requirements-specification` skill to capture what you want to build:

```bash
/phoenix.specify Build a photo organizer app. Albums are grouped by date and can be reorganized by drag-and-drop. Each album shows photos in a tile view. No nested albums allowed.
```

**Focus on:** User needs, features, and behavior—the skill handles structuring this into formal specifications.

---

### Step 3: Design System Architecture *(Optional)*

Use the `architecture-design` skill to document system-level decisions:

```bash
/phoenix.architect Document the system architecture including C4 diagrams, microservices design, and technology stack decisions.
```

**Best for:** Product-level architecture (run once per product, not per feature).

---

### Step 4: Set Coding Standards *(Optional)*

Use the `coding-standards` skill to establish team conventions:

```bash
/phoenix.standardize Create comprehensive coding standards for TypeScript and React, including naming conventions and best practices.
```

---

### Step 6: Refine Your Spec *(Optional)*

Clarify any unclear requirements:

```bash
/phoenix.clarify Focus on security and performance requirements.
```

---

### Step 7: Create Technical Design

Now specify **how** to build it (tech stack and architecture):

```bash
/phoenix.design Use Vite with minimal libraries. Stick to vanilla HTML, CSS, and JavaScript. Store metadata in local SQLite. No image uploads.
```

**What to include:** Tech stack, frameworks, libraries, database choices, architecture patterns.

---

### Step 8: Break Down & Build

**Create tasks:**

```bash
/phoenix.taskify
```

**Validate the plan (optional):**

```bash
/phoenix.analyze
```

**Build it:**

```bash
/phoenix.implement
```

**What happens:** Your AI agent executes all tasks in order, building your application according to the plan.

---

## 📖 Complete Example: Building Taskify

**Project:** A team productivity platform with Kanban boards.

### 1. Set Ground Rules

```bash
/phoenix.set-ground-rules Taskify is "Security-First". Validate all user inputs. Use microservices architecture. Document all code thoroughly.
```

### 2. Define Requirements

```bash
/phoenix.specify Build Taskify, a team productivity platform. Users can create projects, add team members, assign tasks, comment, and move tasks between Kanban boards. Start with 5 predefined users: 1 product manager and 4 engineers. Create 3 sample projects. Use standard Kanban columns: To Do, In Progress, In Review, Done. No login required for this initial version.
```

### 3. Refine with Details

```bash
/phoenix.clarify For task cards: users can change status by dragging between columns, leave unlimited comments, and assign tasks to any user. Show a user picker on launch. Clicking a user shows their projects. Clicking a project opens the Kanban board. Highlight tasks assigned to current user in different color. Users can edit/delete only their own comments.
```

### 4. Validate Specification

```bash
/phoenix.checklist
```

### 5. Create Technical Plan

```bash
/phoenix.design Use .NET Aspire with Postgres database. Frontend: Blazor server with drag-and-drop and real-time updates. Create REST APIs for projects, tasks, and notifications.
```

### 6. Validate and Build

```bash
/phoenix.analyze
/phoenix.implement
```

---

## 🎯 Key Principles

| Principle | What It Means |
| ----------- | --------------- |
| **Be Explicit** | Clearly describe what and why you're building |
| **Skip Tech Early** | Don't worry about tech stack during specification |
| **Iterate** | Refine specs before implementation |
| **Validate First** | Check the plan before coding |
| **Let AI Work** | Trust the agent to handle implementation details |

---

## 📚 Next Steps

**Learn more:**

- 📖 [Complete Methodology](../spec-driven.md) - Deep dive into the full process
- 🔍 [More Examples](../templates) - Explore sample projects
- 💻 [Source Code](https://github.com/dauquangthanh/vinh-phoenix) - Contribute to the project

**Get help:**

- 🐛 [Report Issues](https://github.com/dauquangthanh/vinh-phoenix/issues/new) - Found a bug?
- 💬 [Ask Questions](https://github.com/dauquangthanh/vinh-phoenix/discussions) - Need help?
