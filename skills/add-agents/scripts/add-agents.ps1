# add-agents.ps1 - Download and install an agent command from a GitHub repository
#
# Usage: add-agents.ps1 <repo_url> <branch> <repo_path> <agent_name> <target_dir> [extension] [args_format]

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
    [string]$TargetDir,

    [Parameter(Position=5)]
    [string]$Extension = ".md",

    [Parameter(Position=6)]
    [string]$ArgsFormat = '$ARGUMENTS'
)

$ErrorActionPreference = "Stop"

# Parse owner/repo from URL
if ($RepoUrl -match "https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?$") {
    $Owner = $Matches[1]
    $Repo = $Matches[2]
} else {
    Write-Error "Invalid GitHub repo URL: $RepoUrl"
    exit 1
}

# Build headers
$Headers = @{
    "Accept" = "application/vnd.github.v3+json"
    "User-Agent" = "phoenix-cli"
}
if ($env:GH_TOKEN) {
    $Headers["Authorization"] = "Bearer $env:GH_TOKEN"
} elseif ($env:GITHUB_TOKEN) {
    $Headers["Authorization"] = "Bearer $env:GITHUB_TOKEN"
}

# Download the agent command file
$SourceFile = "$RepoPath/$AgentName.md"
$RawUrl = "https://raw.githubusercontent.com/$Owner/$Repo/$Branch/$SourceFile"

Write-Host "Downloading: $SourceFile from $Owner/$Repo@$Branch"

try {
    $Content = Invoke-RestMethod -Uri $RawUrl -Headers $Headers -TimeoutSec 30
} catch {
    Write-Error "Failed to download $RawUrl : $_"
    exit 1
}

# Replace args format if needed
if ($ArgsFormat -ne '$ARGUMENTS') {
    $Content = $Content -replace [regex]::Escape('$ARGUMENTS'), $ArgsFormat
}

# Create target directory
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

# Write file with correct extension
$TargetFile = Join-Path $TargetDir "$AgentName$Extension"
Set-Content -Path $TargetFile -Value $Content -Encoding UTF8

Write-Host "Installed: $AgentName -> $TargetFile"
