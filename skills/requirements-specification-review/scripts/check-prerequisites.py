#!/usr/bin/env python3
# check-prerequisites.py - Locate feature specification file
#
# Usage:
#   python check-prerequisites.py --json --paths-only
#   python check-prerequisites.py
#
# Arguments:
#   --json         Output results in JSON format
#   --paths-only   Only return path information (no validation)
#
# Requirements:
#   - Python 3.6+
#   - git (optional)

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

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

def main():
    parser = argparse.ArgumentParser(description="Locate feature specification file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--paths-only", action="store_true", help="Only return path information (no validation)")
    args = parser.parse_args()

    # Detect git
    has_git = False
    current_branch = "main"
    feature_dir = ""
    feature_spec = ""
    feature_design = ""
    tasks = ""

    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        subprocess.run(["git", "rev-parse", "--git-dir"], check=True, capture_output=True)
        has_git = True
        result = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True)
        if result.returncode == 0:
            current_branch = result.stdout.strip()
        else:
            # Fallback for repos with commits
            result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
            current_branch = result.stdout.strip() if result.returncode == 0 else "main"
        
        # Check feature branch
        import re
        if re.match(r'^[0-9]+-(.+)$', current_branch):
            feature_dir = f"specs/{current_branch}"
            feature_dir_path = Path(feature_dir)
            if feature_dir_path.is_dir():
                feature_spec = str(feature_dir_path / "spec.md")
                feature_design = str(feature_dir_path / "design.md")
                tasks = str(feature_dir_path / "tasks.md")
                
                if not args.paths_only:
                    print_info(f"Detected feature branch: {current_branch}", args.json)
                    print_info(f"Feature directory: {feature_dir}", args.json)
            else:
                if not args.paths_only:
                    print_warning(f"Feature branch detected but directory not found: {feature_dir}", args.json)
        else:
            if not args.paths_only:
                print_warning("Not on a feature branch (expected format: N-feature-name)", args.json)
                print_warning(f"Current branch: {current_branch}", args.json)
    except subprocess.CalledProcessError:
        if not args.paths_only:
            print_warning("Not in a git repository or git not available", args.json)

    # Check spec exists
    spec_exists = False
    if feature_spec and Path(feature_spec).is_file():
        spec_exists = True
        if not args.paths_only:
            print_success(f"Spec file found: {feature_spec}", args.json)
    else:
        if not args.paths_only:
            print_error("Spec file not found", args.json)
            if feature_spec:
                print_info(f"Expected at: {feature_spec}", args.json)
            print_info("Please create a spec first using requirements-specification skill", args.json)

    # Output
    if args.json:
        result = {
            "has_git": has_git,
            "current_branch": current_branch,
            "feature_dir": feature_dir,
            "feature_spec": feature_spec,
            "feature_design": feature_design,
            "tasks": tasks,
            "spec_exists": spec_exists
        }
        print(json.dumps(result, indent=2))
    else:
        print("")
        if spec_exists:
            print_success("Prerequisites check passed", args.json)
        else:
            print_error("Prerequisites check failed: Spec file not found", args.json)
        print("")
        print(f"Git available: {has_git}")
        print(f"Current branch: {current_branch}")
        print(f"Feature directory: {feature_dir or 'N/A'}")
        print(f"Spec file: {feature_spec or 'N/A'}")
        print(f"Spec exists: {spec_exists}")
        print("")
        
        if not spec_exists:
            print_info("To create a spec, use the requirements-specification skill", args.json)
            sys.exit(1)

if __name__ == "__main__":
    main()