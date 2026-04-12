---
name: list-agents
description: Lists all available agents from configured remote repositories (GitHub and Azure DevOps). Use when user wants to see what agents can be installed, browse available agents, or check what's in the agent catalog. Reads nightlife.yaml for agent repository definitions (url, branch, path).
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.0.0"
  last_updated: "2026-04-12"
---

# List Agents

## Overview

This skill lists all available agents from remote repositories configured in `nightlife.yaml`. It supports both GitHub and Azure DevOps as agent repositories. It helps users discover what agents are available for installation before using the `add-agents` skill.

## When to Use

- User wants to see available agents
- User asks "what agents are available?"
- User wants to browse the agent catalog
- Before using the `add-agents` skill to know what's available
- User mentions: "list agents", "show agents", "available agents", "agent catalog"

## Prerequisites

- `nightlife.yaml` exists in the project root with configured `agents` section
- Internet connection to reach GitHub API and/or Azure DevOps API
- `curl` available on the system (Mac/Linux) or `Invoke-RestMethod` (Windows)

## Instructions

### Step 1: Read Configuration

1. Read `nightlife.yaml` from the project root
2. Parse the `agents:` section — each entry has:
   - `name`: Display name for the repository
   - `url`: Repository URL (GitHub or Azure DevOps)
   - `branch`: Git branch name (e.g., `main`)
   - `path`: Path within repo containing agents (e.g., `agents`)

Example `nightlife.yaml` (supports multiple repositories):
```yaml
agents:
  - name: DaNangNightlifeAgent
    url: https://github.com/owner/repo-a
    branch: main
    path: agents
  - name: VinhPhoenixAgent
    url: https://github.com/owner/repo-b
    branch: main
    path: agents
```

### Step 2: List Available Agents

For each agent repository entry:

**GitHub repos:**
1. Use GitHub API to list contents: `https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}`

**Azure DevOps repos:**
1. Use Azure DevOps Items API: `https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo}/items?scopePath=/{path}&recursionLevel=oneLevel&...`

For both:
2. Filter for directories (agents are folders)
3. Skip hidden directories (starting with `.` or `_`)
4. Display the agent name (directory name)

### Step 3: Present Results

Display results grouped by repository:

```
Repository: {name} ({repo_url}, branch: {branch}, path: {path})
  - agent-name-1
  - agent-name-2
  - ...
  Total: N agents available

Grand total: N agents across M repositories
```

## Running the Script

Execute the listing script. The script is located in this skill's `scripts/` subdirectory. Replace `{SKILL_DIR}` with the actual path to the directory containing this SKILL.md file:

**Mac/Linux:**
```bash
bash {SKILL_DIR}/scripts/list-agents.sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File {SKILL_DIR}/scripts/list-agents.ps1
```

For example, if this skill is installed at `.claude/skills/list-agents/`, run:
```bash
bash .claude/skills/list-agents/scripts/list-agents.sh
```

The script reads `nightlife.yaml` from the project root and lists available agents from each configured repository.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub personal access token for API requests |
| `AZURE_DEVOPS_PAT` / `ADO_TOKEN` | Azure DevOps personal access token for API requests |

## Error Handling

| Error | Resolution |
|-------|------------|
| `nightlife.yaml` not found | Tell user to run `phoenix init --here --force` to restore it, or create it manually |
| GitHub API rate limit (HTTP 403) | Suggest setting `GH_TOKEN` environment variable |
| Azure DevOps auth error (HTTP 401/403) | Suggest setting `AZURE_DEVOPS_PAT` environment variable |
| Repository not found (HTTP 404) | Check the repo URL, branch, and path in nightlife.yaml |
| No agents found | The repository path may not contain agent directories |

## Related Skills

- **add-agents**: Install agents after listing them
- **list-skills**: Similar skill for listing available skills
- **add-skills**: Install skills from remote repositories
