#!/usr/bin/env bash
# add-agents.sh - Download and install an agent command from a GitHub repository
#
# Usage: add-agents.sh <repo_url> <branch> <repo_path> <agent_name> <target_dir> [extension] [args_format]
#
# Arguments:
#   repo_url    - GitHub repository URL (e.g., https://github.com/owner/repo)
#   branch      - Git branch name (e.g., main)
#   repo_path   - Path within repo containing agent commands (e.g., agent-commands)
#   agent_name  - Name of the agent command to download (e.g., specify)
#   target_dir  - Local directory to copy the agent command into
#   extension   - File extension for the target (default: .md)
#   args_format - Args placeholder format for the target agent (default: $ARGUMENTS)

set -euo pipefail

REPO_URL="${1:?Usage: add-agents.sh <repo_url> <branch> <repo_path> <agent_name> <target_dir> [extension] [args_format]}"
BRANCH="${2:?Missing branch}"
REPO_PATH="${3:?Missing repo_path}"
AGENT_NAME="${4:?Missing agent_name}"
TARGET_DIR="${5:?Missing target_dir}"
EXTENSION="${6:-.md}"
ARGS_FORMAT="${7:-\$ARGUMENTS}"

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

# Download the agent command file
SOURCE_FILE="${REPO_PATH}/${AGENT_NAME}.md"
RAW_URL="https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/${SOURCE_FILE}"

echo "Downloading: ${SOURCE_FILE} from ${OWNER}/${REPO}@${BRANCH}"

CONTENT=$(curl "${curl_opts[@]}" "$RAW_URL") || {
    echo "Error: Failed to download ${RAW_URL}" >&2
    exit 1
}

# Replace args format if needed
# Source files use $ARGUMENTS by default
if [ "$ARGS_FORMAT" != '$ARGUMENTS' ]; then
    CONTENT=$(echo "$CONTENT" | sed "s/\\\$ARGUMENTS/${ARGS_FORMAT}/g")
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Write file with correct extension
TARGET_FILE="${TARGET_DIR}/${AGENT_NAME}${EXTENSION}"
echo "$CONTENT" > "$TARGET_FILE"

echo "Installed: ${AGENT_NAME} -> ${TARGET_FILE}"
