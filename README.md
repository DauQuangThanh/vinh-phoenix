<div align="center">

# 🔥 Vinh Phoenix - Phượng Hoàng Trung Đô

## *Drive Quality Together with a Core Installer Framework for AI Agent Skills*

**A lightweight CLI that bootstraps AI coding assistants with core meta-skills and lets you extend them with skills and agents from any configured repository.**

[![Release](https://github.com/dauquangthanh/vinh-phoenix/actions/workflows/release.yml/badge.svg)](https://github.com/dauquangthanh/vinh-phoenix/actions/workflows/release.yml)
[![GitHub stars](https://img.shields.io/github/stars/dauquangthanh/vinh-phoenix?style=social)](https://github.com/dauquangthanh/vinh-phoenix/stargazers)
[![License](https://img.shields.io/github/license/dauquangthanh/vinh-phoenix)](https://github.com/dauquangthanh/vinh-phoenix/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub_Pages-blue)](https://dauquangthanh.github.io/vinh-phoenix/)

</div>

---

## Table of Contents

- [🔥 Vinh Phoenix - Phượng Hoàng Trung Đô](#-vinh-phoenix---phượng-hoàng-trung-đô)
  - [*Drive Quality Together with a Core Installer Framework for AI Agent Skills*](#drive-quality-together-with-a-core-installer-framework-for-ai-agent-skills)
  - [Table of Contents](#table-of-contents)
  - [🎯 What is Vinh Phoenix?](#-what-is-vinh-phoenix)
  - [📦 Core Skills (Installed by Default)](#-core-skills-installed-by-default)
  - [⚡ Quick Start](#-quick-start)
    - [1. Install Phoenix CLI](#1-install-phoenix-cli)
    - [2. Initialize Your Project](#2-initialize-your-project)
    - [3. Browse and Install More Skills](#3-browse-and-install-more-skills)
  - [🔧 Extending with More Skills \& Agents](#-extending-with-more-skills--agents)
    - [How It Works](#how-it-works)
    - [Workflow](#workflow)
  - [📄 nightlife.yaml Configuration](#-nightlifeyaml-configuration)
    - [Catalog Format](#catalog-format)
    - [Using Your Own Repositories](#using-your-own-repositories)
  - [🤖 Supported AI Agents](#-supported-ai-agents)
  - [🔧 Phoenix CLI Reference](#-phoenix-cli-reference)
    - [Commands](#commands)
    - [`phoenix init` Arguments \& Options](#phoenix-init-arguments--options)
    - [Examples](#examples)
    - [Environment Variables](#environment-variables)
  - [🏗️ Project Structure](#️-project-structure)
  - [🛠️ Troubleshooting](#️-troubleshooting)
    - [Git Authentication on Linux](#git-authentication-on-linux)
    - [Meta-skills not finding nightlife.yaml](#meta-skills-not-finding-nightlifeyaml)
    - [API rate limits or auth errors when using list-skills / add-skills](#api-rate-limits-or-auth-errors-when-using-list-skills--add-skills)
  - [🎗️ Support](#️-support)
  - [🙏 Credits](#-credits)
  - [📄 License](#-license)

## 🎯 What is Vinh Phoenix?

**Vinh Phoenix is a core installer framework for AI agent skills.**

It bootstraps your project with a small set of **meta-skills** that manage themselves — letting you list, add, and remove skills and agents from any configured repository. Instead of bundling a fixed library, Phoenix puts you in control:

- ✅ Install the core meta-skills with one command
- ✅ Browse available skills and agents from configured repositories
- ✅ Add exactly the skills your project needs
- ✅ Point `nightlife.yaml` to your own repos to build private catalogs
- ✅ Works with 19 AI coding assistants

> **Think of it like a package manager for AI skills:** Phoenix installs the tooling to discover and install skills. You decide what goes into your project.

## 📦 Core Skills (Installed by Default)

`phoenix init` installs **5 core meta-skills** into every project:

| Skill | Activation Trigger | Purpose |
|-------|--------------------|---------|
| `git-commit` | "commit my changes", "generate commit message" | Generate semantic commit messages following Conventional Commits |
| `list-skills` | "list skills", "what skills are available?", "skill catalog" | Browse available skills from configured repositories |
| `add-skills` | "add skills", "install skills", "download skills" | Download and install skills from remote repositories |
| `list-agents` | "list agents", "what agents are available?" | Browse available agent commands from configured repositories |
| `add-agents` | "add agents", "install agents", "download agent commands" | Download and install agent commands from remote repositories |

These meta-skills form the foundation. They read `nightlife.yaml` to know where to fetch additional skills and agents from.

## ⚡ Quick Start

### 1. Install Phoenix CLI

```bash
# Install once, use everywhere
uv tool install phoenix-cli --from git+https://github.com/dauquangthanh/vinh-phoenix.git
```

**Upgrade to latest version:**

```bash
uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git
```

<details>
<summary><strong>Alternative: Run without installing</strong></summary>

```bash
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <PROJECT_NAME>
```

</details>

### 2. Initialize Your Project

```bash
phoenix init <PROJECT_NAME>
phoenix check
```

This installs the 5 core meta-skills into agent-specific folders (`.github/skills/`, `.claude/skills/`, etc.) and places `nightlife.yaml` in your project root.

<p align="center">
  <img src="./media/vinh-phoenix.png" alt="Vinh Phoenix Installation" width="100%"/>
</p>

### 3. Browse and Install More Skills

Launch your AI assistant and use the meta-skills to extend your setup:

```text
"List all available skills"
"Install the requirements-specification and coding skills"
"Show me what agent commands are available"
"Add the architect and specify agent commands"
```

The `list-skills`, `add-skills`, `list-agents`, and `add-agents` meta-skills handle everything — reading `nightlife.yaml`, fetching catalogs, and installing into the correct folders for your AI assistant.

---

## 🔧 Extending with More Skills & Agents

### How It Works

The meta-skills use `nightlife.yaml` as a directory of skill and agent repositories. Each URL points to a catalog source (GitHub issue or Azure DevOps file) whose body contains a YAML-formatted list of repositories:

```
nightlife.yaml
    └── urls:
         ├── https://github.com/owner/repo/issues/2         → GitHub issue catalog
         ├── https://dev.azure.com/org/proj/_git/repo?path=… → Azure DevOps file catalog
         └── ...
```

When you ask your AI to `list-skills` or `add-skills`, it:
1. Reads `nightlife.yaml`
2. Fetches each catalog source and parses the YAML repo definitions
3. Queries those repos (GitHub API or Azure DevOps API) to find available skills/agents
4. Downloads and installs the ones you select using `git sparse-checkout`

### Workflow

```
phoenix init my-project --ai claude
        ↓
5 core meta-skills installed
        ↓
"List available skills"  (list-skills)
        ↓
Browse catalog from nightlife.yaml repos
        ↓
"Install requirements-specification and coding"  (add-skills)
        ↓
Skills downloaded and installed for all detected AI IDEs
```

---

## 📄 nightlife.yaml Configuration

`nightlife.yaml` is placed in your project root by `phoenix init`. It tells the meta-skills where to find skill and agent catalogs. It supports both **GitHub** and **Azure DevOps** as catalog sources:

```yaml
# DaNang Nightlife - Agent & Skill Repository Configuration
# URLs can point to GitHub issues or Azure DevOps repo files
# containing YAML-formatted lists of skill/agent repositories.
urls:
  # GitHub issue (issue body contains YAML repo list)
  - https://github.com/DauQuangThanh/vinh-phoenix/issues/2
  # Azure DevOps file (YAML file in a repo)
  # - https://dev.azure.com/myorg/myproject/_git/myrepo?path=/catalog.yaml&version=GBmain
```

### Catalog Format

Each catalog source (GitHub issue body or Azure DevOps file) should contain YAML like this:

```yaml
skills:
  - name: vinh-phoenix-skills
    url: https://github.com/owner/skills-repo
    branch: main
    path: skills

agents:
  - name: vinh-phoenix-agents
    url: https://github.com/owner/agents-repo
    branch: main
    path: agent-commands
```

Skill/agent repo URLs can point to either GitHub or Azure DevOps repositories:

```yaml
skills:
  # GitHub repo
  - name: public-skills
    url: https://github.com/owner/skills-repo
    branch: main
    path: skills
  # Azure DevOps repo
  - name: internal-skills
    url: https://dev.azure.com/myorg/myproject/_git/skills-repo
    branch: main
    path: skills
```

### Using Your Own Repositories

To maintain a private or custom skill catalog, update `nightlife.yaml` to point to your own sources:

```yaml
urls:
  # GitHub issue
  - https://github.com/my-org/my-config/issues/1
  # Azure DevOps file
  - https://dev.azure.com/my-org/my-project/_git/config?path=/skills-catalog.yaml&version=GBmain
```

Structure the issue body or file with your repos. This lets teams maintain internal skill catalogs without forking Phoenix — including private Azure DevOps repositories.

---

## 🤖 Supported AI Agents

| Agent | Support | Notes |
|-------|---------|-------|
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ | File-based prompts [do not support argument substitution](https://github.com/aws/amazon-q-developer-cli/issues/3064) despite CLI accepting arguments. |
| [Amp](https://ampcode.com/) | ✅ | Available as CLI/TUI and editor extension. Model-agnostic with role-specific modes. |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview) | ✅ | Command-line interface for agentic code assistance. |
| [Claude Code](https://www.anthropic.com/claude-code) | ✅ | Desktop application powered by Claude AI models. |
| [CodeBuddy CLI](https://www.codebuddy.ai/cli) | ✅ | Command-line AI coding assistant. |
| [Codex CLI](https://github.com/openai/codex) | ✅ | Terminal-based coding assistant. |
| [Cursor](https://cursor.sh/) | ✅ | AI-first code editor based on VS Code. |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ | Open-source terminal AI agent with 1M token context window. Supports MCP servers. |
| [GitHub Copilot](https://code.visualstudio.com/) | ✅ | IDE extension powered by OpenAI models. |
| [Google Antigravity](https://ai.google.dev/) | ✅ | IDE-based agent with slash command support. |
| [IBM Bob](https://www.ibm.com/products/bob) | ✅ | IDE-based agent with code review, vulnerability detection, and modernization support. |
| [Jules](https://jules.google.com/) | ✅ | Autonomous coding agent that works in isolated VMs. Includes built-in peer review. |
| [Kilo Code](https://github.com/Kilo-Org/kilocode) | ✅ | Community-driven AI coding assistant. |
| [opencode](https://opencode.ai/) | ✅ | Open-source AI coding platform. |
| [Qoder CLI](https://qoder.ai) | ✅ | Terminal-based AI development assistant. |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | ✅ | Qwen-powered coding assistant. |
| [Roo Code](https://roocode.com/) | ✅ | Open-source VS Code extension with cloud agent team support. Model-agnostic with role-specific modes. |
| [SHAI (OVHcloud)](https://github.com/ovh/shai) | ✅ | Rust-based terminal agent with HTTP server mode. Supports MCP servers and multiple LLM providers. |
| [Windsurf](https://windsurf.com/) | ✅ | IDE with Cascade agent for autonomous coding. 1M+ users. Supports MCP servers and memories. |

## 🔧 Phoenix CLI Reference

### Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a new Phoenix project with core meta-skills |
| `check` | Check for installed tools (git, VS Code, and all supported AI agent CLIs) |
| `version` | Display CLI version, template version, and system information |

### `phoenix init` Arguments & Options

| Argument/Option | Type | Description |
|-----------------|------|-------------|
| `<project-name>` | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory) |
| `--ai` | Option | AI assistant(s) to use. Single agent or comma-separated list (e.g., `claude,gemini,copilot`). Run `phoenix init --help` for the full list of valid agents. If not specified, an interactive multi-select menu will appear |
| `--ignore-agent-tools` | Flag | Skip checks for AI agent tools like Claude Code |
| `--no-git` | Flag | Skip git repository initialization |
| `--here` | Flag | Initialize project in the current directory instead of creating a new one |
| `--force` | Flag | Force merge/overwrite when initializing in current directory (skip confirmation) |
| `--upgrade` | Flag | Upgrade existing Phoenix project by replacing agent folders with latest templates (creates timestamped backups) |
| `--skip-tls` | Flag | Skip SSL/TLS verification (not recommended) |
| `--debug` | Flag | Enable detailed debug output for troubleshooting |
| `--github-token` | Option | GitHub token for API requests (or set `GH_TOKEN`/`GITHUB_TOKEN` env variable) |
| `--local-templates` | Flag | Use local templates from repository instead of downloading from GitHub (for development) |
| `--template-path` | Option | Path to local template directory (defaults to repo root if `--local-templates` is used) |

### Examples

```bash
# Basic project initialization (interactive agent selection)
phoenix init my-project

# Initialize with specific AI assistant
phoenix init my-project --ai claude

# Initialize with multiple AI assistants (comma-separated)
phoenix init my-project --ai claude,gemini,copilot

# Initialize in current directory
phoenix init . --ai copilot
# or use the --here flag
phoenix init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
phoenix init . --force --ai copilot

# Upgrade existing project (replaces agent folders, creates backups)
phoenix init --upgrade
phoenix init --upgrade --ai claude
phoenix init my-project --upgrade

# Skip git initialization
phoenix init my-project --ai gemini --no-git

# Use local templates for development
phoenix init demo --local-templates --ai claude
phoenix init demo --local-templates --template-path /path/to/vinh-phoenix

# Use GitHub token for API requests (helpful for corporate environments)
phoenix init my-project --ai claude --github-token ghp_your_token_here

# Enable debug output for troubleshooting
phoenix init my-project --ai claude --debug

# Check system requirements
phoenix check

# Display version and system information
phoenix version
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub personal access token for API requests. Increases rate limits and enables access to private repositories. |
| `AZURE_DEVOPS_PAT` / `ADO_TOKEN` | Azure DevOps personal access token. Required for accessing private Azure DevOps repositories and catalog files. |
| `CODEX_HOME` | Path to the `.codex` folder in your project. Required when using the Codex CLI agent so it reads commands from the correct location. |
| `RAINBOW_USE_LOCAL_TEMPLATES` | Set to `1` to use local templates instead of downloading from GitHub (development use). |
| `RAINBOW_TEMPLATE_PATH` | Path to local template directory when using local templates (development use). |
| `SPECIFY_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific feature when not using Git branches. Used by skills at runtime. |

---

## 🏗️ Project Structure

After running `phoenix init`, your project structure:

```
<project-root>/
├── .<agent>/              # Agent-specific folder (.claude/, .github/, .gemini/)
│   └── skills/            # Core meta-skills + any installed skills
│       ├── git-commit/    # Semantic commit message generator
│       ├── list-skills/   # Browse available skills from configured repos
│       ├── add-skills/    # Download and install skills
│       ├── list-agents/   # Browse available agent commands
│       └── add-agents/    # Download and install agent commands
│
└── nightlife.yaml         # Repository catalog configuration
```

After adding more skills via `add-skills`:

```
<project-root>/
├── .<agent>/
│   └── skills/
│       ├── git-commit/
│       ├── list-skills/
│       ├── add-skills/
│       ├── list-agents/
│       ├── add-agents/
│       ├── requirements-specification/   # ← added via add-skills
│       ├── technical-detailed-design/    # ← added via add-skills
│       ├── coding/                       # ← added via add-skills
│       └── ... (whatever you install)
│
├── docs/                  # Created by skills as you use them
└── specs/                 # Created by skills as you use them
```

---

## 🛠️ Troubleshooting

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

### Meta-skills not finding nightlife.yaml

Ensure `nightlife.yaml` exists in your project root. If missing, re-run `phoenix init --here --force`.

### API rate limits or auth errors when using list-skills / add-skills

Set the appropriate token for your repository host:

```bash
# GitHub
export GH_TOKEN=ghp_your_token_here

# Azure DevOps
export AZURE_DEVOPS_PAT=your_pat_here
```

---

## 🎗️ Support

- 🐛 **Bug Reports:** [Open an issue](https://github.com/dauquangthanh/vinh-phoenix/issues/new)
- 💡 **Feature Requests:** [Open an issue](https://github.com/dauquangthanh/vinh-phoenix/issues/new)
- ❓ **Questions:** [Start a discussion](https://github.com/dauquangthanh/vinh-phoenix/discussions)

**Maintainer:** Dau Quang Thanh ([@dauquangthanh](https://github.com/dauquangthanh))

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

**Open source and free to use.** Contributions welcome!
