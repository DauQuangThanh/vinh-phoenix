# ⚡ Quick Start Guide

**Bootstrap your project with core meta-skills, then add what you need.**

---

## 🎯 What You'll Learn

This guide shows you how to:

1. Initialize a project with Phoenix's core meta-skills
2. Use meta-skills to browse and install additional skills
3. Configure `nightlife.yaml` to use custom skill repositories

---

## 🚀 Step 1: Initialize Your Project

```bash
# Create a new project
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <PROJECT_NAME> --ai claude

# OR initialize in current directory
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init --here --ai claude
```

This installs **5 core meta-skills** into the agent-specific folder and places `nightlife.yaml` in your project root.

**What's installed:**

```
<project-root>/
├── .claude/skills/         (for Claude Code)
│   ├── git-commit/
│   ├── list-skills/
│   ├── add-skills/
│   ├── list-agents/
│   └── add-agents/
└── nightlife.yaml
```

---

## 🔍 Step 2: Browse Available Skills

Launch your AI assistant and ask it to show what's available:

```text
"List available skills"
```

The `list-skills` meta-skill reads `nightlife.yaml`, queries each configured repository, and shows you all installable skills.

Example output:

```
Repository: DaNangNightlifeSkill (https://github.com/owner/repo-a, branch: main, path: skills)
  - requirements-specification
  - requirements-specification-review
  - technical-detailed-design
  - task-management
  - coding
  - code-review
  - git-commit
  - ... (more)
  Total: N skills available

Repository: VinhPhoenixSkill (https://github.com/owner/repo-b, branch: main, path: skills)
  - pdf
  - bug-analysis
  Total: M skills available

Grand total: X skills across 2 repositories
```

---

## ➕ Step 3: Install the Skills You Need

Ask your AI to install specific skills:

```text
"Install the requirements-specification, technical-detailed-design, task-management, and coding skills"
```

The `add-skills` meta-skill downloads and installs each skill into the correct folders for all detected AI IDEs in your project. If a skill exists in multiple configured repositories, it will ask you to choose which one to install from.

---

## 🤖 Step 4: Browse and Install Agent Commands

Agent commands are slash-command style shortcuts. Browse and install them the same way:

```text
"List available agent commands"
"Install the specify and architect agent commands"
```

---

## 📄 Understanding nightlife.yaml

`nightlife.yaml` controls where the meta-skills look for skill and agent repositories. It has two sections — `agents:` and `skills:` — each listing one or more repositories directly:

```yaml
# DaNang Nightlife - Agent & Skill Repository Configuration
agents:
  - name: DaNangNightlifeAgent
    url: https://github.com/DauQuangThanh/danang-nightlife
    branch: main
    path: agents
  - name: VinhPhoenixAgent
    url: https://github.com/DauQuangThanh/vinh-phoenix
    branch: main
    path: agents
skills:
  - name: DaNangNightlifeSkill
    url: https://github.com/DauQuangThanh/danang-nightlife
    branch: main
    path: skills
  - name: VinhPhoenixSkill
    url: https://github.com/DauQuangThanh/vinh-phoenix
    branch: main
    path: skills
```

Each entry has:
- `name` — display name for the repository
- `url` — repository URL (GitHub or Azure DevOps)
- `branch` — git branch (default: `main`)
- `path` — path within repo containing skills/agents

**Public repos work without tokens.** For private repos, set `GH_TOKEN` (GitHub) or `AZURE_DEVOPS_PAT` (Azure DevOps).

### Multi-Repo Support

You can configure multiple repositories. When a skill or agent exists in more than one repo, the AI assistant will list all matches and ask you to choose.

### Using Your Own Repositories

Edit `nightlife.yaml` directly to point to your own repos:

```yaml
skills:
  - name: my-team-skills
    url: https://github.com/my-org/ai-skills
    branch: main
    path: skills
  - name: internal-skills
    url: https://dev.azure.com/my-org/my-project/_git/skills-repo
    branch: main
    path: skills
```

Your AI assistant's `list-skills` and `add-skills` will automatically use your configured repositories.

---

## 🧩 Understanding the Meta-Skills

Each meta-skill is self-contained with scripts and follows the Agent Skills standard:

| Meta-Skill | Trigger | What It Does |
|------------|---------|--------------|
| `git-commit` | "commit my changes" | Generates a Conventional Commits message and commits |
| `list-skills` | "list skills", "what skills?" | Queries configured repos, displays available skills |
| `add-skills` | "install skills", "add skills" | Downloads skill folders into all detected AI IDEs |
| `list-agents` | "list agents", "what agents?" | Queries configured repos, displays available agent commands |
| `add-agents` | "install agents", "add agents" | Downloads agent command files into all detected AI IDEs |

---

## 🎯 Key Principles

| Principle | What It Means |
|-----------|---------------|
| **Start Minimal** | Only 5 meta-skills installed by default |
| **Grow On Demand** | Use `add-skills` to install what your project needs |
| **Stay in Control** | Edit `nightlife.yaml` to configure your own skill sources |
| **Multi-Agent** | Skills install to all detected AI IDEs automatically |

---

## 📚 Next Steps

- 💻 [Source Code](https://github.com/dauquangthanh/vinh-phoenix) - Contribute to the project
- 🐛 [Report Issues](https://github.com/dauquangthanh/vinh-phoenix/issues/new) - Found a bug?
- 💬 [Ask Questions](https://github.com/dauquangthanh/vinh-phoenix/discussions) - Need help?
