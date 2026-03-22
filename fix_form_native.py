#!/usr/bin/env python3
"""
Fix form to use native submission like the working LG NJ site
- Remove fetch/AJAX
- Add _next redirect field
- Show popup on redirect return
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

    # 1. Change form action back to non-ajax endpoint
    content = content.replace(
        'formsubmit.co/ajax/insuranceappliance@gmail.com',
        'formsubmit.co/insuranceappliance@gmail.com'
    )

    # 2. Add _next hidden field after _template if not present
    if '_next' not in content and 'formsubmit.co' in content:
        content = re.sub(
            r'(<input type="hidden" name="_template" value="table">)',
            r'\1\n                        <input type="hidden" name="_next" id="formNextUrl">',
            content
        )

    # 3. Remove the fetch-based submit handlers and replace with native + redirect detection
    # Find and remove the old fetch submit handler for scheduleForm
    old_sf_handler = r"""scheduleForm\.addEventListener\('submit', function\(e\) \{
\s*e\.preventDefault\(\);
\s*const email = this\.email\.value\.trim\(\);
\s*document\.getElementById\('replyToField'\)\.value = email;
\s*fetch\('https://formsubmit\.co/insuranceappliance@gmail\.com', \{
\s*method: 'POST',
\s*body: new FormData\(this\),
\s*headers: \{'Accept': 'application/json'\}
\s*\}\)\.then\(function\(response\) \{
\s*if \(response\.ok\) \{
\s*scheduleForm\.reset\(\);
\s*document\.getElementById\('sfSuccessMessage'\)\.innerHTML = '[^']*' \+ email \+ '[^']*';
\s*document\.getElementById\('sfSuccessModal'\)\.classList\.add\('active'\);
\s*document\.getElementById\('sfModalOverlay'\)\.classList\.add\('active'\);
\s*\}
\s*\}\)\.catch\(function\(\) \{
\s*alert\('Failed to send\. Please try again or call us\.'\);
\s*\}\);
\s*\}\);
\s*\}"""

    new_sf_handler = """var sfNextUrl = document.getElementById('formNextUrl');
if (sfNextUrl) {
    sfNextUrl.value = window.location.href.split('?')[0] + '?submitted=true';
}
}

// Show success modal if redirected back after form submission
if (window.location.search.includes('submitted=true')) {
    var sfModal = document.getElementById('sfSuccessModal');
    var sfOverlay = document.getElementById('sfModalOverlay');
    if (sfModal) sfModal.classList.add('active');
    if (sfOverlay) sfOverlay.classList.add('active');
    history.replaceState(null, '', window.location.pathname);
}"""

    # Simple replacement - remove e.preventDefault and fetch, add redirect detection
    # Remove the entire old submit handler block
    content = re.sub(
        r"scheduleForm\.addEventListener\('submit', function\(e\) \{[^}]+\}[^}]+\}[^}]+\}[^}]+\}\);[^}]+\}",
        new_sf_handler,
        content,
        flags=re.DOTALL
    )

    # Also handle cfContactForm similarly
    content = re.sub(
        r"cfContactForm\.addEventListener\('submit', function\(e\) \{[^}]+\}[^}]+\}[^}]+\}[^}]+\}\);[^}]+\}",
        """var cfNextUrl = document.getElementById('formNextUrl');
if (cfNextUrl) {
    cfNextUrl.value = window.location.href.split('?')[0] + '?submitted=true';
}
}""",
        content,
        flags=re.DOTALL
    )

    # Remove replyToField since we don't need it with native submit
    content = re.sub(r'\s*<input type="hidden" name="_replyto" id="replyToField">\s*', '\n', content)

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

    print(f"✅ Fixed forms in {modified} files to use native submission")

if __name__ == '__main__':
    main()
