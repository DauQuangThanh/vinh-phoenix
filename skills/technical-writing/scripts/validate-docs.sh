#!/usr/bin/env bash

# validate-docs.sh - Validate documentation structure and completeness
# Usage: ./validate-docs.sh --dir <directory> --type <type>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
DOC_DIR="./docs"
DOC_TYPE="readme"
VERBOSE=false

# Help function
show_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Validate documentation structure and completeness.

OPTIONS:
    -d, --dir DIR       Documentation directory (default: ./docs)
    -t, --type TYPE     Documentation type: readme, api, user-guide, architecture
    -v, --verbose       Verbose output
    -h, --help          Show this help message

EXAMPLES:
    $(basename "$0") --dir ./docs --type readme
    $(basename "$0") --dir ./api-docs --type api --verbose

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dir)
            DOC_DIR="$2"
            shift 2
            ;;
        -t|--type)
            DOC_TYPE="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option: $1${NC}" >&2
            show_help
            exit 1
            ;;
    esac
done

# Validate directory exists
if [ ! -d "$DOC_DIR" ]; then
    echo -e "${RED}Error: Directory not found: $DOC_DIR${NC}" >&2
    exit 1
fi

# Initialize counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNINGS=0

# Logging functions
log_info() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${GREEN}[INFO]${NC} $1"
    fi
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    ((FAILED_CHECKS++))
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    ((WARNINGS++))
}

log_pass() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${GREEN}[PASS]${NC} $1"
    fi
    ((PASSED_CHECKS++))
}

check() {
    ((TOTAL_CHECKS++))
}

# Validation functions for README
validate_readme() {
    log_info "Validating README documentation..."
    
    local readme_file="$DOC_DIR/README.md"
    
    # Check if README exists
    check
    if [ -f "$readme_file" ]; then
        log_pass "README.md exists"
    else
        log_error "README.md not found in $DOC_DIR"
        return 1
    fi
    
    # Check for required sections
    local content
    content=$(cat "$readme_file")
    
    # Project title
    check
    if echo "$content" | grep -q "^# "; then
        log_pass "Has project title (H1)"
    else
        log_error "Missing project title (# heading)"
    fi
    
    # Description
    check
    if echo "$content" | grep -iq "description\|overview"; then
        log_pass "Has description section"
    else
        log_warning "Consider adding a description or overview section"
    fi
    
    # Installation
    check
    if echo "$content" | grep -iq "## Installation\|## Install\|## Setup"; then
        log_pass "Has installation section"
    else
        log_error "Missing installation section"
    fi
    
    # Usage
    check
    if echo "$content" | grep -iq "## Usage\|## Quick Start\|## Getting Started"; then
        log_pass "Has usage section"
    else
        log_error "Missing usage section"
    fi
    
    # Code examples
    check
    if echo "$content" | grep -q '```'; then
        log_pass "Contains code examples"
    else
        log_warning "Consider adding code examples"
    fi
    
    # License
    check
    if echo "$content" | grep -iq "## License"; then
        log_pass "Has license section"
    else
        log_warning "Consider adding license information"
    fi
    
    # Links check
    check
    local broken_links=0
    while IFS= read -r line; do
        if echo "$line" | grep -q '\[.*\]([^)]*)'; then
            local url
            url=$(echo "$line" | grep -oP '\[.*?\]\(\K[^)]+')
            if [[ "$url" =~ ^https?:// ]]; then
                log_info "Skipping external URL check: $url"
            elif [ -n "$url" ] && [ ! -f "$DOC_DIR/$url" ]; then
                log_warning "Broken link to local file: $url"
                ((broken_links++))
            fi
        fi
    done < "$readme_file"
    
    if [ $broken_links -eq 0 ]; then
        log_pass "No broken local links found"
    fi
}

# Validation functions for API documentation
validate_api() {
    log_info "Validating API documentation..."
    
    # Find API documentation file
    local api_file
    api_file=$(find "$DOC_DIR" -type f -iname "*api*.md" | head -n 1)
    
    check
    if [ -n "$api_file" ]; then
        log_pass "API documentation file found: $api_file"
    else
        log_error "No API documentation file found"
        return 1
    fi
    
    local content
    content=$(cat "$api_file")
    
    # Check for authentication section
    check
    if echo "$content" | grep -iq "## Authentication\|## Auth"; then
        log_pass "Has authentication section"
    else
        log_error "Missing authentication section"
    fi
    
    # Check for endpoints
    check
    if echo "$content" | grep -qE "(GET|POST|PUT|PATCH|DELETE) /"; then
        log_pass "Contains endpoint definitions"
    else
        log_error "Missing endpoint definitions"
    fi
    
    # Check for request examples
    check
    if echo "$content" | grep -iq "request\|example"; then
        log_pass "Contains request examples"
    else
        log_warning "Consider adding request examples"
    fi
    
    # Check for response examples
    check
    if echo "$content" | grep -iq "response"; then
        log_pass "Contains response documentation"
    else
        log_error "Missing response documentation"
    fi
    
    # Check for error codes
    check
    if echo "$content" | grep -qE "(400|401|403|404|500)"; then
        log_pass "Documents error codes"
    else
        log_warning "Consider documenting error codes"
    fi
}

# Validation functions for user guide
validate_user_guide() {
    log_info "Validating user guide documentation..."
    
    local guide_file
    guide_file=$(find "$DOC_DIR" -type f -iname "*user*guide*.md" -o -iname "*guide*.md" | head -n 1)
    
    check
    if [ -n "$guide_file" ]; then
        log_pass "User guide file found: $guide_file"
    else
        log_error "No user guide file found"
        return 1
    fi
    
    local content
    content=$(cat "$guide_file")
    
    # Check for getting started
    check
    if echo "$content" | grep -iq "## Getting Started"; then
        log_pass "Has getting started section"
    else
        log_error "Missing getting started section"
    fi
    
    # Check for screenshots or images
    check
    if echo "$content" | grep -q '!\[.*\]('; then
        log_pass "Contains images/screenshots"
    else
        log_warning "Consider adding screenshots for user guidance"
    fi
    
    # Check for troubleshooting
    check
    if echo "$content" | grep -iq "## Troubleshooting\|## FAQ"; then
        log_pass "Has troubleshooting or FAQ section"
    else
        log_warning "Consider adding troubleshooting section"
    fi
}

# Validation functions for architecture docs
validate_architecture() {
    log_info "Validating architecture documentation..."
    
    local arch_file
    arch_file=$(find "$DOC_DIR" -type f -iname "*architecture*.md" -o -iname "*design*.md" | head -n 1)
    
    check
    if [ -n "$arch_file" ]; then
        log_pass "Architecture file found: $arch_file"
    else
        log_error "No architecture file found"
        return 1
    fi
    
    local content
    content=$(cat "$arch_file")
    
    # Check for system overview
    check
    if echo "$content" | grep -iq "## Overview\|## System Overview"; then
        log_pass "Has system overview"
    else
        log_error "Missing system overview"
    fi
    
    # Check for diagrams
    check
    if echo "$content" | grep -q '!\[.*\]('; then
        log_pass "Contains diagrams"
    else
        log_warning "Consider adding architecture diagrams"
    fi
    
    # Check for components section
    check
    if echo "$content" | grep -iq "## Components"; then
        log_pass "Has components section"
    else
        log_error "Missing components section"
    fi
    
    # Check for design decisions
    check
    if echo "$content" | grep -iq "## Design Decision\|ADR\|Decision"; then
        log_pass "Documents design decisions"
    else
        log_warning "Consider documenting design decisions"
    fi
}

# Main validation logic
echo "========================================"
echo "Documentation Validation"
echo "========================================"
echo "Directory: $DOC_DIR"
echo "Type: $DOC_TYPE"
echo ""

case $DOC_TYPE in
    readme)
        validate_readme
        ;;
    api)
        validate_api
        ;;
    user-guide)
        validate_user_guide
        ;;
    architecture)
        validate_architecture
        ;;
    *)
        echo -e "${RED}Error: Unknown documentation type: $DOC_TYPE${NC}" >&2
        echo "Valid types: readme, api, user-guide, architecture"
        exit 1
        ;;
esac

# Print summary
echo ""
echo "========================================"
echo "Validation Summary"
echo "========================================"
echo -e "Total checks: $TOTAL_CHECKS"
echo -e "${GREEN}Passed: $PASSED_CHECKS${NC}"
echo -e "${RED}Failed: $FAILED_CHECKS${NC}"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
echo ""

# Exit with appropriate code
if [ $FAILED_CHECKS -gt 0 ]; then
    echo -e "${RED}Validation failed${NC}"
    exit 1
else
    echo -e "${GREEN}Validation passed${NC}"
    exit 0
fi
