#!/usr/bin/env python3
import argparse
from pathlib import Path

def find_root():
    """Find the repository root."""
    cwd = Path.cwd()
    for path in [cwd] + list(cwd.parents):
        if (path / ".git").exists() or (path / "pyproject.toml").exists():
            return path
    return cwd

def update_agent_context(agent_type=None):
    root_dir = find_root()
    docs_dir = root_dir / "docs"
    arch_doc = docs_dir / "architecture.md"
    
    if not arch_doc.exists():
        print(f"Warning: Architecture document not found at {arch_doc}")
        return

    # Map agents to their likely configuration files
    agent_configs = {
        "copilot": [".github/copilot-instructions.md"],
        "cursor-agent": [".cursorrules"],
        "windsurf": [".windsurfrules"],
    }

    files_to_update = []
    if agent_type:
        if agent_type in agent_configs:
            files_to_update.extend(agent_configs[agent_type])
        else:
            print(f"Unknown agent type: {agent_type}. Scanning for common configs.")
            for configs in agent_configs.values():
                files_to_update.extend(configs)
    else:
        for configs in agent_configs.values():
            files_to_update.extend(configs)
            
    files_to_update = list(set(files_to_update))
    
    updated_count = 0
    
    for relative_path in files_to_update:
        config_path = root_dir / relative_path
        if config_path.exists():
            content = config_path.read_text()
            
            if "docs/architecture.md" not in content:
                print(f"Updating {relative_path}...")
                addition = "\n\n# Architecture Context\nPlease refer to [System Architecture](docs/architecture.md) for architectural decisions and patterns.\n"
                
                # Append to file
                with open(config_path, "a") as f:
                    f.write(addition)
                print(f"Added architecture reference to {relative_path}")
                updated_count += 1
            else:
                print(f"{relative_path} already references architecture documentation.")

    if updated_count == 0:
        print("No agent context files required updates.")
    else:
        print(f"Updated {updated_count} agent context files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update agent context with architecture links")
    parser.add_argument("agent_type", nargs="?", help="Specific agent type to update")
    args = parser.parse_args()
    
    update_agent_context(args.agent_type)
