#!/usr/bin/env python3
"""Remove the redundant intro section from all brand+appliance pages."""

import re
import glob

def process_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # Pattern: Match section from after reviews-accordion to before the expandable content section
    # This captures the entire "Expert X Y Repair" + brand overview + Common Problems + Why Choose section
    pattern = r'</div></div>\s*\n*\s*<section style="padding: 60px 0; background: #fff;">\s*<div class="container" style="max-width: 900px; margin: 0 auto; padding: 0 20px;">\s*<article>\s*<h2 style="text-align:center;[^>]*>Expert [^<]+</h2>.*?</article>\s*</div>\s*</section>\s*\n*\s*(?=<section[^>]*aria-labelledby="about-section-heading")'
    
    html = re.sub(pattern, '</div></div>\n\n', html, flags=re.DOTALL)
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def main():
    base_path = '/Users/globalaffiliate/westchester-county-repair/brands'
    pages = glob.glob(f'{base_path}/*/*-repair/index.html')
    
    print("=" * 60)
    print("REMOVING REDUNDANT INTRO SECTIONS (v2)")
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
