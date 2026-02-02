#!/usr/bin/env python3
import os
import sys
import json
import glob
from pathlib import Path

def find_feature_directory_candidate(start_path):
    return Path(start_path).absolute()

def check_prerequisites(target_dir):
    target_path = Path(target_dir)
    
    result = {
        "feature_dir": str(target_path),
        "available_docs": [],
        "missing_docs": [],
        "implementation_files": [],
        "test_files": [],
        "checklist_status": "unknown"
    }

    # 1. Check for Required Docs
    required_docs = ["spec.md", "design.md"]
    for doc in required_docs:
        if (target_path / doc).exists():
            result["available_docs"].append(doc)
        else:
            result["missing_docs"].append(doc)

    # 2. Check for Product Level Docs
    repo_root = target_path
    for parent in [target_path] + list(target_path.parents):
        if (parent / ".git").exists():
            repo_root = parent
            break
    
    product_docs = ["docs/architecture.md", "docs/standards.md", "docs/guidelines.md"]
    for pdoc in product_docs:
        if (repo_root / pdoc).exists():
             result["available_docs"].append(str(repo_root / pdoc))
    
    # Check current dir supporting docs
    supporting_docs = ["tasks.md", "data-model.md"]
    for doc in supporting_docs:
        if (target_path / doc).exists():
            result["available_docs"].append(doc)

    # 3. Discover Implementation Files
    exclude_dirs = {'.git', '__pycache__', 'node_modules', 'venv', '.idea', '.vscode', 'skills', 'docs'}
    source_extensions = {'.py', '.js', '.ts', '.java', '.cs', '.cpp', '.h', '.go', '.rs', '.php'}
    test_pattern = ['test', 'spec', 'Tests']

    for root, dirs, files in os.walk(target_path):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            fpath = Path(root) / file
            
            # Skip if file is not relative to target (should not happen with walk)
            try:
                rel_path = fpath.relative_to(target_path)
            except ValueError:
                continue

            if fpath.suffix in source_extensions:
                is_test = False
                for tp in test_pattern:
                    if tp in fpath.name.lower() or tp in str(rel_path).lower():
                        is_test = True
                        break
                
                if is_test:
                    result["test_files"].append(str(rel_path))
                else:
                    result["implementation_files"].append(str(rel_path))

    # 4. Check Checklists
    checklists_dir = target_path / "checklists"
    if checklists_dir.exists() and checklists_dir.is_dir():
        checklist_files = list(checklists_dir.glob("*.md"))
        if checklist_files:
            found_lists = [str(f.relative_to(target_path)) for f in checklist_files]
            result["checklist_status"] = f"Found: {', '.join(found_lists)}"
            result["available_docs"].extend(found_lists)
        else:
             result["checklist_status"] = "No checklists found in checklists/"
    else:
        result["checklist_status"] = "No checklists directory"

    return result

if __name__ == "__main__":
    target = os.getcwd()
    if len(sys.argv) > 1:
        if sys.argv[1] != "--json":
            target = sys.argv[1]

    data = check_prerequisites(target)
    print(json.dumps(data, indent=2))
