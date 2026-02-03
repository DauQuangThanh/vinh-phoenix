#!/usr/bin/env python3
"""
Next.js Mockup Prerequisites Checker
"""

import subprocess
import sys

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except:
        return "", "", 1

def main():
    print("Next.js Mockup - Prerequisites Check")
    print("=" * 45)
    
    # Check Node.js
    stdout, stderr, code = run_command(["node", "--version"])
    if code == 0:
        version = stdout.lstrip("v")
        print(f"[OK] Node.js v{version} detected")
    else:
        print("[FAIL] Node.js not found")
        sys.exit(1)
    
    # Check pnpm
    stdout, stderr, code = run_command(["pnpm", "--version"])
    if code == 0:
        print(f"[OK] pnpm v{stdout} detected (recommended)")
    else:
        # Check npm
        stdout, stderr, code = run_command(["npm", "--version"])
        if code == 0:
            print(f"[OK] npm v{stdout} detected")
        else:
            print("[FAIL] No package manager found")
            sys.exit(1)
    
    print("[OK] All prerequisites met. Ready to create Next.js mockups!")

if __name__ == "__main__":
    main()
