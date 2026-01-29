#!/usr/bin/env bash

# generate-docs.sh - Generate documentation templates
# Usage: ./generate-docs.sh --type <type> --output <file>

set -e

# Default values
DOC_TYPE="readme"
OUTPUT_FILE=""
PROJECT_NAME="My Project"
AUTHOR_NAME="Your Name"

# Help function
show_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Generate documentation templates for different types.

OPTIONS:
    -t, --type TYPE       Documentation type: readme, api, user-guide, architecture
    -o, --output FILE     Output file path (required)
    -p, --project NAME    Project name
    -a, --author NAME     Author name
    -h, --help            Show this help message

EXAMPLES:
    $(basename "$0") --type readme --output ./README.md
    $(basename "$0") --type api --output ./docs/api.md --project "My API"
    $(basename "$0") --type user-guide --output ./docs/guide.md

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            DOC_TYPE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -p|--project)
            PROJECT_NAME="$2"
            shift 2
            ;;
        -a|--author)
            AUTHOR_NAME="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Error: Unknown option: $1" >&2
            show_help
            exit 1
            ;;
    esac
done

# Validate required arguments
if [ -z "$OUTPUT_FILE" ]; then
    echo "Error: Output file is required (use --output)" >&2
    show_help
    exit 1
fi

# Get current date
CURRENT_DATE=$(date +"%Y-%m-%d")

# Generate README template
generate_readme() {
    cat > "$OUTPUT_FILE" << 'EOF'
# Project Name

> One-line description of what this project does

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
npm install project-name
```

## Quick Start

```javascript
const project = require('project-name');

// Your code here
```

## Usage

Detailed usage instructions...

## Configuration

Configuration options...

## API Reference

API documentation...

## Contributing

Contribution guidelines...

## License

MIT
EOF
    
    # Replace placeholders
    sed -i.bak "s/Project Name/$PROJECT_NAME/g" "$OUTPUT_FILE"
    sed -i.bak "s/Your Name/$AUTHOR_NAME/g" "$OUTPUT_FILE"
    rm "${OUTPUT_FILE}.bak"
}

# Generate API documentation template
generate_api() {
    cat > "$OUTPUT_FILE" << 'EOF'
# API Documentation

## Overview

Brief description of the API.

**Base URL:** `https://api.example.com/v1`

## Authentication

```http
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### GET /resource

Description of endpoint.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Resource ID |

**Example Request:**

```bash
curl -X GET https://api.example.com/v1/resource/123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Success Response (200 OK):**

```json
{
  "id": "123",
  "name": "Example"
}
```

**Error Responses:**

- `404 Not Found`: Resource not found

## Rate Limiting

- 100 requests per hour

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |
EOF
}

# Generate user guide template
generate_user_guide() {
    cat > "$OUTPUT_FILE" << 'EOF'
# User Guide

## Introduction

Welcome to [Product Name]! This guide will help you get started.

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
EOF
}

# Generate architecture documentation template
generate_architecture() {
    cat > "$OUTPUT_FILE" << 'EOF'
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
EOF
}

# Create output directory if it doesn't exist
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    echo "Created directory: $OUTPUT_DIR"
fi

# Generate based on type
echo "Generating $DOC_TYPE documentation..."

case $DOC_TYPE in
    readme)
        generate_readme
        ;;
    api)
        generate_api
        ;;
    user-guide)
        generate_user_guide
        ;;
    architecture)
        generate_architecture
        ;;
    *)
        echo "Error: Unknown documentation type: $DOC_TYPE" >&2
        echo "Valid types: readme, api, user-guide, architecture"
        exit 1
        ;;
esac

echo "✓ Generated $DOC_TYPE documentation: $OUTPUT_FILE"
echo ""
echo "Next steps:"
echo "1. Edit the generated file and fill in your content"
echo "2. Replace placeholder text with actual information"
echo "3. Add code examples and diagrams as needed"
echo "4. Validate with: ./validate-docs.sh --dir $(dirname "$OUTPUT_FILE") --type $DOC_TYPE"
