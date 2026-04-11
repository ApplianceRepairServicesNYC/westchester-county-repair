#!/usr/bin/env python3
"""
Standardize all brand+appliance pages with:
1. Unique intro paragraphs (rephrased)
2. The Appliance Repair Advantage checklist
"""

import os
import re
import glob
import random

BRAND_INFO = {
    "ge": {"name": "GE", "full": "General Electric"},
    "samsung": {"name": "Samsung", "full": "Samsung"},
    "lg": {"name": "LG", "full": "LG"},
    "whirlpool": {"name": "Whirlpool", "full": "Whirlpool"},
    "frigidaire": {"name": "Frigidaire", "full": "Frigidaire"},
    "bosch": {"name": "Bosch", "full": "Bosch"},
    "kitchenaid": {"name": "KitchenAid", "full": "KitchenAid"},
    "maytag": {"name": "Maytag", "full": "Maytag"},
    "thermador": {"name": "Thermador", "full": "Thermador"},
    "viking": {"name": "Viking", "full": "Viking"},
    "miele": {"name": "Miele", "full": "Miele"},
    "sub-zero": {"name": "Sub-Zero", "full": "Sub-Zero"},
    "wolf": {"name": "Wolf", "full": "Wolf"},
    "jenn-air": {"name": "Jenn-Air", "full": "Jenn-Air"},
    "dacor": {"name": "Dacor", "full": "Dacor"},
    "electrolux": {"name": "Electrolux", "full": "Electrolux"},
    "kenmore": {"name": "Kenmore", "full": "Kenmore"},
    "amana": {"name": "Amana", "full": "Amana"},
    "fisher-paykel": {"name": "Fisher & Paykel", "full": "Fisher & Paykel"},
    "gaggenau": {"name": "Gaggenau", "full": "Gaggenau"},
}

APPLIANCE_INFO = {
    "cooktop": "cooktop",
    "oven": "oven",
    "refrigerator": "refrigerator",
    "washer": "washer",
    "dryer": "dryer",
    "dishwasher": "dishwasher",
    "microwave": "microwave",
    "vent-hood": "vent hood",
    "wine-cooler": "wine cooler",
}

def get_brand(slug):
    info = BRAND_INFO.get(slug, {"name": slug.replace("-", " ").title(), "full": slug.replace("-", " ").title()})
    return info

def get_appliance(slug):
    app = slug.replace("-repair", "")
    return APPLIANCE_INFO.get(app, app.replace("-", " "))


def generate_content(brand_slug, appliance_slug):
    """Generate the full expandable-text-1 content."""
    b = get_brand(brand_slug)
    a = get_appliance(appliance_slug)
    brand = b["name"]

    # Seed for consistent results
    random.seed(f"{brand_slug}{appliance_slug}")

    # Varied intro paragraph 1
    intros1 = [
        f'When your <strong>{brand}</strong> stops working, you deserve a repair service that delivers results. Our <strong>factory-certified technicians</strong> focus exclusively on household appliances, bringing specialized expertise to every service call across <strong>Westchester County, New York</strong>. We know how frustrating a broken {a} can be to your household.',
        f'Your <strong>{brand} {a}</strong> is essential to your daily routine. When problems occur, our <strong>factory-certified technicians</strong> provide expert repair service throughout <strong>Westchester County, New York</strong>. We understand the urgency of appliance failures and respond accordingly.',
        f'A malfunctioning <strong>{brand} {a}</strong> disrupts your entire household. Our <strong>factory-certified technicians</strong> specialize in {brand} appliances and serve all of <strong>Westchester County, New York</strong>. We deliver the professional repair service you expect.',
    ]

    # Varied intro paragraph 2
    intros2 = [
        f'Our technicians complete <strong>annual training programs</strong> to stay current with evolving {brand} technologies and advanced repair techniques. They also have access to <strong>round-the-clock technical support</strong>, ensuring even the most challenging repairs are resolved quickly and correctly.',
        f'Every technician maintains <strong>current {brand} certifications</strong> through ongoing education and training. With <strong>24/7 technical support</strong> available, we resolve complex {a} repairs efficiently and correctly the first time.',
        f'We invest in <strong>continuous {brand} training</strong> for our entire team. Combined with <strong>round-the-clock expert support</strong> and genuine {brand} parts, we deliver repairs that last.',
    ]

    p1 = random.choice(intros1)
    p2 = random.choice(intros2)

    checklist = f'''<h3 style="font-size: 20px; color: var(--blue); margin: 25px 0 15px;">The Appliance Repair Advantage</h3>
<ul style="list-style: none; padding: 0; margin: 0 0 20px 0;">
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Authorized Westchester County Coverage:</strong> Our skilled technicians are strategically positioned throughout Westchester County, ready to address your repair needs with speed and precision.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Reliable & Prompt Service:</strong> With technicians dispatched from locations across Westchester County, we guarantee swift response times for every appointment.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Fully Equipped Service Vehicles:</strong> Each vehicle carries a comprehensive parts inventory, paired with intelligent dispatch software for maximum efficiency.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Same-Day Repair Solutions:</strong> We stock commonly needed parts to complete the majority of repairs during your first appointment.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Complete Repair Warranty:</strong> Every repair is backed by our comprehensive warranty. If any issues occur, we'll return to resolve them at no extra cost.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Diagnostic Fee Applied to Repair:</strong> Your diagnostic fee is credited toward the total repair cost, reducing your overall expense.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Certified Repair Specialists:</strong> Our technicians hold industry certifications and participate in continuous education to master the latest {brand} repair methods.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Upfront, Honest Pricing:</strong> No surprises or hidden charges—we provide clear pricing before any work begins.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>24/7 Emergency Repairs:</strong> Appliance emergencies don't follow a schedule—neither do we. Urgent service is available when you need it most.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Genuine {brand} Parts Only:</strong> We exclusively use authentic, manufacturer-approved parts to ensure lasting repairs that meet factory specifications.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Dedicated Support Team:</strong> Our friendly customer service representatives are here to answer questions and schedule appointments at your convenience.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Weekend & Flexible Appointments:</strong> We accommodate your schedule with availability seven days a week, including evenings.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Best Price Guarantee:</strong> Found a lower quote? We'll match any competitor's price to deliver exceptional value.</span>
</li>
<li style="padding: 12px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Money Back Guarantee:</strong> If we're unable to repair your appliance, you owe us nothing. It's that simple.</span>
</li>
<li style="padding: 12px 0; display: flex; align-items: flex-start;">
<span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
<span><strong>Fully Insured Service:</strong> We carry comprehensive property damage insurance for your protection. For New York residences, we provide certificates of insurance upon request.</span>
</li>
</ul>'''

    return f'''<p style="margin-bottom: 15px;">{p1}</p>
<p style="margin-bottom: 15px;">{p2}</p>
{checklist}
'''


def process_page(filepath, brand, appliance):
    """Update the expandable-text-1 content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # Pattern to match expandable-text-1 content
    pattern = r'(<div id="expandable-text-1"[^>]*>)(.*?)(</div>\s*<(?:div id="expandable-fade|button id="expandable-btn))'

    new_content = generate_content(brand, appliance)

    def replacer(match):
        return match.group(1) + '\n' + new_content + '\n' + match.group(3)

    html = re.sub(pattern, replacer, html, flags=re.DOTALL)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    base_path = '/Users/globalaffiliate/westchester-county-repair/brands'
    pages = glob.glob(f'{base_path}/*/*-repair/index.html')

    print("=" * 60)
    print("STANDARDIZING INTRO WITH CHECKLIST")
    print("=" * 60)

    updated = 0
    for page in pages:
        parts = page.split('/')
        brand = parts[-3]
        appliance = parts[-2]

        if process_page(page, brand, appliance):
            updated += 1
            print(f"Updated: /brands/{brand}/{appliance}/")

    print(f"\nTotal: {updated} pages standardized")


if __name__ == "__main__":
    main()
