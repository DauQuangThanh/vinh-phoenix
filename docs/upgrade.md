# Upgrade Guide

> Keep your Phoenix skills and CLI tool up to date with the latest improvements, new skills, and bug fixes. This guide covers upgrading both the CLI tool and your project's skills.

---

## Quick Reference

| What to Upgrade | Command | When to Use |
| ---------------- | --------- |-------------|
| **CLI Tool Only** | `uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git` | Get latest CLI features without touching project files |
| **Project Skills** | `phoenix init --here --force --ai <your-agent>` | Update skills, templates, and scripts in your project |
| **Both** | Run CLI upgrade, then project update | Recommended for major version updates |

---

## Part 1: Upgrade the CLI Tool

The CLI tool (`phoenix`) distributes skills to projects. Upgrade it to get the latest distribution features.

### If you installed with `uv tool install`

```bash
uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git
```

### If you use one-shot `uvx` commands

No upgrade needed—`uvx` always fetches the latest version. Just run your commands as normal:

```bash
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init --here --ai copilot
```

### Verify the upgrade

```bash
phoenix check
```

This shows installed tools and confirms the CLI is working.

---

## Part 2: Updating Project Skills

When Phoenix releases new skills or improvements, refresh your project to get the latest versions.

### What gets updated?

Running `phoenix init --here --force` will update:

- ✅ **Agent skill files** - Agent-specific skill definitions and templates
- ✅ **Agent skills** - All 18 skills with their templates and scripts (`.github/skills/`, `.claude/skills/`)
- ✅ **Shared documentation** (`docs/`) - **⚠️ See warnings below**

### What stays safe?

These files are **never touched** by the upgrade—skill packages don't contain them:

- ✅ **Your specifications** (`specs/001-my-feature/spec.md`, etc.) - **CONFIRMED SAFE**
- ✅ **Your implementation plans** (`specs/001-my-feature/plan.md`, `tasks.md`, etc.) - **CONFIRMED SAFE**
- ✅ **Your source code** - **CONFIRMED SAFE**
- ✅ **Your git history** - **CONFIRMED SAFE**

The `specs/` directory is completely excluded from template packages and will never be modified during upgrades.

### Update command

Run this inside your project directory:

```bash
phoenix init --here --force --ai <your-agent>
```

Replace `<your-agent>` with your AI assistant. Refer to this list of [Supported AI Agents](../README.md#-supported-ai-agents)

**Example:**

```bash
phoenix init --here --force --ai copilot
```

### Understanding the `--force` flag

Without `--force`, the CLI warns you and asks for confirmation:

```
Warning: Current directory is not empty (25 items)
Template files will be merged with existing content and may overwrite existing files
Proceed? [y/N]
```

With `--force`, it skips the confirmation and proceeds immediately.

**Important: Your `specs/` directory is always safe.** The `--force` flag only affects Phoenix framework files (commands, skills, documentation). Your feature specifications, plans, and tasks in `specs/` are never included in upgrade packages and cannot be overwritten.

---

## ⚠️ Important Warnings

### 1. Ground rules file will be overwritten

**Known issue:** `phoenix init --here --force` currently overwrites `docs/ground-rules.md` with the default template, erasing any customizations you made.

**Workaround:**

```bash
# 1. Back up your ground rules before upgrading
cp docs/ground-rules.md docs/ground-rules-backup.md

# 2. Run the upgrade
phoenix init --here --force --ai copilot

# 3. Restore your customized ground rules
mv docs/ground-rules-backup.md docs/ground-rules.md
```

Or use git to restore it:

```bash
# After upgrade, restore from git history
git restore docs/ground-rules.md
```

### 2. Duplicate skills (IDE-based agents)

Some IDE-based agents (like Kilo Code, Windsurf) may show **duplicate skills** after upgrading—both old and new versions appear.

**Solution:** Manually delete the old command files from your agent's folder.

**Example for Kilo Code:**

```bash
# Navigate to the agent's commands folder
cd .kilocode/rules/

# List files and identify duplicates
ls -la

# Delete old versions (example filenames - yours may differ)
rm phoenix.specify-old.md
rm phoenix.design-v1.md
```

Restart your IDE to refresh the command list.

---

## Common Scenarios

### Scenario 1: "I just want new agent skills"

```bash
# Upgrade CLI (if using persistent install)
uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git

# Update project files to get new commands
phoenix init --here --force --ai copilot

# Restore your ground rules if customized
git restore docs/ground-rules.md
```

### Scenario 2: "I customized ground-rules"

```bash
# 1. Back up customizations
cp docs/ground-rules.md /tmp/ground-rules-backup.md

# 2. Upgrade CLI
uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git

# 3. Update project
phoenix init --here --force --ai copilot

# 4. Restore customizations
mv /tmp/ground-rules-backup.md docs/ground-rules.md
```

### Scenario 3: "I see duplicate skills in my IDE"

This happens with IDE-based agents (Kilo Code, Windsurf, Roo Code, etc.).

```bash
# Find the agent folder (example: .kilocode/rules/)
cd .kilocode/rules/

# List all files
ls -la

# Delete old command files
rm phoenix.old-command-name.md

# Restart your IDE
```

### Scenario 4: "I'm working on a project without Git"

If you initialized your project with `--no-git`, you can still upgrade:

```bash
# Manually back up files you customized
cp docs/ground-rules.md /tmp/ground-rules-backup.md

# Run upgrade
phoenix init --here --force --ai copilot --no-git

# Restore customizations
mv /tmp/ground-rules-backup.md docs/ground-rules.md
```

The `--no-git` flag skips git initialization but doesn't affect file updates.

---

## Using `--no-git` Flag

The `--no-git` flag tells Vinh Phoenix to **skip git repository initialization**. This is useful when:

- You manage version control differently (Mercurial, SVN, etc.)
- Your project is part of a larger monorepo with existing git setup
- You're experimenting and don't want version control yet

**During initial setup:**

```bash
phoenix init my-project --ai copilot --no-git
```

**During upgrade:**

```bash
phoenix init --here --force --ai copilot --no-git
```

### What `--no-git` does NOT do

❌ Does NOT prevent file updates
❌ Does NOT skip skill installation
❌ Does NOT affect template merging

It **only** skips running `git init` and creating the initial commit.

### Working without Git

If you use `--no-git`, you'll need to manage feature directories manually:

**Set the `SPECIFY_FEATURE` environment variable** before using planning commands:

```bash
# Bash/Zsh
export SPECIFY_FEATURE="001-my-feature"

# PowerShell
$env:SPECIFY_FEATURE = "001-my-feature"
```

This tells Vinh Phoenix which feature directory to use when creating specs, plans, and tasks.

**Why this matters:** Without git, Vinh Phoenix can't detect your current branch name to determine the active feature. The environment variable provides that context manually.

---

## Troubleshooting

### "Skills not available after upgrade"

**Cause:** Agent didn't reload the command files.

**Fix:**

1. **Restart your IDE/editor** completely (not just reload window)
2. **For CLI-based agents**, verify files exist:

   ```bash
   ls -la .claude/commands/      # Claude Code
   ls -la .gemini/commands/       # Gemini
   ls -la .cursor/commands/       # Cursor
   ```

3. **Check agent-specific setup:**
   - Codex requires `CODEX_HOME` environment variable
   - Some agents need workspace restart or cache clearing

### "I lost my ground rules customizations"

**Fix:** Restore from git or backup:

```bash
# If you committed before upgrading
git restore docs/ground-rules.md

# If you backed up manually
cp /tmp/ground-rules-backup.md docs/ground-rules.md
```

**Prevention:** Always commit or back up `ground-rules.md` before upgrading.

### "Warning: Current directory is not empty"

**Full warning message:**

```
Warning: Current directory is not empty (25 items)
Template files will be merged with existing content and may overwrite existing files
Do you want to continue? [y/N]
```

**What this means:**

This warning appears when you run `phoenix init --here` (or `phoenix init .`) in a directory that already has files. It's telling you:

1. **The directory has existing content** - In the example, 25 files/folders
2. **Files will be merged** - New template files will be added alongside your existing files
3. **Some files may be overwritten** - If you already have Vinh Phoenix files (`.claude/`, `.github/`, etc.), they'll be replaced with the new versions

**What gets overwritten:**

Only Vinh Phoenix infrastructure files:

- Agent skills folders (`.github/skills/`, `.claude/skills/`, etc.)
- Shared documentation (`docs/`)

**What stays untouched:**

- Your `specs/` directory (specifications, plans, tasks)
- Your source code files
- Your `.git/` directory and git history
- Any other files not part of Vinh Phoenix templates

**How to respond:**

- **Type `y` and press Enter** - Proceed with the merge (recommended if upgrading)
- **Type `n` and press Enter** - Cancel the operation
- **Use `--force` flag** - Skip this confirmation entirely:

  ```bash
  phoenix init --here --force --ai copilot
  ```

**When you see this warning:**

- ✅ **Expected** when upgrading an existing Vinh Phoenix project
- ✅ **Expected** when adding Vinh Phoenix to an existing codebase
- ⚠️ **Unexpected** if you thought you were creating a new project in an empty directory

**Prevention tip:** Before upgrading, commit or back up your `docs/ground-rules.md` if you customized it.

### "CLI upgrade doesn't seem to work"

Verify the installation:

```bash
# Check installed tools
uv tool list

# Should show phoenix-cli

# Verify path
which phoenix

# Should point to the uv tool installation directory
```

If not found, reinstall:

```bash
uv tool uninstall phoenix-cli
uv tool install phoenix-cli --from git+https://github.com/dauquangthanh/vinh-phoenix.git
```

### "Do I need to run phoenix every time I open my project?"

**Short answer:** No, you only run `phoenix init` once per project (or when upgrading).

**Explanation:**

The `phoenix` CLI tool is used for:

- **Initial setup:** `phoenix init` to bootstrap Vinh Phoenix in your project
- **Upgrades:** `phoenix init --here --force` to update templates and skills
- **Diagnostics:** `phoenix check` to verify tool installation

Once you've run `phoenix init`, the skills are **permanently installed** in your project's agent-specific folders (`.claude/skills/`, `.github/skills/`, etc.). Your AI assistant automatically discovers these skills—no need to run `phoenix` again.

**If your agent isn't discovering skills:**

1. **Verify skill files exist:**

   ```bash
   # For GitHub Copilot
   ls -la .github/skills/

   # For Claude
   ls -la .claude/skills/
   ```

2. **Restart your IDE/editor completely** (not just reload window)

3. **Check you're in the correct directory** where you ran `phoenix init`

4. **For some agents**, you may need to reload the workspace or clear cache

**Related issue:** If Copilot can't open local files or uses PowerShell commands unexpectedly, this is typically an IDE context issue, not related to `phoenix`. Try:

- Restarting VS Code
- Checking file permissions
- Ensuring the workspace folder is properly opened

---

## Version Compatibility

Vinh Phoenix follows semantic versioning for major releases. The CLI and project files are designed to be compatible within the same major version.

**Best practice:** Keep both CLI and project files in sync by upgrading both together during major version changes.

---

## Next Steps

After upgrading:

- **Test skills:** Ask your AI to "establish project ground rules" or similar to verify skills are discovered
- **Review release notes:** Check [GitHub Releases](https://github.com/dauquangthanh/vinh-phoenix/releases) for new features and breaking changes
- **Update workflows:** If new skills were added, update your team's development workflows
- **Check documentation:** Visit [github.io/spec-kit](https://github.github.io/spec-kit/) for updated guides
