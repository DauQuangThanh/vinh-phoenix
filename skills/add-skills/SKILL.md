---
name: add-skills
description: Downloads and installs one or more agent skills from the catalog into the local project. Accepts skill names as input, looks them up in docs/agent-skill-list.md, fetches all files for each skill from their source GitHub repository, and saves them into the correct AI-tool-specific folders (.claude/skills/, .github/skills/, .cursor/rules/, etc.) based on which AI tools are detected in the project. Use when installing skills, adding skills to a project, or setting up skill packages for AI tools.
metadata:
  author: Dau Quang Thanh
  version: "1.0.0"
  last-updated: "2026-03-13"
license: MIT
---

# Add Skills

## Overview

This skill installs one or more agent skills from the catalog into the local project. It looks up requested skill names in `docs/agent-skill-list.md`, fetches all files for each matching skill from their source GitHub repository, and saves them into the correct folder for every AI tool detected in the project.

## When to Use

- Installing new skills into a project
- Setting up skills for multiple AI tools at once
- After running `sync-skills` to populate the catalog
- User mentions: "add skill", "install skill", "download skill", "add skills to project", "set up skills"

## Prerequisites

- `docs/agent-skill-list.md` must exist and be populated (run `sync-skills` first if missing)
- Internet access to fetch from GitHub
- At least one AI tool config folder present in the project (e.g. `.claude/`, `.github/`, `.cursor/`)

## AI Tool Folder Mapping

The skill detects which AI tools are active in the project by checking for their characteristic config directories, then installs skills into the correct subfolder:

| AI Tool | Detection Marker | Skills Folder |
|---------|-----------------|---------------|
| Claude Code | `.claude/` | `.claude/skills/` |
| GitHub Copilot | `.github/` | `.github/skills/` |
| Cursor | `.cursor/` | `.cursor/rules/` |
| Windsurf | `.windsurf/` | `.windsurf/skills/` |
| Amazon Q Developer | `.amazonq/` | `.amazonq/cli-agents/` |
| Roo Code | `.roo/` | `.roo/skills/` |
| Kilo Code | `.kilocode/` | `.kilocode/skills/` |
| Gemini CLI | `.gemini/` | `.gemini/extensions/` |
| Amp | `.agents/` | `.agents/skills/` |
| Auggie CLI | `.augment/` | `.augment/rules/` |
| CodeBuddy CLI | `.codebuddy/` | `.codebuddy/skills/` |
| Codex CLI | `.codex/` | `.codex/skills/` |
| IBM Bob | `.bob/` | `.bob/skills/` |
| opencode | `.opencode/` | `.opencode/skill/` |
| Qoder CLI | `.qoder/` | `.qoder/skills/` |
| Qwen Code | `.qwen/` | `.qwen/skills/` |
| SHAI (OVHcloud) | `.shai/` | `.shai/commands/` |
| Google Antigravity | `.agent/` | `.agent/skills/` |
| Jules | `skills/` (root) | `skills/` |

## Instructions

### Step 1: Check Catalog Exists

1. Check whether `docs/agent-skill-list.md` exists in the project root.
2. If it does **not** exist, stop and report:
   ```
   ❌ docs/agent-skill-list.md not found.
   Please run the sync-skills skill first to populate the skill catalog.
   ```

### Step 2: Parse Requested Skill Names

1. Read the skill names provided by the user as input arguments (space-separated or comma-separated list).
   Example inputs:
   - `git-commit coding code-review`
   - `git-commit, coding, code-review`
   - A single name: `git-commit`
2. Normalize each name: trim whitespace, lowercase.
3. If no names were provided, ask the user:
   ```
   Which skills do you want to add? Please provide skill names (e.g. git-commit coding code-review).
   Refer to docs/agent-skill-list.md for the full list of available skills.
   ```

### Step 3: Look Up Skills in Catalog

1. Read `docs/agent-skill-list.md` and parse the table under `## Skills`. Each row has 5 columns: `Skill Name`, `Description`, `Banned`, `Category`, `URL`.
2. For each requested skill name, find the matching row (case-insensitive match on `Skill Name`).
3. Separate results into:
   - **Found**: skill name matched in the catalog
   - **Not found**: skill name has no match

4. If **all** requested names are not found, stop and report:
   ```
   ❌ None of the requested skills were found in the catalog:
     - <name1>
     - <name2>

   Please refer to docs/agent-skill-list.md to select correct skill names.
   Tip: run sync-skills to refresh the catalog if it is out of date.
   ```

5. If **some** names are not found (partial match), report the missing ones as warnings and continue with the found skills:
   ```
   ⚠️  The following skills were not found in the catalog and will be skipped:
     - <name>  →  not found
   Continuing with matched skills: <name1>, <name2>...
   ```

### Step 4: Handle Banned Skills

1. Check the `Banned` column for each found skill.
2. If any skill has `Banned: yes`, warn the user and ask for explicit confirmation before proceeding:
   ```
   ⚠️  The following skills are marked as banned in the catalog:
     - <name> (Category: <category>)

   Banned skills may be restricted for policy, security, or compatibility reasons.
   Do you want to install them anyway? (yes/no)
   ```
3. If the user says **no**, remove the banned skills from the install list and continue with the remaining ones.
4. If the user says **yes**, proceed with all skills including banned ones.
5. If **all** skills are banned and the user declines, stop with:
   ```
   ℹ️  No skills selected for installation.
   ```

### Step 5: Detect AI Tools in the Project

1. Check the project root for the detection markers listed in the AI Tool Folder Mapping table above.
2. Build a list of detected tools and their target skills folders.
3. If **no** AI tool markers are found, stop and report:
   ```
   ❌ No AI tool configuration folders detected in this project.
   To install skills, create one of the following folders first:
     .claude/        → Claude Code
     .github/        → GitHub Copilot
     .cursor/        → Cursor
     .windsurf/      → Windsurf
     (see docs for full list)
   ```
4. If tools are detected, display them and ask the user to confirm:
   ```
   🔍 Detected AI tools in this project:
     ✓ Claude Code    → .claude/skills/
     ✓ GitHub Copilot → .github/skills/
     ✓ Cursor         → .cursor/rules/

   Skills will be installed for all detected tools. Proceed? (yes/no/select)
   ```
   - **yes**: install for all detected tools
   - **no**: cancel installation
   - **select**: ask the user to pick a subset of the detected tools

### Step 6: Download Each Skill

For each skill to install:

1. **Parse the URL** from the catalog row. The URL format is:
   ```
   https://github.com/<owner>/<repo>/blob/<branch>/skills/<skill-name>/SKILL.md
   ```
   Extract: `owner`, `repo`, `branch`, `skill_dir` (e.g. `skills/git-commit`).

2. **List all files** in the skill directory using the GitHub API:
   ```
   GET https://api.github.com/repos/<owner>/<repo>/git/trees/<branch>?recursive=1
   ```
   Filter all `tree` entries whose `path` starts with `<skill_dir>/` and whose `type` is `blob`.

3. **Download each file** using the raw content URL:
   ```
   https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<file_path>
   ```

4. Collect all `(relative_path, content)` pairs, where `relative_path` is the path **relative to** the skill directory (e.g., `SKILL.md`, `references/best-practices.md`, `scripts/check.py`).

**Error handling during download:**
- If the GitHub API returns 403/429 (rate limit): stop and report the error; advise the user to wait or use a token.
- If a skill URL returns 404/401: skip the skill and report: "Cannot fetch <skill-name>: repository not accessible."
- If an individual file fails: skip that file, log a warning, continue with remaining files.

### Step 7: Save Files to AI Tool Folders

For each detected AI tool and each downloaded skill:

1. Determine the destination root: `<tool_skills_folder>/<skill-name>/`
   - Example for Claude Code: `.claude/skills/git-commit/`
   - Example for GitHub Copilot: `.github/skills/git-commit/`

2. For each `(relative_path, content)` pair, write the file to:
   ```
   <tool_skills_folder>/<skill-name>/<relative_path>
   ```

3. Create intermediate directories as needed.

4. If a file already exists at the destination:
   - **Overwrite** it silently (re-running `add-skills` refreshes installed skills).

### Step 8: Report Results

Print a final summary:

```
✅ Skills installation complete

Skills installed: <N>
AI tools updated: <N>

Installed skills:
  ✓ git-commit   → .claude/skills/git-commit/   (12 files)
  ✓ git-commit   → .github/skills/git-commit/   (12 files)
  ✓ coding       → .claude/skills/coding/        (8 files)
  ✓ coding       → .github/skills/coding/        (8 files)

⚠️  Warnings (if any):
  - Skipped file scripts/check.py in git-commit: download failed
```

## Error Handling

| Error | Action |
|-------|--------|
| `docs/agent-skill-list.md` not found | Stop; suggest running `sync-skills` |
| No skill names provided | Ask user for input |
| All skill names not found in catalog | Stop; suggest referring to `agent-skill-list.md` |
| Some skill names not found | Warn and skip; continue with found skills |
| Skill is banned | Warn and ask confirmation |
| No AI tool folders detected | Stop; list folders user can create |
| GitHub API rate limit (403/429) | Stop; advise user to wait or add token |
| Skill URL not accessible (401/404) | Skip skill; continue with others |
| Individual file download fails | Skip file; warn; continue |
| Destination directory creation fails | Report error for that tool; continue with others |

## Examples

### Example 1: Install a single skill for one AI tool

**Command:** `add-skills git-commit`

**Project has:** `.claude/` only

**Result:**
```
✅ Skills installation complete

Skills installed: 1
AI tools updated: 1

Installed skills:
  ✓ git-commit → .claude/skills/git-commit/ (12 files)
```

### Example 2: Install multiple skills for multiple AI tools

**Command:** `add-skills git-commit coding code-review`

**Project has:** `.claude/`, `.github/`, `.cursor/`

**Result:**
```
✅ Skills installation complete

Skills installed: 3
AI tools updated: 3

Installed skills:
  ✓ git-commit   → .claude/skills/git-commit/    (12 files)
  ✓ git-commit   → .github/skills/git-commit/    (12 files)
  ✓ git-commit   → .cursor/rules/git-commit/     (12 files)
  ✓ coding       → .claude/skills/coding/         (8 files)
  ✓ coding       → .github/skills/coding/         (8 files)
  ✓ coding       → .cursor/rules/coding/          (8 files)
  ✓ code-review  → .claude/skills/code-review/    (5 files)
  ✓ code-review  → .github/skills/code-review/    (5 files)
  ✓ code-review  → .cursor/rules/code-review/     (5 files)
```

### Example 3: Skill name not found in catalog

**Command:** `add-skills gitt-commit`

**Result:**
```
❌ None of the requested skills were found in the catalog:
  - gitt-commit

Please refer to docs/agent-skill-list.md to select correct skill names.
Tip: run sync-skills to refresh the catalog if it is out of date.
```

### Example 4: Mix of found and not-found skills

**Command:** `add-skills git-commit unknown-skill`

**Result:**
```
⚠️  The following skills were not found in the catalog and will be skipped:
  - unknown-skill → not found
Continuing with matched skills: git-commit...

✅ Skills installation complete
...
```

### Example 5: Banned skill with user confirmation

**Command:** `add-skills restricted-skill`

**Interaction:**
```
⚠️  The following skills are marked as banned in the catalog:
  - restricted-skill (Category: development)

Banned skills may be restricted for policy, security, or compatibility reasons.
Do you want to install them anyway? (yes/no)

> yes

✅ Skills installation complete
...
```

## Notes

- Re-running `add-skills` with the same skill names will **overwrite** existing files, effectively upgrading the skill to the latest version from the source repository.
- The skill installs into **all detected AI tool folders** by default. Use the **select** option at the confirmation prompt to target specific tools.
- Files are downloaded directly from the source GitHub repository referenced in the `URL` column of `docs/agent-skill-list.md`. Ensure the source repo is accessible.
- Jules is detected by the presence of a `skills/` directory at the project root. Because this conflicts with the local `skills/` folder used by this project itself, Jules installation is **skipped by default** unless the user explicitly selects it.
