#!/usr/bin/env python3
"""
Remove ALL remaining EmailJS references
"""

import os
import re
import glob

FORMSPREE_URL = "https://formspree.io/f/YOUR_FORM_ID"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    original = content

    # Remove script block with emailjs.init inside try/catch
    content = re.sub(
        r'<script>\s*\(function\(\)\s*\{\s*try\s*\{\s*emailjs\.init\(\{[^}]+\}\);\s*\}\s*catch\s*\(error\)\s*\{[^}]+\}\s*\}\)\(\);\s*</script>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove simpler emailjs.init script block
    content = re.sub(
        r'<script>\s*emailjs\.init\(\{[^}]+\}\);\s*</script>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # Replace remaining emailjs.sendForm with Formspree fetch
    content = re.sub(
        r"emailjs\.sendForm\('service_emxksio',\s*'template_tmexlql',\s*this\)",
        f"fetch('{FORMSPREE_URL}', {{method: 'POST', body: new FormData(this), headers: {{'Accept': 'application/json'}}}})",
        content
    )

    # Clean up any .then patterns that still reference emailjs response patterns
    content = re.sub(
        r"\.then\(function\(\)\s*\{",
        ".then(function(response) { if (response.ok) {",
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # Target specific files first
    files_to_check = [
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/refrigerator-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/microwave-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/wine-cooler-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/washer-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/dishwasher-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/cooktop-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/installation-maintenance/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/vent-hood-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/oven-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/appliances/dryer-repair/index.html',
        '/Users/globalaffiliate/westchester-county-repair-edit/ny/index.html',
    ]

    modified = 0
    for filepath in files_to_check:
        if os.path.exists(filepath) and process_file(filepath):
            modified += 1
            print(f"✓ {filepath}")

    print(f"\n✅ Fixed {modified} files")

if __name__ == '__main__':
    main()
