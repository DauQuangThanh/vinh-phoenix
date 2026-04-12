# list-agents.ps1 - List available agents from configured remote repositories
#
# Reads nightlife.yaml for agent repository definitions (url, branch, path),
# then lists available agents from each repository.
#
# Supports:
#   - GitHub repos:      https://github.com/{owner}/{repo}
#   - Azure DevOps repos: https://dev.azure.com/{org}/{project}/_git/{repo}
#
# No arguments required. Must be run from the project root where nightlife.yaml exists.

$ErrorActionPreference = "Stop"

# ── Auth ────────────────────────────────────────────────────────────────────────

# GitHub headers
$GHHeaders = @{
    "Accept" = "application/vnd.github.v3+json"
    "User-Agent" = "phoenix-cli"
}
if ($env:GH_TOKEN) {
    $GHHeaders["Authorization"] = "Bearer $env:GH_TOKEN"
} elseif ($env:GITHUB_TOKEN) {
    $GHHeaders["Authorization"] = "Bearer $env:GITHUB_TOKEN"
}

# Azure DevOps headers (Basic auth with PAT)
$ADOHeaders = @{
    "Accept" = "application/json"
    "User-Agent" = "phoenix-cli"
}
$adoPat = if ($env:AZURE_DEVOPS_PAT) { $env:AZURE_DEVOPS_PAT } elseif ($env:ADO_TOKEN) { $env:ADO_TOKEN } else { $null }
if ($adoPat) {
    $adoBase64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$adoPat"))
    $ADOHeaders["Authorization"] = "Basic $adoBase64"
}

# ── Parse nightlife.yaml ────────────────────────────────────────────────────────

if (-not (Test-Path "nightlife.yaml")) {
    Write-Host "Error: nightlife.yaml not found in current directory."
    Write-Host "Create one with 'phoenix init' or manually."
    exit 1
}

$content = Get-Content "nightlife.yaml" -Raw
$agentRepos = @()
$inAgents = $false
$currentItem = @{}

foreach ($line in ($content -split "`n")) {
    $stripped = ($line -replace '#.*', '').Trim()
    if ([string]::IsNullOrEmpty($stripped)) { continue }

    # Detect section headers
    if ($stripped -match '^agents:') {
        $inAgents = $true
        $currentItem = @{}
        continue
    }

    # Exit agents section on new top-level key
    if ($inAgents -and $line -match '^[a-zA-Z]') {
        if ($currentItem.url) {
            $agentRepos += [PSCustomObject]@{
                name = if ($currentItem.name) { $currentItem.name } else { "" }
                url = $currentItem.url
                branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
                path = if ($currentItem.path) { $currentItem.path } else { "agents" }
            }
        }
        $inAgents = $false
        $currentItem = @{}
        continue
    }

    if ($inAgents) {
        if ($stripped -match '^- (.+)') {
            # Flush previous entry
            if ($currentItem.url) {
                $agentRepos += [PSCustomObject]@{
                    name = if ($currentItem.name) { $currentItem.name } else { "" }
                    url = $currentItem.url
                    branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
                    path = if ($currentItem.path) { $currentItem.path } else { "agents" }
                }
            }
            $currentItem = @{}

            $kv = $Matches[1]
            if ($kv -match '^(\w+):\s*(.+)') {
                $currentItem[$Matches[1]] = $Matches[2].Trim()
            }
        } elseif ($stripped -match '^(\w+):\s*(.+)') {
            $currentItem[$Matches[1]] = $Matches[2].Trim()
        }
    }
}

# Flush last entry
if ($inAgents -and $currentItem.url) {
    $agentRepos += [PSCustomObject]@{
        name = if ($currentItem.name) { $currentItem.name } else { "" }
        url = $currentItem.url
        branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
        path = if ($currentItem.path) { $currentItem.path } else { "agents" }
    }
}

if ($agentRepos.Count -eq 0) {
    Write-Host "No agent repositories configured in nightlife.yaml."
    exit 0
}

# ── List agents from each repo ──────────────────────────────────────────────────

$grandTotal = 0

foreach ($repoInfo in $agentRepos) {
    $repoName = $repoInfo.name
    $repoUrl = $repoInfo.url
    $branch = $repoInfo.branch
    $path = $repoInfo.path

    Write-Host ""
    if ($repoName) {
        Write-Host "Repository: $repoName ($repoUrl, branch: $branch, path: $path)"
    } else {
        Write-Host "Repository: $repoUrl (branch: $branch, path: $path)"
    }

    # ── GitHub repo ──
    if ($repoUrl -match 'github\.com/([^/]+)/([^/]+?)(?:\.git)?$') {
        $owner = $Matches[1]
        $repo = $Matches[2]
        $apiUrl = "https://api.github.com/repos/$owner/$repo/contents/${path}?ref=$branch"

        try {
            $contents = Invoke-RestMethod -Uri $apiUrl -Headers $GHHeaders -TimeoutSec 30
            $agents = @()

            foreach ($item in $contents) {
                $itemName = $item.name
                if ($itemName.StartsWith(".") -or $itemName.StartsWith("_")) { continue }
                if ($item.type -eq "dir") {
                    $agents += $itemName
                }
            }

            $agents = $agents | Sort-Object
            foreach ($a in $agents) {
                Write-Host "  - $a"
            }
            Write-Host "  Total: $($agents.Count) agents available"
            $grandTotal += $agents.Count
        } catch {
            if ($_.Exception.Response.StatusCode.value__) {
                Write-Host "  Error: HTTP $($_.Exception.Response.StatusCode.value__) - $path not found or inaccessible"
            } else {
                Write-Host "  Error: $_"
            }
        }

    # ── Azure DevOps repo ──
    } elseif ($repoUrl -match 'dev\.azure\.com/([^/]+)/([^/]+)/_git/([^?/]+)') {
        $adoOrg = $Matches[1]
        $adoProject = $Matches[2]
        $adoRepo = $Matches[3]

        $adoApi = "https://dev.azure.com/${adoOrg}/${adoProject}/_apis/git/repositories/${adoRepo}/items?scopePath=/${path}&recursionLevel=oneLevel&versionDescriptor.version=${branch}&api-version=7.0"

        try {
            $listing = Invoke-RestMethod -Uri $adoApi -Headers $ADOHeaders -TimeoutSec 30
            $agents = @()

            foreach ($item in $listing.value) {
                if (-not $item.isFolder) { continue }
                $itemName = Split-Path $item.path -Leaf
                if ($itemName -eq $path) { continue }
                if ($itemName.StartsWith(".") -or $itemName.StartsWith("_")) { continue }
                $agents += $itemName
            }

            $agents = $agents | Sort-Object
            foreach ($a in $agents) {
                Write-Host "  - $a"
            }
            Write-Host "  Total: $($agents.Count) agents available"
            $grandTotal += $agents.Count
        } catch {
            if ($_.Exception.Response.StatusCode.value__) {
                Write-Host "  Error: HTTP $($_.Exception.Response.StatusCode.value__) - $path not found or inaccessible"
            } else {
                Write-Host "  Error: $_"
            }
        }

    } else {
        Write-Host "  Error: Unsupported repo URL format"
        Write-Host "  Supported: github.com or dev.azure.com URLs"
    }
}

Write-Host ""
Write-Host "Grand total: $grandTotal agents across $($agentRepos.Count) repositories"
