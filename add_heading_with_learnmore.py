#!/usr/bin/env python3
"""Add back the heading with Learn More button containing the checklist."""

import re
import glob
import random

BRAND_INFO = {
    "ge": "GE", "samsung": "Samsung", "lg": "LG", "whirlpool": "Whirlpool",
    "frigidaire": "Frigidaire", "bosch": "Bosch", "kitchenaid": "KitchenAid",
    "maytag": "Maytag", "thermador": "Thermador", "viking": "Viking",
    "miele": "Miele", "sub-zero": "Sub-Zero", "wolf": "Wolf",
    "jenn-air": "Jenn-Air", "dacor": "Dacor", "electrolux": "Electrolux",
    "kenmore": "Kenmore", "amana": "Amana", "fisher-paykel": "Fisher & Paykel",
    "gaggenau": "Gaggenau",
}

def get_brand(slug):
    return BRAND_INFO.get(slug, slug.replace("-", " ").title())

def generate_checklist(brand):
    return f'''<ul style="list-style: none; padding: 0; margin: 0;">
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
<span><strong>Fully Insured Service:</strong> We carry comprehensive property damage insurance for your protection.</span>
</li>
</ul>'''

def generate_section(brand_slug):
    brand = get_brand(brand_slug)
    checklist = generate_checklist(brand)
    
    return f'''
<section style="padding: 40px 0 20px; background: #fff;">
<div class="container" style="max-width: 900px; margin: 0 auto; padding: 0 20px; text-align: center;">
<h2 style="font-size:32px; margin-bottom:20px; color: var(--blue);">Expert Appliance Repair in Westchester County</h2>
<div id="learnmore-content" style="display: none; text-align: left; margin-top: 20px;">
<h3 style="font-size: 20px; color: var(--blue); margin: 0 0 15px;">The Appliance Repair Advantage</h3>
{checklist}
</div>
<button id="learnmore-btn" onclick="toggleLearnMore()" style="background: none; border: 2px solid var(--blue); color: var(--blue); padding: 12px 30px; border-radius: 5px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 15px; transition: all 0.3s;">Learn More</button>
</div>
</section>

'''

def process_page(filepath, brand_slug):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # Add the section after reviews accordion and before Factory Certified Service
    section = generate_section(brand_slug)
    
    # Find where to insert - after </div></div> (reviews) and before <section class="alt">
    pattern = r'(</div></div>)\s*\n*\s*(<section class="alt">)'
    replacement = r'\1\n' + section + r'\2'
    
    html = re.sub(pattern, replacement, html, count=1)
    
    # Add the toggleLearnMore function if not present
    if 'toggleLearnMore' not in html:
        js_function = '''
function toggleLearnMore() {
    var content = document.getElementById('learnmore-content');
    var btn = document.getElementById('learnmore-btn');
    if (content.style.display === 'none') {
        content.style.display = 'block';
        btn.innerHTML = 'Show Less';
    } else {
        content.style.display = 'none';
        btn.innerHTML = 'Learn More';
    }
}
'''
        html = html.replace('</script>\n</body>', js_function + '</script>\n</body>')
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def main():
    base_path = '/Users/globalaffiliate/westchester-county-repair/brands'
    pages = glob.glob(f'{base_path}/*/*-repair/index.html')
    
    print("=" * 60)
    print("ADDING HEADING WITH LEARN MORE BUTTON")
    print("=" * 60)
    
    updated = 0
    for page in pages:
        parts = page.split('/')
        brand = parts[-3]
        
        if process_page(page, brand):
            updated += 1
            print(f"Updated: /brands/{brand}/{parts[-2]}/")
    
    print(f"\nTotal: {updated} pages updated")

if __name__ == "__main__":
    main()
