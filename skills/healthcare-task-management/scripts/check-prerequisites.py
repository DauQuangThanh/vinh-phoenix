#!/usr/bin/env python3
# check-prerequisites.py - Check prerequisites for healthcare task management
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
OPTIONAL_DOCS = ["data-model.md", "research.md", "quickstart.md"]
OPTIONAL_DIRS = ["contracts"]
COMPLIANCE_DOCS = ["docs/compliance-framework.md"]
HEALTHCARE_GROUND_RULES = [
    "docs/healthcare-ground-rules.md",
    "docs/ground-rules.md",
]


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

    if is_feature_dir(current_dir):
        return current_dir

    for base in ["phoenix/specs", "specs", "docs/specs"]:
        candidate = current_dir / base
        if candidate.is_dir():
            for subdir in candidate.iterdir():
                if subdir.is_dir() and is_feature_dir(subdir):
                    return subdir

    return None


def scan_documents(feature_dir):
    available_docs = []
    missing_required = []

    for doc in REQUIRED_DOCS:
        if (feature_dir / doc).is_file():
            available_docs.append(doc)
        else:
            missing_required.append(doc)

    for doc in OPTIONAL_DOCS:
        if (feature_dir / doc).is_file():
            available_docs.append(doc)

    for dir_name in OPTIONAL_DIRS:
        dir_path = feature_dir / dir_name
        if dir_path.is_dir():
            file_count = len(list(dir_path.glob("*.md")))
            if file_count > 0:
                available_docs.append(f"{dir_name}/ ({file_count} files)")

    repo_root = find_repo_root(feature_dir)

    compliance_framework = None
    if repo_root:
        for cf_path in COMPLIANCE_DOCS:
            full_path = repo_root / cf_path
            if full_path.is_file():
                compliance_framework = str(full_path)
                available_docs.append(cf_path)
                break

        for gr_path in HEALTHCARE_GROUND_RULES:
            full_path = repo_root / gr_path
            if full_path.is_file():
                available_docs.append(gr_path)
                break

        for arch in ["docs/healthcare-architecture.md", "docs/architecture.md"]:
            full_path = repo_root / arch
            if full_path.is_file():
                available_docs.append(arch)
                break

        e2e_plan = repo_root / "docs" / "e2e-test-plan.md"
        if e2e_plan.is_file():
            available_docs.append("docs/e2e-test-plan.md")

    return available_docs, missing_required, compliance_framework


def main():
    parser = argparse.ArgumentParser(
        description="Check prerequisites for healthcare task management"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--feature-dir", help="Specify feature directory explicitly")
    args = parser.parse_args()

    if args.feature_dir:
        found_dir = Path(args.feature_dir)
    else:
        found_dir = find_feature_dir()
        if not found_dir:
            if args.json:
                result = {
                    "success": False,
                    "error": "No feature directory found",
                    "message": "Could not find feature directory containing design.md or spec.md",
                }
                print(json.dumps(result, indent=2))
            else:
                print_error("No feature directory found", args.json)
            sys.exit(1)

    available_docs, missing_required, compliance_framework = scan_documents(found_dir)

    missing_compliance = compliance_framework is None

    if args.json:
        result = {
            "success": not missing_required and not missing_compliance,
            "feature_dir": str(found_dir),
            "available_docs": available_docs,
            "missing_required": missing_required,
            "compliance_framework": compliance_framework,
        }
        if missing_required:
            result["warning"] = f"Missing required documents: {', '.join(missing_required)}"
        if missing_compliance:
            result["compliance_warning"] = (
                "docs/compliance-framework.md not found — HIPAA task generation requires this file"
            )
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

        if missing_compliance:
            print("")
            print_warning(
                "docs/compliance-framework.md not found — HIPAA task generation requires this file",
                args.json,
            )

    if missing_required or missing_compliance:
        sys.exit(1)


if __name__ == "__main__":
    main()
