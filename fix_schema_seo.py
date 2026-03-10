#!/usr/bin/env python3
"""
Fix Schema.org SEO for Westchester County Repair site.
Issues found:
1. Brand pages: url points to homepage, not the specific page
2. Brand+appliance pages: url points to homepage, name is generic
3. Location+brand pages: Some have correct url but need @id added
4. og:url often points to homepage instead of the page itself
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/westchester-county-repair')
BASE_URL = "https://westchestercountyrepair.com"

# Appliance types
APPLIANCE_TYPES = [
    'cooktop-repair', 'dishwasher-repair', 'microwave-repair', 'oven-repair',
    'refrigerator-repair', 'wine-cooler-repair', 'washer-repair', 'dryer-repair',
    'vent-hood-repair', 'range-repair', 'freezer-repair'
]

# Brand repair types (for location pages)
BRAND_REPAIRS = [
    'thermador-repair', 'samsung-repair', 'ge-repair', 'lg-repair', 'miele-repair',
    'bosch-repair', 'sub-zero-repair', 'wolf-repair', 'viking-repair', 'jenn-air-repair',
    'kitchenaid-repair', 'whirlpool-repair', 'maytag-repair', 'frigidaire-repair',
    'kenmore-repair', 'dacor-repair', 'gaggenau-repair', 'fisher-paykel-repair',
    'amana-repair', 'electrolux-repair', 'speed-queen-repair', 'asko-repair',
    'smeg-repair', 'bertazzoni-repair', 'monogram-repair', 'cafe-repair',
    'haier-repair', 'hotpoint-repair', 'admiral-repair', 'magic-chef-repair'
]

def format_name(slug):
    """Convert slug to proper name."""
    return slug.replace("-", " ").title()

def get_page_info(file_path):
    """Extract page info from file path."""
    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    # Remove index.html
    if parts[-1] == 'index.html':
        parts = parts[:-1]

    if len(parts) < 1:
        return None

    page_url = f"{BASE_URL}/{'/'.join(parts)}/"

    # Brand pages: /brands/thermador/
    if parts[0] == 'brands' and len(parts) == 2:
        brand = format_name(parts[1])
        return {
            'type': 'brand',
            'brand': brand,
            'url': page_url,
            'name': f"{brand} Appliance Repair Westchester County NY"
        }

    # Brand + appliance pages: /brands/jenn-air/dishwasher-repair/
    if parts[0] == 'brands' and len(parts) == 3 and parts[2] in APPLIANCE_TYPES:
        brand = format_name(parts[1])
        appliance = format_name(parts[2])
        return {
            'type': 'brand_appliance',
            'brand': brand,
            'appliance': appliance,
            'url': page_url,
            'name': f"{brand} {appliance} Westchester County NY"
        }

    # Location pages: /ny/white-plains/
    if parts[0] == 'ny' and len(parts) == 2:
        town = format_name(parts[1])
        return {
            'type': 'location',
            'town': town,
            'url': page_url,
            'name': f"Appliance Repair {town} NY"
        }

    # Location + appliance pages: /ny/white-plains/oven-repair/
    if parts[0] == 'ny' and len(parts) == 3 and parts[2] in APPLIANCE_TYPES:
        town = format_name(parts[1])
        appliance = format_name(parts[2])
        return {
            'type': 'location_appliance',
            'town': town,
            'appliance': appliance,
            'url': page_url,
            'name': f"{appliance} {town} NY"
        }

    # Location + brand pages: /ny/white-plains/thermador-repair/
    if parts[0] == 'ny' and len(parts) == 3 and parts[2] in BRAND_REPAIRS:
        town = format_name(parts[1])
        brand = format_name(parts[2].replace('-repair', ''))
        return {
            'type': 'location_brand',
            'town': town,
            'brand': brand,
            'url': page_url,
            'name': f"{brand} Repair {town} NY"
        }

    return None


def fix_file(file_path):
    """Fix Schema.org and og tags in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, None

    info = get_page_info(file_path)
    if not info:
        return False, None

    modified = False

    # Fix JSON-LD Schema
    pattern = r'(<script type="application/ld\+json">)\s*(\{[^<]+\})\s*(</script>)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        try:
            schema = json.loads(match.group(2))

            # Update url and add @id
            schema['url'] = info['url']
            schema['@id'] = info['url']
            schema['name'] = info['name']

            # Update areaServed for specific pages
            if info['type'] in ['location', 'location_appliance', 'location_brand']:
                schema['areaServed'] = {
                    "@type": "City",
                    "name": info['town']
                }

            # Format and replace
            new_json = json.dumps(schema, indent=4)
            new_script = f'{match.group(1)}\n{new_json}\n{match.group(3)}'
            content = content[:match.start()] + new_script + content[match.end():]
            modified = True

        except json.JSONDecodeError:
            pass

    # Fix og:url to point to the specific page
    og_url_pattern = r'<meta property="og:url" content="[^"]*">'
    new_og_url = f'<meta property="og:url" content="{info["url"]}">'
    if re.search(og_url_pattern, content):
        content = re.sub(og_url_pattern, new_og_url, content)
        modified = True

    # Fix og:description to be page-specific
    if info['type'] == 'brand':
        new_og_desc = f"Expert {info['brand']} appliance repair in Westchester County NY. Same-day service for all {info['brand']} appliances."
    elif info['type'] == 'brand_appliance':
        new_og_desc = f"Professional {info['brand']} {info['appliance'].lower()} in Westchester County NY. Factory-certified technicians, same-day service."
    elif info['type'] == 'location':
        new_og_desc = f"Expert appliance repair in {info['town']}, NY. Same-day service for all major brands and appliances."
    elif info['type'] == 'location_appliance':
        new_og_desc = f"Professional {info['appliance'].lower()} in {info['town']}, NY. Same-day service, certified technicians."
    elif info['type'] == 'location_brand':
        new_og_desc = f"Expert {info['brand']} repair in {info['town']}, NY. Factory-certified technicians, same-day service."
    else:
        new_og_desc = None

    if new_og_desc:
        og_desc_pattern = r'<meta property="og:description" content="[^"]*">'
        new_og_desc_tag = f'<meta property="og:description" content="{new_og_desc}">'
        if re.search(og_desc_pattern, content):
            content = re.sub(og_desc_pattern, new_og_desc_tag, content)
            modified = True

    # Fix og:title
    og_title_pattern = r'<meta property="og:title" content="[^"]*">'
    new_og_title = f'<meta property="og:title" content="{info["name"]}">'
    if re.search(og_title_pattern, content):
        content = re.sub(og_title_pattern, new_og_title, content)
        modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, info['type']

    return False, None


def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    print(f"Found {len(html_files)} HTML files")

    counts = {}
    for html_file in html_files:
        if 'assets' in str(html_file) or 'sitemap' in str(html_file):
            continue

        success, page_type = fix_file(html_file)
        if success and page_type:
            counts[page_type] = counts.get(page_type, 0) + 1

    print("\nFixed pages by type:")
    for page_type, count in sorted(counts.items()):
        print(f"  {page_type}: {count}")
    print(f"\nTotal: {sum(counts.values())} pages")


if __name__ == "__main__":
    main()
