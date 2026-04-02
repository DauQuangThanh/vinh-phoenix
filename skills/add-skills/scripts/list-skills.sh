#!/usr/bin/env bash
# list-skills.sh - List available skills from configured remote repositories
#
# Reads nightlife.yaml for catalog URLs (GitHub issues or Azure DevOps repo files),
# fetches repo definitions, and lists available skills from each repository.
#
# Supports:
#   - GitHub issues:     https://github.com/{owner}/{repo}/issues/{number}
#   - Azure DevOps files: https://dev.azure.com/{org}/{project}/_git/{repo}?path={path}&version=GB{branch}
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
    echo "Create one with 'phoenix config-set-url <url1> <url2>' or manually."
    exit 1
fi

urls=()
in_urls=false
while IFS= read -r line; do
    stripped=$(echo "$line" | sed 's/#.*//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    [ -z "$stripped" ] && continue

    if echo "$stripped" | grep -q '^urls:'; then
        in_urls=true
        continue
    fi

    if [ "$in_urls" = true ] && echo "$line" | grep -qE '^[a-zA-Z]'; then
        in_urls=false
        continue
    fi

    if [ "$in_urls" = true ] && echo "$stripped" | grep -q '^- '; then
        url=$(echo "$stripped" | sed 's/^- //')
        urls+=("$url")
    fi
done < "nightlife.yaml"

if [ ${#urls[@]} -eq 0 ]; then
    echo "Error: No 'urls' configured in nightlife.yaml."
    exit 1
fi

# ── Parse YAML body into skill repo entries ─────────────────────────────────────
# Shared parser: reads a YAML body and appends to skill_names/urls/branches/paths arrays.
# Works with or without a 'skills:' header.

parse_skill_repos() {
    local body="$1"

    local in_skills=false
    local has_skills_header=false
    if echo "$body" | grep -q '^skills:'; then
        has_skills_header=true
    elif echo "$body" | grep -qE '^\s*-\s*name:'; then
        in_skills=true
    fi
    local current_name="" current_url="" current_branch="" current_path=""

    while IFS= read -r bline; do
        local stripped
        stripped=$(echo "$bline" | sed 's/#.*//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
        [ -z "$stripped" ] && continue

        if [ "$has_skills_header" = true ] && echo "$stripped" | grep -q '^skills:'; then
            in_skills=true
            continue
        fi

        if [ "$in_skills" = true ] && [ "$has_skills_header" = true ] && echo "$bline" | grep -qE '^[a-zA-Z]'; then
            if [ -n "$current_name" ] && ! echo "$seen_names" | grep -q "|${current_name}|"; then
                seen_names="${seen_names}|${current_name}|"
                skill_names+=("$current_name")
                skill_urls+=("${current_url:-}")
                skill_branches+=("${current_branch:-main}")
                skill_paths+=("${current_path:-skills}")
            fi
            current_name="" current_url="" current_branch="" current_path=""
            in_skills=false
            continue
        fi

        if [ "$in_skills" = true ]; then
            if echo "$stripped" | grep -q '^- '; then
                if [ -n "$current_name" ] && ! echo "$seen_names" | grep -q "|${current_name}|"; then
                    seen_names="${seen_names}|${current_name}|"
                    skill_names+=("$current_name")
                    skill_urls+=("${current_url:-}")
                    skill_branches+=("${current_branch:-main}")
                    skill_paths+=("${current_path:-skills}")
                fi
                current_name="" current_url="" current_branch="" current_path=""

                kv=$(echo "$stripped" | sed 's/^- //')
                key=$(echo "$kv" | cut -d':' -f1 | sed 's/[[:space:]]//g')
                val=$(echo "$kv" | cut -d':' -f2- | sed 's/^[[:space:]]*//')
                case "$key" in
                    name) current_name="$val" ;;
                    url) current_url="$val" ;;
                    branch) current_branch="$val" ;;
                    path) current_path="$val" ;;
                esac
            elif echo "$stripped" | grep -q ':'; then
                key=$(echo "$stripped" | cut -d':' -f1 | sed 's/[[:space:]]//g')
                val=$(echo "$stripped" | cut -d':' -f2- | sed 's/^[[:space:]]*//')
                case "$key" in
                    name) current_name="$val" ;;
                    url) current_url="$val" ;;
                    branch) current_branch="$val" ;;
                    path) current_path="$val" ;;
                esac
            fi
        fi
    done <<< "$body"

    if [ -n "$current_name" ] && ! echo "$seen_names" | grep -q "|${current_name}|"; then
        seen_names="${seen_names}|${current_name}|"
        skill_names+=("$current_name")
        skill_urls+=("${current_url:-}")
        skill_branches+=("${current_branch:-main}")
        skill_paths+=("${current_path:-skills}")
    fi
}

# ── Fetch catalog from each URL ─────────────────────────────────────────────────

skill_names=()
skill_urls=()
skill_branches=()
skill_paths=()
seen_names=""

for catalog_url in "${urls[@]}"; do

    # ── GitHub issue ──
    if echo "$catalog_url" | grep -qE 'github\.com/[^/]+/[^/]+/issues/[0-9]+'; then
        owner=$(echo "$catalog_url" | sed -E 's|.*github\.com/([^/]+)/.*|\1|')
        repo=$(echo "$catalog_url" | sed -E 's|.*github\.com/[^/]+/([^/]+)/.*|\1|')
        number=$(echo "$catalog_url" | sed -E 's|.*/issues/([0-9]+).*|\1|')

        api_url="https://api.github.com/repos/${owner}/${repo}/issues/${number}"

        raw_body=$(gh_curl "$api_url" 2>/dev/null | sed 's/.*"body":"//;s/","[a-z_]*":.*//') || {
            echo "Warning: Failed to fetch GitHub issue $catalog_url"
            continue
        }

        body=$(printf '%b' "$raw_body")
        parse_skill_repos "$body"

    # ── Azure DevOps repo file ──
    # URL format: https://dev.azure.com/{org}/{project}/_git/{repo}?path={path}&version=GB{branch}
    elif echo "$catalog_url" | grep -qE 'dev\.azure\.com/[^/]+/[^/]+/_git/'; then
        ado_org=$(echo "$catalog_url" | sed -E 's|.*dev\.azure\.com/([^/]+)/.*|\1|')
        ado_project=$(echo "$catalog_url" | sed -E 's|.*dev\.azure\.com/[^/]+/([^/]+)/.*|\1|')
        ado_repo=$(echo "$catalog_url" | sed -E 's|.*_git/([^?/]+).*|\1|')

        # Extract path and branch from query params (defaults: path=/, branch=main)
        ado_path="/"
        ado_branch="main"
        if echo "$catalog_url" | grep -qE '[?&]path='; then
            ado_path=$(echo "$catalog_url" | sed -E 's|.*[?&]path=([^&]+).*|\1|' | sed 's/%2F/\//g; s/%20/ /g')
        fi
        if echo "$catalog_url" | grep -qE '[?&]version=GB'; then
            ado_branch=$(echo "$catalog_url" | sed -E 's|.*[?&]version=GB([^&]+).*|\1|')
        fi

        # Fetch file content via Azure DevOps Items API
        ado_api="https://dev.azure.com/${ado_org}/${ado_project}/_apis/git/repositories/${ado_repo}/items?path=${ado_path}&versionDescriptor.version=${ado_branch}&\$format=text&api-version=7.0"

        body=$(ado_curl "$ado_api" 2>/dev/null) || {
            echo "Warning: Failed to fetch Azure DevOps file $catalog_url"
            continue
        }

        parse_skill_repos "$body"

    else
        echo "Warning: Unsupported catalog URL format: $catalog_url"
        echo "  Supported: GitHub issues (github.com/.../issues/N) or Azure DevOps files (dev.azure.com/.../_git/...?path=...)"
        continue
    fi
done

if [ ${#skill_names[@]} -eq 0 ]; then
    echo "No skill repositories configured."
    exit 0
fi

# ── List skills from each repo ──────────────────────────────────────────────────

grand_total=0

for i in "${!skill_names[@]}"; do
    repo_name="${skill_names[$i]}"
    repo_url="${skill_urls[$i]}"
    branch="${skill_branches[$i]}"
    path="${skill_paths[$i]}"

    echo ""
    echo "Repository: ${repo_name} (${repo_url})"

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

        echo "  Total: ${count} skills available"
        grand_total=$((grand_total + count))

    # ── Azure DevOps repo ──
    elif echo "$repo_url" | grep -qE 'dev\.azure\.com/[^/]+/[^/]+/_git/'; then
        ado_org=$(echo "$repo_url" | sed -E 's|.*dev\.azure\.com/([^/]+)/.*|\1|')
        ado_project=$(echo "$repo_url" | sed -E 's|.*dev\.azure\.com/[^/]+/([^/]+)/.*|\1|')
        ado_repo=$(echo "$repo_url" | sed -E 's|.*_git/([^?/]+).*|\1|')

        # Use Items API with recursionLevel=oneLevel to list immediate children
        ado_api="https://dev.azure.com/${ado_org}/${ado_project}/_apis/git/repositories/${ado_repo}/items?scopePath=/${path}&recursionLevel=oneLevel&versionDescriptor.version=${branch}&api-version=7.0"

        listing=$(ado_curl "$ado_api" 2>/dev/null) || {
            echo "  Error: ${path} not found or inaccessible"
            continue
        }

        # Azure DevOps Items API returns {"count":N,"value":[...]}
        # Each item has "path" and "isFolder" fields
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
            # Extract folder name from path (last component)
            item_name=$(basename "$item_path")
            # Skip the root path itself, hidden and internal dirs
            [ "$item_name" = "$path" ] && continue
            case "$item_name" in
                .*|_*) continue ;;
            esac
            echo "  - ${item_name}"
            count=$((count + 1))
        done <<< "$items"

        echo "  Total: ${count} skills available"
        grand_total=$((grand_total + count))

    else
        echo "  Error: Unsupported repo URL format"
        echo "  Supported: github.com or dev.azure.com URLs"
        continue
    fi
done

echo ""
echo "Grand total: ${grand_total} skills across ${#skill_names[@]} repositories"
