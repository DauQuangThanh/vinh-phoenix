#!/usr/bin/env bash
# list-agents.sh - List available agents from configured remote repositories
#
# Reads nightlife.yaml for agent repository definitions (url, branch, path),
# then lists available agents from each repository.
#
# Supports:
#   - GitHub repos:      https://github.com/{owner}/{repo}
#   - Azure DevOps repos: https://dev.azure.com/{org}/{project}/_git/{repo}
#
# No arguments required. Must be run from the project root where nightlife.yaml exists.

set -euo pipefail

# ── Auth ────────────────────────────────────────────────────────────────────────

# GitHub auth
GH_AUTH_HEADER=""
if [ -n "${GH_TOKEN:-}" ]; then
    GH_AUTH_HEADER="Authorization: Bearer $GH_TOKEN"
elif [ -n "${GITHUB_TOKEN:-}" ]; then
    GH_AUTH_HEADER="Authorization: Bearer $GITHUB_TOKEN"
fi

# Azure DevOps auth (Basic auth with PAT)
ADO_AUTH_HEADER=""
if [ -n "${AZURE_DEVOPS_PAT:-}" ]; then
    ADO_AUTH_HEADER="Authorization: Basic $(printf ":%s" "$AZURE_DEVOPS_PAT" | base64 | tr -d '\n')"
elif [ -n "${ADO_TOKEN:-}" ]; then
    ADO_AUTH_HEADER="Authorization: Basic $(printf ":%s" "$ADO_TOKEN" | base64 | tr -d '\n')"
fi

# Curl helper for GitHub API
gh_curl() {
    local opts=(-s -f -L -H "Accept: application/vnd.github.v3+json" -H "User-Agent: phoenix-cli")
    [ -n "$GH_AUTH_HEADER" ] && opts+=(-H "$GH_AUTH_HEADER")
    curl "${opts[@]}" "$@"
}

# Curl helper for Azure DevOps API
ado_curl() {
    local opts=(-s -f -L -H "Accept: application/json" -H "User-Agent: phoenix-cli")
    [ -n "$ADO_AUTH_HEADER" ] && opts+=(-H "$ADO_AUTH_HEADER")
    curl "${opts[@]}" "$@"
}

# ── Parse nightlife.yaml ────────────────────────────────────────────────────────

if [ ! -f "nightlife.yaml" ]; then
    echo "Error: nightlife.yaml not found in current directory."
    echo "Create one with 'phoenix init' or manually."
    exit 1
fi

# Parse agents section: each entry has name, url, branch, path
agent_names=()
agent_urls=()
agent_branches=()
agent_paths=()

in_agents=false
current_name="" current_url="" current_branch="" current_path=""

while IFS= read -r line; do
    stripped=$(echo "$line" | sed 's/#.*//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    [ -z "$stripped" ] && continue

    # Detect section headers
    if echo "$stripped" | grep -q '^agents:'; then
        in_agents=true
        current_name="" current_url="" current_branch="" current_path=""
        continue
    fi

    # Exit agents section on new top-level key
    if [ "$in_agents" = true ] && echo "$line" | grep -qE '^[a-zA-Z]'; then
        # Flush last entry
        if [ -n "$current_url" ]; then
            agent_names+=("${current_name:-}")
            agent_urls+=("$current_url")
            agent_branches+=("${current_branch:-main}")
            agent_paths+=("${current_path:-agents}")
        fi
        in_agents=false
        current_name="" current_url="" current_branch="" current_path=""
        continue
    fi

    if [ "$in_agents" = true ]; then
        # New list item
        if echo "$stripped" | grep -q '^- '; then
            # Flush previous entry
            if [ -n "$current_url" ]; then
                agent_names+=("${current_name:-}")
                agent_urls+=("$current_url")
                agent_branches+=("${current_branch:-main}")
                agent_paths+=("${current_path:-agents}")
            fi
            current_name="" current_url="" current_branch="" current_path=""

            kv=$(echo "$stripped" | sed 's/^- //')
            key=$(echo "$kv" | cut -d':' -f1 | sed 's/[[:space:]]//g')
            val=$(echo "$kv" | cut -d':' -f2- | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
            case "$key" in
                name) current_name="$val" ;;
                url) current_url="$val" ;;
                branch) current_branch="$val" ;;
                path) current_path="$val" ;;
            esac
        elif echo "$stripped" | grep -q ':'; then
            key=$(echo "$stripped" | cut -d':' -f1 | sed 's/[[:space:]]//g')
            val=$(echo "$stripped" | cut -d':' -f2- | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
            case "$key" in
                name) current_name="$val" ;;
                url) current_url="$val" ;;
                branch) current_branch="$val" ;;
                path) current_path="$val" ;;
            esac
        fi
    fi
done < "nightlife.yaml"

# Flush last entry if file ends inside agents section
if [ "$in_agents" = true ] && [ -n "$current_url" ]; then
    agent_names+=("${current_name:-}")
    agent_urls+=("$current_url")
    agent_branches+=("${current_branch:-main}")
    agent_paths+=("${current_path:-agents}")
fi

if [ ${#agent_urls[@]} -eq 0 ]; then
    echo "No agent repositories configured in nightlife.yaml."
    exit 0
fi

# ── List agents from each repo ──────────────────────────────────────────────────

grand_total=0

for i in "${!agent_urls[@]}"; do
    repo_name="${agent_names[$i]}"
    repo_url="${agent_urls[$i]}"
    branch="${agent_branches[$i]}"
    path="${agent_paths[$i]}"

    echo ""
    if [ -n "$repo_name" ]; then
        echo "Repository: ${repo_name} (${repo_url}, branch: ${branch}, path: ${path})"
    else
        echo "Repository: ${repo_url} (branch: ${branch}, path: ${path})"
    fi

    # ── GitHub repo ──
    if echo "$repo_url" | grep -qE 'github\.com/[^/]+/[^/]+'; then
        owner=$(echo "$repo_url" | sed -E 's|.*github\.com/([^/]+)/.*|\1|')
        repo=$(echo "$repo_url" | sed -E 's|.*github\.com/[^/]+/([^/.]+).*|\1|')

        api_url="https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}"

        listing=$(gh_curl "$api_url" 2>/dev/null) || {
            echo "  Error: ${path} not found or inaccessible"
            continue
        }

        count=0
        items=$(echo "$listing" | grep -o '"name": *"[^"]*"\|"type": *"[^"]*"' | \
        sed 's/"name": *"//;s/"type": *"//;s/"$//' | \
        while IFS= read -r name; do
            IFS= read -r type || break
            echo "${type}|${name}"
        done)

        while IFS='|' read -r item_type item_name; do
            [ -z "$item_type" ] && continue
            [ "$item_type" != "dir" ] && continue
            case "$item_name" in
                .*|_*) continue ;;
            esac
            echo "  - ${item_name}"
            count=$((count + 1))
        done <<< "$items"

        echo "  Total: ${count} agents available"
        grand_total=$((grand_total + count))

    # ── Azure DevOps repo ──
    elif echo "$repo_url" | grep -qE 'dev\.azure\.com/[^/]+/[^/]+/_git/'; then
        ado_org=$(echo "$repo_url" | sed -E 's|.*dev\.azure\.com/([^/]+)/.*|\1|')
        ado_project=$(echo "$repo_url" | sed -E 's|.*dev\.azure\.com/[^/]+/([^/]+)/.*|\1|')
        ado_repo=$(echo "$repo_url" | sed -E 's|.*_git/([^?/]+).*|\1|')

        ado_api="https://dev.azure.com/${ado_org}/${ado_project}/_apis/git/repositories/${ado_repo}/items?scopePath=/${path}&recursionLevel=oneLevel&versionDescriptor.version=${branch}&api-version=7.0"

        listing=$(ado_curl "$ado_api" 2>/dev/null) || {
            echo "  Error: ${path} not found or inaccessible"
            continue
        }

        count=0
        items=$(echo "$listing" | grep -o '"path": *"[^"]*"\|"isFolder": *[a-z]*' | \
        sed 's/"path": *"//;s/"isFolder": *//;s/"$//' | \
        while IFS= read -r item_path; do
            IFS= read -r is_folder || break
            echo "${is_folder}|${item_path}"
        done)

        while IFS='|' read -r is_folder item_path; do
            [ -z "$is_folder" ] && continue
            [ "$is_folder" != "true" ] && continue
            item_name=$(basename "$item_path")
            [ "$item_name" = "$path" ] && continue
            case "$item_name" in
                .*|_*) continue ;;
            esac
            echo "  - ${item_name}"
            count=$((count + 1))
        done <<< "$items"

        echo "  Total: ${count} agents available"
        grand_total=$((grand_total + count))

    else
        echo "  Error: Unsupported repo URL format"
        echo "  Supported: github.com or dev.azure.com URLs"
        continue
    fi
done

echo ""
echo "Grand total: ${grand_total} agents across ${#agent_urls[@]} repositories"
