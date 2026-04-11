#!/usr/bin/env python3
"""Remove the entire intro section from brand+appliance pages - go directly to Factory Certified Service."""

import re
import glob

def process_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # Remove the entire "Expert Appliance Repair" section including the expandable content
    # This section starts after </div></div> (reviews accordion) and ends before <section class="alt">
    pattern = r'</div></div>\s*\n*\s*<section style="padding: 60px 0; background: #fff;" aria-labelledby="about-section-heading">.*?</section>\s*\n*\s*(?=<section class="alt">)'
    
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
    print("REMOVING INTRO SECTION - DIRECT TO FACTORY CERTIFIED")
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
