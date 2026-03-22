#!/usr/bin/env python3
"""
Remove remaining EmailJS minified scripts
"""

import os
import glob

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    original = content

    # Find and remove minified emailjs script
    start_marker = "<script>var emailjs=function(e)"
    end_marker = "});</script>"

    while start_marker in content:
        start = content.find(start_marker)
        if start == -1:
            break
        # Find the closing </script> after the emailjs.init call
        search_start = start + len(start_marker)
        end = content.find("});</script>", search_start)
        if end == -1:
            break
        end += len("});</script>")
        content = content[:start] + content[end:]

    # Also clean up any remaining emailjs CDN scripts
    cdn_marker = '<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser'
    while cdn_marker in content:
        start = content.find(cdn_marker)
        end = content.find("</script>", start)
        if end == -1:
            break
        end += len("</script>")
        content = content[:start] + content[end:]

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

    print(f"✅ Removed minified EmailJS from {modified} files")

if __name__ == '__main__':
    main()
