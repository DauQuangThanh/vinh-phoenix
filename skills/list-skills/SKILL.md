---
name: list-skills
description: Lists all available skills from configured remote repositories. Use when user wants to see what skills can be installed, browse available skills, or check what's in the skill catalog. Reads nightlife.yaml for GitHub issue URLs containing repo definitions.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.0.0"
  last_updated: "2026-03-19"
---

# List Skills

## Overview

This skill lists all available skills from remote GitHub repositories configured in `nightlife.yaml`. It helps users discover what skills are available for installation before using the `add-skills` skill.

## When to Use

- User wants to see available skills
- User asks "what skills are available?"
- User wants to browse the skill catalog
- Before using the `add-skills` skill to know what's available
- User mentions: "list skills", "show skills", "available skills", "skill catalog"

## Prerequisites

- `nightlife.yaml` exists in the project root with configured `urls`
- Internet connection to reach GitHub API
- `python3` available on the system

## Instructions

### Step 1: Read Configuration

1. Read `nightlife.yaml` from the project root
2. Extract all URLs from the `urls:` list
3. Each URL points to a GitHub issue whose body contains YAML-formatted repository definitions

### Step 2: Fetch Repository Definitions

For each URL in `nightlife.yaml`:

1. Parse the GitHub issue URL to extract owner, repo, and issue number
2. Fetch the issue body via GitHub API: `https://api.github.com/repos/{owner}/{repo}/issues/{number}`
3. Parse the YAML body to extract `skills:` entries, each with `name`, `url`, `branch`, and `path`

### Step 3: List Available Skills

For each skill repository found:

1. Use GitHub API to list contents: `https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}`
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

```bash
python3 {SKILL_DIR}/scripts/list_skills.py
```

For example, if this skill is installed at `.claude/skills/list-skills/`, run:
```bash
python3 .claude/skills/list-skills/scripts/list_skills.py
```

The script reads `nightlife.yaml` from the project root, fetches repo definitions from all configured GitHub issues, then lists available skills from each repository.

## Error Handling

| Error | Resolution |
|-------|------------|
| `nightlife.yaml` not found | Tell user to create it with `phoenix config-set-url` or manually |
| GitHub API rate limit (HTTP 403) | Suggest setting `GH_TOKEN` environment variable |
| Repository not found (HTTP 404) | Check the repo URL and path in the GitHub issue |
| No skills found | The repository path may not contain skill directories |

## Related Skills

- **add-skills**: Install skills after listing them
- **list-agents**: Similar skill for listing available agent commands
- **add-agents**: Install agent commands from remote repositories
