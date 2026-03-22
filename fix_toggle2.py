#!/usr/bin/env python3
"""
Add missing scheduleFormToggle event handler to pages - v2
"""

import os
import re
import glob

toggle_handler = """
 const scheduleFormToggle = document.getElementById('scheduleFormToggle');
 const scheduleFormContainer = document.getElementById('scheduleFormContainer');
 if (scheduleFormToggle && scheduleFormContainer) {
 scheduleFormToggle.addEventListener('click', function() {
 scheduleFormContainer.classList.toggle('active');
 if (scheduleFormContainer.classList.contains('active')) {
 setTimeout(function() {
 scheduleFormContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
 }, 100);
 }
 });
 }

 const cfContactForm"""

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if already has the handler
    if "scheduleFormToggle.addEventListener" in content:
        return False

    # Skip if no toggle button exists
    if 'id="scheduleFormToggle"' not in content:
        return False

    original = content

    # Replace pattern with flexible whitespace
    content = re.sub(
        r'(\s*)\n(\s*)const cfContactForm',
        toggle_handler,
        content,
        count=1
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    html_files = glob.glob('/Users/globalaffiliate/westchester-county-repair-edit/brands/*/index.html')

    modified = 0
    for filepath in html_files:
        if process_file(filepath):
            modified += 1
            print(f"✓ {os.path.basename(os.path.dirname(filepath))}")

    print(f"\n✅ Fixed {modified} brand pages")

if __name__ == '__main__':
    main()
