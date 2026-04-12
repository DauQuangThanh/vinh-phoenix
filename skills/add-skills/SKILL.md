---
name: add-skills
description: Downloads and installs skills from configured remote repositories (GitHub and Azure DevOps) into the correct AI IDE skill folders. Use when user wants to install, add, or download skills from the catalog. Uses git sparse-checkout to efficiently download the entire skill folder (SKILL.md, scripts, templates, references) for each detected AI IDE.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "2.0.0"
  last_updated: "2026-04-12"
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

- `nightlife.yaml` exists in the project root with configured `skills` section (supports multiple repositories)
- Project has been initialized with at least one AI IDE
- Internet connection to reach GitHub and/or Azure DevOps
- `git` available on the system (used for sparse-checkout downloads)

## Skills Folder Mapping

Skills are installed into these folders per AI IDE (based on AI-Agents-Configs April 2026):

| AI IDE | Skills Folder |
|--------|--------------|
| Amp | `.amp/skills/` |
| Antigravity | `.agent/skills/` |
| Augment Code | `.augment/skills/` |
| Claude Code | `.claude/skills/` |
| Cline | `.cline/skills/` |
| CodeBuddy | `.codebuddy/skills/` |
| Codex CLI | `.codex/skills/` |
| Cursor | `.cursor/skills/` |
| Forge | `.forge/skills/` |
| Gemini CLI | `.gemini/skills/` |
| GitHub Copilot (IDE) | `.github/skills/` |
| GitHub Copilot CLI | `.copilot/skills/` |
| IBM Bob | `.bob/skills/` |
| Junie | `.junie/skills/` |
| Kilo Code | `.kilocode/skills/` |
| Kiro | `.kiro/skills/` |
| Mistral Vibe | `.vibe/skills/` |
| opencode | `.opencode/skills/` |
| Pi Agent | `.omp/skills/` |
| Qoder | `.qoder/skills/` |
| Qwen Code | `.qwen/skills/` |
| Roo Code | `.roo/skills/` |
| Tabnine | `.tabnine/skills/` |
| Trae | `.trae/skills/` |
| Windsurf | `.windsurf/skills/` |

## Instructions

### Important: Script Path Resolution

All script paths in this skill are relative to the directory containing this SKILL.md file. Replace `{SKILL_DIR}` with the actual path to this skill's directory.

For example, if this skill is installed at `.claude/skills/add-skills/`, then `{SKILL_DIR}` = `.claude/skills/add-skills`.

### Step 1: Identify Requested Skills

1. Parse the user's request to determine which skills to install
2. If no specific names given, run `bash {SKILL_DIR}/scripts/list-skills.sh` (Mac/Linux) or `powershell -ExecutionPolicy Bypass -File {SKILL_DIR}/scripts/list-skills.ps1` (Windows) first to show available options and ask the user to choose

Note: The list-skills script is in the **list-skills** skill directory. If you have list-skills installed, use that path instead.

### Step 2: Detect Installed AI IDEs

Check which AI IDE folders exist in the project root. An IDE is "detected" if its config folder (e.g., `.claude/`, `.github/`, `.cursor/`) exists. Only install into detected IDEs.

### Step 3: Find Skill Source

1. Read `nightlife.yaml` to get skill repository entries (name, url, branch, path)
2. Each entry directly provides the repository name, URL, branch, and path where skills are located
3. **Multiple repositories**: nightlife.yaml can contain multiple skill repos — search all of them for the requested skill

### Step 3.1: Disambiguate When Skill Exists in Multiple Repos

If the requested skill name is found in **more than one** configured repository:

1. **List all matches** — show the user each repo that contains the skill:
   ```
   Skill "git-commit" was found in multiple repositories:
     1. DaNangNightlifeSkill (https://github.com/owner/repo-a, path: skills)
     2. VinhPhoenixSkill (https://github.com/owner/repo-b, path: skills)
   ```
2. **Ask the user to choose** which repository to install from
3. Only proceed with installation after the user confirms their choice
4. If the skill exists in only one repo, proceed without asking

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

The script uses `git sparse-checkout` to efficiently download only the specific skill folder from the repository, preserving the full directory structure (`scripts/`, `templates/`, `references/`). Authentication is handled via `GH_TOKEN`/`GITHUB_TOKEN` for GitHub repos or `AZURE_DEVOPS_PAT`/`ADO_TOKEN` for Azure DevOps repos.

### Step 5: Report Results

For each skill installed, report:
- Which IDEs it was installed to
- The directory path created
- Any failures with error details

## Example

### Example 1: Skill found in one repo

User: "Install the pdf skill"

1. Read `nightlife.yaml` → get skill repos (name, url, branch, path)
2. Search all repos for "pdf" → found only in DaNangNightlifeSkill
3. Detect Claude Code (`.claude/` exists) and Copilot (`.github/` exists)
4. Run for Claude:
   ```bash
   bash .claude/skills/add-skills/scripts/add-skills.sh https://github.com/owner/repo-a main skills pdf .claude/skills/pdf
   ```
5. Run for Copilot:
   ```bash
   bash .claude/skills/add-skills/scripts/add-skills.sh https://github.com/owner/repo-a main skills pdf .github/skills/pdf
   ```
6. Report: "Installed pdf to Claude Code and GitHub Copilot"

### Example 2: Skill found in multiple repos (disambiguation)

User: "Install the git-commit skill"

1. Read `nightlife.yaml` → get skill repos (name, url, branch, path)
2. Search all repos for "git-commit" → found in both DaNangNightlifeSkill and VinhPhoenixSkill
3. **Ask user to choose**:
   ```
   Skill "git-commit" was found in multiple repositories:
     1. DaNangNightlifeSkill (https://github.com/owner/repo-a, path: skills)
     2. VinhPhoenixSkill (https://github.com/owner/repo-b, path: skills)
   Which repository would you like to install from?
   ```
4. User chooses "1" → use repo-a
5. Detect Claude Code (`.claude/` exists)
6. Run:
   ```bash
   bash .claude/skills/add-skills/scripts/add-skills.sh https://github.com/owner/repo-a main skills git-commit .claude/skills/git-commit
   ```
7. Report: "Installed git-commit from DaNangNightlifeSkill to Claude Code"

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
- **add-agents**: Install agents instead of skills
- **list-agents**: List available agents
