---
name: list-skills
description: Lists all available skills from configured remote repositories (GitHub and Azure DevOps). Use when user wants to see what skills can be installed, browse available skills, or check what's in the skill catalog. Reads nightlife.yaml for catalog URLs containing repo definitions.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.1.0"
  last_updated: "2026-04-02"
---

# List Skills

## Overview

This skill lists all available skills from remote repositories configured in `nightlife.yaml`. It supports both GitHub and Azure DevOps as catalog sources and skill repositories. It helps users discover what skills are available for installation before using the `add-skills` skill.

## When to Use

- User wants to see available skills
- User asks "what skills are available?"
- User wants to browse the skill catalog
- Before using the `add-skills` skill to know what's available
- User mentions: "list skills", "show skills", "available skills", "skill catalog"

## Prerequisites

- `nightlife.yaml` exists in the project root with configured `urls`
- Internet connection to reach GitHub API and/or Azure DevOps API
- `curl` available on the system (Mac/Linux) or `Invoke-RestMethod` (Windows)

## Instructions

### Step 1: Read Configuration

1. Read `nightlife.yaml` from the project root
2. Extract all URLs from the `urls:` list
3. Each URL points to a catalog source:
   - **GitHub issue**: `https://github.com/{owner}/{repo}/issues/{number}` — issue body contains YAML repo definitions
   - **Azure DevOps file**: `https://dev.azure.com/{org}/{project}/_git/{repo}?path={path}&version=GB{branch}` — file contains YAML repo definitions

### Step 2: Fetch Repository Definitions

For each URL in `nightlife.yaml`:

**GitHub issues:**
1. Parse the URL to extract owner, repo, and issue number
2. Fetch the issue body via GitHub API: `https://api.github.com/repos/{owner}/{repo}/issues/{number}`
3. Parse the YAML body to extract `skills:` entries, each with `name`, `url`, `branch`, and `path`

**Azure DevOps files:**
1. Parse the URL to extract org, project, repo, path, and branch
2. Fetch file content via Azure DevOps Items API: `https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo}/items?path={path}&...`
3. Parse the YAML content to extract `skills:` entries (same format as GitHub)

### Step 3: List Available Skills

For each skill repository found:

**GitHub repos:**
1. Use GitHub API to list contents: `https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}`

**Azure DevOps repos:**
1. Use Azure DevOps Items API: `https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo}/items?scopePath=/{path}&recursionLevel=oneLevel&...`

For both:
2. Filter for directories (skills are folders containing SKILL.md)
3. Skip hidden directories (starting with `.`)
4. Display the skill name (directory name)

### Step 4: Present Results

Display results grouped by repository:

```
Repository: {repo_name} ({repo_url})
  - skill-name-1
  - skill-name-2
  - ...
  Total: N skills available
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

The script reads `nightlife.yaml` from the project root, fetches repo definitions from all configured GitHub issues, then lists available skills from each repository.

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
| Repository not found (HTTP 404) | Check the repo URL and path in the catalog source |
| No skills found | The repository path may not contain skill directories |
| Unsupported URL format | Only GitHub issues and Azure DevOps file URLs are supported |

## Related Skills

- **add-skills**: Install skills after listing them
- **list-agents**: Similar skill for listing available agent commands
- **add-agents**: Install agent commands from remote repositories
