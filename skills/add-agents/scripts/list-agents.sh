#!/usr/bin/env bash
# list-agents.sh - List available agent commands from configured remote repositories
#
# Reads nightlife.yaml for GitHub issue URLs, fetches repo definitions,
# and lists available agent commands from each repository.
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
    # Skip comments and empty lines
    stripped=$(echo "$line" | sed 's/#.*//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    [ -z "$stripped" ] && continue

    if echo "$stripped" | grep -q '^urls:'; then
        in_urls=true
        continue
    fi

    # If we hit a new top-level key, stop
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

# Fetch agent repo definitions from GitHub issues
agent_names=()
agent_urls=()
agent_branches=()
agent_paths=()
seen_names=""

for issue_url in "${urls[@]}"; do
    # Parse owner/repo/number from issue URL
    if ! echo "$issue_url" | grep -qE 'github\.com/[^/]+/[^/]+/issues/[0-9]+'; then
        echo "Warning: Invalid issue URL: $issue_url"
        continue
    fi

    owner=$(echo "$issue_url" | sed -E 's|.*github\.com/([^/]+)/.*|\1|')
    repo=$(echo "$issue_url" | sed -E 's|.*github\.com/[^/]+/([^/]+)/.*|\1|')
    number=$(echo "$issue_url" | sed -E 's|.*/issues/([0-9]+).*|\1|')

    api_url="https://api.github.com/repos/${owner}/${repo}/issues/${number}"

    body=$(curl "${curl_opts[@]}" "$api_url" 2>/dev/null | grep -o '"body":"[^"]*"' | sed 's/"body":"//;s/"$//') || {
        echo "Warning: Failed to fetch $issue_url"
        continue
    }

    # Unescape \r\n to actual newlines
    body=$(echo "$body" | sed 's/\\r\\n/\n/g' | sed 's/\\n/\n/g')

    # Parse agents section from issue body
    in_agents=false
    current_name="" current_url="" current_branch="" current_path=""

    while IFS= read -r bline; do
        stripped=$(echo "$bline" | sed 's/#.*//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
        [ -z "$stripped" ] && continue

        if echo "$stripped" | grep -q '^agents:'; then
            in_agents=true
            continue
        fi

        # New top-level key ends agents section
        if [ "$in_agents" = true ] && echo "$bline" | grep -qE '^[a-zA-Z]'; then
            # Save last item if any
            if [ -n "$current_name" ] && ! echo "$seen_names" | grep -q "|${current_name}|"; then
                seen_names="${seen_names}|${current_name}|"
                agent_names+=("$current_name")
                agent_urls+=("${current_url:-}")
                agent_branches+=("${current_branch:-main}")
                agent_paths+=("${current_path:-agent-commands}")
            fi
            current_name="" current_url="" current_branch="" current_path=""
            in_agents=false
            continue
        fi

        if [ "$in_agents" = true ]; then
            if echo "$stripped" | grep -q '^- '; then
                # Save previous item
                if [ -n "$current_name" ] && ! echo "$seen_names" | grep -q "|${current_name}|"; then
                    seen_names="${seen_names}|${current_name}|"
                    agent_names+=("$current_name")
                    agent_urls+=("${current_url:-}")
                    agent_branches+=("${current_branch:-main}")
                    agent_paths+=("${current_path:-agent-commands}")
                fi
                current_name="" current_url="" current_branch="" current_path=""

                # Parse first key-value on the '- ' line
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

    # Save last item
    if [ -n "$current_name" ] && ! echo "$seen_names" | grep -q "|${current_name}|"; then
        seen_names="${seen_names}|${current_name}|"
        agent_names+=("$current_name")
        agent_urls+=("${current_url:-}")
        agent_branches+=("${current_branch:-main}")
        agent_paths+=("${current_path:-agent-commands}")
    fi
done

if [ ${#agent_names[@]} -eq 0 ]; then
    echo "No agent repositories configured."
    exit 0
fi

# List agents from each repo
grand_total=0

for i in "${!agent_names[@]}"; do
    repo_name="${agent_names[$i]}"
    repo_url="${agent_urls[$i]}"
    branch="${agent_branches[$i]}"
    path="${agent_paths[$i]}"

    if ! echo "$repo_url" | grep -qE 'github\.com/[^/]+/[^/]+'; then
        echo ""
        echo "${repo_name}: Invalid repo URL"
        continue
    fi

    owner=$(echo "$repo_url" | sed -E 's|.*github\.com/([^/]+)/.*|\1|')
    repo=$(echo "$repo_url" | sed -E 's|.*github\.com/[^/]+/([^/]+?)(.git)?$|\1|')

    api_url="https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}"

    echo ""
    echo "Repository: ${repo_name} (${repo_url})"

    listing=$(curl "${curl_opts[@]}" "$api_url" 2>/dev/null) || {
        echo "  Error: ${path} not found or inaccessible"
        continue
    }

    # Extract names of .md files and directories, skip hidden/template items
    count=0
    while IFS= read -r name; do
        [ -z "$name" ] && continue
        # Skip hidden files and templates
        case "$name" in
            .*|_*|*template*|*Template*) continue ;;
        esac
        # Remove .md extension for display
        display_name=$(echo "$name" | sed 's/\.md$//')
        echo "  - ${display_name}"
        count=$((count + 1))
    done < <(echo "$listing" | grep -oE '"name"\s*:\s*"[^"]*"' | sed 's/"name"\s*:\s*"//;s/"$//' | sort)

    echo "  Total: ${count} agent commands available"
    grand_total=$((grand_total + count))
done

echo ""
echo "Grand total: ${grand_total} agent commands across ${#agent_names[@]} repositories"
