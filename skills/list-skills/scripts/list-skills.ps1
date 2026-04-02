# list-skills.ps1 - List available skills from configured remote repositories
#
# Reads nightlife.yaml for catalog URLs (GitHub issues or Azure DevOps repo files),
# fetches repo definitions, and lists available skills from each repository.
#
# Supports:
#   - GitHub issues:      https://github.com/{owner}/{repo}/issues/{number}
#   - Azure DevOps files: https://dev.azure.com/{org}/{project}/_git/{repo}?path={path}&version=GB{branch}
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
    Write-Host "Create one with 'phoenix config-set-url <url1> <url2>' or manually."
    exit 1
}

$content = Get-Content "nightlife.yaml" -Raw
$urls = @()
$inUrls = $false
foreach ($line in ($content -split "`n")) {
    $stripped = ($line -replace '#.*', '').Trim()
    if ([string]::IsNullOrEmpty($stripped)) { continue }

    if ($stripped -match '^urls:') {
        $inUrls = $true
        continue
    }

    if ($inUrls -and $line -match '^[a-zA-Z]') {
        $inUrls = $false
        continue
    }

    if ($inUrls -and $stripped -match '^- (.+)') {
        $urls += $Matches[1].Trim()
    }
}

if ($urls.Count -eq 0) {
    Write-Host "Error: No 'urls' configured in nightlife.yaml."
    exit 1
}

# ── Parse YAML body into skill repo entries ─────────────────────────────────────

function Parse-SkillRepos {
    param([string]$Body)

    $results = @()
    $inSkills = $false
    $hasSkillsHeader = ($Body -match '(?m)^skills:')
    if (-not $hasSkillsHeader -and ($Body -match '(?m)^\s*-\s*name:')) {
        $inSkills = $true
    }
    $currentItem = @{}

    foreach ($bline in ($Body -split "`n")) {
        $bstripped = ($bline -replace '#.*', '').Trim()
        if ([string]::IsNullOrEmpty($bstripped)) { continue }

        if ($hasSkillsHeader -and $bstripped -match '^skills:') {
            $inSkills = $true
            continue
        }

        if ($inSkills -and $hasSkillsHeader -and $bline -match '^[a-zA-Z]') {
            if ($currentItem.name) {
                $results += [PSCustomObject]@{
                    name = $currentItem.name
                    url = if ($currentItem.url) { $currentItem.url } else { "" }
                    branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
                    path = if ($currentItem.path) { $currentItem.path } else { "skills" }
                }
            }
            $currentItem = @{}
            $inSkills = $false
            continue
        }

        if ($inSkills) {
            if ($bstripped -match '^- (.+)') {
                if ($currentItem.name) {
                    $results += [PSCustomObject]@{
                        name = $currentItem.name
                        url = if ($currentItem.url) { $currentItem.url } else { "" }
                        branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
                        path = if ($currentItem.path) { $currentItem.path } else { "skills" }
                    }
                }
                $currentItem = @{}

                $kv = $Matches[1]
                if ($kv -match '^(\w+):\s*(.+)') {
                    $currentItem[$Matches[1]] = $Matches[2].Trim()
                }
            } elseif ($bstripped -match '^(\w+):\s*(.+)') {
                $currentItem[$Matches[1]] = $Matches[2].Trim()
            }
        }
    }

    if ($currentItem.name) {
        $results += [PSCustomObject]@{
            name = $currentItem.name
            url = if ($currentItem.url) { $currentItem.url } else { "" }
            branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
            path = if ($currentItem.path) { $currentItem.path } else { "skills" }
        }
    }

    return $results
}

# ── Fetch catalog from each URL ─────────────────────────────────────────────────

$skillRepos = @()
$seenNames = @{}

foreach ($catalogUrl in $urls) {

    # ── GitHub issue ──
    if ($catalogUrl -match 'github\.com/([^/]+)/([^/]+)/issues/(\d+)') {
        $owner = $Matches[1]
        $repo = $Matches[2]
        $number = $Matches[3]
        $apiUrl = "https://api.github.com/repos/$owner/$repo/issues/$number"

        try {
            $issueData = Invoke-RestMethod -Uri $apiUrl -Headers $GHHeaders -TimeoutSec 30
            $body = $issueData.body
        } catch {
            Write-Host "Warning: Failed to fetch GitHub issue $catalogUrl : $_"
            continue
        }

        $repos = Parse-SkillRepos -Body $body
        foreach ($r in $repos) {
            if (-not $seenNames.ContainsKey($r.name)) {
                $seenNames[$r.name] = $true
                $skillRepos += $r
            }
        }

    # ── Azure DevOps repo file ──
    } elseif ($catalogUrl -match 'dev\.azure\.com/([^/]+)/([^/]+)/_git/([^?/]+)') {
        $adoOrg = $Matches[1]
        $adoProject = $Matches[2]
        $adoRepo = $Matches[3]

        $adoPath = "/"
        $adoBranch = "main"
        if ($catalogUrl -match '[?&]path=([^&]+)') {
            $adoPath = [System.Uri]::UnescapeDataString($Matches[1])
        }
        if ($catalogUrl -match '[?&]version=GB([^&]+)') {
            $adoBranch = $Matches[1]
        }

        $adoApi = "https://dev.azure.com/${adoOrg}/${adoProject}/_apis/git/repositories/${adoRepo}/items?path=${adoPath}&versionDescriptor.version=${adoBranch}&`$format=text&api-version=7.0"

        try {
            $body = Invoke-RestMethod -Uri $adoApi -Headers $ADOHeaders -TimeoutSec 30
        } catch {
            Write-Host "Warning: Failed to fetch Azure DevOps file $catalogUrl : $_"
            continue
        }

        $repos = Parse-SkillRepos -Body $body
        foreach ($r in $repos) {
            if (-not $seenNames.ContainsKey($r.name)) {
                $seenNames[$r.name] = $true
                $skillRepos += $r
            }
        }

    } else {
        Write-Host "Warning: Unsupported catalog URL format: $catalogUrl"
        Write-Host "  Supported: GitHub issues (github.com/.../issues/N) or Azure DevOps files (dev.azure.com/.../_git/...?path=...)"
        continue
    }
}

if ($skillRepos.Count -eq 0) {
    Write-Host "No skill repositories configured."
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
    Write-Host "Repository: $repoName ($repoUrl)"

    # ── GitHub repo ──
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

    # ── Azure DevOps repo ──
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
                # Skip the root path itself, hidden and internal dirs
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
