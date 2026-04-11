#!/usr/bin/env python3
"""
Make the intro section unique for each page while keeping the Appliance Repair Advantage list.
"""

import os
import re
import glob
import random

BRAND_INFO = {
    "ge": {"name": "GE", "aka": "General Electric", "heritage": "American household name since 1892"},
    "samsung": {"name": "Samsung", "aka": "Samsung Electronics", "heritage": "Korean technology leader"},
    "lg": {"name": "LG", "aka": "LG Electronics", "heritage": "global appliance innovator"},
    "whirlpool": {"name": "Whirlpool", "aka": "Whirlpool Corporation", "heritage": "American appliance manufacturer since 1911"},
    "frigidaire": {"name": "Frigidaire", "aka": "Frigidaire", "heritage": "refrigeration pioneer since 1918"},
    "bosch": {"name": "Bosch", "aka": "Bosch Home Appliances", "heritage": "German engineering excellence"},
    "kitchenaid": {"name": "KitchenAid", "aka": "KitchenAid", "heritage": "professional-grade kitchen equipment"},
    "maytag": {"name": "Maytag", "aka": "Maytag", "heritage": "legendary American durability"},
    "thermador": {"name": "Thermador", "aka": "Thermador", "heritage": "luxury cooking innovation since 1916"},
    "viking": {"name": "Viking", "aka": "Viking Range", "heritage": "professional-style home cooking"},
    "miele": {"name": "Miele", "aka": "Miele", "heritage": "German precision engineering since 1899"},
    "sub-zero": {"name": "Sub-Zero", "aka": "Sub-Zero", "heritage": "premium refrigeration specialist"},
    "wolf": {"name": "Wolf", "aka": "Wolf Appliance", "heritage": "commercial-grade cooking performance"},
    "jenn-air": {"name": "Jenn-Air", "aka": "Jenn-Air", "heritage": "downdraft ventilation pioneer"},
    "dacor": {"name": "Dacor", "aka": "Dacor", "heritage": "California luxury appliance design"},
    "electrolux": {"name": "Electrolux", "aka": "Electrolux", "heritage": "Swedish innovation and sustainability"},
    "kenmore": {"name": "Kenmore", "aka": "Kenmore", "heritage": "trusted American value since 1927"},
    "amana": {"name": "Amana", "aka": "Amana", "heritage": "microwave oven pioneer"},
    "fisher-paykel": {"name": "Fisher & Paykel", "aka": "Fisher & Paykel", "heritage": "New Zealand innovation"},
    "gaggenau": {"name": "Gaggenau", "aka": "Gaggenau", "heritage": "ultra-premium German craftsmanship since 1683"},
}

APPLIANCE_INFO = {
    "cooktop": {"name": "cooktop", "daily": "cooking meals", "issue": "burner problems"},
    "oven": {"name": "oven", "daily": "baking and roasting", "issue": "heating failures"},
    "refrigerator": {"name": "refrigerator", "daily": "food preservation", "issue": "cooling problems"},
    "washer": {"name": "washer", "daily": "laundry", "issue": "washing cycle failures"},
    "dryer": {"name": "dryer", "daily": "drying clothes", "issue": "heating or tumbling issues"},
    "dishwasher": {"name": "dishwasher", "daily": "dish cleaning", "issue": "cleaning or drainage problems"},
    "microwave": {"name": "microwave", "daily": "quick heating", "issue": "heating failures"},
    "vent-hood": {"name": "vent hood", "daily": "kitchen ventilation", "issue": "fan or lighting problems"},
    "wine-cooler": {"name": "wine cooler", "daily": "wine storage", "issue": "temperature control problems"},
}

def get_brand(slug):
    return BRAND_INFO.get(slug, {"name": slug.replace("-", " ").title(), "aka": slug.replace("-", " ").title(), "heritage": "quality appliances"})

def get_appliance(slug):
    return APPLIANCE_INFO.get(slug.replace("-repair", ""), {"name": slug.replace("-repair", "").replace("-", " "), "daily": "daily tasks", "issue": "malfunctions"})


def generate_intro(brand_slug, appliance_slug):
    """Generate unique intro paragraphs for each brand+appliance combination."""
    b = get_brand(brand_slug)
    a = get_appliance(appliance_slug)

    # Seed for consistent results per page
    random.seed(f"{brand_slug}{appliance_slug}")

    intros_p1 = [
        f'When your <strong>{b["name"]} {a["name"]}</strong> needs repair, you need technicians who specialize in {b["aka"]} appliances. Our <strong>factory-certified technicians</strong> bring {b["heritage"]} expertise to every service call across <strong>Westchester County, New York</strong>. A malfunctioning {a["name"]} disrupts your entire household routine.',

        f'Your <strong>{b["name"]} {a["name"]}</strong> handles {a["daily"]} for your family every day. When {a["issue"]} occur, our <strong>factory-certified {b["name"]} specialists</strong> respond quickly throughout <strong>Westchester County, New York</strong>. We understand how essential reliable {a["name"]} performance is to your home.',

        f'<strong>{b["name"]}</strong> appliances represent {b["heritage"]}. When your {a["name"]} stops working properly, trust <strong>factory-certified technicians</strong> who know {b["aka"]} inside and out. We serve all of <strong>Westchester County, New York</strong> with same-day availability.',
    ]

    intros_p2 = [
        f'Our {b["name"]} repair specialists complete <strong>brand-specific training programs</strong> covering the latest {b["name"]} technologies and repair procedures. With <strong>round-the-clock technical support</strong> and genuine {b["name"]} parts, we resolve even complex {a["name"]} repairs correctly the first time.',

        f'Every technician on our team maintains <strong>current {b["name"]} certifications</strong> and participates in ongoing education. Access to <strong>24/7 technical resources</strong> and authentic {b["name"]} replacement parts means your {a["name"]} gets the expert care it deserves.',

        f'We invest in <strong>continuous {b["name"]} training</strong> so our technicians stay ahead of evolving technologies. Combined with <strong>round-the-clock expert support</strong> and factory-authorized {b["name"]} components, we deliver repairs that last.',
    ]

    p1 = random.choice(intros_p1)
    p2 = random.choice(intros_p2)

    return f'''<p style="margin-bottom: 15px;">{p1}</p>
<p style="margin-bottom: 15px;">{p2}</p>'''


def process_page(filepath, brand, appliance):
    """Update the intro paragraphs in a page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # Pattern to match the two intro paragraphs before "The Appliance Repair Advantage"
    pattern = r'(<div id="expandable-text-1"[^>]*>)\s*<p style="margin-bottom: 15px;">When your[^<]+</p>\s*<p style="margin-bottom: 15px;">Our technicians complete[^<]+</p>\s*(<h3[^>]*>The Appliance Repair Advantage)'

    new_intro = generate_intro(brand, appliance)
    replacement = r'\1\n' + new_intro + r'\n\2'

    html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    base_path = '/Users/globalaffiliate/westchester-county-repair/brands'

    # Find all brand+appliance pages
    pages = glob.glob(f'{base_path}/*/*-repair/index.html')

    print("=" * 60)
    print("CREATING UNIQUE INTRO CONTENT")
    print("=" * 60)

    updated = 0
    for page in pages:
        parts = page.split('/')
        brand = parts[-3]
        appliance = parts[-2]

        if process_page(page, brand, appliance):
            updated += 1
            print(f"Updated: /brands/{brand}/{appliance}/")

    print(f"\nTotal: {updated} pages updated")


if __name__ == "__main__":
    main()
