#!/usr/bin/env python3
"""
Purge jsDelivr cache for build.json.
Run this AFTER pushing to GitHub.

Usage:
    python purge.py
"""

import urllib.request


JSDELIVR_PURGE_URL = "https://purge.jsdelivr.net/gh/shellbros/mathlete/app/build.json"


def main():
    print("Purging jsDelivr cache for build.json...")
    try:
        req = urllib.request.Request(JSDELIVR_PURGE_URL)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print(f"✓ Cache purged successfully")
                print(f"  URL: {JSDELIVR_PURGE_URL}")
            else:
                print(f"✗ Unexpected status: {response.status}")
    except Exception as e:
        print(f"✗ Failed to purge: {e}")
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
