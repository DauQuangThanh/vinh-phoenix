#!/usr/bin/env bash
# add-agents.sh - Download and install an agent command folder from a GitHub repository
#
# Usage: add-agents.sh <repo_url> <branch> <repo_path> <agent_name> <target_dir> [extension] [args_format]
#
# Downloads the entire agent folder (or single file) recursively.
# Applies extension conversion and args format replacement to .md files.
#
# Arguments:
#   repo_url    - GitHub repository URL (e.g., https://github.com/owner/repo)
#   branch      - Git branch name (e.g., main)
#   repo_path   - Path within repo containing agent commands (e.g., agent-commands)
#   agent_name  - Name of the agent command to download (e.g., specify)
#   target_dir  - Local directory to copy the agent command into
#   extension   - File extension for .md files in target (default: .md)
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

# GitHub API and raw download bases
API_BASE="https://api.github.com/repos/${OWNER}/${REPO}/contents"
RAW_BASE="https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}"
AGENT_PATH="${REPO_PATH}/${AGENT_NAME}"

echo "Downloading agent: ${AGENT_NAME} from ${OWNER}/${REPO}@${BRANCH}"

# Create target directory
mkdir -p "$TARGET_DIR"

# Parse GitHub API JSON array to extract type|name|path tuples
# Shell-native JSON parsing using grep/sed (no python/jq dependency)
parse_github_json() {
    local json="$1"
    # Match each object block and extract type, name, path in order
    echo "$json" | grep -oE '"(type|name|path)"\s*:\s*"[^"]*"' | sed 's/.*"type"\s*:\s*"//;s/.*"name"\s*:\s*"//;s/.*"path"\s*:\s*"//' | sed 's/"$//' | \
    while IFS= read -r val1; do
        IFS= read -r val2 || break
        IFS= read -r val3 || break
        echo "${val1}|${val2}|${val3}"
    done
}

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

    local items
    items=$(parse_github_json "$listing")

    while IFS='|' read -r item_type item_name item_path; do
        [ -z "$item_type" ] && continue

        if [ "$item_type" = "file" ]; then
            local raw_url="${RAW_BASE}/${item_path}"
            local dest_name="$item_name"

            # Apply extension conversion for .md files
            if echo "$dest_name" | grep -q '\.md$'; then
                dest_name=$(echo "$dest_name" | sed "s/\.md$/${EXTENSION}/")
            fi

            local local_file="${local_dir}/${dest_name}"
            curl "${curl_opts[@]}" -o "$local_file" "$raw_url" || {
                echo "Warning: Failed to download ${item_path}" >&2
                continue
            }

            # Replace args format if needed in text files
            if [ "$ARGS_FORMAT" != '$ARGUMENTS' ]; then
                case "$dest_name" in
                    *.md|*.agent.md|*.toml)
                        sed -i.bak "s/\\\$ARGUMENTS/${ARGS_FORMAT}/g" "$local_file" && rm -f "${local_file}.bak"
                        ;;
                esac
            fi

            echo "  Downloaded: ${item_path} -> ${local_file}"
        elif [ "$item_type" = "dir" ]; then
            mkdir -p "${local_dir}/${item_name}"
            download_dir "$item_path" "${local_dir}/${item_name}"
        fi
    done <<< "$items"
}

# Try to access the agent path via API to determine if it's a directory or file
api_url="${API_BASE}/${AGENT_PATH}?ref=${BRANCH}"
response_code=$(curl -s -o /dev/null -w "%{http_code}" -L -H "Accept: application/vnd.github.v3+json" ${AUTH_HEADER:+-H "$AUTH_HEADER"} "$api_url")

if [ "$response_code" = "200" ]; then
    # Path exists - fetch content to check if array (dir) or object (file)
    body=$(curl "${curl_opts[@]}" -H "Accept: application/vnd.github.v3+json" "$api_url")
    first_char=$(echo "$body" | head -c 1)

    if [ "$first_char" = "[" ]; then
        # Directory - download recursively
        echo "Agent is a folder, downloading recursively..."
        download_dir "$AGENT_PATH" "$TARGET_DIR"
    else
        # Single file at exact path - download it
        echo "Agent is a single file, downloading..."
        RAW_URL="${RAW_BASE}/${AGENT_PATH}"
        local_name="${AGENT_NAME}"
        if echo "$local_name" | grep -q '\.md$'; then
            local_name=$(echo "$local_name" | sed "s/\.md$/${EXTENSION}/")
        elif ! echo "$local_name" | grep -q '\.'; then
            local_name="${local_name}${EXTENSION}"
        fi
        TARGET_FILE="${TARGET_DIR}/${local_name}"
        curl "${curl_opts[@]}" -o "$TARGET_FILE" "$RAW_URL" || {
            echo "Error: Failed to download ${RAW_URL}" >&2
            exit 1
        }
        if [ "$ARGS_FORMAT" != '$ARGUMENTS' ]; then
            sed -i.bak "s/\\\$ARGUMENTS/${ARGS_FORMAT}/g" "$TARGET_FILE" && rm -f "${TARGET_FILE}.bak"
        fi
        echo "  Downloaded: ${AGENT_PATH} -> ${TARGET_FILE}"
    fi
else
    # Path not found as-is, try with .md extension
    echo "Agent folder not found, trying as single .md file..."
    RAW_URL="${RAW_BASE}/${AGENT_PATH}.md"
    CONTENT=$(curl "${curl_opts[@]}" "$RAW_URL") || {
        echo "Error: Failed to download ${RAW_URL}" >&2
        exit 1
    }

    if [ "$ARGS_FORMAT" != '$ARGUMENTS' ]; then
        CONTENT=$(echo "$CONTENT" | sed "s/\\\$ARGUMENTS/${ARGS_FORMAT}/g")
    fi

    TARGET_FILE="${TARGET_DIR}/${AGENT_NAME}${EXTENSION}"
    echo "$CONTENT" > "$TARGET_FILE"
    echo "  Downloaded: ${AGENT_PATH}.md -> ${TARGET_FILE}"
fi

echo "Installed: ${AGENT_NAME} -> ${TARGET_DIR}"
