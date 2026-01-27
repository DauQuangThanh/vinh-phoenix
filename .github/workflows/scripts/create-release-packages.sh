#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh (workflow-local)
# Build Vinh Phoenix template release archive containing all skills.
# Usage: .github/workflows/scripts/create-release-packages.sh <version>
#   Version argument should include leading 'v'.

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi
NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release package for $NEW_VERSION"

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

# Build single package with all skills
build_skills_package() {
  local base_dir="$GENRELEASES_DIR/phoenix-skills-package"
  echo "Building unified skills package..."
  mkdir -p "$base_dir"
  
  # Copy all skill subdirectories
  if [[ -d skills ]]; then
    cp -r skills "$base_dir/skills"
    echo "Copied all skills -> $base_dir/skills"
  else
    echo "Warning: skills directory not found"
    exit 1
  fi
  
  # Create the zip file with skills/ at the root
  ( cd "$base_dir" && zip -r "../phoenix-skills-${NEW_VERSION}.zip" skills )
  echo "Created $GENRELEASES_DIR/phoenix-skills-${NEW_VERSION}.zip"
}

build_skills_package

echo "Archive in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/phoenix-skills-"${NEW_VERSION}".zip

