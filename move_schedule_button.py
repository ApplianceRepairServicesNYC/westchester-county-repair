#!/usr/bin/env python3
"""
Move schedule button to be inside service areas section on all pages
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

    # Skip if already moved (has the comment)
    if "Schedule Button moved here" in content:
        return False

    # Skip if no schedule button
    if 'id="scheduleFormToggle"' not in content:
        return False

    original = content

    # Pattern 1: Add button after sa-dropdown-container closing divs
    # Look for the end of dropdown content before </section>
    old_pattern1 = """</div>
</div>
</section>
</div>
</section>

<!-- Schedule Your Repair Form Section -->"""

    new_pattern1 = """</div>
<!-- Schedule Button moved here -->
<div style="text-align: center; margin-top: 30px; margin-bottom: 10px;">
<button id="scheduleFormToggle" style="background: linear-gradient(135deg, #003087 0%, #0052cc 100%); color: white; padding: 20px 50px; border: 3px solid #ffc107; border-radius: 12px; font-size: 20px; font-weight: 700; cursor: pointer; transition: all 0.3s; box-shadow: 0 6px 20px rgba(0,48,135,0.3);">📅 Schedule Your Repair Online</button>
</div>
</div>
</section>
</div>
</section>

<!-- Schedule Your Repair Form Section -->"""

    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_pattern1)

    # Pattern 2: Remove old button location
    old_button = """</style>
<div style="text-align: center; margin-bottom: 10px;">
<button id="scheduleFormToggle" style="background: linear-gradient(135deg, #003087 0%, #0052cc 100%); color: white; padding: 20px 50px; border: 3px solid #ffc107; border-radius: 12px; font-size: 20px; font-weight: 700; cursor: pointer; transition: all 0.3s; box-shadow: 0 6px 20px rgba(0,48,135,0.3);">📅 Schedule Your Repair Online</button>
</div>
<div class="schedule-form-container" id="scheduleFormContainer">"""

    new_button = """</style>
<div class="schedule-form-container" id="scheduleFormContainer">"""

    if old_button in content:
        content = content.replace(old_button, new_button)

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

    print(f"✅ Moved schedule button on {modified} pages")

if __name__ == '__main__':
    main()
