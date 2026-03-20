# 📦 Installation Guide

**Install Phoenix and bootstrap your project with core meta-skills.**

---

## 🎯 What You'll Get

`phoenix init` installs **5 core meta-skills** into your project:

| Skill | Purpose |
|-------|---------|
| `git-commit` | Generate semantic commit messages |
| `list-skills` | Browse available skills from configured repositories |
| `add-skills` | Download and install skills from remote repositories |
| `list-agents` | Browse available agent commands |
| `add-agents` | Download and install agent commands |

It also places `nightlife.yaml` in your project root — the configuration file that tells the meta-skills where to find skill and agent catalogs.

---

## ⚙️ What You Need

Before installing, make sure you have:

| Requirement | Description |
|-------------|-------------|
| **Operating System** | Linux, macOS, or Windows (PowerShell supported) |
| **AI Assistant** | Any [supported agent](../README.md#-supported-ai-agents) |
| **Package Manager** | [uv](https://docs.astral.sh/uv/) |
| **Python** | [Version 3.11 or higher](https://www.python.org/downloads/) |
| **Version Control** | [Git](https://git-scm.com/downloads) |

---

## 🚀 Installation Options

### Option 1: Create a New Project

The easiest way to start:

```bash
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <PROJECT_NAME>
```

### Option 2: Initialize in Current Directory

Already have a project folder?

```bash
# Method 1: Using dot notation
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init .

# Method 2: Using --here flag
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init --here
```

### 🤖 Choose Your AI Agent

Specify which AI assistant to use:

```bash
# Claude Code
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <project_name> --ai claude

# Gemini CLI
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <project_name> --ai gemini

# GitHub Copilot
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <project_name> --ai copilot

# Multiple agents at once
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <project_name> --ai claude,copilot,gemini
```

---

### ⚡ Skip Tool Checks (Optional)

Want to set up without checking if AI tools are installed?

```bash
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <project_name> --ai claude --ignore-agent-tools
```

> **Use this when:** You're setting up on a different machine or want to configure tools later.

---

## ✅ Verify Installation

After setup, verify the core meta-skills are in place:

```bash
# For Claude Code
ls .claude/skills/

# For GitHub Copilot
ls .github/skills/

# For Gemini CLI
ls .gemini/extensions/
```

You should see 5 skill directories: `git-commit`, `list-skills`, `add-skills`, `list-agents`, `add-agents`.

Also check that `nightlife.yaml` exists in your project root:

```bash
cat nightlife.yaml
```

---

## ➕ Adding More Skills

Once initialized, use your AI assistant to extend your project:

```text
"List available skills"
"Install the requirements-specification and coding skills"
"Show what agent commands are available"
```

The `list-skills` and `add-skills` meta-skills handle fetching from the configured repositories in `nightlife.yaml`.

---

## 🛠️ Troubleshooting

### Git Authentication Issues on Linux

Having trouble with Git authentication? Install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e

echo "⬇️ Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb

echo "📦 Installing..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb

echo "⚙️ Configuring Git..."
git config --global credential.helper manager

echo "🧹 Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb

echo "✅ Done! Git Credential Manager is ready."
```

### GitHub API Rate Limits

When using `list-skills` or `add-skills`, set a token to avoid rate limiting:

```bash
export GH_TOKEN=ghp_your_token_here
```

### Need More Help?

- 📖 Check the [Quick Start Guide](quickstart.md) for next steps
- 🐛 [Report an issue](https://github.com/dauquangthanh/vinh-phoenix/issues/new) if something's not working
- 💬 [Ask questions](https://github.com/dauquangthanh/vinh-phoenix/discussions) in our community
