#!/usr/bin/env python3
"""Remove the redundant intro section (Expert X Repair + Common Problems + Why Choose) from brand+appliance pages."""

import os
import re
import glob

def process_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # Pattern to match the redundant section: from "<section" containing "Expert X Y Repair" 
    # through "Common Problems" and "Why Choose" to closing "</section>"
    # This section appears right after the reviews accordion and before the expandable content section
    pattern = r'<section style="padding: 60px 0; background: #fff;">\s*<div class="container" style="max-width: 900px;[^>]*>\s*<article>\s*<h2 style="text-align:center;[^>]*>Expert [^<]+ Repair in Westchester County</h2>\s*<h3[^>]*>Common [^<]+ Problems We Fix</h3>\s*<ul[^>]*>.*?</ul>\s*<h3[^>]*>Why Choose Our [^<]+ Repair Service\?</h3>\s*<p[^>]*>.*?</p>\s*<p[^>]*>.*?</p>\s*</article>\s*</div>\s*</section>'
    
    html = re.sub(pattern, '', html, flags=re.DOTALL)
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def main():
    base_path = '/Users/globalaffiliate/westchester-county-repair/brands'
    pages = glob.glob(f'{base_path}/*/*-repair/index.html')
    
    print("=" * 60)
    print("REMOVING REDUNDANT INTRO SECTIONS")
    print("=" * 60)
    
    updated = 0
    for page in pages:
        parts = page.split('/')
        brand = parts[-3]
        appliance = parts[-2]
        
        if process_page(page):
            updated += 1
            print(f"Updated: /brands/{brand}/{appliance}/")
    
    print(f"\nTotal: {updated} pages updated")

if __name__ == "__main__":
    main()
