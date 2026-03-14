#!/usr/bin/env python3
"""
Add unique content to thin pages to fix Google's "Crawled - currently not indexed" issue.
"""

import os
import re
from pathlib import Path

# Brand descriptions
BRANDS = {
    "jenn-air": {
        "name": "Jenn-Air",
        "desc": "Jenn-Air has been a leader in premium kitchen appliances since 1947, known for introducing the first self-ventilated cooktop. Today, Jenn-Air represents luxury performance with innovative features like connected technology and professional-grade components.",
        "known_for": "downdraft ventilation systems, professional-style ranges, and premium built-in refrigerators"
    },
    "sub-zero": {
        "name": "Sub-Zero",
        "desc": "Sub-Zero has set the standard for food preservation since 1945. Their dual refrigeration system keeps fresh foods and frozen items at optimal conditions separately, extending freshness significantly longer than conventional refrigerators.",
        "known_for": "built-in refrigeration, dual compressor technology, and air purification systems"
    },
    "wolf": {
        "name": "Wolf",
        "desc": "Wolf appliances bring professional restaurant-quality cooking to home kitchens. With precise temperature control and heavy-duty construction, Wolf ranges, ovens, and cooktops deliver consistent results that serious home chefs demand.",
        "known_for": "dual-stacked burners, convection ovens, and precise temperature control"
    },
    "thermador": {
        "name": "Thermador",
        "desc": "Thermador pioneered the cooktop in 1947 and continues to innovate with features like the Star Burner and Freedom Induction technology. As a premium brand, Thermador appliances combine European design with American engineering.",
        "known_for": "Star Burners, steam ovens, and column refrigeration"
    },
    "miele": {
        "name": "Miele",
        "desc": "German-engineered Miele appliances are built to last 20 years of average use. Their commitment to quality means rigorous testing and premium components in every dishwasher, washer, dryer, and cooking appliance they manufacture.",
        "known_for": "exceptional build quality, quiet operation, and energy efficiency"
    },
    "bosch": {
        "name": "Bosch",
        "desc": "Bosch brings German precision engineering to home appliances. Known for whisper-quiet dishwashers and efficient laundry systems, Bosch appliances combine reliability with innovative features that simplify daily tasks.",
        "known_for": "ultra-quiet dishwashers, compact laundry solutions, and induction cooktops"
    },
    "viking": {
        "name": "Viking",
        "desc": "Viking brought professional-grade cooking to residential kitchens in 1987. Their commercial-style ranges and refrigerators feature heavy-duty construction, powerful burners, and the distinctive Viking aesthetic.",
        "known_for": "professional ranges, high-BTU burners, and stainless steel construction"
    },
    "gaggenau": {
        "name": "Gaggenau",
        "desc": "Gaggenau represents the pinnacle of German appliance engineering with over 330 years of manufacturing heritage. Their appliances feature restaurant-quality performance with minimalist, architectural design.",
        "known_for": "combi-steam ovens, Vario cooktops, and wine climate cabinets"
    },
    "dacor": {
        "name": "Dacor",
        "desc": "California-based Dacor has crafted luxury kitchen appliances since 1965. Their innovations include the first smart connected wall oven and ranges that combine powerful performance with sophisticated design.",
        "known_for": "smart home integration, high-altitude cooking features, and sleek design"
    },
    "kitchenaid": {
        "name": "KitchenAid",
        "desc": "KitchenAid has been a trusted name in American kitchens since 1919. Beyond their iconic stand mixers, KitchenAid produces reliable refrigerators, dishwashers, and cooking appliances designed for home cooks who take food seriously.",
        "known_for": "stand mixers, versatile cooking appliances, and dependable refrigeration"
    },
    "ge": {
        "name": "GE",
        "desc": "GE Appliances has been an American household name for over a century. From refrigerators to ranges, GE offers reliable appliances with innovative features at accessible price points for everyday families.",
        "known_for": "reliability, wide product range, and smart home connectivity"
    },
    "whirlpool": {
        "name": "Whirlpool",
        "desc": "Whirlpool has been helping families care for their homes since 1911. As the world's leading home appliance company, they produce dependable washers, dryers, refrigerators, and dishwashers trusted by millions.",
        "known_for": "laundry expertise, adaptive wash technology, and energy-efficient designs"
    },
    "lg": {
        "name": "LG",
        "desc": "LG Electronics combines Korean innovation with American practicality. Their appliances feature smart technology, energy efficiency, and sleek designs that complement modern homes.",
        "known_for": "ThinQ smart technology, InstaView refrigerators, and TurboWash laundry"
    },
    "samsung": {
        "name": "Samsung",
        "desc": "Samsung brings cutting-edge technology to home appliances. From Family Hub refrigerators to AI-powered washers, Samsung appliances feature smart connectivity and innovative solutions for modern living.",
        "known_for": "Family Hub refrigerators, FlexWash laundry, and smart connectivity"
    },
    "frigidaire": {
        "name": "Frigidaire",
        "desc": "Frigidaire invented the self-contained refrigerator in 1916 and has been a trusted name ever since. They offer practical, affordable appliances that deliver solid performance for everyday households.",
        "known_for": "affordable refrigeration, Gallery series upgrades, and reliable performance"
    },
    "electrolux": {
        "name": "Electrolux",
        "desc": "Swedish-designed Electrolux appliances combine Scandinavian aesthetics with innovative functionality. Their laundry systems and kitchen appliances emphasize sustainability and user-friendly operation.",
        "known_for": "European design, Perfect Steam technology, and eco-friendly features"
    },
    "maytag": {
        "name": "Maytag",
        "desc": "Maytag has built its reputation on rugged dependability since 1893. Known for powerful washers and dryers that handle heavy loads, Maytag appliances are built to work hard for years.",
        "known_for": "commercial-grade durability, PowerWash cycle, and 10-year warranties"
    },
    "kenmore": {
        "name": "Kenmore",
        "desc": "Kenmore has been a household staple since 1913, offering quality appliances at competitive prices. Their wide range covers every home need from refrigerators to vacuums.",
        "known_for": "value-oriented pricing, wide selection, and reliable performance"
    },
    "amana": {
        "name": "Amana",
        "desc": "Amana introduced the first side-by-side refrigerator and pioneered the home microwave oven. Today, Amana continues providing straightforward, reliable appliances for practical households.",
        "known_for": "affordable quality, simple controls, and dependable basics"
    },
    "fisher-paykel": {
        "name": "Fisher & Paykel",
        "desc": "New Zealand-based Fisher & Paykel brings innovative design thinking to home appliances. Their DishDrawer dishwashers and SmartDrive washers represent fresh approaches to everyday tasks.",
        "known_for": "DishDrawer dishwashers, innovative design, and ActiveSmart refrigeration"
    }
}

# Default brand info for brands not in the dictionary
DEFAULT_BRAND = {
    "desc": "This trusted appliance brand has earned a reputation for quality and reliability. Our factory-trained technicians have extensive experience servicing their complete product line.",
    "known_for": "quality construction and reliable performance"
}

# Appliance-specific content
APPLIANCES = {
    "dishwasher-repair": {
        "name": "Dishwasher",
        "problems": [
            "Not draining or standing water in the bottom",
            "Dishes coming out dirty or with residue",
            "Strange noises during wash cycles",
            "Door won't latch or seal properly",
            "Water leaking onto the floor",
            "Control panel not responding",
            "Spray arms not spinning correctly"
        ],
        "desc": "Your dishwasher handles thousands of cycles over its lifetime, cleaning everything from delicate glassware to baked-on casserole dishes. When it stops working properly, dirty dishes pile up fast."
    },
    "refrigerator-repair": {
        "name": "Refrigerator",
        "problems": [
            "Not cooling or freezing properly",
            "Ice maker not producing ice",
            "Water dispenser not working",
            "Unusual noises or loud humming",
            "Frost buildup in freezer section",
            "Water pooling inside or underneath",
            "Temperature fluctuations"
        ],
        "desc": "Your refrigerator runs 24/7 to keep food fresh and safe. When cooling problems occur, hundreds of dollars in groceries can spoil within hours, making fast repair service essential."
    },
    "washer-repair": {
        "name": "Washer",
        "problems": [
            "Won't spin or agitate",
            "Not draining water properly",
            "Excessive vibration or walking",
            "Water not filling correctly",
            "Door or lid won't lock",
            "Clothes coming out still wet",
            "Error codes on display"
        ],
        "desc": "Your washing machine handles heavy loads of laundry week after week. When it breaks down, dirty clothes accumulate quickly and trips to the laundromat become necessary."
    },
    "dryer-repair": {
        "name": "Dryer",
        "problems": [
            "Not heating or clothes staying damp",
            "Taking too long to dry clothes",
            "Drum not spinning",
            "Unusual squeaking or grinding noises",
            "Burning smell during operation",
            "Shutting off mid-cycle",
            "Overheating issues"
        ],
        "desc": "A properly functioning dryer is essential for keeping up with laundry demands. When drying problems occur, clothes pile up and energy bills can spike from extended run times."
    },
    "oven-repair": {
        "name": "Oven",
        "problems": [
            "Not heating to correct temperature",
            "Uneven cooking or hot spots",
            "Self-cleaning cycle not working",
            "Door not closing properly",
            "Control panel malfunctions",
            "Igniter not lighting (gas ovens)",
            "Heating element failure"
        ],
        "desc": "Your oven is central to meal preparation, from weeknight dinners to holiday feasts. Temperature problems can ruin recipes you've made perfectly for years."
    },
    "cooktop-repair": {
        "name": "Cooktop",
        "problems": [
            "Burners not igniting (gas)",
            "Electric elements not heating",
            "Induction not detecting cookware",
            "Cracked glass surface",
            "Uneven heating across burners",
            "Control knobs not responding",
            "Gas smell when operating"
        ],
        "desc": "Your cooktop sees daily use for everything from morning coffee to elaborate dinners. When burners fail, your cooking options become severely limited."
    },
    "microwave-repair": {
        "name": "Microwave",
        "problems": [
            "Not heating food properly",
            "Turntable not rotating",
            "Sparking inside the unit",
            "Door not closing or sealing",
            "Display or controls not working",
            "Unusual humming or buzzing",
            "Buttons not responding"
        ],
        "desc": "Modern kitchens rely on microwaves for quick reheating, defrosting, and cooking. When yours stops working, meal prep becomes significantly more time-consuming."
    },
    "vent-hood-repair": {
        "name": "Vent Hood",
        "problems": [
            "Fan not running or weak airflow",
            "Excessive noise during operation",
            "Lights not working",
            "Grease buildup affecting performance",
            "Motor running but not venting",
            "Control panel issues",
            "Vent flap not opening"
        ],
        "desc": "Your range hood removes smoke, steam, and cooking odors from your kitchen. When ventilation fails, cooking fumes linger and grease accumulates on surfaces."
    },
    "wine-cooler-repair": {
        "name": "Wine Cooler",
        "problems": [
            "Not maintaining proper temperature",
            "Compressor running constantly",
            "Excessive vibration affecting wine",
            "Humidity control issues",
            "Door seal problems",
            "LED lighting failures",
            "Temperature fluctuations"
        ],
        "desc": "Wine coolers protect your collection by maintaining precise temperature and humidity levels. When cooling fails, valuable wines can be damaged by temperature swings."
    }
}

DEFAULT_APPLIANCE = {
    "name": "Appliance",
    "problems": [
        "Not turning on or powering up",
        "Strange noises during operation",
        "Not performing as expected",
        "Error codes on display",
        "Intermittent functionality",
        "Control panel issues"
    ],
    "desc": "When your appliance stops working properly, it disrupts your daily routine. Our technicians diagnose and repair all types of issues quickly."
}

def get_brand_info(brand_slug):
    """Get brand information from slug."""
    if brand_slug in BRANDS:
        return BRANDS[brand_slug]
    # Try to make a readable name from slug
    name = brand_slug.replace("-", " ").title()
    return {"name": name, "desc": DEFAULT_BRAND["desc"], "known_for": DEFAULT_BRAND["known_for"]}

def get_appliance_info(appliance_slug):
    """Get appliance information from slug."""
    if appliance_slug in APPLIANCES:
        return APPLIANCES[appliance_slug]
    # Try to make a readable name from slug
    name = appliance_slug.replace("-repair", "").replace("-", " ").title()
    info = DEFAULT_APPLIANCE.copy()
    info["name"] = name
    return info

def generate_brand_appliance_content(brand_slug, appliance_slug):
    """Generate unique content for brand + appliance pages."""
    brand = get_brand_info(brand_slug)
    appliance = get_appliance_info(appliance_slug)

    problems_html = "\n".join([f'<li>{p}</li>' for p in appliance["problems"]])

    content = f'''
<section style="padding: 60px 0; background: #fff;">
<div class="container" style="max-width: 900px; margin: 0 auto; padding: 0 20px;">
<article>
<h2 style="text-align:center; font-size:28px; margin-bottom:25px; color: var(--blue);">Expert {brand["name"]} {appliance["name"]} Repair in Westchester County</h2>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
{appliance["desc"]} When your {brand["name"]} {appliance["name"].lower()} needs repair, you need technicians who understand the brand's specific engineering and technology.
</p>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
{brand["desc"]} {brand["name"]} is particularly known for {brand["known_for"]}.
</p>

<h3 style="font-size:22px; margin: 30px 0 15px; color: var(--blue);">Common {brand["name"]} {appliance["name"]} Problems We Fix</h3>

<ul style="line-height: 2; color: #444; font-size: 16px; padding-left: 20px; margin-bottom: 25px;">
{problems_html}
</ul>

<h3 style="font-size:22px; margin: 30px 0 15px; color: var(--blue);">Why Choose Our {brand["name"]} Repair Service?</h3>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
Our technicians receive specialized training on {brand["name"]} appliances and carry manufacturer-specific parts. We understand the unique components and technology that make {brand["name"]} different from other brands, allowing us to diagnose problems accurately and complete repairs efficiently.
</p>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
<strong>Same-day service available</strong> - We know a broken {appliance["name"].lower()} disrupts your entire household. Call us before noon and we'll have a technician at your door today.
</p>

</article>
</div>
</section>
'''
    return content

def generate_town_brand_content(town_slug, brand_slug):
    """Generate unique content for town + brand pages."""
    brand = get_brand_info(brand_slug)
    town_name = town_slug.replace("-", " ").title()

    content = f'''
<section style="padding: 60px 0; background: #fff;">
<div class="container" style="max-width: 900px; margin: 0 auto; padding: 0 20px;">
<article>
<h2 style="text-align:center; font-size:28px; margin-bottom:25px; color: var(--blue);">{brand["name"]} Appliance Repair in {town_name}, NY</h2>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
{town_name} residents trust our team for fast, reliable {brand["name"]} appliance repair. Whether you're in a historic home or modern residence, we service all {brand["name"]} appliances including refrigerators, dishwashers, washers, dryers, ovens, cooktops, and more.
</p>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
{brand["desc"]} Our technicians have extensive experience with {brand["name"]} products and carry common replacement parts on their service vehicles.
</p>

<h3 style="font-size:22px; margin: 30px 0 15px; color: var(--blue);">Local {brand["name"]} Service for {town_name}</h3>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
We provide same-day {brand["name"]} repair service throughout {town_name} and surrounding Westchester County communities. Our local presence means faster response times and technicians familiar with homes in your area.
</p>

<ul style="line-height: 2; color: #444; font-size: 16px; padding-left: 20px; margin-bottom: 25px;">
<li>Same-day appointments available for {town_name} residents</li>
<li>Factory-trained on all {brand["name"]} appliance models</li>
<li>Genuine {brand["name"]} replacement parts</li>
<li>Upfront pricing with no hidden fees</li>
<li>90-day warranty on all repairs</li>
</ul>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
<strong>Serving all of {town_name}</strong> - From residential neighborhoods to apartment complexes, we repair {brand["name"]} appliances throughout your community. Call now for fast, professional service.
</p>

</article>
</div>
</section>
'''
    return content

def generate_town_appliance_content(town_slug, appliance_slug):
    """Generate unique content for town + appliance pages."""
    appliance = get_appliance_info(appliance_slug)
    town_name = town_slug.replace("-", " ").title()

    problems_html = "\n".join([f'<li>{p}</li>' for p in appliance["problems"][:5]])

    content = f'''
<section style="padding: 60px 0; background: #fff;">
<div class="container" style="max-width: 900px; margin: 0 auto; padding: 0 20px;">
<article>
<h2 style="text-align:center; font-size:28px; margin-bottom:25px; color: var(--blue);">{appliance["name"]} Repair Service in {town_name}, NY</h2>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
{appliance["desc"]} {town_name} homeowners count on our experienced technicians for fast, reliable {appliance["name"].lower()} repair service.
</p>

<h3 style="font-size:22px; margin: 30px 0 15px; color: var(--blue);">Common {appliance["name"]} Problems in {town_name} Homes</h3>

<ul style="line-height: 2; color: #444; font-size: 16px; padding-left: 20px; margin-bottom: 25px;">
{problems_html}
</ul>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
We repair all major {appliance["name"].lower()} brands including Sub-Zero, Wolf, Thermador, Miele, Bosch, KitchenAid, Whirlpool, LG, Samsung, GE, and more. Our technicians arrive with fully-stocked service vehicles and complete most repairs in a single visit.
</p>

<h3 style="font-size:22px; margin: 30px 0 15px; color: var(--blue);">Fast {appliance["name"]} Repair for {town_name} Residents</h3>

<p style="line-height: 1.8; color: #444; font-size: 16px; margin-bottom: 20px;">
<strong>Same-day service available</strong> - Call before noon for same-day {appliance["name"].lower()} repair in {town_name}. We understand that appliance problems don't wait, and neither should you.
</p>

</article>
</div>
</section>
'''
    return content

def insert_content(file_path, content):
    """Insert content into HTML file after reviews accordion."""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if content already added (look for our unique marker)
    if 'Common ' in html and ' Problems We Fix</h3>' in html:
        return False
    if 'Local ' in html and ' Service for ' in html:
        return False

    # Find insertion point - after reviews accordion, before the about section
    # Pattern: </div></div> followed by whitespace and <section
    insertion_pattern = r'(</div></div>\s*\n)(\s*<section style="padding: 60px 0; background: #fff;")'
    match = re.search(insertion_pattern, html)

    if match:
        html = html[:match.end(1)] + content + "\n" + html[match.start(2):]
    else:
        # Try alternate pattern with aria-labelledby
        insertion_pattern2 = r'(</div></div>\s*\n)(\s*<section style="padding: 60px 0; background: #fff;" aria-labelledby)'
        match2 = re.search(insertion_pattern2, html)
        if match2:
            html = html[:match2.end(1)] + content + "\n" + html[match2.start(2):]
        else:
            # Fallback - insert after hero section
            pattern = r'(</section>\s*\n\s*<style>)'
            match3 = re.search(pattern, html)
            if match3:
                # Find the reviews accordion end and insert after
                reviews_end = html.find('</div></div>', html.find('reviews-accordion'))
                if reviews_end > 0:
                    insert_pos = reviews_end + len('</div></div>')
                    html = html[:insert_pos] + "\n" + content + html[insert_pos:]
                else:
                    return False
            else:
                return False

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return True

def process_brand_pages(base_path):
    """Process all brand + appliance sub-pages."""
    brands_path = os.path.join(base_path, 'brands')
    count = 0

    for brand_dir in os.listdir(brands_path):
        brand_path = os.path.join(brands_path, brand_dir)
        if not os.path.isdir(brand_path):
            continue

        for item in os.listdir(brand_path):
            item_path = os.path.join(brand_path, item)
            if os.path.isdir(item_path) and item.endswith('-repair'):
                index_file = os.path.join(item_path, 'index.html')
                if os.path.exists(index_file):
                    content = generate_brand_appliance_content(brand_dir, item)
                    if insert_content(index_file, content):
                        count += 1
                        print(f"Updated: brands/{brand_dir}/{item}/")

    return count

def process_town_pages(base_path):
    """Process all town sub-pages."""
    ny_path = os.path.join(base_path, 'ny')
    count = 0

    for town_dir in os.listdir(ny_path):
        town_path = os.path.join(ny_path, town_dir)
        if not os.path.isdir(town_path):
            continue

        for item in os.listdir(town_path):
            item_path = os.path.join(town_path, item)
            if os.path.isdir(item_path):
                index_file = os.path.join(item_path, 'index.html')
                if os.path.exists(index_file):
                    if item.endswith('-repair'):
                        # This is a brand repair page (e.g., samsung-repair)
                        brand_slug = item.replace('-repair', '')
                        content = generate_town_brand_content(town_dir, brand_slug)
                    else:
                        # This is an appliance page (e.g., dishwasher-repair)
                        content = generate_town_appliance_content(town_dir, item)

                    if insert_content(index_file, content):
                        count += 1
                        print(f"Updated: ny/{town_dir}/{item}/")

    return count

if __name__ == "__main__":
    base_path = "/Users/globalaffiliate/westchester-county-repair"

    print("Adding unique content to brand pages...")
    brand_count = process_brand_pages(base_path)
    print(f"\nUpdated {brand_count} brand pages")

    print("\nAdding unique content to town pages...")
    town_count = process_town_pages(base_path)
    print(f"\nUpdated {town_count} town pages")

    print(f"\n=== TOTAL: {brand_count + town_count} pages updated ===")
