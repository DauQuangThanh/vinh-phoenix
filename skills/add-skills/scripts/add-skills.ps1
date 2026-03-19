# add-skills.ps1 - Download and install a skill from a GitHub repository
#
# Usage: add-skills.ps1 <repo_url> <branch> <repo_path> <skill_name> <target_dir>

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

$ApiBase = "https://api.github.com/repos/$Owner/$Repo/contents"
$RawBase = "https://raw.githubusercontent.com/$Owner/$Repo/$Branch"
$SkillPath = "$RepoPath/$SkillName"

Write-Host "Downloading skill: $SkillName from $Owner/$Repo@$Branch"

# Create target directory
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

function Download-Directory {
    param(
        [string]$RemotePath,
        [string]$LocalDir
    )

    $ApiUrl = "$ApiBase/${RemotePath}?ref=$Branch"

    try {
        $Listing = Invoke-RestMethod -Uri $ApiUrl -Headers $Headers -TimeoutSec 30
    } catch {
        Write-Error "Failed to list $RemotePath : $_"
        return
    }

    foreach ($Item in $Listing) {
        if ($Item.type -eq "file") {
            $RawUrl = "$RawBase/$($Item.path)"
            $LocalFile = Join-Path $LocalDir $Item.name

            try {
                Invoke-WebRequest -Uri $RawUrl -Headers $Headers -OutFile $LocalFile -TimeoutSec 30
                Write-Host "  Downloaded: $($Item.path)"
            } catch {
                Write-Warning "Failed to download $($Item.path): $_"
            }
        } elseif ($Item.type -eq "dir") {
            $SubDir = Join-Path $LocalDir $Item.name
            if (-not (Test-Path $SubDir)) {
                New-Item -ItemType Directory -Path $SubDir -Force | Out-Null
            }
            Download-Directory -RemotePath $Item.path -LocalDir $SubDir
        }
    }
}

# Download the skill directory recursively
Download-Directory -RemotePath $SkillPath -LocalDir $TargetDir

Write-Host "Installed skill: $SkillName -> $TargetDir"
