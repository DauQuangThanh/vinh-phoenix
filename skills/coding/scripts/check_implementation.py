#!/usr/bin/env python3
import os
import sys
import argparse
import json
from pathlib import Path

def check_implementation(feature_dir_str, output_json=False):
    feature_dir = Path(feature_dir_str).resolve()
    
    if not feature_dir.exists():
        if output_json:
            print(json.dumps({"error": f"Directory not found: {feature_dir}"}))
        else:
            print(f"Error: Directory not found: {feature_dir}")
        return False

    required_docs = ["tasks.md", "design.md"]
    optional_docs = [
        "spec.md", 
        "data-model.md",
        "research.md"
    ]
    product_docs = [
        "docs/architecture.md", 
        "docs/standards.md"
    ]
    directories = ["contracts", "checklists"]

    result = {
        "FEATURE_DIR": str(feature_dir),
        "AVAILABLE_DOCS": [],
        "MISSING_REQUIRED": [],
        "TASKS_FILE": None,
        "CHECKLIST_STATUS": "Not Found",
        "CHECKLISTS": []
    }

    # Check Required Docs
    for doc in required_docs:
        doc_path = feature_dir / doc
        if doc_path.exists():
            result["AVAILABLE_DOCS"].append(doc)
            if doc == "tasks.md":
                result["TASKS_FILE"] = str(doc_path)
        else:
            result["MISSING_REQUIRED"].append(doc)

    # Check Optional Docs
    for doc in optional_docs:
        if (feature_dir / doc).exists():
            result["AVAILABLE_DOCS"].append(doc)

    # Check Product Docs
    for doc in product_docs:
        if (feature_dir / doc).exists():
             result["AVAILABLE_DOCS"].append(doc)

    # Check Checklists
    checklists_dir = feature_dir / "checklists"
    if checklists_dir.exists() and checklists_dir.is_dir():
        result["CHECKLIST_STATUS"] = "Found"
        checklists = []
        for f in checklists_dir.glob("*"):
            if f.is_file():
                checklists.append(f.name)
        result["CHECKLISTS"] = checklists

    if output_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Implementation Check for: {feature_dir}")
        print("-" * 40)
        print(f"Required Documents Found: {[d for d in result['AVAILABLE_DOCS'] if d in required_docs]}")
        if result["MISSING_REQUIRED"]:
            print(f"MISSING REQUIRED DOCUMENTS: {result['MISSING_REQUIRED']}")
            print("  - tasks.md: Detailed implementation tasks")
            print("  - design.md: Technical design and architecture")
        print(f"Optional Documents Found: {[d for d in result['AVAILABLE_DOCS'] if d in optional_docs]}")
        print(f"Product Documents Found: {[d for d in result['AVAILABLE_DOCS'] if d in product_docs]}")
        
        if result["CHECKLIST_STATUS"] == "Found":
            print(f"Checklists Found ({len(result['CHECKLISTS'])}): {', '.join(result['CHECKLISTS'])}")
        else:
            print("No checklists found.")

    return len(result["MISSING_REQUIRED"]) == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check implementation prerequisites.")
    parser.add_argument("path", nargs="?", default=".", help="Path to feature directory")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    success = check_implementation(args.path, args.json)
    if not success and not args.json:
        sys.exit(1)
