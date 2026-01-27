# 💻 Local Development Guide

**Work on Phoenix CLI locally without publishing releases.**

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/dauquangthanh/vinh-phoenix.git
cd vinh-phoenix

# Work on a feature branch
git checkout -b your-feature-branch
```

---

### 2. Run CLI Directly (Fastest Way)

Test your changes instantly without installing:

```bash
# From repository root
python -m src.phoenix_cli --help
python -m src.phoenix_cli init demo-project --ai claude --ignore-agent-tools

# Multiple AI agents (comma-separated)
python -m src.phoenix_cli init demo-project --ai claude,gemini,copilot

# Use local templates (no GitHub download)
python -m src.phoenix_cli init demo-project --ai claude --local-templates --template-path .
```

**Alternative:** Run the script directly (uses shebang):

```bash
python src/phoenix_cli/__init__.py init demo-project
```

---

### 3. Use Editable Install (Like Real Users)

Create an isolated environment that matches how users run Phoenix:

```bash
# Create virtual environment (uv manages .venv automatically)
uv venv

# Activate it
source .venv/bin/activate  # Linux/macOS
# or on Windows PowerShell:
.venv\Scripts\Activate.ps1

# Install in editable mode
uv pip install -e .

# Now use 'phoenix' command directly
phoenix --help
```

**Benefit:** No need to reinstall after code changes—it updates automatically!

### 4. Test with uvx (Simulate User Experience)

Test how users will actually run Phoenix:

**From local directory:**

```bash
uvx --from . phoenix init demo-uvx --ai copilot --ignore-agent-tools
```

**From a specific branch (without merging):**

```bash
# Push your branch first
git push origin your-feature-branch

# Test it
uvx --from git+https://github.com/dauquangthanh/vinh-phoenix.git@your-feature-branch phoenix init demo-branch-test
```

#### Run from Anywhere (Absolute Path)

Use absolute paths when you're in a different directory:

```bash
uvx --from /mnt/c/GitHub/vinh-phoenix phoenix --help
uvx --from /mnt/c/GitHub/vinh-phoenix phoenix init demo-anywhere --ai copilot
```

**Make it easier with an environment variable:**

```bash
# Set once
export RAINBOW_SRC=/mnt/c/GitHub/vinh-phoenix

# Use anywhere
uvx --from "$RAINBOW_SRC" phoenix init demo-env --ai copilot
```

**Or create a shell function:**

```bash
phoenix-dev() { uvx --from /mnt/c/GitHub/vinh-phoenix phoenix "$@"; }

# Then just use
phoenix-dev --help
```

---

### 5. Check Script Permissions

After running `init`, verify shell scripts are executable (Linux/macOS only):

```bash
ls -l scripts | grep .sh
# Expect: -rwxr-xr-x (owner execute bit set)
```

> **Note:** Windows PowerShell scripts (`.ps1`) don't need chmod.

---

### 6. Quick Sanity Check

Verify your code imports correctly:

```bash
python -c "import phoenix_cli; print('Import OK')"
```

---

### 7. Build a Wheel (Optional)

Test packaging before publishing:

```bash
uv build
ls dist/
```

Install the built wheel in a fresh environment if needed.

### 8. Use a Temporary Workspace

Test `init --here` without cluttering your repo:

```bash
mkdir /tmp/phoenix-test && cd /tmp/phoenix-test
python -m src.phoenix_cli init --here --ai claude --ignore-agent-tools
```

---

### 9. Debug Network Issues

Skip TLS validation during local testing (not for production!):

```bash
phoenix check --skip-tls
phoenix init demo --skip-tls --ai gemini --ignore-agent-tools
```

---

## � Repository Structure

Understanding the Phoenix CLI repository layout:

```
vinh-phoenix/
├── skills/               # Reusable skill modules (copied to agent skills folders)
│   ├── architecture-design/
│   ├── coding/
│   ├── context-assessment/
│   ├── nextjs-mockup/
│   └── ... (17 skills total)
│
├── docs/                 # Documentation site
├── scripts/              # Automation scripts (bash + PowerShell)
├── src/phoenix_cli/      # CLI source code
├── rules/                # Agent-specific rules and guidelines
└── .github/workflows/    # CI/CD and release automation
```

**Note:** The `skills/` folder contains source templates. When you run `phoenix init`, these are copied into your project's agent-specific skills folders (`.claude/skills/`, `.github/skills/`, etc.).

---

## �🔄 Quick Reference

| What You Want | Command |
| --------------- | ---------- |
| **Run CLI directly** | `python -m src.phoenix_cli --help` |
| **Editable install** | `uv pip install -e .` then `phoenix ...` |
| **Local uvx (repo root)** | `uvx --from . phoenix ...` |
| **Local uvx (absolute path)** | `uvx --from /path/to/vinh-phoenix phoenix ...` |
| **Test specific branch** | `uvx --from git+URL@branch phoenix ...` |
| **Build package** | `uv build` |
| **Clean up** | `rm -rf .venv dist build *.egg-info` |

---

## 🧹 Cleanup

Remove build artifacts and virtual environments:

```bash
rm -rf .venv dist build *.egg-info
```

---

## 🛠️ Common Issues

| Problem | Solution |
| --------- | ---------- |
| **`ModuleNotFoundError: typer`** | Run `uv pip install -e .` to install dependencies |
| **Scripts not executable (Linux)** | Re-run init or manually run `chmod +x scripts/*.sh` |
| **Git step skipped** | You passed `--no-git` or Git isn't installed |
| **TLS errors (corporate network)** | Try `--skip-tls` (not recommended for production) |

---

## 👉 Next Steps

1. **Test your changes** - Run through the Quick Start guide with your modified CLI
2. **Update docs** - Document any new features or changes
3. **Open a PR** - Share your improvements when ready
4. **Tag a release** - Once merged to `main`, create a release tag (optional)

---

## 📚 Resources

- 📖 [Quick Start Guide](quickstart.md) - Test your changes end-to-end
- 🐛 [Report Issues](https://github.com/dauquangthanh/vinh-phoenix/issues/new) - Found a bug?
- 💬 [Discussions](https://github.com/dauquangthanh/vinh-phoenix/discussions) - Ask questions
