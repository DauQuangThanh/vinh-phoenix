---
name: sync-skills
description: Syncs agent skills from external GitHub repositories into the local skill list. Reads repository URLs from the GitHub issue https://github.com/DauQuangThanh/vinh-phoenix/issues/2, fetches all SKILL.md files from each repo's skills/ directory, extracts skill name and description, then adds or merges entries into docs/agent-skill-list.md (5 columns: skill name, description, banned, category, url). Use when refreshing the skill catalog, adding new skill repos, or auditing available skills.
metadata:
  author: Dau Quang Thanh
  version: "1.1.0"
  last-updated: "2026-03-13"
license: MIT
---

# Sync Skills

## Overview

This skill reads a list of GitHub repository URLs from the GitHub issue at **https://github.com/DauQuangThanh/vinh-phoenix/issues/2**, fetches all agent skills defined in those repositories, and merges them into the local skill catalog at `docs/agent-skill-list.md`.

The catalog tracks five columns per skill: name, description, banned status, category, and URL. Existing entries are updated (name, description, and URL refreshed) while preserving any manually configured `banned` and `category` values. New skills are added with defaults (`banned: yes`, `category: development`).

## When to Use

- Refreshing the local skill catalog from upstream repositories
- After a new repository URL is added to the tracking GitHub issue
- Auditing what skills are available across all registered repos
- Onboarding a new project and populating its skill list
- User mentions: "sync skills", "update skill list", "refresh skills", "fetch skills from repos"

## Prerequisites

- Internet access to fetch from GitHub (uses raw content and GitHub API)
- `docs/agent-skill-list.md` exists (will be created if absent)

## Instructions

### Step 1: Read Repository URLs from GitHub Issue

1. Fetch the GitHub issue using the GitHub API:
   ```
   GET https://api.github.com/repos/DauQuangThanh/vinh-phoenix/issues/2
   ```
   Extract the `body` field from the JSON response.

2. Parse the issue body and extract all GitHub repository URLs. Valid URLs match the pattern `https://github.com/<owner>/<repo>` (with or without trailing `.git`). Accept URLs in any of these formats within the body:
   - Bare URL: `https://github.com/owner/repo`
   - Markdown link: `[label](https://github.com/owner/repo)`
   - List item: `- https://github.com/owner/repo`

3. Skip any URLs that are not GitHub repository URLs (e.g., issue links, profile links).

4. If the issue cannot be fetched (401/404), report: "Cannot access https://github.com/DauQuangThanh/vinh-phoenix/issues/2. Ensure the repository is public or provide a GitHub token." Then stop.

5. If no repository URLs are found in the issue body, report: "No repository URLs found in the issue body. Add at least one GitHub repository URL to https://github.com/DauQuangThanh/vinh-phoenix/issues/2 and retry." Then stop.

### Step 2: Fetch Skills from Each Repository

For each repository URL:

1. **Determine the default branch** using the GitHub API:
   ```
   GET https://api.github.com/repos/<owner>/<repo>
   ```
   Extract `default_branch` from the JSON response (usually `main` or `master`). If the API call fails, fall back to `main`.

2. **List all files in the repository** using the Git Trees API:
   ```
   GET https://api.github.com/repos/<owner>/<repo>/git/trees/<default_branch>?recursive=1
   ```
   Parse the `tree` array and collect all entries whose `path` matches the pattern `skills/*/SKILL.md` (exactly two path segments under `skills/`).

3. **Fetch each SKILL.md file** using the raw content URL:
   ```
   https://raw.githubusercontent.com/<owner>/<repo>/<default_branch>/<path>
   ```

4. **Parse the YAML frontmatter** from each SKILL.md:
   - Extract `name` (string)
   - Extract `description` (string)
   - If either field is missing or the file has no frontmatter, skip with a warning: "Skipped <path>: missing name or description in frontmatter."

5. For each fetched SKILL.md, construct the skill URL as the GitHub web-browsable link to the file:
   ```
   https://github.com/<owner>/<repo>/blob/<default_branch>/<path>
   ```
   Example: `https://github.com/acme/skills/blob/main/skills/git-commit/SKILL.md`

6. Collect all valid `(name, description, url, source_repo)` tuples.

**Rate limiting**: If the GitHub API returns HTTP 403 or 429, report the error and stop. Do not retry automatically — inform the user to check their network or GitHub token.

**Private repos**: If a repo returns HTTP 404 or 401, report: "Cannot access <url>. Ensure the repository is public or provide a GitHub token." Skip the repo and continue.

### Step 3: Load Existing Skill List

1. Read `docs/agent-skill-list.md`.
2. Parse the markdown table under the `## Skills` heading. Each data row has 4 columns: `Skill Name`, `Description`, `Banned`, `Category`.
3. Build an in-memory map keyed by `skill name` (case-insensitive):
   ```
   { "skill-name": { description, banned, category, url } }
   ```
4. If the file doesn't exist or has no table rows, start with an empty map.

### Step 4: Merge Skills

For each fetched skill `(name, description)`:

- **If the skill already exists** in the map (matched by name, case-insensitive):
  - Update `description` and `url` with the freshly fetched values.
  - Keep existing `banned` and `category` values unchanged.
- **If the skill is new**:
  - Add it with defaults: `banned: yes`, `category: development`, and the fetched `url`.

After processing all fetched skills, keep any existing skills in the map that were **not** found in any fetched repo (do not delete them — they may be locally added or from a repo that is temporarily unavailable).

### Step 5: Write Updated Skill List

1. Sort the merged skill map alphabetically by skill name (case-insensitive).
2. Rewrite `docs/agent-skill-list.md` preserving the header section and replacing the table under `## Skills`:

```markdown
# Agent Skill List

Managed by the `sync-skills` agent skill. Do not edit the `Skill Name` or `Description` columns manually — they are synced from repositories listed in https://github.com/DauQuangThanh/vinh-phoenix/issues/2. You may update `Banned` and `Category` columns freely.

**Columns:**
- **Skill Name** — Unique skill identifier (from SKILL.md frontmatter `name`)
- **Description** — Short description of the skill (from SKILL.md frontmatter `description`)
- **Banned** — Whether this skill is blocked from use (`yes` / `no`, default: `yes`)
- **Category** — Skill domain: `development` / `testing` / `maintenance` / `managed services` (default: `development`)
- **URL** — GitHub link to the SKILL.md file in the source repository

## Skills

| Skill Name | Description | Banned | Category | URL |
|------------|-------------|--------|----------|-----|
| <name> | <description> | <banned> | <category> | <url> |
...
```

3. Ensure descriptions containing pipe characters (`|`) are escaped as `\|` to avoid breaking the markdown table.
4. Render the URL column as a markdown link: `[SKILL.md](<url>)` for readability.

### Step 6: Report Summary

Print a summary:

```
✅ Sync complete

Repositories processed: <N>
Skills fetched:         <N>
  - New skills added:   <N>
  - Existing updated:   <N>
  - Skipped (errors):   <N>

Skill list written to: docs/agent-skill-list.md
```

If any repos or files were skipped with errors, list them:
```
⚠️  Warnings:
  - Skipped https://github.com/owner/repo: Cannot access repository
  - Skipped skills/bad-skill/SKILL.md: missing name or description
```

## Error Handling

| Error | Action |
|-------|--------|
| GitHub issue not accessible (401/404) | Report error and stop |
| No URLs found in issue body | Report and stop |
| GitHub API rate limit (403/429) | Report and stop; advise user to wait or add a token |
| Repo not accessible (401/404) | Skip repo, continue with others |
| SKILL.md missing frontmatter | Skip file, log warning |
| SKILL.md missing `name` or `description` | Skip file, log warning |
| `docs/agent-skill-list.md` parse error | Start fresh with empty map, log warning |

## Examples

### Example 1: First-time sync with one repository

**Issue body at https://github.com/DauQuangThanh/vinh-phoenix/issues/2:**
```
- https://github.com/acme/agent-skills
```

**Fetched skills:** `git-commit`, `coding`, `code-review` (3 new)

**Output `docs/agent-skill-list.md` table:**

| Skill Name | Description | Banned | Category | URL |
|------------|-------------|--------|----------|-----|
| code-review | Reviews code for quality... | yes | development | [SKILL.md](https://github.com/acme/agent-skills/blob/main/skills/code-review/SKILL.md) |
| coding | Executes feature implementation... | yes | development | [SKILL.md](https://github.com/acme/agent-skills/blob/main/skills/coding/SKILL.md) |
| git-commit | Generates well-structured git commits... | yes | development | [SKILL.md](https://github.com/acme/agent-skills/blob/main/skills/git-commit/SKILL.md) |

### Example 2: Re-sync after updating descriptions upstream

Existing entry: `coding | old description | no | development | [SKILL.md](...old-url...)`
Fetched update: `coding | new description | url: ...new-url...`

Result: `coding | new description | no | development | [SKILL.md](...new-url...)` — description and URL updated, `banned: no` and `category` preserved.

### Example 3: Adding a second repository

Two repos in the issue body. Repo A has 5 skills, Repo B has 3 skills, two names overlap. Result: 6 unique skills in the list (overlapping skills merged, last-listed repo's description wins).

## Notes

- This skill uses **WebFetch** to access GitHub API and raw content endpoints. No local git operations are performed.
- The skill does **not** download or install skills locally — it only updates the catalog document.
- The `banned` and `category` columns are intentionally human-managed. The sync only touches `name` and `description`.
- If a skill name appears in multiple repositories, the last repo processed wins for the description. Repos are processed in the order they appear in the issue body.
- To add or remove a repository from the sync list, edit the issue body at https://github.com/DauQuangThanh/vinh-phoenix/issues/2.
