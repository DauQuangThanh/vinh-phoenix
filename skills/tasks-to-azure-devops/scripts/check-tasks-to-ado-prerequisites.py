#!/usr/bin/env python3
# check-tasks-to-ado-prerequisites.py - Check prerequisites and identify task files before running tasks-to-azure-devops skill
#
# Usage:
#   python check-tasks-to-ado-prerequisites.py [--json]
#
# Arguments:
#   --json         Output results as JSON
#
# Requirements:
#   - Python 3.6+

import argparse
import json
import os
import re
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

def get_workspace_root():
    # Assuming script is in skills/tasks-to-azure-devops/scripts/
    script_dir = Path(__file__).parent
    return script_dir.parent.parent.parent

def find_tasks_files(workspace_root):
    tasks_files = []
    for file_path in workspace_root.rglob("tasks.md"):
        # Exclude node_modules and .git
        if "node_modules" not in str(file_path) and ".git" not in str(file_path):
            tasks_files.append(str(file_path))
    return tasks_files

def parse_azure_devops_remote(remote_url):
    ado_org = ""
    ado_project = ""
    ado_repo = ""

    # Parse: https://dev.azure.com/{organization}/{project}/_git/{repository}
    match = re.search(r'dev\.azure\.com/([^/]+)/([^/]+)/_git/([^/]+)', remote_url)
    if match:
        ado_org = match.group(1)
        ado_project = match.group(2)
        ado_repo = match.group(3)
        return ado_org, ado_project, ado_repo

    # Parse: git@ssh.dev.azure.com:v3/{organization}/{project}/{repository}
    match = re.search(r'ssh\.dev\.azure\.com:v3/([^/]+)/([^/]+)/([^/]+)', remote_url)
    if match:
        ado_org = match.group(1)
        ado_project = match.group(2)
        ado_repo = match.group(3)
        return ado_org, ado_project, ado_repo

    # Parse: https://{organization}.visualstudio.com/{project}/_git/{repository}
    match = re.search(r'([^/]+)\.visualstudio\.com/([^/]+)/_git/([^/]+)', remote_url)
    if match:
        ado_org = match.group(1)
        ado_project = match.group(2)
        ado_repo = match.group(3)
        return ado_org, ado_project, ado_repo

    # Parse: https://{organization}.visualstudio.com/DefaultCollection/{project}/_git/{repository}
    match = re.search(r'([^/]+)\.visualstudio\.com/DefaultCollection/([^/]+)/_git/([^/]+)', remote_url)
    if match:
        ado_org = match.group(1)
        ado_project = match.group(2)
        ado_repo = match.group(3)
        return ado_org, ado_project, ado_repo

    return ado_org, ado_project, ado_repo

def main():
    parser = argparse.ArgumentParser(description="Check prerequisites for tasks-to-azure-devops skill")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    workspace_root = get_workspace_root()

    # Initialize variables
    tasks_file = ""
    git_remote = ""
    ado_org = ""
    ado_project = ""
    ado_repo = ""
    is_azure_devops = False
    is_git_repo = False
    git_available = False

    all_required_present = True
    errors = []
    warnings = []
    info = []

    # Check if git is available
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        git_available = True
        info.append("Git command is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        all_required_present = False
        errors.append("Git command not found (required for repository operations)")

    # Check if we're in a git repository
    if git_available:
        try:
            subprocess.run(["git", "rev-parse", "--git-dir"], check=True, capture_output=True, cwd=workspace_root)
            is_git_repo = True
            info.append("Repository is a Git repository")
        except subprocess.CalledProcessError:
            all_required_present = False
            errors.append("Not a Git repository (run 'git init' to initialize)")

    # Get Git remote if available
    if is_git_repo:
        try:
            result = subprocess.run(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True, cwd=workspace_root)
            if result.returncode == 0:
                git_remote = result.stdout.strip()
                if not git_remote:
                    all_required_present = False
                    errors.append("No Git remote configured (run 'git remote add origin <url>')")
                else:
                    info.append(f"Git remote found: {git_remote}")

                    # Check if remote is Azure DevOps
                    if 'dev.azure.com' in git_remote or 'visualstudio.com' in git_remote:
                        is_azure_devops = True
                        if 'dev.azure.com' in git_remote:
                            info.append("Remote is an Azure DevOps repository")
                        else:
                            info.append("Remote is an Azure DevOps repository (legacy URL)")

                        ado_org, ado_project, ado_repo = parse_azure_devops_remote(git_remote)
                        if ado_org and ado_project:
                            info.append(f"Organization: {ado_org}, Project: {ado_project}, Repository: {ado_repo}")
                        else:
                            warnings.append("Could not parse organization/project from Azure DevOps remote URL")
                    else:
                        all_required_present = False
                        errors.append("Remote is not an Azure DevOps repository (this skill only works with Azure DevOps)")
            else:
                all_required_present = False
                errors.append("Failed to get Git remote configuration")
        except Exception as e:
            all_required_present = False
            errors.append(f"Failed to get Git remote: {e}")

    # Search for tasks.md files
    tasks_files = find_tasks_files(workspace_root)

    if not tasks_files:
        all_required_present = False
        errors.append("No tasks.md file found in repository")
    elif len(tasks_files) == 1:
        tasks_file = tasks_files[0]
        info.append(f"Found tasks.md at: {tasks_file}")
    else:
        tasks_file = tasks_files[0]
        warnings.append(f"Multiple tasks.md files found ({len(tasks_files)}), using first: {tasks_file}")

    # Check for Azure DevOps MCP server availability (informational)
    if is_azure_devops:
        info.append("Azure DevOps MCP server is required for work item creation")

    # Output results
    if args.json:
        result = {
            "success": all_required_present,
            "workspace_root": str(workspace_root),
            "git": {
                "available": git_available,
                "is_repository": is_git_repo,
                "remote": git_remote,
                "is_azure_devops": is_azure_devops
            },
            "ado": {
                "organization": ado_org,
                "project": ado_project,
                "repository": ado_repo
            },
            "tasks_file": tasks_file,
            "errors": errors,
            "warnings": warnings,
            "info": info
        }
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print("")
        print("Tasks to Azure DevOps - Prerequisites Check")
        print("================================================")
        print("")

        # Workspace info
        print("Workspace: ", end="")
        print(str(workspace_root))
        print("")

        # Git section
        print("Git Configuration:")
        if git_available:
            print("  ✓ Git command available")
        else:
            print("  ✗ Git command not found (REQUIRED)")

        if is_git_repo:
            print("  ✓ Git repository initialized")
        else:
            print("  ✗ Not a Git repository (REQUIRED)")

        if git_remote:
            print("  ✓ Git remote configured")
            print(f"    Remote: {git_remote}")
        else:
            print("  ✗ No Git remote configured (REQUIRED)")

        if is_azure_devops:
            print("  ✓ Remote is Azure DevOps")
            if ado_org and ado_project:
                print(f"    Organization: {ado_org}")
                print(f"    Project: {ado_project}")
                print(f"    Repository: {ado_repo}")
        elif git_remote:
            print("  ✗ Remote is not Azure DevOps (REQUIRED - this skill only works with Azure DevOps)")

        print("")

        # Tasks file section
        print("Task File:")
        if tasks_file:
            print("  ✓ tasks.md found")
            print(f"    Path: {tasks_file}")
        else:
            print("  ✗ tasks.md not found (REQUIRED)")

        print("")

        # Errors
        if errors:
            print("Errors:")
            for error in errors:
                print(f"  ✗ {error}")
            print("")

        # Warnings
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"  ⚠ {warning}")
            print("")

        # Summary
        if all_required_present:
            print("✓ All prerequisites met. Ready to sync tasks to Azure DevOps work items.")
            print("")
            print("Next steps:")
            print("  1. Ensure Azure DevOps MCP server is configured with authentication")
            print("  2. Run tasks-to-azure-devops skill to create work items")
            if ado_org and ado_project:
                print(f"  3. Review created work items in project: https://dev.azure.com/{ado_org}/{ado_project}/_workitems")
        else:
            print("✗ Missing required prerequisites. Please resolve the following before proceeding:")
            for error in errors:
                print(f"  - {error}")
            print("")
            print("Tips:")
            if not git_available:
                print("  - Install Git: https://git-scm.com/downloads")
            if not is_git_repo:
                print("  - Initialize Git repository: git init")
            if not git_remote:
                print("  - Add Azure DevOps remote: git remote add origin https://dev.azure.com/org/project/_git/repo")
            if not is_azure_devops and git_remote:
                print("  - This skill only works with Azure DevOps repositories")
                print("  - Change remote to Azure DevOps or use manual work item creation")
            if not tasks_file:
                print("  - Create tasks.md with task definitions")
                print("  - Run 'taskify' command to generate tasks from specifications")
        print("")

    # Exit with appropriate code
    sys.exit(0 if all_required_present else 1)

if __name__ == "__main__":
    main()