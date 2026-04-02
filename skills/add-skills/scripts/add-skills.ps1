# add-skills.ps1 - Download and install a skill from a GitHub repository using git
#
# Usage: add-skills.ps1 <repo_url> <branch> <repo_path> <skill_name> <target_dir>
#
# Uses git sparse-checkout to download only the specific skill folder,
# avoiding recursive GitHub API calls and rate limits.

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$RepoUrl,

    [Parameter(Mandatory=$true, Position=1)]
    [string]$Branch,

    [Parameter(Mandatory=$true, Position=2)]
    [string]$RepoPath,

    [Parameter(Mandatory=$true, Position=3)]
    [string]$SkillName,

    [Parameter(Mandatory=$true, Position=4)]
    [string]$TargetDir
)

$ErrorActionPreference = "Stop"

$SkillPath = "$RepoPath/$SkillName"

# Ensure git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git is required but not found. Install git and try again."
    exit 1
}

# Build authenticated repo URL if GH_TOKEN is set
$AuthRepoUrl = $RepoUrl
if ($env:GH_TOKEN) {
    $AuthRepoUrl = $RepoUrl -replace 'https://github.com', "https://x-access-token:$($env:GH_TOKEN)@github.com"
} elseif ($env:GITHUB_TOKEN) {
    $AuthRepoUrl = $RepoUrl -replace 'https://github.com', "https://x-access-token:$($env:GITHUB_TOKEN)@github.com"
}

Write-Host "Downloading skill: $SkillName from $RepoUrl@$Branch"

# Create a temporary directory for sparse checkout
$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("phoenix-skill-" + [System.Guid]::NewGuid().ToString("N").Substring(0, 8))

try {
    # Use git sparse-checkout to download only the specific skill folder
    # --depth 1: only latest commit (no history)
    # --filter=blob:none: skip downloading blobs until needed
    # --sparse: enable sparse-checkout mode
    $cloneOutput = git clone --depth 1 --filter=blob:none --sparse --branch $Branch `
        $AuthRepoUrl $TempDir --quiet 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to clone ${RepoUrl} (branch: ${Branch}): $cloneOutput"
        exit 1
    }

    # Configure sparse-checkout to fetch only the skill folder
    $sparseOutput = git -C $TempDir sparse-checkout set $SkillPath 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to sparse-checkout ${SkillPath}: $sparseOutput"
        exit 1
    }

    # Verify the skill directory exists in the checkout
    $SkillFullPath = Join-Path $TempDir $SkillPath
    if (-not (Test-Path $SkillFullPath)) {
        Write-Error "Skill '$SkillName' not found at path '$SkillPath' in $RepoUrl"
        exit 1
    }

    # Create target directory and copy skill files
    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    }
    Copy-Item -Path "$SkillFullPath\*" -Destination $TargetDir -Recurse -Force

    Write-Host "Installed skill: $SkillName -> $TargetDir"
} finally {
    # Clean up temporary directory
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
