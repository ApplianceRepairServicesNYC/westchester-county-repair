#!/usr/bin/env python3
"""
Fix schedule form header h2 - remove duplicate color and ensure !important
"""

import os
import glob

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    original = content

    # Fix double color declaration
    bad_pattern = """.schedule-form-header h2 {
 color: white !important;
 color: white;"""

    good_pattern = """.schedule-form-header h2 {
 color: white !important;"""

    if bad_pattern in content:
        content = content.replace(bad_pattern, good_pattern)

    # Also fix if only has color: white without !important
    old_pattern = """.schedule-form-header h2 {
 color: white;"""

    new_pattern = """.schedule-form-header h2 {
 color: white !important;"""

    if old_pattern in content and "color: white !important" not in content:
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

    print(f"✅ Fixed {modified} pages")

if __name__ == '__main__':
    main()
