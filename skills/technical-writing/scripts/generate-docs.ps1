# generate-docs.ps1 - Generate documentation templates
# Usage: .\generate-docs.ps1 -Type <type> -Output <file>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("readme", "api", "user-guide", "architecture")]
    [string]$Type = "readme",
    
    [Parameter(Mandatory=$true)]
    [string]$Output,
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectName = "My Project",
    
    [Parameter(Mandatory=$false)]
    [string]$AuthorName = "Your Name"
)

$CurrentDate = Get-Date -Format "yyyy-MM-dd"

# Generate README template
function New-ReadmeDoc {
    param([string]$OutputFile)
    
    $content = @"
# $ProjectName

> One-line description of what this project does

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

``````bash
npm install project-name
``````

## Quick Start

``````javascript
const project = require('project-name');

// Your code here
``````

## Usage

Detailed usage instructions...

## Configuration

Configuration options...

## API Reference

API documentation...

## Contributing

Contribution guidelines...

## License

MIT © $AuthorName
"@
    
    Set-Content -Path $OutputFile -Value $content
}

# Generate API documentation template
function New-ApiDoc {
    param([string]$OutputFile)
    
    $content = @"
# API Documentation

## Overview

Brief description of the API.

**Base URL:** ``https://api.example.com/v1``

## Authentication

``````http
Authorization: Bearer YOUR_API_KEY
``````

## Endpoints

### GET /resource

Description of endpoint.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Resource ID |

**Example Request:**

``````bash
curl -X GET https://api.example.com/v1/resource/123 \
  -H "Authorization: Bearer YOUR_API_KEY"
``````

**Success Response (200 OK):**

``````json
{
  "id": "123",
  "name": "Example"
}
``````

**Error Responses:**

- ``404 Not Found``: Resource not found

## Rate Limiting

- 100 requests per hour

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |
"@
    
    Set-Content -Path $OutputFile -Value $content
}

# Generate user guide template
function New-UserGuideDoc {
    param([string]$OutputFile)
    
    $content = @"
# User Guide

## Introduction

Welcome to $ProjectName! This guide will help you get started.

## Getting Started

### Step 1: Setup

Instructions for setup...

### Step 2: Configuration

Configuration steps...

## Basic Features

### Feature 1

How to use feature 1...

### Feature 2

How to use feature 2...

## Advanced Features

Advanced usage instructions...

## Troubleshooting

### Issue 1

**Problem:** Description

**Solution:** Steps to resolve

## FAQ

**Q: Common question?**

A: Answer

## Additional Resources

- Link to resource 1
- Link to resource 2
"@
    
    Set-Content -Path $OutputFile -Value $content
}

# Generate architecture documentation template
function New-ArchitectureDoc {
    param([string]$OutputFile)
    
    $content = @"
# Architecture Documentation

## System Overview

Brief description of the system.

## Architecture Diagram

[Include diagram here]

## Components

### Component 1

**Purpose:** What it does

**Technology:** Tech stack

**Responsibilities:**
- Responsibility 1
- Responsibility 2

## Data Flow

1. Step 1
2. Step 2
3. Step 3

## Design Decisions

### Decision 1

**Context:** Why this decision was needed

**Decision:** What was decided

**Rationale:** Why this was chosen

**Consequences:** Impact of decision

## Technology Stack

- Frontend: Technology
- Backend: Technology
- Database: Technology

## Security

Security considerations...

## Deployment

Deployment strategy...

## Future Considerations

- Future enhancement 1
- Future enhancement 2
"@
    
    Set-Content -Path $OutputFile -Value $content
}

# Main execution
Write-Host "Generating $Type documentation..." -ForegroundColor Green

# Create output directory if it doesn't exist
$outputDir = Split-Path -Parent $Output
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    Write-Host "Created directory: $outputDir" -ForegroundColor Yellow
}

# Generate based on type
switch ($Type) {
    "readme" { New-ReadmeDoc -OutputFile $Output }
    "api" { New-ApiDoc -OutputFile $Output }
    "user-guide" { New-UserGuideDoc -OutputFile $Output }
    "architecture" { New-ArchitectureDoc -OutputFile $Output }
}

Write-Host "✓ Generated $Type documentation: $Output" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit the generated file and fill in your content"
Write-Host "2. Replace placeholder text with actual information"
Write-Host "3. Add code examples and diagrams as needed"
Write-Host "4. Validate with: .\validate-docs.ps1 -Directory $(Split-Path -Parent $Output) -Type $Type"
