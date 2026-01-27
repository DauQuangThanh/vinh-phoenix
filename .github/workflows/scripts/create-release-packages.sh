#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh (workflow-local)
# Build Vinh Phoenix template release archives for each supported AI assistant.
# Both bash and PowerShell script versions are included in each package.
# Usage: .github/workflows/scripts/create-release-packages.sh <version>
#   Version argument should include leading 'v'.
#   Optionally set AGENTS and/or SCRIPTS env vars to limit what gets built.
#     AGENTS  : space or comma separated subset of: claude gemini copilot cursor-agent qwen opencode windsurf codex amp shai bob (default: all)
#     SCRIPTS : space or comma separated subset of: sh ps (default: both)
#   Examples:
#     AGENTS=claude SCRIPTS=sh $0 v0.2.0
#     AGENTS="copilot,gemini" $0 v0.2.0
#     SCRIPTS=ps $0 v0.2.0

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi
NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release packages for $NEW_VERSION"

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

rewrite_paths() {
  # Path rewriting is no longer needed - skills contain their own paths
  cat
}

# Commands are now distributed as part of skills - no separate generate_commands function needed

generate_skills() {
  local agent=$1 output_dir=$2
  [[ -d skills ]] || return 0
  mkdir -p "$output_dir"
  
  # Copy all skill subdirectories
  for skill_dir in skills/*; do
    [[ -d "$skill_dir" ]] || continue
    local skill_name=$(basename "$skill_dir")
    cp -r "$skill_dir" "$output_dir/$skill_name"
  done
  
  echo "Copied skills -> $output_dir"
}

build_variant() {
  local agent=$1 script=$2
  local base_dir="$GENRELEASES_DIR/sdd-${agent}-package-${script}"
  echo "Building $agent ($script) package..."
  mkdir -p "$base_dir"
  
  # Copy skills - all templates and scripts are now within individual skill folders
  
  # NOTE: We substitute {ARGS} internally. Outward tokens differ intentionally:
  #   * Markdown/prompt (claude, copilot, cursor-agent, opencode): $ARGUMENTS
  #   * TOML (gemini, qwen): {{args}}
  # This keeps formats readable without extra abstraction.

  case $agent in
    claude)
      generate_skills claude "$base_dir/.claude/skills" ;;
    gemini)
      generate_skills gemini "$base_dir/.gemini/extensions"
      [[ -f agent_templates/gemini/GEMINI.md ]] && cp agent_templates/gemini/GEMINI.md "$base_dir/GEMINI.md" ;;
    copilot)
      generate_skills copilot "$base_dir/.github/skills" ;;
    cursor-agent)
      generate_skills cursor-agent "$base_dir/.cursor/rules" ;;
    qwen)
      generate_skills qwen "$base_dir/.qwen/skills"
      [[ -f agent_templates/qwen/QWEN.md ]] && cp agent_templates/qwen/QWEN.md "$base_dir/QWEN.md" ;;
    opencode)
      generate_skills opencode "$base_dir/.opencode/skill" ;;
    windsurf)
      generate_skills windsurf "$base_dir/.windsurf/skills" ;;
    codex)
      generate_skills codex "$base_dir/.codex/skills" ;;
    kilocode)
      generate_skills kilocode "$base_dir/.kilocode/skills" ;;
    auggie)
      generate_skills auggie "$base_dir/.augment/rules" ;;
    roo)
      generate_skills roo "$base_dir/.roo/skills" ;;
    codebuddy)
      generate_skills codebuddy "$base_dir/.codebuddy/skills" ;;
    amp)
      generate_skills amp "$base_dir/.agents/skills" ;;
    shai)
      generate_skills shai "$base_dir/.shai/commands" ;;
    q)
      generate_skills q "$base_dir/.amazonq/cli-agents" ;;
    bob)
      generate_skills bob "$base_dir/.bob/skills" ;;
    jules)
      generate_skills jules "$base_dir/skills" ;;
    qoder)
      generate_skills qoder "$base_dir/.qoder/skills" ;;
    antigravity)
      generate_skills antigravity "$base_dir/.agent/skills" ;;
  esac
  ( cd "$base_dir" && zip -r "../phoenix-template-${agent}-${script}-${NEW_VERSION}.zip" . )
  echo "Created $GENRELEASES_DIR/phoenix-template-${agent}-${script}-${NEW_VERSION}.zip"
}

# Determine agent list
ALL_AGENTS=(claude gemini copilot cursor-agent qwen opencode windsurf codex kilocode auggie roo codebuddy amp shai q bob jules qoder antigravity)
ALL_SCRIPTS=(sh ps)

norm_list() {
  # convert comma+space separated -> line separated unique while preserving order of first occurrence
  tr ',\n' '  ' | awk '{for(i=1;i<=NF;i++){if(!seen[$i]++){printf((out?"\n":"") $i);out=1}}}END{printf("\n")}'
}

validate_subset() {
  local type=$1; shift; local -n allowed=$1; shift; local items=("$@")
  local invalid=0
  for it in "${items[@]}"; do
    local found=0
    for a in "${allowed[@]}"; do [[ $it == "$a" ]] && { found=1; break; }; done
    if [[ $found -eq 0 ]]; then
      echo "Error: unknown $type '$it' (allowed: ${allowed[*]})" >&2
      invalid=1
    fi
  done
  return $invalid
}

if [[ -n ${AGENTS:-} ]]; then
  mapfile -t AGENT_LIST < <(printf '%s' "$AGENTS" | norm_list)
  validate_subset agent ALL_AGENTS "${AGENT_LIST[@]}" || exit 1
else
  AGENT_LIST=("${ALL_AGENTS[@]}")
fi

if [[ -n ${SCRIPTS:-} ]]; then
  mapfile -t SCRIPT_LIST < <(printf '%s' "$SCRIPTS" | norm_list)
  validate_subset script ALL_SCRIPTS "${SCRIPT_LIST[@]}" || exit 1
else
  SCRIPT_LIST=("${ALL_SCRIPTS[@]}")
fi

echo "Agents: ${AGENT_LIST[*]}"
echo "Scripts: ${SCRIPT_LIST[*]}"

for agent in "${AGENT_LIST[@]}"; do
  for script in "${SCRIPT_LIST[@]}"; do
    build_variant "$agent" "$script"
  done
done

echo "Archives in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/phoenix-template-*-"${NEW_VERSION}".zip

