#!/usr/bin/env python3
"""
GraphQL Schema Validator

Validates GraphQL schema files for syntax errors and structural issues.
Works cross-platform on Windows, macOS, and Linux.

Usage:
    python validate-schema.py <schema-file>
    python validate-schema.py schema.graphql

Requirements:
    - Python 3.8+
    - graphql-core >= 3.2.0
    
Install dependencies:
    pip install graphql-core
"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple

try:
    from graphql import parse, build_schema, GraphQLError, validate_schema
except ImportError:
    print("Error: graphql-core is not installed.")
    print("Install it with: pip install graphql-core")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def validate_schema_file(schema_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a GraphQL schema file.
    
    Args:
        schema_path: Path to the schema file
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check if file exists
    if not schema_path.exists():
        errors.append(f"Schema file not found: {schema_path}")
        return False, errors
    
    # Read schema file
    try:
        schema_content = schema_path.read_text(encoding='utf-8')
    except Exception as e:
        errors.append(f"Failed to read schema file: {e}")
        return False, errors
    
    # Check if file is empty
    if not schema_content.strip():
        errors.append("Schema file is empty")
        return False, errors
    
    # Parse schema
    try:
        document = parse(schema_content)
    except GraphQLError as e:
        errors.append(f"Syntax error: {e.message}")
        if hasattr(e, 'locations') and e.locations:
            loc = e.locations[0]
            errors.append(f"  at line {loc.line}, column {loc.column}")
        return False, errors
    except Exception as e:
        errors.append(f"Failed to parse schema: {e}")
        return False, errors
    
    # Build and validate schema
    try:
        schema = build_schema(schema_content)
        validation_errors = validate_schema(schema)
        
        if validation_errors:
            for error in validation_errors:
                errors.append(f"Schema error: {error.message}")
            return False, errors
            
    except GraphQLError as e:
        errors.append(f"Schema validation error: {e.message}")
        return False, errors
    except Exception as e:
        errors.append(f"Failed to validate schema: {e}")
        return False, errors
    
    return True, []


def print_success(message: str):
    """Print success message in green"""
    print(f"{Colors.GREEN}✓{Colors.RESET} {message}")


def print_error(message: str):
    """Print error message in red"""
    print(f"{Colors.RED}✗{Colors.RESET} {message}")


def print_info(message: str):
    """Print info message in blue"""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate GraphQL schema files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate-schema.py schema.graphql
  python validate-schema.py path/to/schema.graphql
        """
    )
    parser.add_argument(
        'schema_file',
        type=str,
        help='Path to the GraphQL schema file'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    schema_path = Path(args.schema_file)
    
    print_info(f"Validating schema: {schema_path}")
    print()
    
    is_valid, errors = validate_schema_file(schema_path)
    
    if is_valid:
        print_success("Schema is valid!")
        
        if args.verbose:
            print()
            print_info("Schema file details:")
            print(f"  Path: {schema_path.absolute()}")
            print(f"  Size: {schema_path.stat().st_size} bytes")
            
        return 0
    else:
        print_error("Schema validation failed:")
        print()
        for error in errors:
            print(f"  {error}")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
