---
name: add-skills
description: Downloads and installs skills from configured remote repositories (GitHub and Azure DevOps) into the correct AI IDE skill folders. Use when user wants to install, add, or download skills from the catalog. Uses git sparse-checkout to efficiently download the entire skill folder (SKILL.md, scripts, templates, references) for each detected AI IDE.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.1.0"
  last_updated: "2026-04-02"
---

# Add Skills

## Overview

This skill downloads complete skill packages (SKILL.md + scripts/ + templates/ + references/) from remote repositories and installs them into the correct skill folders for all detected AI IDEs in the project. Supports both GitHub and Azure DevOps repositories.

## When to Use

- User wants to install skills from the catalog
- User asks to "add skills", "install skills", or "download skills"
- After using `list-skills` to see what's available
- User mentions specific skill names to install (e.g., "install git-commit", "add bug-analysis")

## Prerequisites

- `nightlife.yaml` exists in the project root with configured `urls`
- Project has been initialized with at least one AI IDE
- Internet connection to reach GitHub and/or Azure DevOps
- `git` available on the system (used for sparse-checkout downloads)

## Skills Folder Mapping

Skills are installed into these folders per AI IDE:

| AI IDE | Skills Folder |
|--------|--------------|
| GitHub Copilot | `.github/skills/` |
| Claude Code | `.claude/skills/` |
| Cursor | `.cursor/rules/` |
| Gemini CLI | `.gemini/extensions/` |
| Qwen Code | `.qwen/skills/` |
| Open Code | `.opencode/skill/` |
| Codex CLI | `.codex/skills/` |
| Windsurf | `.windsurf/skills/` |
| Kilo Code | `.kilocode/skills/` |
| Auggie CLI | `.augment/rules/` |
| CodeBuddy | `.codebuddy/skills/` |
| Roo Code | `.roo/skills/` |
| Amazon Q | `.amazonq/cli-agents/` |
| Amp | `.agents/skills/` |
| SHAI | `.shai/commands/` |
| IBM Bob | `.bob/skills/` |
| Jules | `skills/` |
| Qoder CLI | `.qoder/skills/` |
| Antigravity | `.agent/skills/` |

## Instructions

### Important: Script Path Resolution

All script paths in this skill are relative to the directory containing this SKILL.md file. Replace `{SKILL_DIR}` with the actual path to this skill's directory.

For example, if this skill is installed at `.claude/skills/add-skills/`, then `{SKILL_DIR}` = `.claude/skills/add-skills`.

### Step 1: Identify Requested Skills

1. Parse the user's request to determine which skills to install
2. If no specific names given, run `bash {SKILL_DIR}/scripts/list-skills.sh` (Mac/Linux) or `powershell -ExecutionPolicy Bypass -File {SKILL_DIR}/scripts/list-skills.ps1` (Windows) first to show available options and ask the user to choose

### Step 2: Detect Installed AI IDEs

Check which AI IDE folders exist in the project root. An IDE is "detected" if its agent folder or skills folder exists. Only install into detected IDEs.

### Step 3: Fetch Skill Source

1. Read `nightlife.yaml` to get issue URLs
2. Fetch repo definitions from each issue
3. Find which repository contains the requested skill

### Step 4: Install Using Shell Script

For each detected AI IDE, run the installation script:

**Mac/Linux:**
```bash
bash {SKILL_DIR}/scripts/add-skills.sh <repo_url> <branch> <repo_path> <skill_name> <target_dir>
```

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File {SKILL_DIR}/scripts/add-skills.ps1 <repo_url> <branch> <repo_path> <skill_name> <target_dir>
```

**Parameters:**
- `repo_url`: Repository URL — GitHub (`https://github.com/owner/repo`) or Azure DevOps (`https://dev.azure.com/org/project/_git/repo`)
- `branch`: Git branch (e.g., `main`)
- `repo_path`: Path in repo containing skills (e.g., `skills`)
- `skill_name`: Name of the skill to download (e.g., `git-commit`)
- `target_dir`: Local target directory (e.g., `.claude/skills/git-commit`)

The script uses `git sparse-checkout` to efficiently download only the specific skill folder from the repository, preserving the full directory structure (`scripts/`, `templates/`, `references/`). This avoids recursive API calls and is not affected by API rate limits. Authentication is handled via `GH_TOKEN`/`GITHUB_TOKEN` for GitHub repos or `AZURE_DEVOPS_PAT`/`ADO_TOKEN` for Azure DevOps repos.

### Step 5: Report Results

For each skill installed, report:
- Which IDEs it was installed to
- The directory path created
- Any failures with error details

## Example

User: "Install the git-commit and pdf skills"

1. Read `nightlife.yaml` -> fetch repos from issues -> find skill repos with their `url`, `branch`, and `path`
2. Find which repos contain `git-commit` (e.g., repo-a at `https://github.com/owner/repo-a`, path `skills`) and `pdf` (e.g., repo-b at `https://github.com/owner/repo-b`, path `skills`)
3. Detect Claude Code (`.claude/skills/` exists) and Copilot (`.github/skills/` exists)
4. Run for Claude + git-commit (assuming skill is at `.claude/skills/add-skills/`):
   ```bash
   bash .claude/skills/add-skills/scripts/add-skills.sh https://github.com/owner/repo-a main skills git-commit .claude/skills/git-commit
   ```
5. Run for Copilot + git-commit:
   ```bash
   bash .claude/skills/add-skills/scripts/add-skills.sh https://github.com/owner/repo-a main skills git-commit .github/skills/git-commit
   ```
6. Run for Claude + pdf:
   ```bash
   bash .claude/skills/add-skills/scripts/add-skills.sh https://github.com/owner/repo-b main skills pdf .claude/skills/pdf
   ```
7. Run for Copilot + pdf:
   ```bash
   bash .claude/skills/add-skills/scripts/add-skills.sh https://github.com/owner/repo-b main skills pdf .github/skills/pdf
   ```
8. Report: "Installed git-commit and pdf to Claude Code and GitHub Copilot"

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub personal access token (used for git clone auth) |
| `AZURE_DEVOPS_PAT` / `ADO_TOKEN` | Azure DevOps personal access token (used for git clone auth) |

## Error Handling

| Error | Resolution |
|-------|------------|
| Skill not found in any repo | Run `list-skills` to show available names |
| No AI IDE folders detected | Run `phoenix init` first to set up the project |
| Git clone failed | Check internet connection, repo URL, and auth tokens |
| Permission denied | Check write permissions on target directories |
| Azure DevOps auth error | Set `AZURE_DEVOPS_PAT` environment variable with a valid PAT |

## Related Skills

- **list-skills**: List available skills before installing
- **add-agents**: Install agent commands instead of skills
- **list-agents**: List available agent commands
