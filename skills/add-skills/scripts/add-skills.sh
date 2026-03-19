#!/usr/bin/env bash
# add-skills.sh - Download and install a skill from a GitHub repository
#
# Usage: add-skills.sh <repo_url> <branch> <repo_path> <skill_name> <target_dir>
#
# Arguments:
#   repo_url    - GitHub repository URL (e.g., https://github.com/owner/repo)
#   branch      - Git branch name (e.g., main)
#   repo_path   - Path within repo containing skills (e.g., skills)
#   skill_name  - Name of the skill to download (e.g., git-commit)
#   target_dir  - Local directory to copy the skill into

set -euo pipefail

REPO_URL="${1:?Usage: add-skills.sh <repo_url> <branch> <repo_path> <skill_name> <target_dir>}"
BRANCH="${2:?Missing branch}"
REPO_PATH="${3:?Missing repo_path}"
SKILL_NAME="${4:?Missing skill_name}"
TARGET_DIR="${5:?Missing target_dir}"

# Parse owner/repo from URL
OWNER_REPO=$(echo "$REPO_URL" | sed -E 's|https?://github\.com/||' | sed 's|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d'/' -f1)
REPO=$(echo "$OWNER_REPO" | cut -d'/' -f2)

# Build auth header if GH_TOKEN is set
AUTH_HEADER=""
if [ -n "${GH_TOKEN:-}" ]; then
    AUTH_HEADER="Authorization: Bearer $GH_TOKEN"
elif [ -n "${GITHUB_TOKEN:-}" ]; then
    AUTH_HEADER="Authorization: Bearer $GITHUB_TOKEN"
fi

curl_opts=(-s -f -L)
if [ -n "$AUTH_HEADER" ]; then
    curl_opts+=(-H "$AUTH_HEADER")
fi

# GitHub API base for contents
API_BASE="https://api.github.com/repos/${OWNER}/${REPO}/contents"
RAW_BASE="https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}"
SKILL_PATH="${REPO_PATH}/${SKILL_NAME}"

echo "Downloading skill: ${SKILL_NAME} from ${OWNER}/${REPO}@${BRANCH}"

# Create target directory
mkdir -p "$TARGET_DIR"

# Recursive function to download all files in a directory
download_dir() {
    local remote_path="$1"
    local local_dir="$2"

    local api_url="${API_BASE}/${remote_path}?ref=${BRANCH}"
    local listing
    listing=$(curl "${curl_opts[@]}" -H "Accept: application/vnd.github.v3+json" "$api_url") || {
        echo "Error: Failed to list ${remote_path}" >&2
        return 1
    }

    # Parse JSON array - extract name, type, and path for each item
    # Using simple grep/sed parsing to avoid jq dependency
    local items
    items=$(echo "$listing" | python3 -c "
import sys, json
items = json.load(sys.stdin)
if isinstance(items, list):
    for item in items:
        print(f\"{item['type']}|{item['name']}|{item['path']}\")
" 2>/dev/null) || {
        echo "Error: Failed to parse directory listing for ${remote_path}" >&2
        return 1
    }

    while IFS='|' read -r item_type item_name item_path; do
        [ -z "$item_type" ] && continue

        if [ "$item_type" = "file" ]; then
            # Download file
            local raw_url="${RAW_BASE}/${item_path}"
            local local_file="${local_dir}/${item_name}"
            curl "${curl_opts[@]}" -o "$local_file" "$raw_url" || {
                echo "Warning: Failed to download ${item_path}" >&2
                continue
            }
            echo "  Downloaded: ${item_path}"
        elif [ "$item_type" = "dir" ]; then
            # Recursively download subdirectory
            mkdir -p "${local_dir}/${item_name}"
            download_dir "$item_path" "${local_dir}/${item_name}"
        fi
    done <<< "$items"
}

# Download the skill directory recursively
download_dir "$SKILL_PATH" "$TARGET_DIR"

echo "Installed skill: ${SKILL_NAME} -> ${TARGET_DIR}"
