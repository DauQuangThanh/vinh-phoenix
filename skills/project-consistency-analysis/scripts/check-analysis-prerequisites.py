#!/usr/bin/env python3
"""
check-analysis-prerequisites.py
Detects required artifacts for project consistency analysis
Usage: python3 check-analysis-prerequisites.py [feature-directory] [--json]
Output: JSON with artifact paths and status
"""

import argparse
import json
import os
import sys
from pathlib import Path


class PrerequisitesChecker:
    def __init__(self):
        self.artifacts = {
            'spec': '',
            'design': '',
            'tasks': '',
            'groundRules': '',
            'architecture': '',
            'standards': ''
        }

    def find_file(self, directory: Path, pattern: str) -> str:
        """Find file with case-insensitive pattern in directory."""
        try:
            for file_path in directory.iterdir():
                if file_path.is_file() and file_path.name.lower() == pattern.lower():
                    return str(file_path.resolve())
        except OSError:
            pass
        return ''

    def check_directory(self, feature_dir: str) -> dict:
        """Check the feature directory for required and optional artifacts."""
        feature_path = Path(feature_dir).resolve()

        if not feature_path.exists() or not feature_path.is_dir():
            return {
                'success': False,
                'error': f'Directory not found: {feature_dir}',
                'featureDirectory': str(feature_path)
            }

        # Required artifacts
        self.artifacts['spec'] = self.find_file(feature_path, 'spec.md')
        self.artifacts['design'] = self.find_file(feature_path, 'design.md')
        self.artifacts['tasks'] = self.find_file(feature_path, 'tasks.md')

        # Optional artifacts - check memory and docs subdirectories, also parent
        memory_dir = feature_path / 'memory'
        parent_memory_dir = feature_path.parent / 'memory'
        docs_dir = feature_path / 'docs'
        parent_docs_dir = feature_path.parent / 'docs'

        # Ground rules
        if memory_dir.exists():
            self.artifacts['groundRules'] = self.find_file(memory_dir, 'ground-rules.md')
        elif parent_memory_dir.exists():
            self.artifacts['groundRules'] = self.find_file(parent_memory_dir, 'ground-rules.md')

        # Architecture and standards
        if docs_dir.exists():
            self.artifacts['architecture'] = self.find_file(docs_dir, 'architecture.md')
            self.artifacts['standards'] = self.find_file(docs_dir, 'standards.md')
        elif parent_docs_dir.exists():
            self.artifacts['architecture'] = self.find_file(parent_docs_dir, 'architecture.md')
            self.artifacts['standards'] = self.find_file(parent_docs_dir, 'standards.md')

        # Check required artifacts
        missing_required = []
        if not self.artifacts['spec']:
            missing_required.append('spec.md')
        if not self.artifacts['design']:
            missing_required.append('design.md')
        if not self.artifacts['tasks']:
            missing_required.append('tasks.md')

        # Determine overall status
        success = len(missing_required) == 0
        message = 'All required artifacts found' if success else f'Missing required artifacts: {", ".join(missing_required)}'

        # Count artifacts
        total_found = sum(1 for v in self.artifacts.values() if v)
        required_found = sum(1 for k, v in self.artifacts.items() if k in ['spec', 'design', 'tasks'] and v)
        optional_found = total_found - required_found

        return {
            'success': success,
            'message': message,
            'featureDirectory': str(feature_path),
            'artifacts': {
                'required': {
                    'spec': self.artifacts['spec'],
                    'design': self.artifacts['design'],
                    'tasks': self.artifacts['tasks']
                },
                'optional': {
                    'groundRules': self.artifacts['groundRules'],
                    'architecture': self.artifacts['architecture'],
                    'standards': self.artifacts['standards']
                }
            },
            'summary': {
                'totalFound': total_found,
                'requiredFound': required_found,
                'optionalFound': optional_found,
                'missingRequired': missing_required
            }
        }

    def print_human_readable(self, result: dict):
        """Print results in human-readable format."""
        print("\nProject Consistency Analysis - Prerequisite Check")
        print("=" * 60)
        print(f"\nFeature Directory: {result['featureDirectory']}")

        success = result['success']
        print(f"\nStatus: {'SUCCESS' if success else 'INCOMPLETE'}")
        print(f"Message: {result['message']}\n")

        print("Required Artifacts:")
        artifacts = result['artifacts']['required']
        for name, path in artifacts.items():
            status = "FOUND" if path else "MISSING"
            color = "\033[92m" if path else "\033[91m"  # Green if found, red if missing
            reset = "\033[0m"
            print(f"  {name}.md       : {color}{status}{reset}")
            if path:
                print(f"                  {path}")

        print("\nOptional Artifacts:")
        artifacts = result['artifacts']['optional']
        for name, path in artifacts.items():
            status = "FOUND" if path else "NOT FOUND"
            color = "\033[92m" if path else "\033[90m"  # Green if found, gray if not found
            reset = "\033[0m"
            print(f"  {name}.md : {color}{status}{reset}")
            if path:
                print(f"                    {path}")

        summary = result['summary']
        print("\nSummary:")
        print(f"  Total Found     : {summary['totalFound']}")
        print(f"  Required Found  : {summary['requiredFound']} / 3")
        print(f"  Optional Found  : {summary['optionalFound']} / 3")

        if summary['missingRequired']:
            print(f"\nMissing Required: {', '.join(summary['missingRequired'])}")

        print("")


def main():
    parser = argparse.ArgumentParser(
        description="Check project consistency analysis prerequisites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 check-analysis-prerequisites.py                    # Check current directory
  python3 check-analysis-prerequisites.py /path/to/feature  # Check specific directory
  python3 check-analysis-prerequisites.py --json            # JSON output
        """
    )
    parser.add_argument(
        'feature_directory',
        nargs='?',
        default='.',
        help='Feature directory to check (default: current directory)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    checker = PrerequisitesChecker()
    result = checker.check_directory(args.feature_directory)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        checker.print_human_readable(result)

    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()