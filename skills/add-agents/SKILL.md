---
name: add-agents
description: Downloads and installs agent commands from configured remote repositories into the correct AI IDE folders. Use when user wants to install, add, or download agent commands from the catalog. Handles multi-IDE installation with correct file extensions and argument format conversion.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.0.0"
  last_updated: "2026-03-19"
---

# Add Agents

## Overview

This skill downloads agent command files from remote GitHub repositories and installs them into the correct folders for all detected AI IDEs in the project. It handles file extension conversion and argument format replacement per IDE.

## When to Use

- User wants to install agent commands from the catalog
- User asks to "add agents", "install agents", or "download agent commands"
- After using `list-agents` to see what's available
- User mentions specific agent command names to install (e.g., "install specify", "add architect")

## Prerequisites

- `nightlife.yaml` exists in the project root with configured `urls`
- Project has been initialized with at least one AI IDE (folders like `.claude/`, `.github/`, etc.)
- Internet connection to reach GitHub
- `curl` available (Mac/Linux) or `Invoke-WebRequest` (Windows)

## Agent Folder Mapping

The following AI IDEs are supported. Agent commands are installed into these folders:

| AI IDE | Agent Folder | Extension | Args Format |
|--------|-------------|-----------|-------------|
| GitHub Copilot | `.github/agents/` | `.agent.md` | `$ARGUMENTS` |
| Claude Code | `.claude/commands/` | `.md` | `$ARGUMENTS` |
| Cursor | `.cursor/commands/` | `.md` | `$ARGUMENTS` |
| Gemini CLI | `.gemini/commands/` | `.toml` | `{{args}}` |
| Qwen Code | `.qwen/commands/` | `.toml` | `{{args}}` |
| Open Code | `.opencode/command/` | `.md` | `$ARGUMENTS` |
| Codex CLI | `.codex/commands/` | `.md` | `$ARGUMENTS` |
| Windsurf | `.windsurf/workflows/` | `.md` | `$ARGUMENTS` |
| Kilo Code | `.kilocode/rules/` | `.md` | `$ARGUMENTS` |
| Auggie CLI | `.augment/rules/` | `.md` | `$ARGUMENTS` |
| CodeBuddy | `.codebuddy/commands/` | `.md` | `$ARGUMENTS` |
| Roo Code | `.roo/rules/` | `.md` | `$ARGUMENTS` |
| Amazon Q | `.amazonq/prompts/` | `.md` | `$ARGUMENTS` |
| Amp | `.agents/commands/` | `.md` | `$ARGUMENTS` |
| SHAI | `.shai/commands/` | `.md` | `$ARGUMENTS` |
| IBM Bob | `.bob/commands/` | `.md` | `$ARGUMENTS` |
| Jules | `.agent/` | `.md` | `$ARGUMENTS` |
| Qoder CLI | `.qoder/commands/` | `.md` | `$ARGUMENTS` |
| Antigravity | `.agent/rules/` | `.md` | `$ARGUMENTS` |

## Instructions

### Step 1: Identify Requested Agents

1. Parse the user's request to determine which agent commands to install
2. If no specific names given, run `python3 scripts/list_agents.py` first to show available options and ask the user to choose

### Step 2: Detect Installed AI IDEs

Check which AI IDE folders exist in the project root. An IDE is "detected" if its agent folder or skills folder exists. Only install into detected IDEs.

### Step 3: Fetch Agent Source

1. Read `nightlife.yaml` to get issue URLs
2. Fetch repo definitions from each issue
3. Find which repository contains the requested agent command

### Step 4: Install Using Shell Script

For each detected AI IDE, run the installation script:

**Mac/Linux:**
```bash
bash scripts/add-agents.sh <repo_url> <branch> <repo_path> <agent_name> <target_dir> <extension> <args_format>
```

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/add-agents.ps1 <repo_url> <branch> <repo_path> <agent_name> <target_dir> <extension> <args_format>
```

**Parameters:**
- `repo_url`: GitHub repository URL (e.g., `https://github.com/owner/repo`)
- `branch`: Git branch (e.g., `main`)
- `repo_path`: Path in repo containing agents (e.g., `agent-commands`)
- `agent_name`: Name of the agent to download (e.g., `specify`)
- `target_dir`: Local target directory (e.g., `.claude/commands/`)
- `extension`: File extension for target IDE (e.g., `.md`, `.agent.md`, `.toml`)
- `args_format`: Args placeholder (e.g., `$ARGUMENTS` or `{{args}}`)

### Step 5: Report Results

For each agent command installed, report:
- Which IDEs it was installed to
- The file path created
- Any failures with error details

## Example

User: "Install the specify and architect agent commands"

1. Read `nightlife.yaml` -> fetch repos from issues -> find agent repos with their `url`, `branch`, and `path`
2. Find which repo contains `specify` (e.g., repo `my-agents` at `https://github.com/owner/my-agents`, path `agent-commands`)
3. Detect Claude Code (`.claude/commands/` exists) and Copilot (`.github/agents/` exists)
4. Run for Claude:
   ```bash
   bash scripts/add-agents.sh https://github.com/owner/my-agents main agent-commands specify .claude/commands/ .md '$ARGUMENTS'
   ```
5. Run for Copilot:
   ```bash
   bash scripts/add-agents.sh https://github.com/owner/my-agents main agent-commands specify .github/agents/ .agent.md '$ARGUMENTS'
   ```
6. Repeat for `architect`
7. Report: "Installed specify and architect to Claude Code and GitHub Copilot"

## Error Handling

| Error | Resolution |
|-------|------------|
| Agent not found in any repo | Run `list-agents` to show available names |
| No AI IDE folders detected | Run `phoenix init` first to set up the project |
| Download failed (HTTP error) | Check internet connection and repo accessibility |
| Permission denied | Check write permissions on target directories |

## Related Skills

- **list-agents**: List available agents before installing
- **add-skills**: Install skills instead of agent commands
- **list-skills**: List available skills
