#!/usr/bin/env python3
"""
Remove duplicate schedule button from old location
"""

import os
import glob

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Count buttons
    button_count = content.count('id="scheduleFormToggle"')
    if button_count <= 1:
        return False

    original = content

    # Remove the OLD button location (after </style> and before schedule-form-container)
    # Pattern: </style> then div with button, then schedule-form-container
    old_button_pattern = """</style>
<div style="text-align: center; margin-bottom: 10px;">
<button id="scheduleFormToggle" style="background: linear-gradient(135deg, #003087 0%, #0052cc 100%); color: white; padding: 20px 50px; border: 3px solid #ffc107; border-radius: 12px; font-size: 20px; font-weight: 700; cursor: pointer; transition: all 0.3s; box-shadow: 0 6px 20px rgba(0,48,135,0.3);">&#x1F4C5; Schedule Your Repair Online</button>
</div>
<div class="schedule-form-container" id="scheduleFormContainer">"""

    new_pattern = """</style>
<div class="schedule-form-container" id="scheduleFormContainer">"""

    if old_button_pattern in content:
        content = content.replace(old_button_pattern, new_pattern)

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

    print(f"✅ Removed duplicate buttons from {modified} pages")

if __name__ == '__main__':
    main()
