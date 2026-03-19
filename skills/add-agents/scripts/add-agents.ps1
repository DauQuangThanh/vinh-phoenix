# add-agents.ps1 - Download and install an agent command folder from a GitHub repository
#
# Usage: add-agents.ps1 <repo_url> <branch> <repo_path> <agent_name> <target_dir> [extension] [args_format]
#
# Downloads the entire agent folder (or single file) recursively.
# Applies extension conversion and args format replacement to .md files.

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

$ApiBase = "https://api.github.com/repos/$Owner/$Repo/contents"
$RawBase = "https://raw.githubusercontent.com/$Owner/$Repo/$Branch"
$AgentPath = "$RepoPath/$AgentName"

Write-Host "Downloading agent: $AgentName from $Owner/$Repo@$Branch"

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
            $DestName = $Item.name

            # Apply extension conversion for .md files
            if ($DestName -match '\.md$') {
                $DestName = $DestName -replace '\.md$', $Extension
            }

            $LocalFile = Join-Path $LocalDir $DestName

            try {
                Invoke-WebRequest -Uri $RawUrl -Headers $Headers -OutFile $LocalFile -TimeoutSec 30

                # Replace args format if needed in text files
                if ($ArgsFormat -ne '$ARGUMENTS') {
                    if ($DestName -match '\.(md|agent\.md|toml)$') {
                        $FileContent = Get-Content -Path $LocalFile -Raw -Encoding UTF8
                        $FileContent = $FileContent -replace [regex]::Escape('$ARGUMENTS'), $ArgsFormat
                        Set-Content -Path $LocalFile -Value $FileContent -Encoding UTF8
                    }
                }

                Write-Host "  Downloaded: $($Item.path) -> $LocalFile"
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

# Try to access the agent path via API to determine if it's a directory or file
try {
    $ApiUrl = "$ApiBase/${AgentPath}?ref=$Branch"
    $Response = Invoke-RestMethod -Uri $ApiUrl -Headers $Headers -TimeoutSec 30

    if ($Response -is [System.Array]) {
        # Directory - download recursively
        Write-Host "Agent is a folder, downloading recursively..."
        Download-Directory -RemotePath $AgentPath -LocalDir $TargetDir
    } else {
        # Single file at exact path
        Write-Host "Agent is a single file, downloading..."
        $RawUrl = "$RawBase/$AgentPath"
        $DestName = $AgentName
        if ($DestName -match '\.md$') {
            $DestName = $DestName -replace '\.md$', $Extension
        } elseif ($DestName -notmatch '\.') {
            $DestName = "$DestName$Extension"
        }
        $TargetFile = Join-Path $TargetDir $DestName
        Invoke-WebRequest -Uri $RawUrl -Headers $Headers -OutFile $TargetFile -TimeoutSec 30

        if ($ArgsFormat -ne '$ARGUMENTS') {
            $FileContent = Get-Content -Path $TargetFile -Raw -Encoding UTF8
            $FileContent = $FileContent -replace [regex]::Escape('$ARGUMENTS'), $ArgsFormat
            Set-Content -Path $TargetFile -Value $FileContent -Encoding UTF8
        }
        Write-Host "  Downloaded: $AgentPath -> $TargetFile"
    }
} catch {
    # Path not found as-is, try with .md extension
    Write-Host "Agent folder not found, trying as single .md file..."
    $RawUrl = "$RawBase/${AgentPath}.md"

    try {
        $Content = Invoke-RestMethod -Uri $RawUrl -Headers $Headers -TimeoutSec 30
    } catch {
        Write-Error "Failed to download $RawUrl : $_"
        exit 1
    }

    if ($ArgsFormat -ne '$ARGUMENTS') {
        $Content = $Content -replace [regex]::Escape('$ARGUMENTS'), $ArgsFormat
    }

    $TargetFile = Join-Path $TargetDir "$AgentName$Extension"
    Set-Content -Path $TargetFile -Value $Content -Encoding UTF8
    Write-Host "  Downloaded: ${AgentPath}.md -> $TargetFile"
}

Write-Host "Installed: $AgentName -> $TargetDir"
