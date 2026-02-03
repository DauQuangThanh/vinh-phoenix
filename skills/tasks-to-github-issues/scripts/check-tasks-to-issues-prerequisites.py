#!/usr/bin/env python3
# check-tasks-to-issues-prerequisites.py - Check prerequisites for tasks-to-github-issues skill
#
# Usage:
#   python check-tasks-to-issues-prerequisites.py [--json]
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
    # Assuming script is in skills/tasks-to-github-issues/scripts/
    script_dir = Path(__file__).parent
    return script_dir.parent.parent.parent

def find_tasks_files(workspace_root):
    tasks_files = []
    for file_path in workspace_root.rglob("tasks.md"):
        # Exclude node_modules and .git
        if "node_modules" not in str(file_path) and ".git" not in str(file_path):
            tasks_files.append(str(file_path))
    return tasks_files

def parse_github_remote(remote_url):
    repo_owner = ""
    repo_name = ""

    # Parse: https://github.com/{owner}/{repo}.git or https://github.com/{owner}/{repo}
    match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', remote_url)
    if match:
        repo_owner = match.group(1)
        repo_name = match.group(2)
        # Remove .git if present
        repo_name = repo_name.replace('.git', '')
        return repo_owner, repo_name

    return repo_owner, repo_name

def main():
    parser = argparse.ArgumentParser(description="Check prerequisites for tasks-to-github-issues skill")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    workspace_root = get_workspace_root()

    # Initialize variables
    tasks_file = ""
    git_remote = ""
    repo_owner = ""
    repo_name = ""
    is_github = False
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

                    # Check if remote is GitHub
                    if 'github.com' in git_remote:
                        is_github = True
                        info.append("Remote is a GitHub repository")

                        repo_owner, repo_name = parse_github_remote(git_remote)
                        if repo_owner and repo_name:
                            info.append(f"Repository: {repo_owner}/{repo_name}")
                        else:
                            warnings.append("Could not parse repository owner/name from remote URL")
                    else:
                        all_required_present = False
                        errors.append("Remote is not a GitHub repository (this skill only works with GitHub)")
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

    # Check for GitHub MCP server availability (informational)
    if is_github:
        info.append("GitHub MCP server is required for issue creation")

    # Output results
    if args.json:
        result = {
            "success": all_required_present,
            "workspace_root": str(workspace_root),
            "git": {
                "available": git_available,
                "is_repository": is_git_repo,
                "remote": git_remote,
                "is_github": is_github
            },
            "repository": {
                "owner": repo_owner,
                "name": repo_name
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
        print("Tasks to GitHub Issues - Prerequisites Check")
        print("================================================")
        print("")

        # Workspace info
        print(f"Workspace: {workspace_root}")
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

        if is_github:
            print("  ✓ Remote is GitHub")
            print(f"    Repository: {repo_owner}/{repo_name}")
        elif git_remote:
            print("  ✗ Remote is not GitHub (REQUIRED - this skill only works with GitHub)")

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
            print("✓ All prerequisites met. Ready to sync tasks to GitHub issues.")
            print("")
            print("Next steps:")
            print("  1. Ensure GitHub MCP server is configured with authentication")
            print("  2. Run tasks-to-github-issues skill to create issues")
            if repo_owner and repo_name:
                print(f"  3. Review created issues in repository: https://github.com/{repo_owner}/{repo_name}/issues")
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
                print("  - Add GitHub remote: git remote add origin https://github.com/owner/repo.git")
            if not is_github and git_remote:
                print("  - This skill only works with GitHub repositories")
                print("  - Change remote to GitHub or use manual issue creation")
            if not tasks_file:
                print("  - Create tasks.md with task definitions")
                print("  - Run 'taskify' command to generate tasks from specifications")
        print("")

    # Exit with appropriate code
    sys.exit(0 if all_required_present else 1)

if __name__ == "__main__":
    main()