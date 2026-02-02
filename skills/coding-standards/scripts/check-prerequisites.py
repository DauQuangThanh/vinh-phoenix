#!/usr/bin/env python3
"""Detect required files for the coding-standards skill.

Usage: python3 tools/check-prerequisites.py [--json]
Cross-platform: macOS, Linux, Windows (requires Python 3.8+)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


def find_repo_root(start: Optional[Path] = None) -> Path:
    p = (start or Path(__file__).resolve()).parent
    # Ascend until we find a repository marker
    for _ in range(16):
        if (p / "pyproject.toml").exists() or (p / "README.md").exists() or (p / ".git").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    return Path.cwd()


def case_insensitive_find(directory: Path, filename: str) -> Optional[Path]:
    if not directory.exists():
        return None
    target = filename.lower()
    for child in directory.iterdir():
        if child.name.lower() == target:
            return child
    return None


def find_specs(root: Path) -> List[str]:
    specs = []
    specs_dir = root / "specs"
    if not specs_dir.exists():
        return specs
    for p in specs_dir.rglob("spec.md"):
        specs.append(str(p.relative_to(root)))
    return specs


def check_files(root: Path) -> Dict:
    docs_dir = root / "docs"
    result = {
        "repo_root": str(root),
        "found": {},
        "specs": [],
    }

    # Files to check
    checks = {
        "ground_rules": (docs_dir, "ground-rules.md"),
        "architecture": (docs_dir, "architecture.md"),
        "standards": (docs_dir, "standards.md"),
    }

    for key, (dirpath, fname) in checks.items():
        p = case_insensitive_find(dirpath, fname)
        result["found"][key] = str(p.relative_to(root)) if p else None

    # Specs
    result["specs"] = find_specs(root)

    return result


def parse_args():
    p = argparse.ArgumentParser(description="Check coding-standards prerequisites")
    p.add_argument("--json", action="store_true", help="Output JSON")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = find_repo_root()
    result = check_files(repo_root)

    # Determine status
    status = {
        "ground_rules_present": bool(result["found"].get("ground_rules")),
        "architecture_present": bool(result["found"].get("architecture")),
        "standards_present": bool(result["found"].get("standards")),
        "specs_count": len(result["specs"]),
    }

    if args.json:
        out = {**result, "status": status}
        print(json.dumps(out, indent=2))
        return 0

    # Human readable output
    print(f"Repository root: {result['repo_root']}")
    print("Checks:")
    print(f" - docs/ground-rules.md: {result['found'].get('ground_rules') or 'MISSING'}")
    print(f" - docs/architecture.md: {result['found'].get('architecture') or 'MISSING'}")
    print(f" - docs/standards.md: {result['found'].get('standards') or 'MISSING'}")
    print(f" - specs/*/spec.md count: {status['specs_count']}")

    if not status["ground_rules_present"]:
        print("\nERROR: ground-rules.md is required. Create docs/ground-rules.md and re-run.")
        # Return non-zero to indicate missing required file
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
