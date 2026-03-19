# list-agents.ps1 - List available agent commands from configured remote repositories
#
# Reads nightlife.yaml for GitHub issue URLs, fetches repo definitions,
# and lists available agent commands from each repository.
#
# No arguments required. Must be run from the project root where nightlife.yaml exists.

$ErrorActionPreference = "Stop"

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

# Check nightlife.yaml exists
if (-not (Test-Path "nightlife.yaml")) {
    Write-Host "Error: nightlife.yaml not found in current directory."
    Write-Host "Create one with 'phoenix config-set-url <url1> <url2>' or manually."
    exit 1
}

# Parse URLs from nightlife.yaml
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

# Fetch agent repo definitions from GitHub issues
$agentRepos = @()
$seenNames = @{}

foreach ($issueUrl in $urls) {
    if ($issueUrl -notmatch 'github\.com/([^/]+)/([^/]+)/issues/(\d+)') {
        Write-Host "Warning: Invalid issue URL: $issueUrl"
        continue
    }

    $owner = $Matches[1]
    $repo = $Matches[2]
    $number = $Matches[3]
    $apiUrl = "https://api.github.com/repos/$owner/$repo/issues/$number"

    try {
        $issueData = Invoke-RestMethod -Uri $apiUrl -Headers $Headers -TimeoutSec 30
        $body = $issueData.body
    } catch {
        Write-Host "Warning: Failed to fetch $issueUrl : $_"
        continue
    }

    # Parse agents section from issue body
    $inAgents = $false
    $currentItem = @{}

    foreach ($bline in ($body -split "`n")) {
        $bstripped = ($bline -replace '#.*', '').Trim()
        if ([string]::IsNullOrEmpty($bstripped)) { continue }

        if ($bstripped -match '^agents:') {
            $inAgents = $true
            continue
        }

        if ($inAgents -and $bline -match '^[a-zA-Z]') {
            if ($currentItem.name -and -not $seenNames.ContainsKey($currentItem.name)) {
                $seenNames[$currentItem.name] = $true
                $agentRepos += [PSCustomObject]@{
                    name = $currentItem.name
                    url = if ($currentItem.url) { $currentItem.url } else { "" }
                    branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
                    path = if ($currentItem.path) { $currentItem.path } else { "agent-commands" }
                }
            }
            $currentItem = @{}
            $inAgents = $false
            continue
        }

        if ($inAgents) {
            if ($bstripped -match '^- (.+)') {
                # Save previous item
                if ($currentItem.name -and -not $seenNames.ContainsKey($currentItem.name)) {
                    $seenNames[$currentItem.name] = $true
                    $agentRepos += [PSCustomObject]@{
                        name = $currentItem.name
                        url = if ($currentItem.url) { $currentItem.url } else { "" }
                        branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
                        path = if ($currentItem.path) { $currentItem.path } else { "agent-commands" }
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

    # Save last item
    if ($currentItem.name -and -not $seenNames.ContainsKey($currentItem.name)) {
        $seenNames[$currentItem.name] = $true
        $agentRepos += [PSCustomObject]@{
            name = $currentItem.name
            url = if ($currentItem.url) { $currentItem.url } else { "" }
            branch = if ($currentItem.branch) { $currentItem.branch } else { "main" }
            path = if ($currentItem.path) { $currentItem.path } else { "agent-commands" }
        }
    }
}

if ($agentRepos.Count -eq 0) {
    Write-Host "No agent repositories configured."
    exit 0
}

# List agents from each repo
$grandTotal = 0

foreach ($repoInfo in $agentRepos) {
    $repoName = $repoInfo.name
    $repoUrl = $repoInfo.url
    $branch = $repoInfo.branch
    $path = $repoInfo.path

    if ($repoUrl -notmatch 'github\.com/([^/]+)/([^/]+?)(?:\.git)?$') {
        Write-Host ""
        Write-Host "${repoName}: Invalid repo URL"
        continue
    }

    $owner = $Matches[1]
    $repo = $Matches[2]
    $apiUrl = "https://api.github.com/repos/$owner/$repo/contents/${path}?ref=$branch"

    Write-Host ""
    Write-Host "Repository: $repoName ($repoUrl)"

    try {
        $contents = Invoke-RestMethod -Uri $apiUrl -Headers $Headers -TimeoutSec 30
        $agents = @()

        foreach ($item in $contents) {
            $itemName = $item.name
            if ($itemName.StartsWith(".") -or $itemName.StartsWith("_")) { continue }
            if ($itemName -match 'template') { continue }

            if ($item.type -eq "file" -and $itemName.EndsWith(".md")) {
                $agents += ($itemName -replace '\.md$', '')
            } elseif ($item.type -eq "dir") {
                $agents += $itemName
            }
        }

        $agents = $agents | Sort-Object
        foreach ($a in $agents) {
            Write-Host "  - $a"
        }
        Write-Host "  Total: $($agents.Count) agent commands available"
        $grandTotal += $agents.Count
    } catch {
        if ($_.Exception.Response.StatusCode.value__) {
            Write-Host "  Error: HTTP $($_.Exception.Response.StatusCode.value__) - $path not found or inaccessible"
        } else {
            Write-Host "  Error: $_"
        }
    }
}

Write-Host ""
Write-Host "Grand total: $grandTotal agent commands across $($agentRepos.Count) repositories"
