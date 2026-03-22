#!/usr/bin/env python3
"""
Move the schedule form container to be right below the schedule button
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

    # Skip if already processed (form already moved)
    if "<!-- Form Container Moved Here -->" in content:
        return False

    # Skip if no schedule button or form container
    if 'id="scheduleFormToggle"' not in content or 'id="scheduleFormContainer"' not in content:
        return False

    original = content

    # Extract the form container div (from <div class="schedule-form-container" to closing </div>)
    # Find where form container starts
    form_start_match = re.search(r'<div class="schedule-form-container" id="scheduleFormContainer">', content)
    if not form_start_match:
        return False

    form_start = form_start_match.start()

    # Find the scheduleFormContainer closing - it's followed by </div></section>
    # The pattern is: </form>\n</div>\n</div>\n</section>
    form_end_match = re.search(r'</form>\s*</div>\s*</div>\s*</section>', content[form_start:])
    if not form_end_match:
        return False

    form_end = form_start + form_end_match.end()

    # Extract form container HTML (just the div, not the section wrapper)
    form_container_match = re.search(
        r'(<div class="schedule-form-container" id="scheduleFormContainer">.*?</form>\s*</div>)',
        content,
        re.DOTALL
    )
    if not form_container_match:
        return False

    form_container_html = form_container_match.group(1)

    # Now find where to insert - right after the schedule button div
    button_pattern = r'(<button id="scheduleFormToggle"[^>]*>.*?</button>\s*</div>)'
    button_match = re.search(button_pattern, content)
    if not button_match:
        return False

    # Insert form container after button
    insert_pos = button_match.end()

    # Build new content
    # 1. Remove the old form container from its section
    new_content = re.sub(
        r'<div class="schedule-form-container" id="scheduleFormContainer">.*?</form>\s*</div>\s*</div>\s*</section>',
        '</div>\n</section>',
        content,
        flags=re.DOTALL,
        count=1
    )

    # 2. Insert form container after button
    new_content = re.sub(
        r'(<button id="scheduleFormToggle"[^>]*>.*?</button>\s*</div>)',
        r'\1\n<!-- Form Container Moved Here -->\n' + form_container_html.replace('\\', '\\\\').replace('\n', '\n'),
        new_content,
        count=1
    )

    if new_content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    # Start with just index.html to test
    test_file = '/Users/globalaffiliate/westchester-county-repair-edit/index.html'
    if process_file(test_file):
        print(f"✓ Fixed index.html")
    else:
        print("Could not process index.html")

if __name__ == '__main__':
    main()
