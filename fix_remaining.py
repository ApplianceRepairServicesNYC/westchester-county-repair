#!/usr/bin/env python3
"""
Fix remaining pages with old fetch code
"""

import os
import re

files_to_fix = [
    '/Users/globalaffiliate/westchester-county-repair-edit/appliances/vent-hood-repair/index.html',
    '/Users/globalaffiliate/westchester-county-repair-edit/repairs/refrigerator-compressor-replacement/index.html',
    '/Users/globalaffiliate/westchester-county-repair-edit/troubleshooting/appliance-troubleshooting/index.html'
]

for filepath in files_to_fix:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    original = content

    # Remove replyToField line
    content = re.sub(r"document\.getElementById\('replyToField'\)\.value = email;\s*", '', content)

    # Replace fetch block with native form setup
    # Find the fetch pattern and replace with redirect setup
    old_fetch = r"""fetch\('https://formsubmit\.co/insuranceappliance@gmail\.com', \{method: 'POST', body: new FormData\(this\), headers: \{'Accept': 'application/json'\}\}\)
\s*\.then\(\(\) => \{
\s*console\.log\('Form submission successful, email:', email\);
\s*this\.reset\(\);
\s*document\.getElementById\('cfContactFormSection'\)\.classList\.remove\('active'\);
\s*document\.getElementById\('successMessage'\)\.innerHTML = ` <strong>Thank you!</strong><br><br> Your request has been sent\.<br><br> We will contact you at<br><strong>\$\{email\}</strong><br> within the next 30 minutes\. `;
\s*document\.getElementById\('cfSuccessModal'\)\.classList\.add\('active'\);
\s*document\.getElementById\('cfModalOverlay'\)\.classList\.add\('active'\);
\s*\}\)
\s*\.catch\(\(error\) => \{
\s*console\.error\('Form submission failed:', error\);
\s*alert\('Failed to send\. Please try again or call us\.'\);
\s*\}\);"""

    # Remove e.preventDefault and the entire fetch handler
    content = re.sub(r"e\.preventDefault\(\);\s*console\.log\('Form submitted \(mobile:'[^;]+;\s*const email = this\.email\.value\.trim\(\);",
                     "// Form submits natively", content)

    # Remove the fetch call entirely
    content = re.sub(old_fetch, "// Native form POST", content, flags=re.DOTALL)

    # Simpler approach - just remove the problematic lines
    content = content.replace("document.getElementById('replyToField').value = email;", "")
    content = content.replace("fetch('https://formsubmit.co/insuranceappliance@gmail.com', {method: 'POST', body: new FormData(this), headers: {'Accept': 'application/json'}})", "this.submit()")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {filepath}")

print("Done")
