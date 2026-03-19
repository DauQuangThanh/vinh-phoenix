#!/usr/bin/env python3
"""List available skills from configured remote repositories.

Reads nightlife.yaml for GitHub issue URLs, fetches repo definitions,
and lists available skills from each repository.
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error


def parse_simple_yaml(text: str) -> dict:
    """Parse simple YAML structure from nightlife.yaml or issue bodies."""
    result = {}
    current_top_key = None
    current_item = None
    items = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        comment_idx = stripped.find(" #")
        if comment_idx > 0:
            stripped = stripped[:comment_idx].strip()

        if not line.startswith(" ") and not line.startswith("\t") and ":" in stripped:
            if current_item is not None:
                items.append(current_item)
                current_item = None
            if current_top_key and items:
                result[current_top_key] = items
                items = []
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value:
                result[key] = value
                current_top_key = None
            else:
                current_top_key = key
                items = []
            current_item = None
            continue

        if stripped.startswith("- "):
            if current_item is not None:
                items.append(current_item)
                current_item = None
            stripped = stripped[2:].strip()
            if ":" in stripped and not stripped.startswith("http"):
                current_item = {}
                k, _, v = stripped.partition(":")
                current_item[k.strip()] = v.strip()
            else:
                items.append(stripped)
            continue

        if current_item is not None and ":" in stripped:
            k, _, v = stripped.partition(":")
            current_item[k.strip()] = v.strip()
            continue

    if current_item is not None:
        items.append(current_item)
    if current_top_key and items:
        result[current_top_key] = items
    return result


def github_request(url: str) -> dict:
    """Make a GitHub API request with optional token auth."""
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "phoenix-cli"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main():
    # Read nightlife.yaml
    if not os.path.exists("nightlife.yaml"):
        print("Error: nightlife.yaml not found in current directory.")
        print("Create one with 'phoenix config-set-url <url1> <url2>' or manually.")
        sys.exit(1)

    with open("nightlife.yaml", encoding="utf-8") as f:
        config = parse_simple_yaml(f.read())

    urls = config.get("urls", [])
    if not urls or not isinstance(urls, list):
        print("Error: No 'urls' configured in nightlife.yaml.")
        sys.exit(1)

    # Fetch repo definitions from all issues
    skill_repos = []
    seen = set()

    for issue_url in urls:
        match = re.match(r"https?://github\.com/([^/]+)/([^/]+)/issues/(\d+)", issue_url)
        if not match:
            print(f"Warning: Invalid issue URL: {issue_url}")
            continue
        owner, repo, number = match.groups()
        api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{number}"

        try:
            data = github_request(api_url)
            body = data.get("body", "")
            repos = parse_simple_yaml(body)
            for skill in repos.get("skills", []):
                name = skill.get("name", "")
                if name and name not in seen:
                    seen.add(name)
                    skill_repos.append(skill)
        except Exception as e:
            print(f"Warning: Failed to fetch {issue_url}: {e}")

    if not skill_repos:
        print("No skill repositories configured.")
        sys.exit(0)

    # List skills from each repo
    total = 0
    for repo_info in skill_repos:
        repo_name = repo_info.get("name", "unknown")
        repo_url = repo_info.get("url", "")
        branch = repo_info.get("branch", "main")
        path = repo_info.get("path", "skills")

        match = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?$", repo_url)
        if not match:
            print(f"\n{repo_name}: Invalid repo URL")
            continue

        owner, repo = match.groups()
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"

        print(f"\nRepository: {repo_name} ({repo_url})")
        try:
            contents = github_request(api_url)
            skills = []
            for item in contents:
                name = item["name"]
                if name.startswith(".") or name.startswith("_"):
                    continue
                if item["type"] == "dir":
                    skills.append(name)

            for s in sorted(skills):
                print(f"  - {s}")
            print(f"  Total: {len(skills)} skills available")
            total += len(skills)
        except urllib.error.HTTPError as e:
            print(f"  Error: HTTP {e.code} - {path} not found or inaccessible")
        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nGrand total: {total} skills across {len(skill_repos)} repositories")


if __name__ == "__main__":
    main()
