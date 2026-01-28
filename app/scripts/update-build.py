#!/usr/bin/env python3
"""
Updates build.json with the current git commit hash and increments build number.
Run this AFTER committing synced files.

Usage:
    python update-build.py           # Update build.json
    python update-build.py --dry-run # Preview changes
"""

import json
import subprocess
import sys
from pathlib import Path

DRY_RUN = '--dry-run' in sys.argv or '-d' in sys.argv


def get_git_hash():
    """Get the current git commit hash."""
    result = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    raise RuntimeError(f"Failed to get git hash: {result.stderr}")


def main():
    script_dir = Path(__file__).resolve().parent
    build_file = script_dir.parent / 'build.json'

    # Get current hash
    git_hash = get_git_hash()
    print(f"Current git hash: {git_hash[:8]}...")

    # Read current build.json
    with open(build_file, 'r') as f:
        data = json.load(f)

    old_version = data.get('build_version', '')
    old_number = data.get('build_number', 0)

    # Check if version changed
    if old_version == git_hash:
        print(f"No change: build_version is already {git_hash[:8]}...")
        print(f"  build_number remains: {old_number}")
        return

    # Update values (only increment build_number if version changed)
    data['build_version'] = git_hash
    data['build_number'] = old_number + 1

    if DRY_RUN:
        print(f"[DRY-RUN] Would update {build_file}:")
        print(f"  build_version: {old_version[:8] if old_version else '(empty)'} → {git_hash[:8]}")
        print(f"  build_number: {old_number} → {old_number + 1}")
    else:
        with open(build_file, 'w') as f:
            json.dump(data, f, indent='\t')
            f.write('\n')
        print(f"✓ Updated build.json")
        print(f"  build_version: {git_hash}")
        print(f"  build_number: {old_number + 1}")


if __name__ == '__main__':
    main()
