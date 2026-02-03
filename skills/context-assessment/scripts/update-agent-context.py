#!/usr/bin/env python3
"""
Update agent context files with assessment findings.

Usage: python3 scripts/update-agent-context.py [agent-type]

Platforms: Windows, macOS, Linux
Requirements: Python 3.8+
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

def find_repo_root(start_path: Path) -> Path:
    """Find repository root by searching upward for .git directory."""
    current = start_path.resolve()
    while current != current.parent:  # Stop at filesystem root
        if (current / ".git").is_dir():
            return current
        current = current.parent
    return start_path.resolve()

def log_info(message: str):
    """Log info message."""
    print(f"\033[0;32mINFO:\033[0m {message}")

def log_warn(message: str):
    """Log warning message."""
    print(f"\033[1;33mWARNING:\033[0m {message}")

def log_error(message: str):
    """Log error message."""
    print(f"\033[0;31mERROR:\033[0m {message}", file=sys.stderr)

def get_agent_files(repo_root: Path):
    """Get mapping of agent types to their file paths."""
    return {
        "claude": repo_root / "CLAUDE.md",
        "gemini": repo_root / "GEMINI.md",
        "copilot": repo_root / ".github" / "agents" / "copilot-instructions.md",
        "cursor-agent": repo_root / ".cursor" / "rules" / "phoenix-rules.mdc",
        "qwen": repo_root / "QWEN.md",
        "opencode": repo_root / "AGENTS.md",
        "codex": repo_root / "AGENTS.md",
        "windsurf": repo_root / ".windsurf" / "rules" / "phoenix-rules.md",
        "kilocode": repo_root / ".kilocode" / "rules" / "phoenix-rules.md",
        "auggie": repo_root / ".augment" / "rules" / "phoenix-rules.md",
        "roo": repo_root / ".roo" / "rules" / "phoenix-rules.md",
        "codebuddy": repo_root / "CODEBUDDY.md",
        "amp": repo_root / "AGENTS.md",
        "shai": repo_root / "SHAI.md",
        "q": repo_root / "AGENTS.md",
        "bob": repo_root / "AGENTS.md",
        "jules": repo_root / "AGENTS.md",
        "qoder": repo_root / "QODER.md",
        "antigravity": repo_root / "AGENTS.md",
    }

def extract_summary(assessment_file: Path) -> str:
    """Extract key findings summary from assessment file."""
    try:
        content = assessment_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Assessment file not found: {assessment_file}")
    
    lines = content.split("\n")
    summary_lines = []
    
    # Extract technical health score
    score_pattern = r"\*\*Technical Health Score\*\*: (\d+)/100"
    score_match = re.search(score_pattern, content)
    score = score_match.group(1) if score_match else None
    
    # Extract key findings (first 3 bullet points)
    findings = []
    in_findings_section = False
    
    for line in lines:
        if line.strip() == "**Key Findings**:":
            in_findings_section = True
            continue
        elif line.startswith("**") and in_findings_section:
            break
        elif in_findings_section and line.strip().startswith("- "):
            findings.append(f"  • {line.strip()[2:]}")
            if len(findings) >= 3:
                break
    
    # Build summary
    summary_lines.append("## Context Assessment Summary")
    summary_lines.append("")
    summary_lines.append(f"**Assessment Date**: {datetime.now().strftime('%Y-%m-%d')}")
    if score:
        summary_lines.append(f"**Technical Health Score**: {score}/100")
    summary_lines.append("")
    if findings:
        summary_lines.append("**Key Findings**:")
        summary_lines.extend(findings)
    summary_lines.append("")
    summary_lines.append("**Full Assessment**: See `docs/context-assessment.md`")
    summary_lines.append("")
    
    return "\n".join(summary_lines)

def update_agent_file(agent_key: str, agent_file: Path, summary: str):
    """Update a single agent file with context assessment summary."""
    try:
        content = agent_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        log_warn(f"Agent file not found: {agent_file} (skipping {agent_key})")
        return
    
    log_info(f"Updating {agent_key} context at {agent_file}")
    
    start_marker = "<!-- CONTEXT_ASSESSMENT_START -->"
    end_marker = "<!-- CONTEXT_ASSESSMENT_END -->"
    
    if start_marker in content:
        # Update existing section
        lines = content.split("\n")
        new_lines = []
        skip = False
        
        for line in lines:
            if line.strip() == start_marker:
                new_lines.append(line)
                new_lines.extend(summary.split("\n"))
                skip = True
            elif line.strip() == end_marker:
                skip = False
            elif not skip:
                new_lines.append(line)
        
        new_content = "\n".join(new_lines)
    else:
        # Append new section
        new_content = content.rstrip() + "\n\n"
        new_content += start_marker + "\n"
        new_content += summary + "\n"
        new_content += end_marker + "\n"
    
    # Write back to file
    agent_file.write_text(new_content, encoding="utf-8")
    log_info(f"✓ Updated context assessment section in {agent_key}")

def main():
    parser = argparse.ArgumentParser(
        description="Update agent context files with assessment findings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/update-agent-context.py
  python3 scripts/update-agent-context.py claude
  python3 scripts/update-agent-context.py copilot
        """
    )
    parser.add_argument(
        "agent_type",
        nargs="?",
        help="Specific agent type to update (optional)"
    )
    
    args = parser.parse_args()
    
    # Find repository root
    repo_root = find_repo_root(Path.cwd())
    context_assessment = repo_root / "docs" / "context-assessment.md"
    
    # Validate environment
    if not context_assessment.is_file():
        log_error(f"Context assessment not found at {context_assessment}")
        log_info("Run setup-context-assessment.py first")
        return 1
    
    # Get agent files mapping
    agent_files = get_agent_files(repo_root)
    
    try:
        # Extract summary
        summary = extract_summary(context_assessment)
        
        if args.agent_type:
            # Update specific agent
            agent_type = args.agent_type.lower()
            if agent_type not in agent_files:
                log_error(f"Unknown agent type: {agent_type}")
                log_info(f"Supported agents: {', '.join(agent_files.keys())}")
                return 1
            update_agent_file(agent_type, agent_files[agent_type], summary)
        else:
            # Update all existing agent files
            updated = 0
            for agent_key, agent_file in agent_files.items():
                if agent_file.is_file():
                    update_agent_file(agent_key, agent_file, summary)
                    updated += 1
            
            if updated == 0:
                log_warn("No agent files found in repository")
                log_info("Create an agent file first, then run this script")
            else:
                log_info(f"✓ Updated {updated} agent file(s)")
        
        log_info("✓ Agent context update complete")
        return 0
        
    except Exception as e:
        log_error(f"Failed to update agent context: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())