#!/usr/bin/env python3
# generate-docs.py - Generate documentation templates
# Usage: python3 generate-docs.py --type <type> --output <file>

import argparse
import os
from datetime import datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Generate documentation templates for different types.')
    parser.add_argument('-t', '--type', required=True,
                       choices=['readme', 'api', 'user-guide', 'architecture'],
                       help='Documentation type')
    parser.add_argument('-o', '--output', required=True,
                       help='Output file path')
    parser.add_argument('-p', '--project', default='My Project',
                       help='Project name')
    parser.add_argument('-a', '--author', default='Your Name',
                       help='Author name')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate based on type
    print(f"Generating {args.type} documentation...")

    if args.type == 'readme':
        generate_readme(output_path, args.project, args.author)
    elif args.type == 'api':
        generate_api(output_path)
    elif args.type == 'user-guide':
        generate_user_guide(output_path)
    elif args.type == 'architecture':
        generate_architecture(output_path)

    print(f"✓ Generated {args.type} documentation: {args.output}")
    print()
    print("Next steps:")
    print("1. Edit the generated file and fill in your content")
    print("2. Replace placeholder text with actual information")
    print("3. Add code examples and diagrams as needed")
    print("4. Validate with: python3 validate-docs.py --dir $(dirname {}) --type {}".format(args.output, args.type))

def generate_readme(output_path, project_name, author_name):
    content = f"""# {project_name}

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
"""

    with open(output_path, 'w') as f:
        f.write(content)

    # Replace placeholders
    content = content.replace('Project Name', project_name)
    content = content.replace('Your Name', author_name)

    with open(output_path, 'w') as f:
        f.write(content)

def generate_api(output_path):
    content = """# API Documentation

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
curl -X GET https://api.example.com/v1/resource/123 \\
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
"""

    with open(output_path, 'w') as f:
        f.write(content)

def generate_user_guide(output_path):
    content = """# User Guide

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
"""

    with open(output_path, 'w') as f:
        f.write(content)

def generate_architecture(output_path):
    content = """# Architecture Documentation

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
"""

    with open(output_path, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    main()