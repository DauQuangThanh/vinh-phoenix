#!/usr/bin/env python3
# check-prerequisites.py - Check prerequisites and identify feature directory
#
# Usage:
#   python check-prerequisites.py [--json]
#   python check-prerequisites.py --feature-dir /path/to/feature
#
# Arguments:
#   --json         Output results as JSON
#   --feature-dir  Specify feature directory explicitly
#
# Requirements:
#   - Python 3.6+

import argparse
import json
import os
import sys
from pathlib import Path

REQUIRED_DOCS = ["design.md", "spec.md"]
OPTIONAL_DOCS = ["data-model.md", "research.md", "quickstart.md", "architecture.md"]
OPTIONAL_DIRS = ["contracts"]

def print_info(message, output_json=False):
    if not output_json:
        print(f"ℹ {message}")

def print_success(message, output_json=False):
    if not output_json:
        print(f"✓ {message}")

def print_error(message, output_json=False):
    if output_json:
        error_obj = {"error": message}
        print(json.dumps(error_obj), file=sys.stderr)
    else:
        print(f"✗ {message}", file=sys.stderr)

def print_warning(message, output_json=False):
    if not output_json:
        print(f"⚠ {message}", file=sys.stderr)

def is_feature_dir(path):
    return (path / "design.md").is_file() or (path / "spec.md").is_file()

def find_repo_root(start_path):
    current = start_path
    while current != current.parent:
        if (current / ".git").is_dir():
            return current
        current = current.parent
    return None

def find_feature_dir():
    current_dir = Path.cwd()

    # Check current directory first
    if is_feature_dir(current_dir):
        return current_dir

    # Check phoenix/specs/* subdirectories
    phoenix_specs = current_dir / "phoenix" / "specs"
    if phoenix_specs.is_dir():
        for subdir in phoenix_specs.iterdir():
            if subdir.is_dir() and is_feature_dir(subdir):
                return subdir

    # Check specs/* subdirectories
    specs_dir = current_dir / "specs"
    if specs_dir.is_dir():
        for subdir in specs_dir.iterdir():
            if subdir.is_dir() and is_feature_dir(subdir):
                return subdir

    # Check docs/specs/* subdirectories
    docs_specs = current_dir / "docs" / "specs"
    if docs_specs.is_dir():
        for subdir in docs_specs.iterdir():
            if subdir.is_dir() and is_feature_dir(subdir):
                return subdir

    return None

def scan_documents(feature_dir):
    available_docs = []
    missing_required = []

    # Check required documents
    for doc in REQUIRED_DOCS:
        if (feature_dir / doc).is_file():
            available_docs.append(doc)
        else:
            missing_required.append(doc)

    # Check optional documents
    for doc in OPTIONAL_DOCS:
        if (feature_dir / doc).is_file():
            available_docs.append(doc)

    # Check optional directories
    for dir_name in OPTIONAL_DIRS:
        dir_path = feature_dir / dir_name
        if dir_path.is_dir():
            file_count = len(list(dir_path.glob("*.md")))
            if file_count > 0:
                available_docs.append(f"{dir_name}/ ({file_count} files)")

    # Check product-level architecture.md
    repo_root = find_repo_root(feature_dir)
    if repo_root and (repo_root / "docs" / "architecture.md").is_file():
        available_docs.append("docs/architecture.md")

    return available_docs, missing_required

def main():
    parser = argparse.ArgumentParser(description="Check prerequisites and identify feature directory")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--feature-dir", help="Specify feature directory explicitly")
    args = parser.parse_args()

    # Find or use specified feature directory
    if args.feature_dir:
        found_dir = Path(args.feature_dir)
    else:
        found_dir = find_feature_dir()
        if not found_dir:
            if args.json:
                result = {
                    "success": False,
                    "error": "No feature directory found",
                    "message": "Could not find feature directory. Looking for directory containing design.md or spec.md",
                    "searched_paths": [
                        str(Path.cwd()),
                        str(Path.cwd() / "phoenix" / "specs"),
                        str(Path.cwd() / "specs"),
                        str(Path.cwd() / "docs" / "specs")
                    ]
                }
                print(json.dumps(result, indent=2))
            else:
                print_error("No feature directory found", args.json)
                print("")
                print("Could not find feature directory. Looking for directory containing design.md or spec.md")
                print("")
                print("Searched paths:")
                print(f"  • {Path.cwd()}")
                print(f"  • {Path.cwd() / 'phoenix' / 'specs'}")
                print(f"  • {Path.cwd() / 'specs'}")
                print(f"  • {Path.cwd() / 'docs' / 'specs'}")
            sys.exit(1)

    # Scan documents
    available_docs, missing_required = scan_documents(found_dir)

    # Output results
    if args.json:
        result = {
            "success": True,
            "feature_dir": str(found_dir),
            "available_docs": available_docs,
            "missing_required": missing_required
        }
        if missing_required:
            result["warning"] = f"Missing required documents: {', '.join(missing_required)}"
        print(json.dumps(result, indent=2))
    else:
        print_success(f"Feature directory: {found_dir}", args.json)
        print("")
        print_success(f"Available documents ({len(available_docs)}):", args.json)
        for doc in available_docs:
            print(f"  • {doc}")

        if missing_required:
            print("")
            print_warning("Missing required documents:", args.json)
            for doc in missing_required:
                print(f"  • {doc}")

    # Exit with error if missing required documents
    if missing_required:
        sys.exit(1)

if __name__ == "__main__":
    main()