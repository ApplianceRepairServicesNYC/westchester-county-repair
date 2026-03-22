#!/usr/bin/env python3
"""
Remove EmailJS and replace with Formspree (free form submission)
"""

import os
import re
import glob

# Formspree endpoint - UPDATE THIS with your actual form ID
FORMSPREE_URL = "https://formspree.io/f/YOUR_FORM_ID"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    original = content

    # 1. Remove EmailJS CDN script tag
    content = re.sub(
        r'<script\s+src="https://cdn\.jsdelivr\.net/npm/@emailjs/browser@4/dist/email\.min\.js"\s*></script>\s*',
        '',
        content
    )

    # 2. Remove EmailJS init block
    content = re.sub(
        r'<script>\s*emailjs\.init\(\{[^}]+\}\);\s*</script>\s*',
        '',
        content
    )

    # 3. Remove inline minified EmailJS script (the big one)
    content = re.sub(
        r'<script>var emailjs=function\(e\)\{[^<]+emailjs\.init\(\{publicKey:[\'"][^\'"]+[\'"]\}\);</script>\s*',
        '',
        content
    )

    # 4. Replace emailjs.sendForm calls with Formspree fetch
    # For scheduleForm
    content = re.sub(
        r"emailjs\.sendForm\('service_emxksio',\s*'template_tmexlql',\s*this\)\s*\.then\(function\(\)\s*\{",
        "fetch('" + FORMSPREE_URL + "', {method: 'POST', body: new FormData(this), headers: {'Accept': 'application/json'}}).then(function(response) { if (response.ok) {",
        content
    )

    # 5. Fix the catch block
    content = re.sub(
        r"\}\)\s*\.catch\(function\(\)\s*\{",
        "} }).catch(function() {",
        content
    )

    # 6. Add form action and method as backup
    content = re.sub(
        r'<form\s+id="scheduleForm"\s+class="schedule-form">',
        f'<form id="scheduleForm" class="schedule-form" action="{FORMSPREE_URL}" method="POST">',
        content
    )
    content = re.sub(
        r'<form\s+id="cfContactForm"\s+class="cf-contact-form">',
        f'<form id="cfContactForm" class="cf-contact-form" action="{FORMSPREE_URL}" method="POST">',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # Find all HTML files
    html_files = glob.glob('/Users/globalaffiliate/westchester-county-repair-edit/**/*.html', recursive=True)

    modified = 0
    for filepath in html_files:
        if process_file(filepath):
            modified += 1
            print(f"✓ {filepath}")

    print(f"\n✅ Modified {modified} files")
    print(f"\n⚠️  IMPORTANT: Replace YOUR_FORM_ID with your Formspree form ID")
    print(f"   Get free form at: https://formspree.io/")

if __name__ == '__main__':
    main()
