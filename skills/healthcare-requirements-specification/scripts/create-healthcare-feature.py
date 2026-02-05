#!/usr/bin/env python3
"""
create-healthcare-feature.py - Create a new healthcare feature branch and spec structure

Usage:
  python3 create-healthcare-feature.py --number 5 --short-name "patient-portal" "Add HIPAA-compliant patient portal"
  python3 create-healthcare-feature.py --json --number 5 --short-name "patient-portal" "Add HIPAA-compliant patient portal"

Arguments:
  --number N           Feature number (required)
  --short-name NAME    Short name for the feature (required)
  --json               Output results as JSON
  description          Healthcare feature description (all remaining arguments)

Requirements:
  - git
  - Python 3.6+
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class HealthcareFeatureCreator:
    def __init__(self):
        self.output_json = False

    def run_command(self, cmd, capture_output=True, check=True):
        """Run a command and return the result."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            if check:
                raise e
            return e

    def print_info(self, message):
        """Print informational message."""
        if not self.output_json:
            print(f"ℹ {message}")

    def print_success(self, message):
        """Print success message."""
        if not self.output_json:
            print(f"✓ {message}")

    def print_error(self, message):
        """Print error message."""
        if self.output_json:
            error_result = {"error": message}
            print(json.dumps(error_result), file=sys.stderr)
        else:
            print(f"✗ {message}", file=sys.stderr)

    def print_warning(self, message):
        """Print warning message."""
        if not self.output_json:
            print(f"⚠ {message}", file=sys.stderr)

    def validate_short_name(self, name):
        """Validate short name format."""
        # Check length
        if len(name) < 1 or len(name) > 64:
            self.print_error("Short name must be 1-64 characters")
            return False

        # Check format: lowercase, numbers, hyphens only
        if not re.match(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$', name):
            self.print_error("Short name must use lowercase letters, numbers, and hyphens only")
            self.print_error("Cannot start/end with hyphen or have consecutive hyphens")
            return False

        # Check for consecutive hyphens
        if '--' in name:
            self.print_error("Short name cannot contain consecutive hyphens")
            return False

        return True

    def get_script_dir(self):
        """Get the directory containing this script."""
        return Path(__file__).parent

    def get_skill_dir(self):
        """Get the skill directory."""
        return self.get_script_dir().parent

    def get_templates_dir(self):
        """Get the templates directory."""
        return self.get_skill_dir() / "templates"

    def create_healthcare_feature(self, number, short_name, description):
        """Create a healthcare feature specification."""
        # Construct paths
        branch_name = f"{number}-{short_name}"
        specs_dir = Path(f"specs/{branch_name}")
        spec_file = specs_dir / "spec.md"
        checklist_dir = specs_dir / "checklists"
        checklist_file = checklist_dir / "healthcare-requirements.md"

        self.print_info(f"Creating feature: {branch_name}")
        self.print_info(f"Description: {description}")

        # Check if git is available
        try:
            self.run_command("git --version", check=False)
        except FileNotFoundError:
            self.print_error("git is not installed or not in PATH")
            return False

        # Check if we're in a git repository
        result = self.run_command("git rev-parse --git-dir", check=False)
        if result.returncode != 0:
            self.print_error("Not in a git repository")
            return False

        # Check if branch already exists
        result = self.run_command(f"git show-ref --verify --quiet refs/heads/{branch_name}", check=False)
        if result.returncode == 0:
            self.print_error(f"Branch '{branch_name}' already exists")
            return False

        # Create and checkout new branch
        self.print_info(f"Creating branch: {branch_name}")
        try:
            self.run_command(f"git checkout -b {branch_name}")
            self.print_success("Branch created and checked out")
        except subprocess.CalledProcessError:
            self.print_error(f"Failed to create branch '{branch_name}'")
            return False

        # Create directory structure
        self.print_info("Creating directory structure")
        specs_dir.mkdir(parents=True, exist_ok=True)
        checklist_dir.mkdir(parents=True, exist_ok=True)
        self.print_success("Directories created")

        # Copy spec template
        templates_dir = self.get_templates_dir()
        spec_template = templates_dir / "healthcare-spec-template.md"

        if spec_template.exists():
            self.print_info("Copying spec template")
            shutil.copy2(spec_template, spec_file)

            # Replace placeholders
            current_date = datetime.now().strftime("%Y-%m-%d")
            content = spec_file.read_text()
            content = content.replace("[Feature Name]", short_name)
            content = content.replace("[Number-ShortName]", branch_name)
            content = content.replace("[Date]", current_date)
            spec_file.write_text(content)

            self.print_success("Spec template created")
        else:
            self.print_warning("Spec template not found, creating basic spec file")
            current_date = datetime.now().strftime("%Y-%m-%d")
            basic_spec = f"""# {short_name}

**Feature ID**: {branch_name}
**Status**: Draft
**Created**: {current_date}

## Overview

{description}

## User Scenarios & Testing

[To be filled]

## Functional Requirements

[To be filled]

## Success Criteria

[To be filled]

## Assumptions

[To be filled]

## Out of Scope

[To be filled]
"""
            spec_file.write_text(basic_spec)
            self.print_success("Basic spec file created")

        # Copy checklist template
        checklist_template = templates_dir / "healthcare-checklist-template.md"

        if checklist_template.exists():
            self.print_info("Copying checklist template")
            shutil.copy2(checklist_template, checklist_file)

            # Replace placeholders
            current_date = datetime.now().strftime("%Y-%m-%d")
            content = checklist_file.read_text()
            content = content.replace("[FEATURE NAME]", short_name)
            content = content.replace("[DATE]", current_date)
            content = content.replace("[Link to spec.md]", "[spec.md](../spec.md)")
            checklist_file.write_text(content)

            self.print_success("Checklist template created")
        else:
            self.print_warning("Checklist template not found, creating basic checklist file")
            current_date = datetime.now().strftime("%Y-%m-%d")
            basic_checklist = f"""# Specification Quality Checklist: {short_name}

**Feature**: [spec.md](../spec.md)
**Created**: {current_date}

## Content Quality
- [ ] No implementation details
- [ ] Focused on user value
- [ ] All mandatory sections completed

## Requirement Completeness
- [ ] Requirements are testable
- [ ] Success criteria are measurable
- [ ] Edge cases identified

## Feature Readiness
- [ ] Ready for next phase
"""
            checklist_file.write_text(basic_checklist)
            self.print_success("Basic checklist file created")

        return {
            "success": True,
            "branch_name": branch_name,
            "feature_number": number,
            "short_name": short_name,
            "description": description,
            "spec_file": str(spec_file),
            "checklist_file": str(checklist_file),
            "specs_dir": str(specs_dir)
        }


def main():
    parser = argparse.ArgumentParser(
        description="Create a new healthcare feature branch and spec structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 create-healthcare-feature.py --number 5 --short-name "patient-portal" "Add HIPAA-compliant patient portal"
  python3 create-healthcare-feature.py --json --number 5 --short-name "patient-portal" "Add HIPAA-compliant patient portal"
        """
    )
    parser.add_argument(
        '--number',
        type=int,
        required=True,
        help='Feature number (required)'
    )
    parser.add_argument(
        '--short-name',
        required=True,
        help='Short name for the feature (required)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        'description',
        nargs='+',
        help='Healthcare feature description'
    )

    args = parser.parse_args()

    # Join description arguments
    description = ' '.join(args.description)

    creator = HealthcareFeatureCreator()
    creator.output_json = args.json

    # Validate short name
    if not creator.validate_short_name(args.short_name):
        sys.exit(1)

    # Create the feature
    result = creator.create_healthcare_feature(args.number, args.short_name, description)

    if not result:
        sys.exit(1)

    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("")
        creator.print_success("Healthcare feature created successfully!")
        print("")
        print(f"Branch: {result['branch_name']}")
        print(f"Spec file: {result['spec_file']}")
        print(f"Checklist: {result['checklist_file']}")
        print("")
        creator.print_info("Next steps:")
        print(f"  1. Fill in the specification: {result['spec_file']}")
        print(f"  2. Validate using checklist: {result['checklist_file']}")
        print(f"  3. Commit your changes: git add . && git commit -m 'docs: add specification for {args.short_name}'")

    sys.exit(0)


if __name__ == "__main__":
    main()