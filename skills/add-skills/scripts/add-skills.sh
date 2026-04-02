#!/usr/bin/env bash
# add-skills.sh - Download and install a skill from a GitHub repository using git
#
# Usage: add-skills.sh <repo_url> <branch> <repo_path> <skill_name> <target_dir>
#
# Arguments:
#   repo_url    - GitHub repository URL (e.g., https://github.com/owner/repo)
#   branch      - Git branch name (e.g., main)
#   repo_path   - Path within repo containing skills (e.g., skills)
#   skill_name  - Name of the skill to download (e.g., git-commit)
#   target_dir  - Local directory to copy the skill into
#
# Uses git sparse-checkout to download only the specific skill folder,
# avoiding recursive GitHub API calls and rate limits.

set -euo pipefail

REPO_URL="${1:?Usage: add-skills.sh <repo_url> <branch> <repo_path> <skill_name> <target_dir>}"
BRANCH="${2:?Missing branch}"
REPO_PATH="${3:?Missing repo_path}"
SKILL_NAME="${4:?Missing skill_name}"
TARGET_DIR="${5:?Missing target_dir}"

SKILL_PATH="${REPO_PATH}/${SKILL_NAME}"

# Ensure git is available
if ! command -v git >/dev/null 2>&1; then
    echo "Error: git is required but not found. Install git and try again." >&2
    exit 1
fi

# Build authenticated repo URL if GH_TOKEN is set
AUTH_REPO_URL="$REPO_URL"
if [ -n "${GH_TOKEN:-}" ]; then
    AUTH_REPO_URL=$(echo "$REPO_URL" | sed "s|https://github.com|https://x-access-token:${GH_TOKEN}@github.com|")
elif [ -n "${GITHUB_TOKEN:-}" ]; then
    AUTH_REPO_URL=$(echo "$REPO_URL" | sed "s|https://github.com|https://x-access-token:${GITHUB_TOKEN}@github.com|")
fi

echo "Downloading skill: ${SKILL_NAME} from ${REPO_URL}@${BRANCH}"

# Create a temporary directory for sparse checkout
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# Use git sparse-checkout to download only the specific skill folder
# --depth 1: only latest commit (no history)
# --filter=blob:none: skip downloading blobs until needed
# --sparse: enable sparse-checkout mode
git clone --depth 1 --filter=blob:none --sparse --branch "$BRANCH" \
    "$AUTH_REPO_URL" "$TEMP_DIR" --quiet 2>&1 || {
    echo "Error: Failed to clone ${REPO_URL} (branch: ${BRANCH})" >&2
    exit 1
}

# Configure sparse-checkout to fetch only the skill folder
git -C "$TEMP_DIR" sparse-checkout set "$SKILL_PATH" 2>&1 || {
    echo "Error: Failed to sparse-checkout ${SKILL_PATH}" >&2
    exit 1
}

# Verify the skill directory exists in the checkout
if [ ! -d "$TEMP_DIR/$SKILL_PATH" ]; then
    echo "Error: Skill '${SKILL_NAME}' not found at path '${SKILL_PATH}' in ${REPO_URL}" >&2
    exit 1
fi

# Create target directory and copy skill files
mkdir -p "$TARGET_DIR"
cp -a "$TEMP_DIR/$SKILL_PATH/." "$TARGET_DIR/"

# Make scripts executable
if [ -d "$TARGET_DIR/scripts" ]; then
    find "$TARGET_DIR/scripts" -type f \( -name "*.sh" -o -name "*.bash" \) -exec chmod +x {} \;
fi

echo "Installed skill: ${SKILL_NAME} -> ${TARGET_DIR}"
