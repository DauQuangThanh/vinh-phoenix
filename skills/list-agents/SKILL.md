---
name: list-agents
description: Lists all available agent commands from configured remote repositories. Use when user wants to see what agent commands can be installed, browse available agents, or check what's in the catalog. Reads nightlife.yaml for GitHub issue URLs containing repo definitions.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.0.0"
  last_updated: "2026-03-19"
---

# List Agents

## Overview

This skill lists all available agent commands from remote GitHub repositories configured in `nightlife.yaml`. It helps users discover what agent commands are available for installation before using the `add-agents` skill.

## When to Use

- User wants to see available agent commands
- User asks "what agents are available?"
- User wants to browse the agent catalog
- Before using the `add-agents` skill to know what's available
- User mentions: "list agents", "show agents", "available agents", "agent catalog"

## Prerequisites

- `nightlife.yaml` exists in the project root with configured `urls`
- Internet connection to reach GitHub API
- `curl` available on the system (Mac/Linux) or `Invoke-RestMethod` (Windows)

## Instructions

### Step 1: Read Configuration

1. Read `nightlife.yaml` from the project root
2. Extract all URLs from the `urls:` list
3. Each URL points to a GitHub issue whose body contains YAML-formatted repository definitions

### Step 2: Fetch Repository Definitions

For each URL in `nightlife.yaml`:

1. Parse the GitHub issue URL to extract owner, repo, and issue number
2. Fetch the issue body via GitHub API: `https://api.github.com/repos/{owner}/{repo}/issues/{number}`
3. Parse the YAML body to extract `agents:` entries, each with `name`, `url`, `branch`, and `path`

### Step 3: List Available Agent Commands

For each agent repository found:

1. Use GitHub API to list contents: `https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}`
2. Filter for `.md` files (agent commands are markdown files)
3. Skip hidden files (starting with `.`) and template directories
4. Display the agent command name (filename without `.md` extension)

### Step 4: Present Results

Display results grouped by repository:

```
Repository: {repo_name} ({repo_url})
  - agent-command-1
  - agent-command-2
  - ...
  Total: N agent commands available
```

## Running the Script

Execute the listing script:

```bash
python3 scripts/list_agents.py
```

The script reads `nightlife.yaml`, fetches repo definitions from all configured GitHub issues, then lists available agent commands from each repository.

## Error Handling

| Error | Resolution |
|-------|------------|
| `nightlife.yaml` not found | Tell user to create it with `phoenix config-set-url` or manually |
| GitHub API rate limit (HTTP 403) | Suggest setting `GH_TOKEN` environment variable |
| Repository not found (HTTP 404) | Check the repo URL and path in the GitHub issue |
| No agent commands found | The repository path may not contain `.md` files |

## Related Skills

- **add-agents**: Install agent commands after listing them
- **list-skills**: Similar skill for listing available skills instead of agents
- **add-skills**: Install skills from remote repositories
