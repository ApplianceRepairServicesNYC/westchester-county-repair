#!/usr/bin/env python3
"""
Fix schedule form header h2 to have white text
"""

import os
import glob

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if already fixed
    if "color: white !important;" in content and ".schedule-form-header h2" in content:
        return False

    original = content

    # Fix the h2 color
    old_pattern = """.schedule-form-header h2 {
 color: white;"""

    new_pattern = """.schedule-form-header h2 {
 color: white !important;"""

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    html_files = glob.glob('/Users/globalaffiliate/westchester-county-repair-edit/**/*.html', recursive=True)

    modified = 0
    for filepath in html_files:
        if process_file(filepath):
            modified += 1

    print(f"✅ Fixed white text on {modified} pages")

if __name__ == '__main__':
    main()
