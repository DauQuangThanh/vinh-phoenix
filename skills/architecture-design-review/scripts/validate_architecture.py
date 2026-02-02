#!/usr/bin/env python3
import os
import json
import glob
import argparse
from pathlib import Path

def validate_architecture(root_dir):
    root = Path(root_dir)
    docs_dir = root / "docs"
    
    results = {
        "architecture_file": None,
        "adr_files": [],
        "adr_count": 0,
        "ground_rules_file": None,
        "specs_files": [],
        "specs_count": 0,
        "deployment_guide": None,
        "available_docs": []
    }

    # Check architecture.md
    arch_file = docs_dir / "architecture.md"
    if arch_file.exists():
        results["architecture_file"] = str(arch_file)
        results["available_docs"].append("architecture.md")

    # Check ADRs
    adr_dir = docs_dir / "adr"
    if adr_dir.exists():
        adrs = list(adr_dir.glob("*.md"))
        results["adr_files"] = [str(f) for f in adrs]
        results["adr_count"] = len(adrs)
        if results["adr_count"] > 0:
            results["available_docs"].append("adr/")

    # Check ground-rules.md
    ground_rules = docs_dir / "ground-rules.md"
    if ground_rules.exists():
        results["ground_rules_file"] = str(ground_rules)
        results["available_docs"].append("ground-rules.md")
    
    # Check deployment-guide.md
    deployment = docs_dir / "deployment-guide.md"
    if deployment.exists():
        results["deployment_guide"] = str(deployment)
        results["available_docs"].append("deployment-guide.md")

    # Check specs
    specs_dir = root / "specs"
    if specs_dir.exists():
        specs = list(specs_dir.glob("**/spec.md"))
        results["specs_files"] = [str(f) for f in specs]
        results["specs_count"] = len(specs)
        if results["specs_count"] > 0:
            results["available_docs"].append("specs/")

    return results

def main():
    parser = argparse.ArgumentParser(description="Validate architecture documentation structure.")
    parser.add_argument("root_dir", nargs="?", default=".", help="Root directory of the repository")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    data = validate_architecture(args.root_dir)
    
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"Architecture File: {data['architecture_file'] or 'Not Found'}")
        print(f"ADR Files: {data['adr_count']}")
        print(f"Ground Rules: {data['ground_rules_file'] or 'Not Found'}")
        print(f"Deployment Guide: {data['deployment_guide'] or 'Not Found'}")
        print(f"Specs Files: {data['specs_count']}")

if __name__ == "__main__":
    main()
