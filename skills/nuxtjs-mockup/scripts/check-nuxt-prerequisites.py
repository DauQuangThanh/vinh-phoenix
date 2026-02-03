#!/usr/bin/env python3
"""
check-nuxt-prerequisites.py
Checks for required tools and configuration before running nuxtjs-mockup skill
Usage: python3 check-nuxt-prerequisites.py [--json]
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


class PrerequisitesChecker:
    def __init__(self):
        self.node_version = ""
        self.node_available = False
        self.package_manager = ""
        self.package_manager_version = ""
        self.npm_version = ""
        self.pnpm_version = ""
        self.yarn_version = ""
        self.nuxt_project = False
        self.all_required_present = True
        self.errors = []
        self.warnings = []
        self.info = []

    def run_command(self, cmd, capture_output=True):
        """Run a command and return the result."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                timeout=30
            )
            return result
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return None

    def check_node_js(self):
        """Check if Node.js is available and meets version requirements."""
        result = self.run_command("node --version")
        if result and result.returncode == 0:
            version_output = result.stdout.strip()
            self.node_version = version_output.replace('v', '')
            self.node_available = True
            self.info.append(f"Node.js is available: {version_output}")

            # Parse major version
            try:
                node_major = int(self.node_version.split('.')[0])
            except (ValueError, IndexError):
                node_major = 0

            # Check if version meets minimum requirement (18+)
            if node_major < 18:
                self.all_required_present = False
                self.errors.append(f"Node.js version {self.node_version} is too old. Nuxt 4 requires Node.js 18.0.0 or higher")
            else:
                self.info.append("Node.js version meets requirements (18+)")
        else:
            self.all_required_present = False
            self.node_available = False
            self.errors.append("Node.js not found. Install from https://nodejs.org/ (v20+ recommended)")

    def check_package_managers(self):
        """Check for available package managers."""
        if not self.node_available:
            return

        # Check for pnpm (preferred)
        result = self.run_command("pnpm --version")
        if result and result.returncode == 0:
            self.pnpm_version = result.stdout.strip()
            self.package_manager = "pnpm"
            self.package_manager_version = self.pnpm_version
            self.info.append(f"pnpm is available: v{self.pnpm_version} (recommended)")

        # Check for yarn
        result = self.run_command("yarn --version")
        if result and result.returncode == 0:
            self.yarn_version = result.stdout.strip()
            if not self.package_manager:
                self.package_manager = "yarn"
                self.package_manager_version = self.yarn_version
                self.info.append(f"yarn is available: v{self.yarn_version}")
            else:
                self.info.append(f"yarn is also available: v{self.yarn_version}")

        # Check for npm (fallback)
        result = self.run_command("npm --version")
        if result and result.returncode == 0:
            self.npm_version = result.stdout.strip()
            if not self.package_manager:
                self.package_manager = "npm"
                self.package_manager_version = self.npm_version
                self.info.append(f"npm is available: v{self.npm_version}")
            else:
                self.info.append(f"npm is also available: v{self.npm_version}")

        # If no package manager found
        if not self.package_manager:
            self.all_required_present = False
            self.errors.append("No package manager found. npm should be bundled with Node.js")
        else:
            self.info.append(f"Using package manager: {self.package_manager} v{self.package_manager_version}")

    def check_project_files(self):
        """Check for existing Nuxt project files."""
        # Get workspace root (assuming script is in skills/nuxtjs-mockup/scripts/)
        script_dir = Path(__file__).parent
        workspace_root = script_dir.parent.parent.parent

        # Check if in a Nuxt project
        package_json = workspace_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '"nuxt"' in content:
                        self.nuxt_project = True
                        self.info.append("Detected existing Nuxt project in workspace")
            except (IOError, OSError):
                pass

        # Check for common project files
        nuxt_files = ["nuxt.config.ts", "nuxt.config.js"]
        for nuxt_file in nuxt_files:
            if (workspace_root / nuxt_file).exists():
                self.info.append(f"Found Nuxt configuration file: {nuxt_file}")
                break

        tailwind_files = ["tailwind.config.js", "tailwind.config.ts"]
        for tw_file in tailwind_files:
            if (workspace_root / tw_file).exists():
                self.info.append("Found Tailwind CSS configuration")
                break

        return str(workspace_root)

    def run_checks(self):
        """Run all prerequisite checks."""
        self.check_node_js()
        self.check_package_managers()
        workspace_root = self.check_project_files()
        return workspace_root

    def to_dict(self, workspace_root):
        """Convert results to dictionary."""
        try:
            node_major = int(self.node_version.split('.')[0]) if self.node_version else 0
        except (ValueError, IndexError):
            node_major = 0

        return {
            "success": self.all_required_present,
            "workspace_root": workspace_root,
            "node": {
                "available": self.node_available,
                "version": self.node_version,
                "major_version": node_major
            },
            "package_manager": {
                "name": self.package_manager,
                "version": self.package_manager_version,
                "npm_version": self.npm_version,
                "pnpm_version": self.pnpm_version,
                "yarn_version": self.yarn_version
            },
            "project": {
                "is_nuxt": self.nuxt_project
            },
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info
        }

    def print_human_readable(self, workspace_root):
        """Print results in human-readable format."""
        print("")
        print("Nuxt.js Mockup - Prerequisites Check")
        print("=" * 50)
        print("")

        # Workspace info
        print(f"Workspace: {workspace_root}")
        print("")

        # Node.js section
        print("Node.js:")
        if self.node_available:
            print("  ✓ Node.js installed")
            print(f"    Version: v{self.node_version}")

            try:
                node_major = int(self.node_version.split('.')[0])
            except (ValueError, IndexError):
                node_major = 0

            if node_major >= 18:
                print("  ✓ Version meets requirements (18+)")
            else:
                print(f"  ✗ Version too old (need 18+, have {node_major})")
        else:
            print("  ✗ Node.js not found (REQUIRED)")
        print("")

        # Package Manager section
        print("Package Manager:")
        if self.package_manager:
            print(f"  ✓ {self.package_manager} v{self.package_manager_version} detected")

            if self.pnpm_version:
                print("  ✓ pnpm available (recommended)")

            if self.yarn_version:
                print(f"    yarn v{self.yarn_version} also available")

            if self.npm_version:
                print(f"    npm v{self.npm_version} also available")
        else:
            print("  ✗ No package manager found (REQUIRED)")
        print("")

        # Project status
        print("Project Status:")
        if self.nuxt_project:
            print("  ✓ Existing Nuxt project detected")
        else:
            print("    No Nuxt project detected (will initialize new project)")
        print("")

        # Errors
        if self.errors:
            print("Errors:")
            for error in self.errors:
                print(f"  ✗ {error}")
            print("")

        # Warnings
        if self.warnings:
            print("Warnings:")
            for warning in self.warnings:
                print(f"  ! {warning}")
            print("")

        # Summary
        if self.all_required_present:
            print("✓ All prerequisites met. Ready to create Nuxt mockups!")
            print("")
            print("Next steps:")
            print("  1. Run skill to create mockup project")
            print(f"  2. Or manually initialize: {self.package_manager} create nuxt@latest mockup")
            print(f"  3. Install dependencies: cd mockup && {self.package_manager} install")
            print(f"  4. Start dev server: {self.package_manager} dev")
            print("")
            print("Latest versions:")
            print("  - Nuxt: 4.3.x")
            print("  - Vue: 3.5.x")
            print("  - Tailwind CSS: 4.x")
            print("  - Vite: 5.x (built into Nuxt)")
        else:
            print("✗ Missing required prerequisites. Please resolve the following:")
            for error in self.errors:
                print(f"  - {error}")
            print("")
            print("Installation Tips:")
            if not self.node_available:
                print("  - Install Node.js v20 LTS: https://nodejs.org/")
                print("  - Or use version manager: nvm install 20")
            elif self.node_available:
                try:
                    node_major = int(self.node_version.split('.')[0])
                except (ValueError, IndexError):
                    node_major = 0
                if node_major < 18:
                    print("  - Upgrade Node.js: nvm install 20 && nvm use 20")
                    print("  - Or download from: https://nodejs.org/")
            if not self.pnpm_version:
                print("  - Install pnpm (recommended): npm install -g pnpm")
        print("")


def main():
    parser = argparse.ArgumentParser(description="Check Nuxt.js prerequisites")
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    args = parser.parse_args()

    checker = PrerequisitesChecker()
    workspace_root = checker.run_checks()

    if args.json:
        result = checker.to_dict(workspace_root)
        print(json.dumps(result, indent=2))
    else:
        checker.print_human_readable(workspace_root)

    # Exit with appropriate code
    sys.exit(0 if checker.all_required_present else 1)


if __name__ == "__main__":
    main()