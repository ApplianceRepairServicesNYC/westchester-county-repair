#!/usr/bin/env python3
"""
Fix form JavaScript to use correct field names and proper submit handling
"""

import os
import re
import glob

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    original = content

    # Fix user_email references to email
    content = content.replace('this.user_email.value', 'this.email.value')

    # Fix the messy fetch structure - make it cleaner
    # Old pattern with broken structure
    old_pattern = r"fetch\('https://formsubmit\.co/insuranceappliance@gmail\.com', \{method: 'POST', body: new FormData\(this\), headers: \{'Accept': 'application/json'\}\}\)\.then\(function\(response\) \{ if \(response\.ok\) \{"

    new_pattern = """fetch('https://formsubmit.co/insuranceappliance@gmail.com', {
                        method: 'POST',
                        body: new FormData(this),
                        headers: {'Accept': 'application/json'}
                    }).then(function(response) {
                        if (response.ok) {"""

    content = re.sub(old_pattern, new_pattern, content)

    # Fix the closing of the if/then block
    content = content.replace("} }).catch(function()", "}\n                    }).catch(function()")

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

    print(f"✅ Fixed JavaScript in {modified} files")

if __name__ == '__main__':
    main()
