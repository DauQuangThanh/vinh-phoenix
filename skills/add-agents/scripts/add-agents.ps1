# add-agents.ps1 - Download and install an agent from a git repository
#
# Usage: add-agents.ps1 <repo_url> <branch> <repo_path> <agent_name> <target_dir>
#
# Supports GitHub and Azure DevOps repositories.
# Uses git sparse-checkout to download only the specific agent folder,
# avoiding recursive API calls and rate limits.

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$RepoUrl,

    [Parameter(Mandatory=$true, Position=1)]
    [string]$Branch,

    [Parameter(Mandatory=$true, Position=2)]
    [string]$RepoPath,

    [Parameter(Mandatory=$true, Position=3)]
    [string]$AgentName,

    [Parameter(Mandatory=$true, Position=4)]
    [string]$TargetDir
)

$ErrorActionPreference = "Stop"

$AgentPath = "$RepoPath/$AgentName"

# Ensure git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git is required but not found. Install git and try again."
    exit 1
}

# Build authenticated repo URL based on provider (used as fallback for private repos)
$AuthRepoUrl = $null
if ($RepoUrl -match 'github\.com') {
    if ($env:GH_TOKEN) {
        $AuthRepoUrl = $RepoUrl -replace 'https://github.com', "https://x-access-token:$($env:GH_TOKEN)@github.com"
    } elseif ($env:GITHUB_TOKEN) {
        $AuthRepoUrl = $RepoUrl -replace 'https://github.com', "https://x-access-token:$($env:GITHUB_TOKEN)@github.com"
    }
} elseif ($RepoUrl -match 'dev\.azure\.com') {
    $adoPat = if ($env:AZURE_DEVOPS_PAT) { $env:AZURE_DEVOPS_PAT } elseif ($env:ADO_TOKEN) { $env:ADO_TOKEN } else { $null }
    if ($adoPat) {
        $AuthRepoUrl = $RepoUrl -replace 'https://dev\.azure\.com', "https://pat:${adoPat}@dev.azure.com"
    }
}

Write-Host "Downloading agent: $AgentName from $RepoUrl@$Branch"

# Create a temporary directory for sparse checkout
$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("phoenix-agent-" + [System.Guid]::NewGuid().ToString("N").Substring(0, 8))

try {
    # Clone strategy: try public (no auth) first, fall back to authenticated if available
    $cloneOk = $false
    $env:GIT_TERMINAL_PROMPT = "0"

    # Attempt 1: clone without auth (works for public repos)
    $cloneOutput = git clone --depth 1 --filter=blob:none --sparse --branch $Branch `
        $RepoUrl $TempDir --quiet 2>&1
    if ($LASTEXITCODE -eq 0) {
        $cloneOk = $true
    }

    # Attempt 2: clone with auth token (for private repos)
    if (-not $cloneOk -and $AuthRepoUrl) {
        if (Test-Path $TempDir) {
            Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
        }
        $cloneOutput = git clone --depth 1 --filter=blob:none --sparse --branch $Branch `
            $AuthRepoUrl $TempDir --quiet 2>&1
        if ($LASTEXITCODE -eq 0) {
            $cloneOk = $true
        }
    }

    if (-not $cloneOk) {
        $hint = ""
        if (-not $AuthRepoUrl) {
            $hint = "`nHint: If this is a private repo, set GH_TOKEN/GITHUB_TOKEN (GitHub) or AZURE_DEVOPS_PAT/ADO_TOKEN (Azure DevOps)"
        }
        Write-Error "Failed to clone ${RepoUrl} (branch: ${Branch}): $cloneOutput$hint"
        exit 1
    }

    # Configure sparse-checkout to fetch only the agent folder
    $sparseOutput = git -C $TempDir sparse-checkout set $AgentPath 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to sparse-checkout ${AgentPath}: $sparseOutput"
        exit 1
    }

    # Verify the agent directory exists in the checkout
    $AgentFullPath = Join-Path $TempDir $AgentPath
    if (-not (Test-Path $AgentFullPath)) {
        Write-Error "Agent '$AgentName' not found at path '$AgentPath' in $RepoUrl"
        exit 1
    }

    # Create target directory and copy agent files
    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    }
    Copy-Item -Path "$AgentFullPath\*" -Destination $TargetDir -Recurse -Force

    Write-Host "Installed agent: $AgentName -> $TargetDir"
} finally {
    # Clean up temporary directory
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
