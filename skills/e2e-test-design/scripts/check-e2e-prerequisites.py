#!/usr/bin/env python3
"""
E2E Test Prerequisites Checker

This script checks for the existence of required files and directories
for end-to-end testing setup.

Usage:
    python3 check-e2e-prerequisites.py [--json]

Options:
    --json    Output results in JSON format instead of colored text
"""

import argparse
import json
import sys
from pathlib import Path


def check_file_exists(file_path: Path, description: str) -> dict:
    """Check if a file exists and return result dict."""
    exists = file_path.exists()
    return {
        "file": str(file_path),
        "description": description,
        "exists": exists,
        "status": "✓" if exists else "✗"
    }


def print_colored(message: str, color_code: str) -> None:
    """Print message with ANSI color codes."""
    print(f"\033[{color_code}m{message}\033[0m")


def main():
    parser = argparse.ArgumentParser(description="Check E2E test prerequisites")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    # Assume we're running from the project root
    workspace_root = Path.cwd()

    # Define required files and directories to check
    checks = [
        # Architecture documentation
        (workspace_root / "docs" / "architecture.md", "Architecture documentation"),
        (workspace_root / "docs" / "ground-rules.md", "Project ground rules"),

        # Specification files (check if any spec.md exists in specs/*/ directories)
        (workspace_root / "specs", "Specifications directory"),

        # Design documents
        (workspace_root / "docs" / "technical-detailed-design.md", "Technical detailed design"),
        (workspace_root / "docs" / "requirements-specification.md", "Requirements specification"),
    ]

    results = []

    # Check individual files
    for file_path, description in checks[:-1]:  # Exclude specs directory for now
        result = check_file_exists(file_path, description)
        results.append(result)

    # Check specs directory and look for spec.md files
    specs_dir = workspace_root / "specs"
    if specs_dir.exists():
        spec_files = list(specs_dir.glob("*/spec.md"))
        if spec_files:
            results.append({
                "file": str(specs_dir),
                "description": "Specifications directory with spec.md files",
                "exists": True,
                "status": "✓",
                "spec_files_found": len(spec_files)
            })
        else:
            results.append({
                "file": str(specs_dir),
                "description": "Specifications directory with spec.md files",
                "exists": False,
                "status": "✗",
                "spec_files_found": 0
            })
    else:
        results.append({
            "file": str(specs_dir),
            "description": "Specifications directory",
            "exists": False,
            "status": "✗"
        })

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("E2E Test Prerequisites Check")
        print("=" * 40)

        all_good = True
        for result in results:
            status = result["status"]
            file_desc = result["description"]
            file_path = result["file"]

            if result["exists"]:
                print_colored(f"{status} {file_desc}", "32")  # Green
                print(f"   Found: {file_path}")
            else:
                print_colored(f"{status} {file_desc}", "31")  # Red
                print(f"   Missing: {file_path}")
                all_good = False

            # Special handling for specs
            if "spec_files_found" in result:
                spec_count = result["spec_files_found"]
                if spec_count > 0:
                    print(f"   Found {spec_count} specification file(s)")
                else:
                    print("   No spec.md files found in subdirectories")

        print("\n" + "=" * 40)
        if all_good:
            print_colored("✓ All prerequisites satisfied!", "32")
            sys.exit(0)
        else:
            print_colored("✗ Some prerequisites are missing. Please create the required files.", "31")
            sys.exit(1)


if __name__ == "__main__":
    main()
