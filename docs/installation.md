# 📦 Installation Guide

**Install Phoenix skills into your development workflow.**

---

## 🎯 What You'll Get

Phoenix provides **18 production-ready skills** for AI coding assistants, covering:

- Requirements specification and clarification
- Architecture design and review
- Technical planning and implementation
- Code quality and consistency
- Testing and project management

The **Phoenix CLI** installs these skills into your project, making them discoverable by your AI assistant. Skills are automatically loaded when tasks match their descriptions.

---

## ⚙️ What You Need

Before installing, make sure you have:

| Requirement | Description |
| ------------- | ------------- |
| **Operating System** | Linux, macOS, or Windows (PowerShell supported) |
| **AI Assistant** | [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), or [CodeBuddy CLI](https://www.codebuddy.ai/cli) |
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

# CodeBuddy CLI
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init <project_name> --ai codebuddy
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

After setup, check that everything works:

### 1. Check for Agent Skills

Your AI agent should have discovered these core skills:

**Core Workflow:**

| Skill | When Used |
| --------- | ---------- |
| `project-ground-rules-setup` | When you ask to establish project principles |
| `requirements-specification` | When you describe what to build |
| `technical-detailed-design` | When you specify tech stack and implementation |
| `task-management` | When you ask to break down work |
| `coding` | When you ask to implement |

### 2. Check Installation

Verify that agent-specific skills have been installed to your project.

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

### Need More Help?

- 📖 Check the [Quick Start Guide](quickstart.md) for next steps
- 🐛 [Report an issue](https://github.com/dauquangthanh/vinh-phoenix/issues/new) if something's not working
- 💬 [Ask questions](https://github.com/dauquangthanh/vinh-phoenix/discussions) in our community
