#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with all template zip files
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}

gh release create "$VERSION" \
  .genreleases/phoenix-template-copilot-sh-"$VERSION".zip \
  .genreleases/phoenix-template-copilot-ps-"$VERSION".zip \
  .genreleases/phoenix-template-claude-sh-"$VERSION".zip \
  .genreleases/phoenix-template-claude-ps-"$VERSION".zip \
  .genreleases/phoenix-template-gemini-sh-"$VERSION".zip \
  .genreleases/phoenix-template-gemini-ps-"$VERSION".zip \
  .genreleases/phoenix-template-cursor-agent-sh-"$VERSION".zip \
  .genreleases/phoenix-template-cursor-agent-ps-"$VERSION".zip \
  .genreleases/phoenix-template-opencode-sh-"$VERSION".zip \
  .genreleases/phoenix-template-opencode-ps-"$VERSION".zip \
  .genreleases/phoenix-template-qwen-sh-"$VERSION".zip \
  .genreleases/phoenix-template-qwen-ps-"$VERSION".zip \
  .genreleases/phoenix-template-windsurf-sh-"$VERSION".zip \
  .genreleases/phoenix-template-windsurf-ps-"$VERSION".zip \
  .genreleases/phoenix-template-codex-sh-"$VERSION".zip \
  .genreleases/phoenix-template-codex-ps-"$VERSION".zip \
  .genreleases/phoenix-template-kilocode-sh-"$VERSION".zip \
  .genreleases/phoenix-template-kilocode-ps-"$VERSION".zip \
  .genreleases/phoenix-template-auggie-sh-"$VERSION".zip \
  .genreleases/phoenix-template-auggie-ps-"$VERSION".zip \
  .genreleases/phoenix-template-roo-sh-"$VERSION".zip \
  .genreleases/phoenix-template-roo-ps-"$VERSION".zip \
  .genreleases/phoenix-template-codebuddy-sh-"$VERSION".zip \
  .genreleases/phoenix-template-codebuddy-ps-"$VERSION".zip \
  .genreleases/phoenix-template-amp-sh-"$VERSION".zip \
  .genreleases/phoenix-template-amp-ps-"$VERSION".zip \
  .genreleases/phoenix-template-shai-sh-"$VERSION".zip \
  .genreleases/phoenix-template-shai-ps-"$VERSION".zip \
  .genreleases/phoenix-template-q-sh-"$VERSION".zip \
  .genreleases/phoenix-template-q-ps-"$VERSION".zip \
  .genreleases/phoenix-template-bob-sh-"$VERSION".zip \
  .genreleases/phoenix-template-bob-ps-"$VERSION".zip \
  .genreleases/phoenix-template-jules-sh-"$VERSION".zip \
  .genreleases/phoenix-template-jules-ps-"$VERSION".zip \
  .genreleases/phoenix-template-qoder-sh-"$VERSION".zip \
  .genreleases/phoenix-template-qoder-ps-"$VERSION".zip \
  .genreleases/phoenix-template-antigravity-sh-"$VERSION".zip \
  .genreleases/phoenix-template-antigravity-ps-"$VERSION".zip \
  --title "Vinh Phoenix - $VERSION_NO_V" \
  --notes-file release_notes.md
