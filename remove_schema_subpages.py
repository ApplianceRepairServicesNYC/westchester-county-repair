#!/usr/bin/env python3
"""
Remove JSON-LD Schema from all subpages, keep only on homepage.
"""

import re
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/westchester-county-repair')

def remove_schema(file_path):
    """Remove JSON-LD script block from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Pattern to match the entire JSON-LD script block
    pattern = r'\s*<script type="application/ld\+json">[\s\S]*?</script>\s*'

    new_content = re.sub(pattern, '\n', content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    print(f"Found {len(html_files)} HTML files")

    # Skip homepage
    homepage = BASE_DIR / 'index.html'

    removed = 0
    for html_file in html_files:
        # Keep Schema on homepage only
        if html_file == homepage:
            print(f"KEEPING Schema on: {html_file.relative_to(BASE_DIR)}")
            continue

        # Skip non-content directories
        if 'assets' in str(html_file):
            continue

        if remove_schema(html_file):
            removed += 1

    print(f"\nRemoved Schema from {removed} subpages")
    print("Kept Schema on homepage only")


if __name__ == "__main__":
    main()
