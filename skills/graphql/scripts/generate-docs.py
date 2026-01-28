#!/usr/bin/env python3
"""
GraphQL Documentation Generator

Generates markdown documentation from GraphQL schema files.
Works cross-platform on Windows, macOS, and Linux.

Usage:
    python generate-docs.py --schema schema.graphql --output docs.md
    python generate-docs.py --schema schema.graphql

Requirements:
    - Python 3.8+
    - graphql-core >= 3.2.0
    
Install dependencies:
    pip install graphql-core
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

try:
    from graphql import (
        build_schema, 
        GraphQLSchema,
        GraphQLObjectType,
        GraphQLInterfaceType,
        GraphQLUnionType,
        GraphQLEnumType,
        GraphQLInputObjectType,
        GraphQLField,
        GraphQLArgument,
        is_scalar_type,
        is_enum_type,
        is_object_type,
        is_interface_type,
        is_union_type,
        is_input_object_type,
    )
except ImportError:
    print("Error: graphql-core is not installed.")
    print("Install it with: pip install graphql-core")
    sys.exit(1)


def format_type(type_obj) -> str:
    """Format a GraphQL type for display"""
    if hasattr(type_obj, 'of_type'):
        inner = format_type(type_obj.of_type)
        if type_obj.__class__.__name__ == 'GraphQLNonNull':
            return f"{inner}!"
        elif type_obj.__class__.__name__ == 'GraphQLList':
            return f"[{inner}]"
    return type_obj.name


def generate_field_docs(field: GraphQLField, indent: int = 0) -> List[str]:
    """Generate documentation for a field"""
    lines = []
    prefix = "  " * indent
    
    # Field signature
    args_str = ""
    if field.args:
        arg_list = [f"{arg.name}: {format_type(arg.type)}" for arg in field.args.values()]
        args_str = f"({', '.join(arg_list)})"
    
    lines.append(f"{prefix}- **{field.name}**{args_str}: `{format_type(field.type)}`")
    
    # Description
    if field.description:
        lines.append(f"{prefix}  - {field.description}")
    
    # Arguments details
    if field.args:
        lines.append(f"{prefix}  - **Arguments:**")
        for arg in field.args.values():
            arg_desc = f"{prefix}    - `{arg.name}`: `{format_type(arg.type)}`"
            if arg.description:
                arg_desc += f" - {arg.description}"
            lines.append(arg_desc)
    
    return lines


def generate_type_docs(schema: GraphQLSchema) -> List[str]:
    """Generate documentation for all types"""
    lines = []
    
    # Get all types
    type_map = schema.type_map
    
    # Separate types by category
    objects = []
    interfaces = []
    unions = []
    enums = []
    inputs = []
    
    for name, type_obj in type_map.items():
        # Skip internal types
        if name.startswith('__'):
            continue
        
        if is_object_type(type_obj) and name not in ['Query', 'Mutation', 'Subscription']:
            objects.append((name, type_obj))
        elif is_interface_type(type_obj):
            interfaces.append((name, type_obj))
        elif is_union_type(type_obj):
            unions.append((name, type_obj))
        elif is_enum_type(type_obj):
            enums.append((name, type_obj))
        elif is_input_object_type(type_obj):
            inputs.append((name, type_obj))
    
    # Document Query type
    if schema.query_type:
        lines.append("## Queries\n")
        if schema.query_type.description:
            lines.append(f"{schema.query_type.description}\n")
        for field_name, field in schema.query_type.fields.items():
            lines.extend(generate_field_docs(field))
        lines.append("")
    
    # Document Mutation type
    if schema.mutation_type:
        lines.append("## Mutations\n")
        if schema.mutation_type.description:
            lines.append(f"{schema.mutation_type.description}\n")
        for field_name, field in schema.mutation_type.fields.items():
            lines.extend(generate_field_docs(field))
        lines.append("")
    
    # Document Subscription type
    if schema.subscription_type:
        lines.append("## Subscriptions\n")
        if schema.subscription_type.description:
            lines.append(f"{schema.subscription_type.description}\n")
        for field_name, field in schema.subscription_type.fields.items():
            lines.extend(generate_field_docs(field))
        lines.append("")
    
    # Document Object types
    if objects:
        lines.append("## Types\n")
        for name, type_obj in sorted(objects):
            lines.append(f"### {name}\n")
            if type_obj.description:
                lines.append(f"{type_obj.description}\n")
            
            lines.append("**Fields:**\n")
            for field_name, field in type_obj.fields.items():
                lines.extend(generate_field_docs(field))
            lines.append("")
    
    # Document Input types
    if inputs:
        lines.append("## Input Types\n")
        for name, type_obj in sorted(inputs):
            lines.append(f"### {name}\n")
            if type_obj.description:
                lines.append(f"{type_obj.description}\n")
            
            lines.append("**Fields:**\n")
            for field_name, field in type_obj.fields.items():
                lines.append(f"- **{field_name}**: `{format_type(field.type)}`")
                if field.description:
                    lines.append(f"  - {field.description}")
            lines.append("")
    
    # Document Enums
    if enums:
        lines.append("## Enums\n")
        for name, type_obj in sorted(enums):
            lines.append(f"### {name}\n")
            if type_obj.description:
                lines.append(f"{type_obj.description}\n")
            
            lines.append("**Values:**\n")
            for value in type_obj.values.values():
                lines.append(f"- `{value.name}`")
                if value.description:
                    lines.append(f"  - {value.description}")
            lines.append("")
    
    # Document Interfaces
    if interfaces:
        lines.append("## Interfaces\n")
        for name, type_obj in sorted(interfaces):
            lines.append(f"### {name}\n")
            if type_obj.description:
                lines.append(f"{type_obj.description}\n")
            
            lines.append("**Fields:**\n")
            for field_name, field in type_obj.fields.items():
                lines.extend(generate_field_docs(field))
            lines.append("")
    
    # Document Unions
    if unions:
        lines.append("## Unions\n")
        for name, type_obj in sorted(unions):
            lines.append(f"### {name}\n")
            if type_obj.description:
                lines.append(f"{type_obj.description}\n")
            
            type_names = [t.name for t in type_obj.types]
            lines.append(f"**Possible types:** {', '.join(type_names)}\n")
    
    return lines


def generate_documentation(schema_path: Path, output_path: Optional[Path] = None) -> bool:
    """Generate documentation from schema file"""
    try:
        # Read schema
        schema_content = schema_path.read_text(encoding='utf-8')
        
        # Build schema
        schema = build_schema(schema_content)
        
        # Generate docs
        lines = [
            f"# GraphQL API Documentation\n",
            f"Generated from `{schema_path.name}`\n",
            "---\n"
        ]
        
        lines.extend(generate_type_docs(schema))
        
        # Write output
        output = "\n".join(lines)
        
        if output_path:
            output_path.write_text(output, encoding='utf-8')
            print(f"✓ Documentation written to: {output_path}")
        else:
            print(output)
        
        return True
        
    except Exception as e:
        print(f"✗ Error generating documentation: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate markdown documentation from GraphQL schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate-docs.py --schema schema.graphql --output api-docs.md
  python generate-docs.py --schema schema.graphql
        """
    )
    
    parser.add_argument(
        '--schema',
        '-s',
        required=True,
        help='Path to GraphQL schema file'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (prints to stdout if not specified)'
    )
    
    args = parser.parse_args()
    
    schema_path = Path(args.schema)
    output_path = Path(args.output) if args.output else None
    
    if not schema_path.exists():
        print(f"✗ Schema file not found: {schema_path}")
        return 1
    
    success = generate_documentation(schema_path, output_path)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
