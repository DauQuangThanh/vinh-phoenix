---
name: list-skills
description: Lists all available skills from configured remote repositories (GitHub and Azure DevOps). Use when user wants to see what skills can be installed, browse available skills, or check what's in the skill catalog. Reads nightlife.yaml for skill repository definitions (url, branch, path).
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "2.0.0"
  last_updated: "2026-04-12"
---

# List Skills

## Overview

This skill lists all available skills from remote repositories configured in `nightlife.yaml`. It supports both GitHub and Azure DevOps as skill repositories. It helps users discover what skills are available for installation before using the `add-skills` skill.

## When to Use

- User wants to see available skills
- User asks "what skills are available?"
- User wants to browse the skill catalog
- Before using the `add-skills` skill to know what's available
- User mentions: "list skills", "show skills", "available skills", "skill catalog"

## Prerequisites

- `nightlife.yaml` exists in the project root with configured `skills` section
- Internet connection to reach GitHub API and/or Azure DevOps API
- `curl` available on the system (Mac/Linux) or `Invoke-RestMethod` (Windows)

## Instructions

### Step 1: Read Configuration

1. Read `nightlife.yaml` from the project root
2. Parse the `skills:` section — each entry has:
   - `name`: Display name for the repository
   - `url`: Repository URL (GitHub or Azure DevOps)
   - `branch`: Git branch name (e.g., `main`)
   - `path`: Path within repo containing skills (e.g., `skills`)

Example `nightlife.yaml` (supports multiple repositories):
```yaml
skills:
  - name: DaNangNightlifeSkill
    url: https://github.com/owner/repo-a
    branch: main
    path: skills
  - name: VinhPhoenixSkill
    url: https://github.com/owner/repo-b
    branch: main
    path: skills
```

### Step 2: List Available Skills

For each skill repository entry:

**GitHub repos:**
1. Use GitHub API to list contents: `https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}`

**Azure DevOps repos:**
1. Use Azure DevOps Items API: `https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo}/items?scopePath=/{path}&recursionLevel=oneLevel&...`

For both:
2. Filter for directories (skills are folders containing SKILL.md)
3. Skip hidden directories (starting with `.` or `_`)
4. Display the skill name (directory name)

### Step 3: Present Results

Display results grouped by repository:

```
Repository: {name} ({repo_url}, branch: {branch}, path: {path})
  - skill-name-1
  - skill-name-2
  - ...
  Total: N skills available

Grand total: N skills across M repositories
```

## Running the Script

Execute the listing script. The script is located in this skill's `scripts/` subdirectory. Replace `{SKILL_DIR}` with the actual path to the directory containing this SKILL.md file:

**Mac/Linux:**
```bash
bash {SKILL_DIR}/scripts/list-skills.sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File {SKILL_DIR}/scripts/list-skills.ps1
```

For example, if this skill is installed at `.claude/skills/list-skills/`, run:
```bash
bash .claude/skills/list-skills/scripts/list-skills.sh
```

The script reads `nightlife.yaml` from the project root and lists available skills from each configured repository.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub personal access token for API requests |
| `AZURE_DEVOPS_PAT` / `ADO_TOKEN` | Azure DevOps personal access token for API requests |

## Error Handling

| Error | Resolution |
|-------|------------|
| `nightlife.yaml` not found | Tell user to run `vinh-phoenix init --here --force` to restore it, or create it manually |
| GitHub API rate limit (HTTP 403) | Suggest setting `GH_TOKEN` environment variable |
| Azure DevOps auth error (HTTP 401/403) | Suggest setting `AZURE_DEVOPS_PAT` environment variable |
| Repository not found (HTTP 404) | Check the repo URL, branch, and path in nightlife.yaml |
| No skills found | The repository path may not contain skill directories |

## Related Skills

- **add-skills**: Install skills after listing them
- **list-agents**: Similar skill for listing available agents
- **add-agents**: Install agents from remote repositories
