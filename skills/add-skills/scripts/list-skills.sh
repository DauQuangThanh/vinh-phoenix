#!/usr/bin/env bash
# list-skills.sh - List available skills from configured remote repositories
#
# Reads nightlife.yaml for GitHub issue URLs, fetches repo definitions,
# and lists available skills from each repository.
#
# No arguments required. Must be run from the project root where nightlife.yaml exists.

set -euo pipefail

# Build auth header if GH_TOKEN is set
AUTH_HEADER=""
if [ -n "${GH_TOKEN:-}" ]; then
    AUTH_HEADER="Authorization: Bearer $GH_TOKEN"
elif [ -n "${GITHUB_TOKEN:-}" ]; then
    AUTH_HEADER="Authorization: Bearer $GITHUB_TOKEN"
fi

curl_opts=(-s -f -L -H "Accept: application/vnd.github.v3+json" -H "User-Agent: phoenix-cli")
if [ -n "$AUTH_HEADER" ]; then
    curl_opts+=(-H "$AUTH_HEADER")
fi

# Check nightlife.yaml exists
if [ ! -f "nightlife.yaml" ]; then
    echo "Error: nightlife.yaml not found in current directory."
    echo "Create one with 'phoenix config-set-url <url1> <url2>' or manually."
    exit 1
fi

# Parse URLs from nightlife.yaml (extract lines under 'urls:' that start with '- ')
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

# Fetch skill repo definitions from GitHub issues
skill_names=()
skill_urls=()
skill_branches=()
skill_paths=()
seen_names=""

for issue_url in "${urls[@]}"; do
    if ! echo "$issue_url" | grep -qE 'github\.com/[^/]+/[^/]+/issues/[0-9]+'; then
        echo "Warning: Invalid issue URL: $issue_url"
        continue
    fi

    owner=$(echo "$issue_url" | sed -E 's|.*github\.com/([^/]+)/.*|\1|')
    repo=$(echo "$issue_url" | sed -E 's|.*github\.com/[^/]+/([^/]+)/.*|\1|')
    number=$(echo "$issue_url" | sed -E 's|.*/issues/([0-9]+).*|\1|')

    api_url="https://api.github.com/repos/${owner}/${repo}/issues/${number}"

    raw_body=$(curl "${curl_opts[@]}" "$api_url" 2>/dev/null | sed 's/.*"body":"//;s/","[a-z_]*":.*//') || {
        echo "Warning: Failed to fetch $issue_url"
        continue
    }

    # Unescape \n to actual newlines
    body=$(printf '%b' "$raw_body")

    # Parse skills section from issue body
    in_skills=false
    current_name="" current_url="" current_branch="" current_path=""

    while IFS= read -r bline; do
        stripped=$(echo "$bline" | sed 's/#.*//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
        [ -z "$stripped" ] && continue

        if echo "$stripped" | grep -q '^skills:'; then
            in_skills=true
            continue
        fi

        if [ "$in_skills" = true ] && echo "$bline" | grep -qE '^[a-zA-Z]'; then
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
done

if [ ${#skill_names[@]} -eq 0 ]; then
    echo "No skill repositories configured."
    exit 0
fi

# List skills from each repo
grand_total=0

for i in "${!skill_names[@]}"; do
    repo_name="${skill_names[$i]}"
    repo_url="${skill_urls[$i]}"
    branch="${skill_branches[$i]}"
    path="${skill_paths[$i]}"

    if ! echo "$repo_url" | grep -qE 'github\.com/[^/]+/[^/]+'; then
        echo ""
        echo "${repo_name}: Invalid repo URL"
        continue
    fi

    owner=$(echo "$repo_url" | sed -E 's|.*github\.com/([^/]+)/.*|\1|')
    repo=$(echo "$repo_url" | sed -E 's|.*github\.com/[^/]+/([^/.]+).*|\1|')

    api_url="https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}"

    echo ""
    echo "Repository: ${repo_name} (${repo_url})"

    listing=$(curl "${curl_opts[@]}" "$api_url" 2>/dev/null) || {
        echo "  Error: ${path} not found or inaccessible"
        continue
    }

    # Extract directory names only (skills are folders), skip hidden items
    count=0
    # Get name|type pairs from pretty-printed JSON (name appears before type per object)
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
done

echo ""
echo "Grand total: ${grand_total} skills across ${#skill_names[@]} repositories"
