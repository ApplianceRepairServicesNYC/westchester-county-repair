#!/usr/bin/env python3
"""
Add FormSubmit configuration hidden fields to forms
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

    # FormSubmit config fields to add after form tag
    formsubmit_config = '''
                        <input type="hidden" name="_subject" value="New Appliance Repair Request - Westchester County">
                        <input type="hidden" name="_captcha" value="false">
                        <input type="hidden" name="_template" value="table">'''

    # Add to scheduleForm
    if 'formsubmit.co' in content and '_captcha' not in content:
        # Add after scheduleForm opening tag
        content = re.sub(
            r'(<form id="scheduleForm"[^>]*>)',
            r'\1' + formsubmit_config,
            content
        )
        # Add after cfContactForm opening tag
        content = re.sub(
            r'(<form id="cfContactForm"[^>]*>)',
            r'\1' + formsubmit_config,
            content
        )

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

    print(f"✅ Added FormSubmit config to {modified} files")

if __name__ == '__main__':
    main()
