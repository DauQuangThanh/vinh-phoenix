#!/usr/bin/env python3
# validate-docs.py - Validate documentation structure and completeness
# Usage: python3 validate-docs.py --dir <directory> --type <type>

import argparse
import glob
import os
import re
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
    NC = '\033[0m' if HAS_COLORAMA else ''

class Validator:
    def __init__(self, doc_dir, doc_type, verbose=False):
        self.doc_dir = Path(doc_dir)
        self.doc_type = doc_type
        self.verbose = verbose
        self.total_checks = 0
        self.passed_checks = 0
        self.failed_checks = 0
        self.warnings = 0

    def log_info(self, message):
        if self.verbose:
            print(f"{Colors.GREEN}[INFO]{Colors.NC} {message}")

    def log_error(self, message):
        print(f"{Colors.RED}[ERROR]{Colors.NC} {message}", file=sys.stderr)
        self.failed_checks += 1

    def log_warning(self, message):
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")
        self.warnings += 1

    def log_pass(self, message):
        if self.verbose:
            print(f"{Colors.GREEN}[PASS]{Colors.NC} {message}")
        self.passed_checks += 1

    def check(self):
        self.total_checks += 1

    def validate_readme(self):
        self.log_info("Validating README documentation...")

        readme_file = self.doc_dir / 'README.md'

        # Check if README exists
        self.check()
        if readme_file.exists():
            self.log_pass("README.md exists")
        else:
            self.log_error(f"README.md not found in {self.doc_dir}")
            return

        content = readme_file.read_text()

        # Project title
        self.check()
        if re.search(r'^# ', content, re.MULTILINE):
            self.log_pass("Has project title (H1)")
        else:
            self.log_error("Missing project title (# heading)")

        # Description
        self.check()
        if re.search(r'(?i)description|overview', content):
            self.log_pass("Has description section")
        else:
            self.log_warning("Consider adding a description or overview section")

        # Installation
        self.check()
        if re.search(r'(?i)## Installation|## Install|## Setup', content):
            self.log_pass("Has installation section")
        else:
            self.log_error("Missing installation section")

        # Usage
        self.check()
        if re.search(r'(?i)## Usage|## Quick Start|## Getting Started', content):
            self.log_pass("Has usage section")
        else:
            self.log_error("Missing usage section")

        # Code examples
        self.check()
        if '```' in content:
            self.log_pass("Contains code examples")
        else:
            self.log_warning("Consider adding code examples")

        # License
        self.check()
        if re.search(r'(?i)## License', content):
            self.log_pass("Has license section")
        else:
            self.log_warning("Consider adding license information")

        # Links check
        self.check()
        broken_links = 0
        for line in content.split('\n'):
            # Find markdown links [text](url)
            link_match = re.search(r'\[.*?\]\(([^)]+)\)', line)
            if link_match:
                url = link_match.group(1)
                if url.startswith(('http://', 'https://')):
                    self.log_info(f"Skipping external URL check: {url}")
                elif url and not (self.doc_dir / url).exists():
                    self.log_warning(f"Broken link to local file: {url}")
                    broken_links += 1

        if broken_links == 0:
            self.log_pass("No broken local links found")

    def validate_api(self):
        self.log_info("Validating API documentation...")

        # Find API documentation file
        api_files = list(self.doc_dir.glob('*api*.md'))
        if not api_files:
            api_files = list(self.doc_dir.glob('*.md'))  # fallback

        self.check()
        if api_files:
            api_file = api_files[0]
            self.log_pass(f"API documentation file found: {api_file}")
        else:
            self.log_error("No API documentation file found")
            return

        content = api_file.read_text()

        # Check for authentication section
        self.check()
        if re.search(r'(?i)## Authentication|## Auth', content):
            self.log_pass("Has authentication section")
        else:
            self.log_error("Missing authentication section")

        # Check for endpoints
        self.check()
        if re.search(r'(GET|POST|PUT|PATCH|DELETE) /', content):
            self.log_pass("Contains endpoint definitions")
        else:
            self.log_error("Missing endpoint definitions")

        # Check for request examples
        self.check()
        if re.search(r'(?i)request|example', content):
            self.log_pass("Contains request examples")
        else:
            self.log_warning("Consider adding request examples")

        # Check for response examples
        self.check()
        if re.search(r'(?i)response', content):
            self.log_pass("Contains response documentation")
        else:
            self.log_error("Missing response documentation")

        # Check for error codes
        self.check()
        if re.search(r'\b(400|401|403|404|500)\b', content):
            self.log_pass("Documents error codes")
        else:
            self.log_warning("Consider documenting error codes")

    def validate_user_guide(self):
        self.log_info("Validating user guide documentation...")

        # Find user guide file
        guide_patterns = ['*user*guide*.md', '*guide*.md']
        guide_file = None
        for pattern in guide_patterns:
            matches = list(self.doc_dir.glob(pattern))
            if matches:
                guide_file = matches[0]
                break

        self.check()
        if guide_file:
            self.log_pass(f"User guide file found: {guide_file}")
        else:
            self.log_error("No user guide file found")
            return

        content = guide_file.read_text()

        # Check for getting started
        self.check()
        if re.search(r'(?i)## Getting Started', content):
            self.log_pass("Has getting started section")
        else:
            self.log_error("Missing getting started section")

        # Check for screenshots or images
        self.check()
        if re.search(r'!\[.*?\]\(', content):
            self.log_pass("Contains images/screenshots")
        else:
            self.log_warning("Consider adding screenshots for user guidance")

        # Check for troubleshooting
        self.check()
        if re.search(r'(?i)## Troubleshooting|## FAQ', content):
            self.log_pass("Has troubleshooting or FAQ section")
        else:
            self.log_warning("Consider adding troubleshooting section")

    def validate_architecture(self):
        self.log_info("Validating architecture documentation...")

        # Find architecture file
        arch_patterns = ['*architecture*.md', '*design*.md']
        arch_file = None
        for pattern in arch_patterns:
            matches = list(self.doc_dir.glob(pattern))
            if matches:
                arch_file = matches[0]
                break

        self.check()
        if arch_file:
            self.log_pass(f"Architecture file found: {arch_file}")
        else:
            self.log_error("No architecture file found")
            return

        content = arch_file.read_text()

        # Check for system overview
        self.check()
        if re.search(r'(?i)## Overview|## System Overview', content):
            self.log_pass("Has system overview")
        else:
            self.log_error("Missing system overview")

        # Check for diagrams
        self.check()
        if re.search(r'!\[.*?\]\(', content):
            self.log_pass("Contains diagrams")
        else:
            self.log_warning("Consider adding architecture diagrams")

        # Check for components section
        self.check()
        if re.search(r'(?i)## Components', content):
            self.log_pass("Has components section")
        else:
            self.log_error("Missing components section")

        # Check for design decisions
        self.check()
        if re.search(r'(?i)## Design Decision|ADR|Decision', content):
            self.log_pass("Documents design decisions")
        else:
            self.log_warning("Consider documenting design decisions")

    def run_validation(self):
        print("========================================")
        print("Documentation Validation")
        print("========================================")
        print(f"Directory: {self.doc_dir}")
        print(f"Type: {self.doc_type}")
        print()

        if self.doc_type == 'readme':
            self.validate_readme()
        elif self.doc_type == 'api':
            self.validate_api()
        elif self.doc_type == 'user-guide':
            self.validate_user_guide()
        elif self.doc_type == 'architecture':
            self.validate_architecture()
        else:
            print(f"{Colors.RED}Error: Unknown documentation type: {self.doc_type}{Colors.NC}", file=sys.stderr)
            print("Valid types: readme, api, user-guide, architecture")
            return False

        # Print summary
        print()
        print("========================================")
        print("Validation Summary")
        print("========================================")
        print(f"Total checks: {self.total_checks}")
        print(f"{Colors.GREEN}Passed: {self.passed_checks}{Colors.NC}")
        print(f"{Colors.RED}Failed: {self.failed_checks}{Colors.NC}")
        print(f"{Colors.YELLOW}Warnings: {self.warnings}{Colors.NC}")
        print()

        if self.failed_checks > 0:
            print(f"{Colors.RED}Validation failed{Colors.NC}")
            return False
        else:
            print(f"{Colors.GREEN}Validation passed{Colors.NC}")
            return True

def main():
    parser = argparse.ArgumentParser(description='Validate documentation structure and completeness.')
    parser.add_argument('-d', '--dir', default='./docs',
                       help='Documentation directory (default: ./docs)')
    parser.add_argument('-t', '--type', required=True,
                       choices=['readme', 'api', 'user-guide', 'architecture'],
                       help='Documentation type')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    # Validate directory exists
    if not os.path.isdir(args.dir):
        print(f"{Colors.RED}Error: Directory not found: {args.dir}{Colors.NC}", file=sys.stderr)
        sys.exit(1)

    validator = Validator(args.dir, args.type, args.verbose)
    success = validator.run_validation()

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()