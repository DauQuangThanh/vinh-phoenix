#!/usr/bin/env python3
# check-design.py - Check for technical design documentation and prerequisites
#
# Usage:
#   python3 check-design.py
#   python3 check-design.py --json
#
# Arguments:
#   --json    Output results in JSON format
#
# Requirements:
#   - Python 3.6+
#   - git (optional - will work without git)

import argparse
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import colorama
    colorama.init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

# Color codes for output
class Colors:
    RED = '\033[0;31m' if HAS_COLORAMA else ''
    GREEN = '\033[0;32m' if HAS_COLORAMA else ''
    YELLOW = '\033[1;33m' if HAS_COLORAMA else ''
    BLUE = '\033[0;34m' if HAS_COLORAMA else ''
    NC = '\033[0m' if HAS_COLORAMA else ''

def print_info(message, output_json=False):
    if not output_json:
        print(f"{Colors.BLUE}ℹ {Colors.NC}{message}")

def print_success(message, output_json=False):
    if not output_json:
        print(f"{Colors.GREEN}✓{Colors.NC} {message}")

def print_error(message, output_json=False):
    if not output_json:
        print(f"{Colors.RED}✗{Colors.NC}{message}", file=sys.stderr)
    else:
        print(json.dumps({"error": message}), file=sys.stderr)

def print_warning(message, output_json=False):
    if not output_json:
        print(f"{Colors.YELLOW}⚠{Colors.NC}{message}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='Check for technical design documentation and prerequisites')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')
    args = parser.parse_args()

    output_json = args.json

    repo_root = Path.cwd()

    # Detect if we're in a git repository
    has_git = False
    current_branch = ""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
        has_git = True
        result = subprocess.run(['git', 'branch', '--show-current'],
                              capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Determine design directory location
    design_dir = None
    if has_git and re.match(r'^\d+-.+$', current_branch):
        # Feature branch pattern (e.g., 123-feature-name)
        feature_num = re.match(r'^(\d+)-', current_branch).group(1)
        specs_pattern = repo_root / 'specs' / f'{feature_num}-*'
        matching_dirs = list(repo_root.glob(f'specs/{feature_num}-*'))
        if matching_dirs:
            design_dir = matching_dirs[0]
    else:
        # Default location
        design_dir = repo_root / 'design'

    # Check for design documentation
    design_file = ""
    research_file = ""
    data_model_file = ""
    contracts_dir = ""
    quickstart_file = ""
    feature_spec = ""
    ground_rules_file = ""
    architecture_file = ""

    missing_files = []
    found_files = []

    # Check main design file
    design_file_path = design_dir / 'design.md'
    if design_file_path.exists():
        design_file = str(design_file_path)
        found_files.append("design.md")
        print_success(f"Found design.md: {design_file}", output_json)
    else:
        missing_files.append("design.md")
        print_error(f"Missing design.md in {design_dir}", output_json)

    # Check research file
    research_file_path = design_dir / 'research' / 'research.md'
    if research_file_path.exists():
        research_file = str(research_file_path)
        found_files.append("research.md")
        print_success(f"Found research.md: {research_file}", output_json)
    else:
        missing_files.append("research/research.md")
        print_error(f"Missing research/research.md in {design_dir}", output_json)

    # Check data model file
    data_model_file_path = design_dir / 'data-model.md'
    if data_model_file_path.exists():
        data_model_file = str(data_model_file_path)
        found_files.append("data-model.md")
        print_success(f"Found data-model.md: {data_model_file}", output_json)
    else:
        missing_files.append("data-model.md")
        print_error(f"Missing data-model.md in {design_dir}", output_json)

    # Check contracts directory
    contracts_dir_path = design_dir / 'contracts'
    if contracts_dir_path.exists() and contracts_dir_path.is_dir():
        contracts_dir = str(contracts_dir_path)
        contract_count = len(list(contracts_dir_path.glob('*.md')))
        found_files.append(f"contracts/ ({contract_count} files)")
        print_success(f"Found contracts directory: {contracts_dir} ({contract_count} files)", output_json)
    else:
        missing_files.append("contracts/")
        print_error(f"Missing contracts directory in {design_dir}", output_json)

    # Check quickstart file (optional)
    quickstart_file_path = design_dir / 'quickstart.md'
    if quickstart_file_path.exists():
        quickstart_file = str(quickstart_file_path)
        found_files.append("quickstart.md")
        print_success(f"Found quickstart.md: {quickstart_file}", output_json)
    else:
        print_warning("Optional quickstart.md not found", output_json)

    # Check for feature specification
    if has_git and re.match(r'^\d+-.+$', current_branch):
        feature_num = re.match(r'^(\d+)-', current_branch).group(1)
        spec_pattern = repo_root / 'specs' / f'{feature_num}-*' / 'spec.md'
        matching_specs = list(repo_root.glob(f'specs/{feature_num}-*/spec.md'))
        if matching_specs:
            feature_spec = str(matching_specs[0])
            found_files.append("spec.md")
            print_success(f"Found feature spec: {feature_spec}", output_json)
        else:
            print_warning(f"Feature specification not found (expected in specs/{feature_num}-*/spec.md)", output_json)
    elif (repo_root / 'specs' / 'spec.md').exists():
        feature_spec = str(repo_root / 'specs' / 'spec.md')
        found_files.append("spec.md")
        print_success(f"Found spec.md: {feature_spec}", output_json)
    else:
        print_warning("Feature specification not found", output_json)

    # Check for ground rules (optional)
    ground_rules_path = repo_root / 'docs' / 'ground-rules.md'
    if ground_rules_path.exists():
        ground_rules_file = str(ground_rules_path)
        found_files.append("ground-rules.md")
        print_success(f"Found ground-rules.md: {ground_rules_file}", output_json)
    else:
        print_warning("Optional ground-rules.md not found", output_json)

    # Check for architecture (optional)
    architecture_path = repo_root / 'docs' / 'architecture.md'
    if architecture_path.exists():
        architecture_file = str(architecture_path)
        found_files.append("architecture.md")
        print_success(f"Found architecture.md: {architecture_file}", output_json)
    else:
        print_warning("Optional architecture.md not found", output_json)

    # Output results
    if output_json:
        # JSON output
        result = {
            "design_file": design_file,
            "research_file": research_file,
            "data_model_file": data_model_file,
            "contracts_dir": contracts_dir,
            "quickstart_file": quickstart_file,
            "feature_spec": feature_spec,
            "ground_rules_file": ground_rules_file,
            "architecture_file": architecture_file,
            "design_dir": str(design_dir) if design_dir else "",
            "current_branch": current_branch,
            "has_git": has_git,
            "found_files": found_files,
            "missing_files": missing_files,
            "status": "complete" if len(missing_files) == 0 else "incomplete"
        }
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print()
        print("==================================")
        print("Technical Design Prerequisites")
        print("==================================")
        print()
        print(f"Repository: {repo_root}")
        print(f"Design Directory: {design_dir}")
        if has_git:
            print(f"Current Branch: {current_branch}")
        print()
        print(f"Found Files ({len(found_files)}):")
        for file in found_files:
            print(f"  ✓ {file}")
        print()
        if missing_files:
            print(f"Missing Files ({len(missing_files)}):")
            for file in missing_files:
                print(f"  ✗ {file}")
            print()

        if len(missing_files) == 0:
            print(f"Status: {Colors.GREEN}All required files found{Colors.NC}")
            print()
            print("Ready for technical design review!")
        else:
            print(f"Status: {Colors.RED}Missing required files{Colors.NC}")
            print()
            print("Please ensure all design documents are complete before review.")
            print("Run the technical-design skill to generate missing files.")
            sys.exit(1)

if __name__ == '__main__':
    main()