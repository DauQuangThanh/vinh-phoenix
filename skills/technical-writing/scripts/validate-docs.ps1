# validate-docs.ps1 - Validate documentation structure and completeness
# Usage: .\validate-docs.ps1 -Directory <directory> -Type <type>

param(
    [Parameter(Mandatory=$false)]
    [string]$Directory = ".\docs",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("readme", "api", "user-guide", "architecture")]
    [string]$Type = "readme",
    
    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

# Initialize counters
$script:TotalChecks = 0
$script:PassedChecks = 0
$script:FailedChecks = 0
$script:Warnings = 0

# Logging functions
function Write-Info {
    param([string]$Message)
    if ($Verbose) {
        Write-Host "[INFO] $Message" -ForegroundColor Green
    }
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
    $script:FailedChecks++
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
    $script:Warnings++
}

function Write-Pass {
    param([string]$Message)
    if ($Verbose) {
        Write-Host "[PASS] $Message" -ForegroundColor Green
    }
    $script:PassedChecks++
}

function Add-Check {
    $script:TotalChecks++
}

# Validate README
function Test-ReadmeDoc {
    param([string]$DocDir)
    
    Write-Info "Validating README documentation..."
    
    $readmeFile = Join-Path $DocDir "README.md"
    
    # Check if README exists
    Add-Check
    if (Test-Path $readmeFile) {
        Write-Pass "README.md exists"
    } else {
        Write-Error-Custom "README.md not found in $DocDir"
        return
    }
    
    $content = Get-Content $readmeFile -Raw
    
    # Check for required sections
    Add-Check
    if ($content -match "^# ") {
        Write-Pass "Has project title (H1)"
    } else {
        Write-Error-Custom "Missing project title (# heading)"
    }
    
    Add-Check
    if ($content -match "(?i)description|overview") {
        Write-Pass "Has description section"
    } else {
        Write-Warning-Custom "Consider adding a description or overview section"
    }
    
    Add-Check
    if ($content -match "(?i)## Installation|## Install|## Setup") {
        Write-Pass "Has installation section"
    } else {
        Write-Error-Custom "Missing installation section"
    }
    
    Add-Check
    if ($content -match "(?i)## Usage|## Quick Start|## Getting Started") {
        Write-Pass "Has usage section"
    } else {
        Write-Error-Custom "Missing usage section"
    }
    
    Add-Check
    if ($content -match "```") {
        Write-Pass "Contains code examples"
    } else {
        Write-Warning-Custom "Consider adding code examples"
    }
    
    Add-Check
    if ($content -match "(?i)## License") {
        Write-Pass "Has license section"
    } else {
        Write-Warning-Custom "Consider adding license information"
    }
    
    # Check for broken links
    Add-Check
    $brokenLinks = 0
    $linkPattern = '\[.*?\]\(([^)]+)\)'
    $matches = [regex]::Matches($content, $linkPattern)
    
    foreach ($match in $matches) {
        $url = $match.Groups[1].Value
        if ($url -match '^https?://') {
            Write-Info "Skipping external URL check: $url"
        } elseif ($url -and -not (Test-Path (Join-Path $DocDir $url))) {
            Write-Warning-Custom "Broken link to local file: $url"
            $brokenLinks++
        }
    }
    
    if ($brokenLinks -eq 0) {
        Write-Pass "No broken local links found"
    }
}

# Validate API documentation
function Test-ApiDoc {
    param([string]$DocDir)
    
    Write-Info "Validating API documentation..."
    
    $apiFile = Get-ChildItem -Path $DocDir -Filter "*api*.md" -Recurse | Select-Object -First 1
    
    Add-Check
    if ($apiFile) {
        Write-Pass "API documentation file found: $($apiFile.FullName)"
    } else {
        Write-Error-Custom "No API documentation file found"
        return
    }
    
    $content = Get-Content $apiFile.FullName -Raw
    
    Add-Check
    if ($content -match "(?i)## Authentication|## Auth") {
        Write-Pass "Has authentication section"
    } else {
        Write-Error-Custom "Missing authentication section"
    }
    
    Add-Check
    if ($content -match "(GET|POST|PUT|PATCH|DELETE) /") {
        Write-Pass "Contains endpoint definitions"
    } else {
        Write-Error-Custom "Missing endpoint definitions"
    }
    
    Add-Check
    if ($content -match "(?i)request|example") {
        Write-Pass "Contains request examples"
    } else {
        Write-Warning-Custom "Consider adding request examples"
    }
    
    Add-Check
    if ($content -match "(?i)response") {
        Write-Pass "Contains response documentation"
    } else {
        Write-Error-Custom "Missing response documentation"
    }
    
    Add-Check
    if ($content -match "(400|401|403|404|500)") {
        Write-Pass "Documents error codes"
    } else {
        Write-Warning-Custom "Consider documenting error codes"
    }
}

# Validate user guide
function Test-UserGuideDoc {
    param([string]$DocDir)
    
    Write-Info "Validating user guide documentation..."
    
    $guideFile = Get-ChildItem -Path $DocDir -Filter "*guide*.md" -Recurse | Select-Object -First 1
    
    Add-Check
    if ($guideFile) {
        Write-Pass "User guide file found: $($guideFile.FullName)"
    } else {
        Write-Error-Custom "No user guide file found"
        return
    }
    
    $content = Get-Content $guideFile.FullName -Raw
    
    Add-Check
    if ($content -match "(?i)## Getting Started") {
        Write-Pass "Has getting started section"
    } else {
        Write-Error-Custom "Missing getting started section"
    }
    
    Add-Check
    if ($content -match "!\[.*?\]\(") {
        Write-Pass "Contains images/screenshots"
    } else {
        Write-Warning-Custom "Consider adding screenshots for user guidance"
    }
    
    Add-Check
    if ($content -match "(?i)## Troubleshooting|## FAQ") {
        Write-Pass "Has troubleshooting or FAQ section"
    } else {
        Write-Warning-Custom "Consider adding troubleshooting section"
    }
}

# Validate architecture documentation
function Test-ArchitectureDoc {
    param([string]$DocDir)
    
    Write-Info "Validating architecture documentation..."
    
    $archFile = Get-ChildItem -Path $DocDir -Filter "*architecture*.md", "*design*.md" -Recurse | Select-Object -First 1
    
    Add-Check
    if ($archFile) {
        Write-Pass "Architecture file found: $($archFile.FullName)"
    } else {
        Write-Error-Custom "No architecture file found"
        return
    }
    
    $content = Get-Content $archFile.FullName -Raw
    
    Add-Check
    if ($content -match "(?i)## Overview|## System Overview") {
        Write-Pass "Has system overview"
    } else {
        Write-Error-Custom "Missing system overview"
    }
    
    Add-Check
    if ($content -match "!\[.*?\]\(") {
        Write-Pass "Contains diagrams"
    } else {
        Write-Warning-Custom "Consider adding architecture diagrams"
    }
    
    Add-Check
    if ($content -match "(?i)## Components") {
        Write-Pass "Has components section"
    } else {
        Write-Error-Custom "Missing components section"
    }
    
    Add-Check
    if ($content -match "(?i)## Design Decision|ADR|Decision") {
        Write-Pass "Documents design decisions"
    } else {
        Write-Warning-Custom "Consider documenting design decisions"
    }
}

# Main execution
Write-Host "========================================"
Write-Host "Documentation Validation"
Write-Host "========================================"
Write-Host "Directory: $Directory"
Write-Host "Type: $Type"
Write-Host ""

# Validate directory exists
if (-not (Test-Path $Directory)) {
    Write-Host "Error: Directory not found: $Directory" -ForegroundColor Red
    exit 1
}

# Run appropriate validation
switch ($Type) {
    "readme" { Test-ReadmeDoc -DocDir $Directory }
    "api" { Test-ApiDoc -DocDir $Directory }
    "user-guide" { Test-UserGuideDoc -DocDir $Directory }
    "architecture" { Test-ArchitectureDoc -DocDir $Directory }
}

# Print summary
Write-Host ""
Write-Host "========================================"
Write-Host "Validation Summary"
Write-Host "========================================"
Write-Host "Total checks: $TotalChecks"
Write-Host "Passed: $PassedChecks" -ForegroundColor Green
Write-Host "Failed: $FailedChecks" -ForegroundColor Red
Write-Host "Warnings: $Warnings" -ForegroundColor Yellow
Write-Host ""

# Exit with appropriate code
if ($FailedChecks -gt 0) {
    Write-Host "Validation failed" -ForegroundColor Red
    exit 1
} else {
    Write-Host "Validation passed" -ForegroundColor Green
    exit 0
}
