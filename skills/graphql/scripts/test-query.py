#!/usr/bin/env python3
"""
GraphQL Query Tester

Tests GraphQL queries against an endpoint with support for variables and headers.
Works cross-platform on Windows, macOS, and Linux.

Usage:
    python test-query.py --endpoint URL --query "query { ... }"
    python test-query.py --endpoint URL --query-file query.graphql --variables '{"id": "123"}'
    python test-query.py --endpoint URL --query-file query.graphql --token "Bearer xxx"

Requirements:
    - Python 3.8+
    - requests >= 2.28.0
    
Install dependencies:
    pip install requests
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import requests
except ImportError:
    print("Error: requests library is not installed.")
    print("Install it with: pip install requests")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def execute_query(
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Execute a GraphQL query against an endpoint.
    
    Args:
        endpoint: GraphQL endpoint URL
        query: GraphQL query string
        variables: Optional query variables
        headers: Optional HTTP headers
        
    Returns:
        Response data as dictionary
    """
    payload = {
        "query": query
    }
    
    if variables:
        payload["variables"] = variables
    
    default_headers = {
        "Content-Type": "application/json"
    }
    
    if headers:
        default_headers.update(headers)
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=default_headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "errors": [
                {
                    "message": f"Request failed: {str(e)}"
                }
            ]
        }


def print_success(message: str):
    """Print success message in green"""
    print(f"{Colors.GREEN}✓{Colors.RESET} {message}")


def print_error(message: str):
    """Print error message in red"""
    print(f"{Colors.RED}✗{Colors.RESET} {message}")


def print_warning(message: str):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")


def print_info(message: str):
    """Print info message in blue"""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")


def print_json(data: Any, indent: int = 2):
    """Print formatted JSON with syntax highlighting"""
    json_str = json.dumps(data, indent=indent)
    print(f"{Colors.CYAN}{json_str}{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Test GraphQL queries against an endpoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple query
  python test-query.py --endpoint http://localhost:4000/graphql --query "{ users { id name } }"
  
  # Query from file with variables
  python test-query.py --endpoint http://localhost:4000/graphql \\
    --query-file query.graphql \\
    --variables '{"userId": "123"}'
  
  # With authentication token
  python test-query.py --endpoint http://localhost:4000/graphql \\
    --query-file query.graphql \\
    --token "Bearer your-jwt-token"
  
  # With custom headers
  python test-query.py --endpoint http://localhost:4000/graphql \\
    --query-file query.graphql \\
    --header "Authorization: Bearer token" \\
    --header "X-API-Key: key123"
        """
    )
    
    parser.add_argument(
        '--endpoint',
        '-e',
        required=True,
        help='GraphQL endpoint URL'
    )
    
    query_group = parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument(
        '--query',
        '-q',
        help='GraphQL query string'
    )
    query_group.add_argument(
        '--query-file',
        '-f',
        help='Path to file containing GraphQL query'
    )
    
    parser.add_argument(
        '--variables',
        '-v',
        help='Query variables as JSON string'
    )
    parser.add_argument(
        '--variables-file',
        help='Path to file containing variables JSON'
    )
    parser.add_argument(
        '--token',
        '-t',
        help='Authorization token (will be added as Authorization header)'
    )
    parser.add_argument(
        '--header',
        '-H',
        action='append',
        dest='headers',
        help='Custom header in format "Key: Value" (can be used multiple times)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Get query
    if args.query:
        query = args.query
    else:
        query_path = Path(args.query_file)
        if not query_path.exists():
            print_error(f"Query file not found: {query_path}")
            return 1
        try:
            query = query_path.read_text(encoding='utf-8')
        except Exception as e:
            print_error(f"Failed to read query file: {e}")
            return 1
    
    # Get variables
    variables = None
    if args.variables:
        try:
            variables = json.loads(args.variables)
        except json.JSONDecodeError as e:
            print_error(f"Invalid JSON in variables: {e}")
            return 1
    elif args.variables_file:
        var_path = Path(args.variables_file)
        if not var_path.exists():
            print_error(f"Variables file not found: {var_path}")
            return 1
        try:
            variables = json.loads(var_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            print_error(f"Invalid JSON in variables file: {e}")
            return 1
    
    # Build headers
    headers = {}
    if args.token:
        headers['Authorization'] = args.token
    
    if args.headers:
        for header in args.headers:
            if ':' not in header:
                print_warning(f"Skipping invalid header format: {header}")
                continue
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    
    # Print request details if verbose
    if args.verbose:
        print_info("Request details:")
        print(f"  Endpoint: {args.endpoint}")
        print(f"  Query length: {len(query)} characters")
        if variables:
            print(f"  Variables: {json.dumps(variables)}")
        if headers:
            print(f"  Headers: {', '.join(headers.keys())}")
        print()
    
    print_info("Executing query...")
    print()
    
    # Execute query
    result = execute_query(args.endpoint, query, variables, headers)
    
    # Check for errors
    if "errors" in result:
        print_error("Query returned errors:")
        print()
        print_json(result["errors"])
        print()
        
        # Still show data if present
        if "data" in result:
            print_warning("Partial data returned:")
            print()
            print_json(result["data"])
        
        return 1
    
    # Show success
    if "data" in result:
        print_success("Query executed successfully!")
        print()
        print_json(result["data"])
        return 0
    else:
        print_warning("No data or errors in response")
        print()
        print_json(result)
        return 1


if __name__ == "__main__":
    sys.exit(main())
