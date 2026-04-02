# Upgrade Guide

> Keep your Phoenix CLI and core meta-skills up to date with the latest improvements and bug fixes.

---

## Quick Reference

| What to Upgrade | Command | When to Use |
|-----------------|---------|-------------|
| **CLI Tool Only** | `uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git` | Get latest CLI features without touching project files |
| **Project Meta-Skills** | `phoenix init --upgrade` | Update the 5 core meta-skills in your project (creates timestamped backups) |
| **Both** | Run CLI upgrade, then project update | Recommended for major version updates |

---

## Part 1: Upgrade the CLI Tool

The CLI tool (`phoenix`) installs meta-skills into projects. Upgrade it to get the latest distribution features.

### If you installed with `uv tool install`

```bash
uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git
```

### If you use one-shot `uvx` commands

No upgrade needed — `uvx` always fetches the latest version:

```bash
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git phoenix init --here --ai copilot
```

### Verify the upgrade

```bash
phoenix check
```

---

## Part 2: Updating Project Meta-Skills

When Phoenix releases improvements to the core meta-skills, refresh your project to get the latest versions.

### What gets updated?

Running `phoenix init --upgrade` will:

- ✅ **Create timestamped backups** of existing agent folders (e.g., `.claude.backup.20260402_143000`)
- ✅ **Replace core meta-skills** — `git-commit`, `list-skills`, `add-skills`, `list-agents`, `add-agents`
- ✅ **Preserve `nightlife.yaml`** — only created if not already present

### What stays safe?

These files are **never touched** by the upgrade:

- ✅ **Your specifications** (`specs/`) — **CONFIRMED SAFE**
- ✅ **Your source code** — **CONFIRMED SAFE**
- ✅ **Your git history** — **CONFIRMED SAFE**
- ✅ **Skills you installed via `add-skills`** — backed up and preserved
- ✅ **Your `nightlife.yaml` customizations** — never overwritten

### Update command

Run this inside your project directory:

```bash
# Upgrade with interactive agent selection
phoenix init --upgrade

# Upgrade with specific agent
phoenix init --upgrade --ai copilot

# Upgrade and skip confirmation
phoenix init --upgrade --force --ai copilot
```

The `--upgrade` flag detects existing Phoenix agent folders, creates backups with timestamps, then replaces them with the latest templates.

### nightlife.yaml during upgrades

`phoenix init` will **not overwrite** an existing `nightlife.yaml` — your custom URL configuration is preserved.

If you want to reset it to the defaults:

```bash
# Back up your customizations first
cp nightlife.yaml nightlife.yaml.backup

# Re-run init (will skip nightlife.yaml since it already exists)
phoenix init --here --force --ai copilot
```

---

## ⚠️ Important Warnings

### Duplicate skills (IDE-based agents)

Some IDE-based agents (like Kilo Code, Windsurf) may show **duplicate skills** after upgrading — both old and new versions appear.

**Solution:** Manually delete the old skill files from your agent's folder.

**Example for Kilo Code:**

```bash
cd .kilocode/skills/
ls -la
rm -rf old-skill-name/
```

Restart your IDE to refresh the command list.

---

## Common Scenarios

### Scenario 1: "I just want updated meta-skills"

```bash
# Upgrade CLI
uv tool install phoenix-cli --force --from git+https://github.com/dauquangthanh/vinh-phoenix.git

# Update project meta-skills (creates backups automatically)
phoenix init --upgrade --ai copilot
```

### Scenario 2: "I customized nightlife.yaml"

Your customizations are safe — `phoenix init` does not overwrite an existing `nightlife.yaml`.

### Scenario 3: "I see duplicate skills in my IDE"

This happens with IDE-based agents (Kilo Code, Windsurf, Roo Code, etc.):

```bash
# Navigate to the agent's skills folder (example: .kilocode/skills/)
cd .kilocode/skills/

# List all files
ls -la

# Delete old versions
rm -rf old-skill-name/

# Restart your IDE
```

### Scenario 4: "I'm working on a project without Git"

```bash
# Run upgrade with --no-git
phoenix init --upgrade --ai copilot --no-git
```

---

## Using `--no-git` Flag

The `--no-git` flag tells Phoenix to **skip git repository initialization**. Useful when:

- You manage version control differently (Mercurial, SVN, etc.)
- Your project is part of a larger monorepo with existing git setup
- You're experimenting and don't want version control yet

---

## Troubleshooting

### "Skills not available after upgrade"

**Fix:**

1. **Restart your IDE/editor** completely (not just reload window)
2. **Verify meta-skill files exist:**

   ```bash
   ls -la .claude/skills/      # Claude Code
   ls -la .gemini/extensions/  # Gemini
   ls -la .github/skills/      # GitHub Copilot
   ```

3. **For some agents**, you may need to reload the workspace or clear cache

### "CLI upgrade doesn't seem to work"

Verify the installation:

```bash
uv tool list  # Should show phoenix-cli
which phoenix
```

If not found, reinstall:

```bash
uv tool uninstall phoenix-cli
uv tool install phoenix-cli --from git+https://github.com/dauquangthanh/vinh-phoenix.git
```

### "Do I need to run phoenix every time I open my project?"

**Short answer:** No. Run `phoenix init` once per project (or when upgrading).

Once meta-skills are installed, your AI assistant automatically discovers and uses them. The meta-skills then handle all further skill management via `nightlife.yaml`.

---

## Version Compatibility

Vinh Phoenix follows semantic versioning for major releases. The CLI and project meta-skills are designed to be compatible within the same major version.

**Best practice:** Keep both CLI and project meta-skills in sync by upgrading both together during major version changes.

---

## Next Steps

After upgrading:

- **Test meta-skills:** Ask your AI to "list available skills" to verify `list-skills` is working
- **Review release notes:** Check [GitHub Releases](https://github.com/dauquangthanh/vinh-phoenix/releases) for new features and breaking changes
