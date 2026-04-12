# list-skills.ps1 - List available skills from configured remote repositories
# (Bundled copy for add-skills — identical to list-skills/scripts/list-skills.ps1)
#
# Reads nightlife.yaml for skill repository definitions (name, url, branch, path),
# then lists available skills from each repository.
#
# Supports:
#   - GitHub repos:      https://github.com/{owner}/{repo}
#   - Azure DevOps repos: https://dev.azure.com/{org}/{project}/_git/{repo}
#
# No arguments required. Must be run from the project root where nightlife.yaml exists.

$ErrorActionPreference = "Stop"

# ── Auth ────────────────────────────────────────────────────────────────────────

$GHHeaders = @{
    "Accept" = "application/vnd.github.v3+json"
    "User-Agent" = "phoenix-cli"
}
if ($env:GH_TOKEN) {
    $GHHeaders["Authorization"] = "Bearer $env:GH_TOKEN"
} elseif ($env:GITHUB_TOKEN) {
    $GHHeaders["Authorization"] = "Bearer $env:GITHUB_TOKEN"
}

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
$skillRepos = @()
$inSkills = $false
$currentItem = @{}

foreach ($line in ($content -split "`n")) {
    $stripped = ($line -replace '#.*', '').Trim()
    if ([string]::IsNullOrEmpty($stripped)) { continue }

    if ($stripped -match '^skills:') {
        $inSkills = $true
        $currentItem = @{}
        continue
    }

    if ($inSkills -and $line -match '^[a-zA-Z]') {
        if ($currentItem.url) {
            $skillRepos += [PSCustomObject]@{
                name = if ($currentItem.name) { $currentItem.name } else { "" }
                url = $currentItem.url
                branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
                path = if ($currentItem.path) { $currentItem.path } else { "skills" }
            }
        }
        $inSkills = $false
        $currentItem = @{}
        continue
    }

    if ($inSkills) {
        if ($stripped -match '^- (.+)') {
            if ($currentItem.url) {
                $skillRepos += [PSCustomObject]@{
                    name = if ($currentItem.name) { $currentItem.name } else { "" }
                    url = $currentItem.url
                    branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
                    path = if ($currentItem.path) { $currentItem.path } else { "skills" }
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

if ($inSkills -and $currentItem.url) {
    $skillRepos += [PSCustomObject]@{
        name = if ($currentItem.name) { $currentItem.name } else { "" }
        url = $currentItem.url
        branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
        path = if ($currentItem.path) { $currentItem.path } else { "skills" }
    }
}

if ($skillRepos.Count -eq 0) {
    Write-Host "No skill repositories configured in nightlife.yaml."
    exit 0
}

# ── List skills from each repo ──────────────────────────────────────────────────

$grandTotal = 0

foreach ($repoInfo in $skillRepos) {
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

    if ($repoUrl -match 'github\.com/([^/]+)/([^/]+?)(?:\.git)?$') {
        $owner = $Matches[1]
        $repo = $Matches[2]
        $apiUrl = "https://api.github.com/repos/$owner/$repo/contents/${path}?ref=$branch"

        try {
            $contents = Invoke-RestMethod -Uri $apiUrl -Headers $GHHeaders -TimeoutSec 30
            $skills = @()

            foreach ($item in $contents) {
                $itemName = $item.name
                if ($itemName.StartsWith(".") -or $itemName.StartsWith("_")) { continue }
                if ($item.type -eq "dir") {
                    $skills += $itemName
                }
            }

            $skills = $skills | Sort-Object
            foreach ($s in $skills) {
                Write-Host "  - $s"
            }
            Write-Host "  Total: $($skills.Count) skills available"
            $grandTotal += $skills.Count
        } catch {
            if ($_.Exception.Response.StatusCode.value__) {
                Write-Host "  Error: HTTP $($_.Exception.Response.StatusCode.value__) - $path not found or inaccessible"
            } else {
                Write-Host "  Error: $_"
            }
        }

    } elseif ($repoUrl -match 'dev\.azure\.com/([^/]+)/([^/]+)/_git/([^?/]+)') {
        $adoOrg = $Matches[1]
        $adoProject = $Matches[2]
        $adoRepo = $Matches[3]

        $adoApi = "https://dev.azure.com/${adoOrg}/${adoProject}/_apis/git/repositories/${adoRepo}/items?scopePath=/${path}&recursionLevel=oneLevel&versionDescriptor.version=${branch}&api-version=7.0"

        try {
            $listing = Invoke-RestMethod -Uri $adoApi -Headers $ADOHeaders -TimeoutSec 30
            $skills = @()

            foreach ($item in $listing.value) {
                if (-not $item.isFolder) { continue }
                $itemName = Split-Path $item.path -Leaf
                if ($itemName -eq $path) { continue }
                if ($itemName.StartsWith(".") -or $itemName.StartsWith("_")) { continue }
                $skills += $itemName
            }

            $skills = $skills | Sort-Object
            foreach ($s in $skills) {
                Write-Host "  - $s"
            }
            Write-Host "  Total: $($skills.Count) skills available"
            $grandTotal += $skills.Count
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
Write-Host "Grand total: $grandTotal skills across $($skillRepos.Count) repositories"
