---
name: add-agents
description: Downloads and installs agents from configured remote repositories (GitHub and Azure DevOps) into the correct AI IDE agent folders. Use when user wants to install, add, or download agents from the catalog. Uses git sparse-checkout to efficiently download the entire agent folder for each detected AI IDE.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.0.0"
  last_updated: "2026-04-12"
---

# Add Agents

## Overview

This skill downloads agent packages from remote repositories and installs them into the correct agent folders for all detected AI IDEs in the project. Supports both GitHub and Azure DevOps repositories.

## When to Use

- User wants to install agents from the catalog
- User asks to "add agents", "install agents", or "download agents"
- After using `list-agents` to see what's available
- User mentions specific agent names to install (e.g., "install code-reviewer", "add devops-agent")

## Prerequisites

- `nightlife.yaml` exists in the project root with configured `agents` section (supports multiple repositories)
- Project has been initialized with at least one AI IDE
- Internet connection to reach GitHub and/or Azure DevOps
- `git` available on the system (used for sparse-checkout downloads)

## Agents Folder Mapping

Agents are installed into these folders per AI IDE (based on AI-Agents-Configs April 2026):

| AI IDE | Agents Folder |
|--------|--------------|
| Amp | `.amp/agents/` |
| Antigravity | `.agent/workflows/` |
| Augment Code | `.augment/agents/` |
| Claude Code | `.claude/agents/` |
| Cline | `.cline/agents/` |
| CodeBuddy | `.codebuddy/agents/` |
| Codex CLI | `.codex/agents/` |
| Cursor | `.cursor/agents/` |
| Forge | `.forge/agents/` |
| Gemini CLI | `.gemini/agents/` |
| GitHub Copilot (IDE) | `.github/agents/` |
| GitHub Copilot CLI | `.copilot/agents/` |
| IBM Bob | `.bob/agents/` |
| Junie | `.junie/agents/` |
| Kilo Code | `.kilocode/agents/` |
| Kiro | `.kiro/agents/` |
| Mistral Vibe | `.vibe/agents/` |
| opencode | `.opencode/agents/` |
| Pi Agent | `.omp/agents/` |
| Qoder | `.qoder/agents/` |
| Qwen Code | `.qwen/agents/` |
| Roo Code | `.roo/agents/` |
| Tabnine | `.tabnine/agents/` |
| Trae | `.trae/agents/` |
| Windsurf | `.windsurf/agents/` |

## Instructions

### Important: Script Path Resolution

All script paths in this skill are relative to the directory containing this SKILL.md file. Replace `{SKILL_DIR}` with the actual path to this skill's directory.

For example, if this skill is installed at `.claude/skills/add-agents/`, then `{SKILL_DIR}` = `.claude/skills/add-agents`.

### Step 1: Identify Requested Agents

1. Parse the user's request to determine which agents to install
2. If no specific names given, run `bash {SKILL_DIR}/scripts/list-agents.sh` (Mac/Linux) or `powershell -ExecutionPolicy Bypass -File {SKILL_DIR}/scripts/list-agents.ps1` (Windows) first to show available options and ask the user to choose

Note: The list-agents script is in the **list-agents** skill directory. If you have list-agents installed, use that path instead.

### Step 2: Detect Installed AI IDEs

Check which AI IDE folders exist in the project root. An IDE is "detected" if its config folder (e.g., `.claude/`, `.github/`, `.cursor/`) exists. Only install into detected IDEs.

### Step 3: Find Agent Source

1. Read `nightlife.yaml` to get agent repository entries (name, url, branch, path)
2. Each entry directly provides the repository name, URL, branch, and path where agents are located
3. **Multiple repositories**: nightlife.yaml can contain multiple agent repos — search all of them for the requested agent

### Step 3.1: Disambiguate When Agent Exists in Multiple Repos

If the requested agent name is found in **more than one** configured repository:

1. **List all matches** — show the user each repo that contains the agent:
   ```
   Agent "code-reviewer" was found in multiple repositories:
     1. DaNangNightlifeAgent (https://github.com/owner/repo-a, path: agents)
     2. VinhPhoenixAgent (https://github.com/owner/repo-b, path: agents)
   ```
2. **Ask the user to choose** which repository to install from
3. Only proceed with installation after the user confirms their choice
4. If the agent exists in only one repo, proceed without asking

### Step 4: Install Using Shell Script

For each detected AI IDE, run the installation script:

**Mac/Linux:**
```bash
bash {SKILL_DIR}/scripts/add-agents.sh <repo_url> <branch> <repo_path> <agent_name> <target_dir>
```

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File {SKILL_DIR}/scripts/add-agents.ps1 <repo_url> <branch> <repo_path> <agent_name> <target_dir>
```

**Parameters:**
- `repo_url`: Repository URL — GitHub (`https://github.com/owner/repo`) or Azure DevOps (`https://dev.azure.com/org/project/_git/repo`)
- `branch`: Git branch (e.g., `main`)
- `repo_path`: Path in repo containing agents (e.g., `agents`)
- `agent_name`: Name of the agent to download (e.g., `code-reviewer`)
- `target_dir`: Local target directory (e.g., `.claude/agents/code-reviewer`)

The script uses `git sparse-checkout` to efficiently download only the specific agent folder from the repository. Authentication is handled via `GH_TOKEN`/`GITHUB_TOKEN` for GitHub repos or `AZURE_DEVOPS_PAT`/`ADO_TOKEN` for Azure DevOps repos.

### Step 5: Report Results

For each agent installed, report:
- Which IDEs it was installed to
- The directory path created
- Any failures with error details

## Example

### Example 1: Agent found in one repo

User: "Install the code-reviewer agent"

1. Read `nightlife.yaml` → get agent repos (name, url, branch, path)
2. Search all repos for "code-reviewer" → found only in DaNangNightlifeAgent
3. Detect Claude Code (`.claude/` exists) and Copilot (`.github/` exists)
4. Run for Claude Code (assuming skill is at `.claude/skills/add-agents/`):
   ```bash
   bash .claude/skills/add-agents/scripts/add-agents.sh https://github.com/owner/repo-a main agents code-reviewer .claude/agents/code-reviewer
   ```
5. Run for Copilot:
   ```bash
   bash .claude/skills/add-agents/scripts/add-agents.sh https://github.com/owner/repo-a main agents code-reviewer .github/agents/code-reviewer
   ```
6. Report: "Installed code-reviewer agent from DaNangNightlifeAgent to Claude Code and GitHub Copilot"

### Example 2: Agent found in multiple repos (disambiguation)

User: "Install the devops-agent"

1. Read `nightlife.yaml` → get agent repos (name, url, branch, path)
2. Search all repos for "devops-agent" → found in both DaNangNightlifeAgent and VinhPhoenixAgent
3. **Ask user to choose**:
   ```
   Agent "devops-agent" was found in multiple repositories:
     1. DaNangNightlifeAgent (https://github.com/owner/repo-a, path: agents)
     2. VinhPhoenixAgent (https://github.com/owner/repo-b, path: agents)
   Which repository would you like to install from?
   ```
4. User chooses "2" → use repo-b
5. Detect Claude Code (`.claude/` exists)
6. Run:
   ```bash
   bash .claude/skills/add-agents/scripts/add-agents.sh https://github.com/owner/repo-b main agents devops-agent .claude/agents/devops-agent
   ```
7. Report: "Installed devops-agent from VinhPhoenixAgent to Claude Code"

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub personal access token (used for git clone auth) |
| `AZURE_DEVOPS_PAT` / `ADO_TOKEN` | Azure DevOps personal access token (used for git clone auth) |

## Error Handling

| Error | Resolution |
|-------|------------|
| Agent not found in any repo | Run `list-agents` to show available names |
| No AI IDE folders detected | Run `phoenix init` first to set up the project |
| Git clone failed | Check internet connection, repo URL, and auth tokens |
| Permission denied | Check write permissions on target directories |
| Azure DevOps auth error | Set `AZURE_DEVOPS_PAT` environment variable with a valid PAT |

## Related Skills

- **list-agents**: List available agents before installing
- **add-skills**: Install skills instead of agents
- **list-skills**: List available skills
