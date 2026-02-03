#!/usr/bin/env python3
# setup-design.py - Set up design directory structure and templates
#
# Usage:
#   python3 setup-design.py
#   python3 setup-design.py --json
#
# Arguments:
#   --json    Output results in JSON format
#
# Requirements:
#   - Python 3.6+
#   - git (optional - will work without git)

import argparse
import json
import re
import shutil
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
    parser = argparse.ArgumentParser(description='Set up design directory structure and templates')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')
    args = parser.parse_args()

    output_json = args.json

    # Script directory
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    templates_dir = skill_dir / 'templates'

    # Detect if we're in a git repository and on a feature branch
    has_git = False
    current_branch = "main"
    feature_dir = None
    feature_spec = None

    try:
        # Check if git is available
        subprocess.run(['git', '--version'], check=True, capture_output=True)

        # Check if in git repo
        subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
        has_git = True

        # Get current branch
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                              capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()

        # Check if we're on a feature branch (format: N-feature-name)
        if re.match(r'^[0-9]+-(.+)$', current_branch):
            feature_dir = Path('specs') / current_branch
            feature_spec = feature_dir / 'spec.md'
            print_info(f"Detected feature branch: {current_branch}", output_json)
        else:
            print_error("Not on a feature branch. Technical design requires a feature branch (format: N-feature-name)", output_json)
            print_error("Please create and checkout a feature branch first", output_json)
            sys.exit(1)

    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Git repository required for technical design workflow", output_json)
        print_error("Please initialize git repository and create a feature branch (format: N-feature-name)", output_json)
        sys.exit(1)

    # Design directory location - always feature-specific
    if feature_dir and feature_dir.exists():
        design_dir = feature_dir
        print_info(f"Using feature-specific design directory: {design_dir}", output_json)
    else:
        print_error(f"Feature directory not found: {feature_dir}", output_json)
        print_error(f"Please ensure specs/{current_branch} directory exists", output_json)
        sys.exit(1)

    feature_design = design_dir / 'design.md'
    research_file = design_dir / 'research' / 'research.md'
    data_model_file = design_dir / 'data-model.md'
    quickstart_file = design_dir / 'quickstart.md'
    contracts_dir = design_dir / 'contracts'

    # Create directory structure
    print_info("Creating design directory structure", output_json)
    design_dir.mkdir(parents=True, exist_ok=True)
    (design_dir / 'research').mkdir(parents=True, exist_ok=True)
    contracts_dir.mkdir(parents=True, exist_ok=True)
    print_success("Directories created", output_json)

    # Copy design template
    design_template = templates_dir / 'design-template.md'
    if design_template.exists():
        print_info("Copying design template", output_json)
        shutil.copy2(design_template, feature_design)
        print_success(f"Design template copied to {feature_design}", output_json)
    else:
        print_error(f"Design template not found at {design_template}", output_json)
        sys.exit(1)

    # Copy research template
    research_template = templates_dir / 'research-template.md'
    if research_template.exists():
        print_info("Copying research template", output_json)
        shutil.copy2(research_template, research_file)
        print_success(f"Research template copied to {research_file}", output_json)
    else:
        print_warning("Research template not found, skipping", output_json)

    # Copy data model template
    data_model_template = templates_dir / 'data-model-template.md'
    if data_model_template.exists():
        print_info("Copying data model template", output_json)
        shutil.copy2(data_model_template, data_model_file)
        print_success(f"Data model template copied to {data_model_file}", output_json)
    else:
        print_warning("Data model template not found, skipping", output_json)

    # Create placeholder API contract
    contract_template = templates_dir / 'api-contract-template.md'
    if contract_template.exists():
        print_info("Copying API contract template", output_json)
        shutil.copy2(contract_template, contracts_dir / 'example-contract.md')
        print_success(f"API contract template copied to {contracts_dir}/", output_json)
    else:
        print_warning("API contract template not found, skipping", output_json)

    # Output results
    if output_json:
        # JSON output
        result = {
            "success": True,
            "has_git": has_git,
            "current_branch": current_branch,
            "feature_spec": str(feature_spec) if feature_spec else "",
            "feature_design": str(feature_design),
            "research_file": str(research_file),
            "data_model_file": str(data_model_file),
            "quickstart_file": str(quickstart_file),
            "contracts_dir": str(contracts_dir),
            "design_dir": str(design_dir)
        }
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print()
        print_success("Design workspace created successfully!", output_json)
        print()
        print(f"Design directory: {design_dir}")
        print(f"Design document: {feature_design}")
        print(f"Research document: {research_file}")
        print(f"Data model: {data_model_file}")
        print(f"Contracts directory: {contracts_dir}")
        if feature_spec:
            print(f"Feature spec: {feature_spec}")
        print()
        print_info("Next steps:", output_json)
        print(f"  1. Review and fill in {feature_design}")
        print(f"  2. Conduct research and document in {research_file}")
        print(f"  3. Design data models in {data_model_file}")
        print(f"  4. Create API contracts in {contracts_dir}/")

if __name__ == '__main__':
    main()