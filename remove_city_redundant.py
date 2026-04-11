#!/usr/bin/env python3
"""Remove redundant intro section from city+brand pages."""

import re
import glob

def process_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # Pattern: Match section from after reviews-accordion to before the "Expert Appliance Repair" section
    # This is the redundant "[Brand] Appliance Repair in [City], NY" section
    pattern = r'(</div></div>)\s*\n*\s*<section style="padding: 60px 0; background: #fff;">\s*<div class="container" style="max-width: 900px; margin: 0 auto; padding: 0 20px;">\s*<article>\s*<h2 style="text-align:center;[^>]*>[^<]+</h2>.*?</article>\s*</div>\s*</section>\s*\n*\s*(?=<section[^>]*aria-labelledby="about-section-heading")'
    
    html = re.sub(pattern, r'\1\n\n', html, flags=re.DOTALL)
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def main():
    # City pages are in ny/ directory
    pages = glob.glob('/Users/globalaffiliate/westchester-county-repair/ny/*/*/index.html')
    
    print("=" * 60)
    print("REMOVING REDUNDANT SECTIONS FROM CITY PAGES")
    print("=" * 60)
    
    updated = 0
    for page in pages:
        parts = page.split('/')
        city = parts[-3]
        brand = parts[-2]
        
        if process_page(page):
            updated += 1
            print(f"Updated: /ny/{city}/{brand}/")
    
    print(f"\nTotal: {updated} pages updated")

if __name__ == "__main__":
    main()
