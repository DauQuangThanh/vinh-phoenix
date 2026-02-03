#!/usr/bin/env python3
"""
Setup context assessment for brownfield project.
Creates assessment environment and copies template.

Usage: python3 scripts/setup-context-assessment.py [--json]

Platforms: Windows, macOS, Linux
Requirements: Python 3.8+
"""

import argparse
import json
import os
import shutil
from pathlib import Path

def find_repo_root(start_path: Path) -> Path:
    """Find repository root by searching upward for .git directory."""
    current = start_path.resolve()
    while current != current.parent:  # Stop at filesystem root
        if (current / ".git").is_dir():
            return current
        current = current.parent
    return start_path.resolve()

def setup_context_assessment(json_mode: bool = False) -> dict:
    """Setup context assessment environment."""
    # Get script directory and skill directory
    script_dir = Path(__file__).parent.resolve()
    skill_dir = script_dir.parent

    # Detect repository root
    repo_root = find_repo_root(Path.cwd())

    # Ensure docs directory exists
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    # Set context assessment file path
    context_assessment = docs_dir / "context-assessment.md"

    # Copy template from skill directory
    template = skill_dir / "templates" / "context-assessment-template.md"
    if template.is_file():
        shutil.copy2(template, context_assessment)
        if not json_mode:
            print(f"✓ Copied context assessment template to {context_assessment}")
    else:
        if not json_mode:
            print(f"WARNING: Context assessment template not found at {template}", file=os.sys.stderr)
            print("Creating empty assessment file", file=os.sys.stderr)
        context_assessment.touch()

    # Check if we're in a git repo
    has_git = str((repo_root / ".git").is_dir()).lower()

    result = {
        "CONTEXT_ASSESSMENT": str(context_assessment),
        "DOCS_DIR": str(docs_dir),
        "REPO_ROOT": str(repo_root),
        "HAS_GIT": has_git
    }

    return result

def main():
    parser = argparse.ArgumentParser(
        description="Setup context assessment for brownfield project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/setup-context-assessment.py
  python3 scripts/setup-context-assessment.py --json
        """
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )

    args = parser.parse_args()

    try:
        result = setup_context_assessment(json_mode=args.json)

        if args.json:
            print(json.dumps(result))
        else:
            print(f"Repository root: {result['REPO_ROOT']}")
            print(f"Documentation directory: {result['DOCS_DIR']}")
            print(f"Assessment file: {result['CONTEXT_ASSESSMENT']}")
            print(f"Git repository: {result['HAS_GIT']}")
            print()
            print("✓ Setup complete. Context assessment template is ready at:")
            print(f"  {result['CONTEXT_ASSESSMENT']}")

    except Exception as e:
        print(f"ERROR: {e}", file=os.sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
