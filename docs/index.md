# 🔥 Vinh Phoenix

## *Core Installer Framework for AI Agent Skills*

**A lightweight CLI that bootstraps AI coding assistants with core meta-skills, then lets you extend with skills and agents from any configured repository.**

---

## 💡 What is Vinh Phoenix?

**Vinh Phoenix is a core installer framework** — not a fixed skills library.

`phoenix init` installs **5 core meta-skills** into your project and drops a `nightlife.yaml` configuration file. From there, your AI assistant uses those meta-skills to browse and install additional skills and agent commands from any configured repository.

- **Meta-skills** - Discover and install more skills/agents on demand
- **nightlife.yaml** - Points to GitHub issues or Azure DevOps files as skill catalogs
- **Extensible** - Configure your own private repos in `nightlife.yaml`

> **Think of Phoenix as a package manager for AI skills:** It installs the tooling to discover and install skills. You decide what goes into your project.

## 🚀 Getting Started

**New to Vinh Phoenix?** Follow these guides:

| Guide | Description |
|-------|-------------|
| 📦 [Installation Guide](installation.md) | Set up Phoenix CLI and prerequisites |
| ⚡ [Quick Start Guide](quickstart.md) | Bootstrap your project and add skills |
| 🔄 [Upgrade Guide](upgrade.md) | Update to the latest version |
| 💻 [Local Development](local-development.md) | Contribute and develop locally |

---

## 📦 Core Meta-Skills (Installed by Default)

After `phoenix init`, your AI assistant automatically discovers these 5 skills:

| Skill | When the AI Uses It |
|-------|---------------------|
| `git-commit` | When you ask to commit changes or generate a commit message |
| `list-skills` | When you ask what skills are available or want to browse the catalog |
| `add-skills` | When you ask to install or download skills |
| `list-agents` | When you ask what agent commands are available |
| `add-agents` | When you ask to install or download agent commands |

---

## 🔧 Extending Your Project

Use the meta-skills to add whatever you need:

```
"List available skills"       → list-skills reads nightlife.yaml, queries repos, shows catalog
"Install requirements-specification and coding"  → add-skills downloads & installs
"Show available agent commands"  → list-agents shows what's in configured repos
"Add the specify agent command"  → add-agents downloads & installs
```

---

## 📄 nightlife.yaml

`nightlife.yaml` (placed in your project root) tells the meta-skills where to find skill and agent catalogs. It supports both **GitHub** and **Azure DevOps** as catalog sources:

```yaml
urls:
  # GitHub issue (issue body contains YAML repo list)
  - https://github.com/DauQuangThanh/vinh-phoenix/issues/2
  # Azure DevOps file (YAML file in a repo)
  # - https://dev.azure.com/myorg/myproject/_git/myrepo?path=/catalog.yaml&version=GBmain
```

Each URL points to a catalog source whose body/content lists skill repositories. Update these URLs to use your own catalogs.

---

## 🧩 Architecture: Agent Skills Standard

Vinh Phoenix uses the [Agent Skills format](https://agentskills.io) — an open standard for giving AI agents new capabilities:

**How It Works:**

1. **Discovery** - At startup, agents load the name and description of each skill
2. **Activation** - When your task matches a skill's description, the AI loads full instructions
3. **Execution** - The AI follows instructions, using templates and scripts as needed

**What Gets Installed by `phoenix init`:**

- 5 core meta-skills in agent-specific folders (`.github/skills/`, `.claude/skills/`, etc.)
- `nightlife.yaml` in project root for catalog configuration
- Each skill has SKILL.md (instructions), scripts (bash & PowerShell)

This architecture enables:

- ✅ Progressive disclosure — skills load context only when needed
- ✅ Multi-agent support — 19 AI assistants use the same skills format
- ✅ Easy updates — upgrade with `phoenix init --upgrade`
- ✅ Custom catalogs — point `nightlife.yaml` at your own repos

---

## 🎯 Core Philosophy

Phoenix enables **extensible, on-demand skill management**:

| Principle | What It Means |
|-----------|---------------|
| **Start Minimal** | Only the essentials are installed by default |
| **Grow On Demand** | Add skills as you need them via `add-skills` |
| **Stay in Control** | Configure your own repos in `nightlife.yaml` |
| **Multi-Agent** | Same skills work across 19 AI assistants |

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
