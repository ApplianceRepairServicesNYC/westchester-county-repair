#!/usr/bin/env python3
"""
Remove duplicate hidden email fields from forms
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

    # Remove hidden email fields
    content = re.sub(r'\s*<input type="hidden" name="reply_to" id="sfReplyTo">\s*', '\n', content)
    content = re.sub(r'\s*<input type="hidden" name="email" id="sfEmailHidden">\s*', '\n', content)
    content = re.sub(r'\s*<input type="hidden" name="from_email" id="sfFromEmail">\s*', '\n', content)
    content = re.sub(r'\s*<input type="hidden" name="customer_email" id="sfCustomerEmail">\s*', '\n', content)

    # Remove JavaScript that sets these values
    content = re.sub(r"\s*document\.getElementById\('sfReplyTo'\)\.value = email;\s*", '\n', content)
    content = re.sub(r"\s*document\.getElementById\('sfEmailHidden'\)\.value = email;\s*", '\n', content)
    content = re.sub(r"\s*document\.getElementById\('sfFromEmail'\)\.value = email;\s*", '\n', content)
    content = re.sub(r"\s*document\.getElementById\('sfCustomerEmail'\)\.value = email;\s*", '\n', content)

    # Also clean up contact form hidden fields (cf prefix)
    content = re.sub(r'\s*<input type="hidden" name="reply_to" id="cfReplyTo">\s*', '\n', content)
    content = re.sub(r'\s*<input type="hidden" name="email" id="cfEmailHidden">\s*', '\n', content)
    content = re.sub(r'\s*<input type="hidden" name="from_email" id="cfFromEmail">\s*', '\n', content)
    content = re.sub(r'\s*<input type="hidden" name="customer_email" id="cfCustomerEmail">\s*', '\n', content)

    content = re.sub(r"\s*document\.getElementById\('cfReplyTo'\)\.value = email;\s*", '\n', content)
    content = re.sub(r"\s*document\.getElementById\('cfEmailHidden'\)\.value = email;\s*", '\n', content)
    content = re.sub(r"\s*document\.getElementById\('cfFromEmail'\)\.value = email;\s*", '\n', content)
    content = re.sub(r"\s*document\.getElementById\('cfCustomerEmail'\)\.value = email;\s*", '\n', content)

    # Rename user_email to just "email" for cleaner output
    content = re.sub(r'name="user_email"', 'name="email"', content)
    content = re.sub(r'name="from_name"', 'name="name"', content)

    # Add FormSubmit config hidden fields (for reply-to and subject)
    # Add _replyto field so replies go to customer
    if 'name="_replyto"' not in content and 'formsubmit.co' in content:
        # Add after the email field
        content = re.sub(
            r'(<input[^>]*name="email"[^>]*>)',
            r'\1\n<input type="hidden" name="_replyto" id="replyToField">',
            content
        )
        # Add JS to set _replyto
        content = re.sub(
            r"(const email = this\.(?:user_email|email)\.value\.trim\(\);)",
            r"\1\ndocument.getElementById('replyToField').value = email;",
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

    print(f"✅ Cleaned up {modified} files")
    print("Form fields now: name, email, phone, subject, address, message")

if __name__ == '__main__':
    main()
