#!/usr/bin/env python3
"""
Fix form position - remove the separate section wrapper so form opens directly below button
"""

import os
import glob

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if already has the fix marker
    if "<!-- Form Container Moved Here -->" in content:
        return False

    # Skip index.html as it's already fixed
    if filepath.endswith('/index.html') and '/ny/' not in filepath and '/brands/' not in filepath and '/appliances/' not in filepath:
        return False

    original = content

    # Pattern to match: button div closing, then section closings, then form section opening
    old_pattern = """</button>
</div>
</div>
</section>
</div>
</section>

<!-- Schedule Your Repair Form Section -->
<section style="padding: 60px 0; background: #fff;">
<div class="container" style="max-width: 800px;">"""

    new_pattern = """</button>
</div>
<!-- Form Container Moved Here -->"""

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

    print(f"✅ Fixed form position on {modified} pages")

if __name__ == '__main__':
    main()
