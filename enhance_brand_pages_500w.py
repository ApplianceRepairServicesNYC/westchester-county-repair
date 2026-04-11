#!/usr/bin/env python3
"""
Enhance brand + appliance pages (e.g., /brands/ge/cooktop-repair/) with ~500 words unique content.
Only processes affected URLs from GSC CSV.
"""

import os
import re
import csv
from urllib.parse import urlparse

# Brand-specific detailed information
BRANDS = {
    "samsung": {
        "name": "Samsung",
        "founded": "1938 in South Korea",
        "hq": "Suwon, South Korea",
        "known_for": "innovative smart home technology, Family Hub refrigerators, FlexWash laundry systems, and Bespoke customizable appliances",
        "tech": "SmartThings connectivity, AI-powered sensors, Bespoke design platform",
        "history": "Samsung entered the appliance market in 1974 and has become a global leader in smart home technology, bringing cutting-edge features from their electronics expertise to household appliances."
    },
    "lg": {
        "name": "LG",
        "founded": "1958 in South Korea",
        "hq": "Seoul, South Korea",
        "known_for": "ThinQ smart technology, InstaView refrigerators, TurboWash laundry systems, and linear compressor reliability",
        "tech": "ThinQ AI, Inverter Linear Compressor, TurboWash 360, proactive customer care",
        "history": "Originally Lucky-Goldstar, LG has pioneered appliance innovations including the first refrigerator with a door-in-door design and AI-powered washing machines that detect fabric types."
    },
    "whirlpool": {
        "name": "Whirlpool",
        "founded": "1911 in Michigan, USA",
        "hq": "Benton Harbor, Michigan",
        "known_for": "dependable American-made appliances, Load & Go detergent systems, and adaptive wash technology",
        "tech": "Adaptive Wash technology, 6th Sense sensors, Load & Go XL dispensers",
        "history": "For over a century, Whirlpool has been America's most trusted appliance brand, manufacturing millions of washers, dryers, and kitchen appliances that families depend on daily."
    },
    "ge": {
        "name": "GE Appliances",
        "founded": "1907 in Kentucky, USA",
        "hq": "Louisville, Kentucky",
        "known_for": "innovative American engineering, Profile and Cafe premium lines, and UltraFresh laundry technology",
        "tech": "UltraFresh Vent System, TwinChill evaporators, WiFi Connect",
        "history": "GE Appliances has been an American household name for over 115 years, pioneering the electric refrigerator and continuing to innovate with smart home features and premium styling."
    },
    "bosch": {
        "name": "Bosch",
        "founded": "1886 in Germany",
        "hq": "Stuttgart, Germany",
        "known_for": "German engineering precision, whisper-quiet dishwashers, and compact European-style laundry",
        "tech": "PrecisionWash, Home Connect, EcoSilence Drive motors, CrystalDry",
        "history": "Bosch brings 135+ years of German engineering excellence to home appliances, particularly renowned for dishwashers so quiet they carry decibel ratings as a selling point."
    },
    "miele": {
        "name": "Miele",
        "founded": "1899 in Germany",
        "hq": "Gütersloh, Germany",
        "known_for": "exceptional 20-year build quality, German precision engineering, and premium materials",
        "tech": "TwinDos automatic dispensing, SteamCare, Miele@home connectivity",
        "history": "Miele remains family-owned after 125 years, testing every appliance to last 20 years of average use. Their commitment to quality means higher upfront costs but exceptional longevity."
    },
    "thermador": {
        "name": "Thermador",
        "founded": "1916 in California, USA",
        "hq": "Irvine, California (BSH Home Appliances)",
        "known_for": "Star Burner technology, Freedom refrigeration, and professional-grade cooking performance",
        "tech": "Star Burner patented design, Freedom Hinge, ExtraLow simmer",
        "history": "Thermador invented the built-in cooktop in 1947 and the downdraft ventilation system. Today, as part of BSH, Thermador continues to set standards for luxury American kitchen design."
    },
    "sub-zero": {
        "name": "Sub-Zero",
        "founded": "1945 in Wisconsin, USA",
        "hq": "Madison, Wisconsin",
        "known_for": "dual refrigeration systems, NASA air purification, and built-in refrigeration excellence",
        "tech": "dual compressors, magnetic door seals, antimicrobial air purification",
        "history": "Sub-Zero pioneered the built-in refrigerator and remains the gold standard for food preservation. Their dual refrigeration keeps produce fresh significantly longer than conventional units."
    },
    "wolf": {
        "name": "Wolf",
        "founded": "1934 in California, USA",
        "hq": "Madison, Wisconsin (Sub-Zero Group)",
        "known_for": "dual-stacked burners, professional cooking performance, and VertiCross convection",
        "tech": "Dual-Stacked sealed burners, VertiCross convection, infrared broilers",
        "history": "Wolf brought commercial cooking technology to home kitchens, becoming the choice of serious home chefs. Now part of the Sub-Zero family, Wolf continues to define luxury cooking."
    },
    "viking": {
        "name": "Viking",
        "founded": "1987 in Mississippi, USA",
        "hq": "Greenwood, Mississippi",
        "known_for": "professional-style ranges, high-BTU burners, and distinctive stainless steel design",
        "tech": "TruConvec convection, VariSimmer settings, Elevation burners",
        "history": "Viking revolutionized home kitchens by introducing the first professional-style range for residential use in 1987, creating an entirely new appliance category."
    },
    "gaggenau": {
        "name": "Gaggenau",
        "founded": "1683 in Germany",
        "hq": "Munich, Germany (BSH Home Appliances)",
        "known_for": "over 340 years of manufacturing heritage, architectural design, and restaurant-quality performance",
        "tech": "Full-surface induction, Combi-steam cooking, Vario modular cooktops",
        "history": "Gaggenau is one of the oldest industrial companies in Germany, evolving from metalworking to become the pinnacle of luxury kitchen appliances with uncompromising quality."
    },
    "dacor": {
        "name": "Dacor",
        "founded": "1965 in California, USA",
        "hq": "Los Angeles, California (Samsung subsidiary)",
        "known_for": "California innovation, smart connected ovens, and Illumina burner knobs",
        "tech": "iQ Controller, Four-Part Pure Convection, Illumina LED knobs",
        "history": "Founded by a rocket scientist, Dacor brought aerospace precision to kitchen appliances. Now part of Samsung, Dacor continues to innovate with smart home integration."
    },
    "kitchenaid": {
        "name": "KitchenAid",
        "founded": "1919 in Ohio, USA",
        "hq": "Benton Harbor, Michigan (Whirlpool subsidiary)",
        "known_for": "iconic stand mixers, professional-style cooking, and bold design",
        "tech": "Even-Heat True Convection, PrintShield finish, FreeFlex Third Rack",
        "history": "KitchenAid started with the legendary stand mixer and expanded to full kitchen suites. The brand represents serious cooking equipment for home chefs who demand professional results."
    },
    "jenn-air": {
        "name": "Jenn-Air",
        "founded": "1947 in Indiana, USA",
        "hq": "Benton Harbor, Michigan (Whirlpool subsidiary)",
        "known_for": "downdraft ventilation innovation, Rise and Noir design styles, and connected cooking",
        "tech": "V2 Vertical Dual-Fan convection, Downdraft systems, WiFi connectivity",
        "history": "Jenn-Air invented the self-ventilated downdraft cooktop in 1961, revolutionizing kitchen island design. Today's Jenn-Air offers two distinct design expressions: Rise and Noir."
    },
    "frigidaire": {
        "name": "Frigidaire",
        "founded": "1918 in Indiana, USA",
        "hq": "Charlotte, North Carolina (Electrolux subsidiary)",
        "known_for": "inventing the self-contained refrigerator, reliable value, and Gallery series upgrades",
        "tech": "EvenTemp cooling, PureAir Ultra filtration, SpaceWise organization",
        "history": "Frigidaire invented the first self-contained refrigerator in 1916, and the brand name became synonymous with refrigerators for decades. Today, Frigidaire offers practical appliances at competitive prices."
    },
    "electrolux": {
        "name": "Electrolux",
        "founded": "1919 in Sweden",
        "hq": "Stockholm, Sweden",
        "known_for": "Scandinavian design, Perfect Steam technology, and sustainable engineering",
        "tech": "Perfect Steam, SmartBoost premixing, LuxCare wash system",
        "history": "Electrolux is the world's second-largest appliance maker, bringing Swedish design sensibility and environmental consciousness to home appliances across the globe."
    },
    "maytag": {
        "name": "Maytag",
        "founded": "1893 in Iowa, USA",
        "hq": "Benton Harbor, Michigan (Whirlpool subsidiary)",
        "known_for": "commercial-grade durability, PowerWash agitator, and industry-leading warranties",
        "tech": "PowerWash cycle, Extra Power button, Commercial Technology",
        "history": "Maytag built its reputation on the 'lonely repairman' campaign, emphasizing reliability. Today's Maytag appliances carry on that legacy with 10-year limited warranties on key components."
    },
    "kenmore": {
        "name": "Kenmore",
        "founded": "1913 as Sears brand",
        "hq": "Hoffman Estates, Illinois",
        "known_for": "value-oriented quality, wide selection across categories, and accessible pricing",
        "tech": "Accela-Wash, Smart Motion, SmartDry",
        "history": "Kenmore was Sears' premium appliance brand for over a century, offering quality appliances at competitive prices. The brand continues to provide reliable household essentials."
    },
    "amana": {
        "name": "Amana",
        "founded": "1934 in Iowa, USA",
        "hq": "Benton Harbor, Michigan (Whirlpool subsidiary)",
        "known_for": "pioneering the home microwave oven, side-by-side refrigerators, and practical value",
        "tech": "Temp Assure freshness, simple controls, dependable basics",
        "history": "Amana introduced the first countertop microwave oven in 1967 and the first side-by-side refrigerator. The brand continues to offer straightforward, reliable appliances for everyday households."
    },
    "fisher-paykel": {
        "name": "Fisher & Paykel",
        "founded": "1934 in New Zealand",
        "hq": "Auckland, New Zealand (Haier subsidiary)",
        "known_for": "innovative DishDrawer design, SmartDrive technology, and thoughtful engineering",
        "tech": "DishDrawer dishwashers, SmartDrive direct drive, ActiveSmart refrigeration",
        "history": "Fisher & Paykel brought fresh thinking to appliance design, most notably the revolutionary DishDrawer that changed how we think about dishwashers. Their New Zealand heritage emphasizes practical innovation."
    }
}

# Appliance-specific content for brand pages (Westchester-wide focus)
def get_brand_washer_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("ge"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Washer Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]}, {b["founded"]}, is {b["known_for"]}. {b["history"]} When your {b["name"]} washing machine needs repair anywhere in Westchester County, our factory-certified technicians bring specialized expertise to your home.</p>
<p style="margin-bottom: 12px;">We service {b["name"]} washers in every Westchester community from Yonkers to Rye, White Plains to Larchmont. Our technicians understand the unique installation challenges in Westchester homes—from compact laundry closets in condos to spacious utility rooms in estates. {b["name"]} technology like {b["tech"]} requires specialized diagnostic knowledge that our certified team provides.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Washer Repair Services:</strong> Our Westchester technicians diagnose and repair all {b["name"]} washer issues including spin cycle failures, drainage problems, excessive vibration, water fill issues, door/lid lock malfunctions, and error codes. We replace drum bearings, door boot seals, drain pumps, motor couplings, water inlet valves, transmissions, clutch assemblies, shock absorbers, and control boards using genuine {b["name"]} parts.</p>
<p style="margin-bottom: 12px;">Every {b["name"]} washer repair in Westchester County includes our comprehensive warranty and upfront pricing. We arrive with fully-stocked vehicles and complete most repairs in one visit. Same-day service is available throughout Westchester for urgent washer breakdowns that can't wait.</p>
'''

def get_brand_dryer_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("ge"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Dryer Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]} dryers incorporate {b["tech"]} to deliver efficient, effective drying performance. {b["history"]} Our Westchester County technicians are factory-certified to repair all {b["name"]} dryer models, from basic electric units to advanced heat pump technology.</p>
<p style="margin-bottom: 12px;">Dryer problems require prompt attention—clothes pile up fast when drying stops. We serve all Westchester communities including Scarsdale, Bronxville, Harrison, New Rochelle, and every town in between. Whether you have a gas dryer requiring ignition system expertise or an electric model with heating element concerns, our technicians arrive prepared with genuine {b["name"]} parts.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Dryer Repair Services:</strong> We diagnose and repair all {b["name"]} dryer issues: no heat, insufficient heat, overheating, drum not turning, squeaking noises, burning smells, mid-cycle shutoffs, and extended dry times. Our technicians replace heating elements, thermal fuses, drum rollers, belts, igniters, gas valve coils, motors, blower wheels, thermistors, and door switches.</p>
<p style="margin-bottom: 12px;">Proper venting is critical for dryer performance and safety. We inspect ventilation during every {b["name"]} dryer service call in Westchester County and recommend professional cleaning when needed. All repairs include our warranty protection and are completed with genuine {b["name"]} replacement parts.</p>
'''

def get_brand_refrigerator_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("ge"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Refrigerator Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]} refrigeration, {b["founded"]}, features {b["tech"]}. {b["history"]} When cooling problems threaten your food supply in any Westchester County home, our certified technicians provide rapid response to protect your groceries.</p>
<p style="margin-bottom: 12px;">Refrigerator emergencies can't wait—spoiled food costs money and poses health risks. We provide same-day {b["name"]} refrigerator repair throughout Westchester County, from waterfront communities in Mamaroneck to estate neighborhoods in Purchase. Our technicians understand the sophisticated technology in {b["name"]} refrigerators and carry the diagnostic tools to service all models.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Refrigerator Repair Services:</strong> We diagnose and repair all {b["name"]} refrigerator problems: cooling failures, ice maker issues, water dispenser problems, unusual noises, frost buildup, temperature fluctuations, and water leaks. Our technicians service compressors, evaporator fans, condenser coils, defrost systems, thermostats, start relays, door gaskets, ice makers, water filters, and control boards.</p>
<p style="margin-bottom: 12px;">Westchester homes feature everything from built-in refrigerator installations to counter-depth configurations. Our {b["name"]} certified technicians have experience with all installation types and understand the specific requirements of each. Every refrigerator repair includes genuine {b["name"]} parts and our comprehensive service warranty.</p>
'''

def get_brand_dishwasher_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("ge"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Dishwasher Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]} dishwashers feature {b["tech"]} for superior cleaning results. {b["history"]} When your {b["name"]} dishwasher stops cleaning effectively in your Westchester County kitchen, dirty dishes pile up and hand-washing becomes a daily burden.</p>
<p style="margin-bottom: 12px;">We service {b["name"]} dishwashers in every Westchester community—from compact condos in White Plains to estate kitchens in Scarsdale. Our technicians understand the specific water conditions in Westchester County and how they affect dishwasher performance. {b["name"]} technology requires trained technicians who can properly diagnose issues with sophisticated wash systems and sensors.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Dishwasher Repair Services:</strong> We diagnose and repair all {b["name"]} dishwasher problems: poor cleaning, drainage failures, leaking water, door latch issues, spray arm problems, detergent dispenser malfunctions, drying failures, and error codes. Our technicians service circulation pumps, drain pumps, door mechanisms, spray arms, float switches, inlet valves, heating elements, control boards, rack components, and gaskets.</p>
<p style="margin-bottom: 12px;">Hard water in many Westchester areas affects dishwasher performance over time. We provide maintenance advice along with repairs to help your {b["name"]} dishwasher perform optimally. All service calls include genuine {b["name"]} parts and our satisfaction guarantee.</p>
'''

def get_brand_oven_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("ge"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Oven & Range Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]} cooking appliances bring {b["tech"]} to Westchester County kitchens. {b["history"]} When your {b["name"]} oven stops heating properly, family meals and entertaining plans are disrupted until our certified technicians restore full cooking capability.</p>
<p style="margin-bottom: 12px;">We service {b["name"]} ovens and ranges throughout Westchester County, from Yonkers to Yorktown, Tarrytown to Tuckahoe. Our technicians are trained on both gas and electric {b["name"]} cooking appliances, with expertise in convection systems, self-cleaning mechanisms, and smart oven technology. Luxury kitchens in Westchester often feature premium {b["name"]} ranges that require specialized service knowledge.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Oven Repair Services:</strong> We diagnose and repair all {b["name"]} oven issues: heating failures, uneven cooking, temperature inaccuracy, self-clean problems, door issues, igniter failures in gas ovens, and control malfunctions. Our technicians replace bake elements, broil elements, igniters, thermostats, control boards, door hinges, gaskets, convection fans, temperature sensors, and safety valves.</p>
<p style="margin-bottom: 12px;">Gas oven repairs require licensed expertise in ignition systems and gas line safety—qualifications our technicians maintain. We carry genuine {b["name"]} parts and provide same-day service for urgent cooking needs throughout Westchester County. Every repair includes our comprehensive warranty.</p>
'''

def get_brand_cooktop_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("ge"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Cooktop Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]} cooktops feature {b["tech"]} for precise cooking control. {b["history"]} When burners fail or heating elements stop working in your Westchester County kitchen, cooking options become severely limited until repairs are made.</p>
<p style="margin-bottom: 12px;">We service all {b["name"]} cooktop types throughout Westchester—gas, electric, and induction. From island installations in gourmet kitchens to standard cooktops in family homes, our technicians understand the specific requirements of each configuration. {b["name"]} cooktops in Westchester homes range from basic models to sophisticated professional-style surfaces with unique repair needs.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Cooktop Repair Services:</strong> We diagnose and repair all {b["name"]} cooktop problems: ignition failures on gas burners, electric elements that don't heat, induction zones that won't detect cookware, cracked glass surfaces, uneven heating, control issues, and gas odors. Our technicians service igniters, spark modules, gas valves, heating elements, infinite switches, induction coils, control knobs, and wiring systems.</p>
<p style="margin-bottom: 12px;">Cooktop safety is paramount—gas leaks and electrical issues require professional attention. Our licensed technicians verify proper operation before completing any {b["name"]} cooktop repair in Westchester County. We carry genuine parts and provide upfront pricing on all service calls.</p>
'''

def get_brand_microwave_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("ge"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Microwave Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]} microwaves incorporate {b["tech"]} for convenient cooking and reheating. {b["history"]} When your {b["name"]} microwave stops heating in your Westchester County home, quick meal prep becomes significantly more time-consuming.</p>
<p style="margin-bottom: 12px;">We service all {b["name"]} microwave types throughout Westchester County—over-the-range units that combine cooking with ventilation, built-in models in custom cabinetry, and countertop units. Our technicians understand the safety protocols required for microwave repair, particularly with high-voltage components like magnetrons and capacitors.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Microwave Repair Services:</strong> We diagnose and repair all {b["name"]} microwave problems: no heating despite operation, turntable failures, sparking, door latch issues, display malfunctions, unresponsive controls, lighting failures, and unusual sounds. Our technicians service magnetrons, capacitors, diodes, door switches, turntable motors, control boards, waveguide covers, fuses, and touchpads.</p>
<p style="margin-bottom: 12px;">Over-the-range microwaves in Westchester kitchens require service for both cooking and ventilation functions. We repair exhaust fans, lighting, and filter systems alongside microwave components. All {b["name"]} microwave repairs include genuine parts and our service warranty.</p>
'''

def get_brand_wine_cooler_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("sub-zero"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Wine Cooler Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]} wine storage utilizes {b["tech"]} to protect valuable wine collections. {b["history"]} Westchester County's wine enthusiasts invest significantly in their collections, making proper storage temperature and humidity control essential for preservation.</p>
<p style="margin-bottom: 12px;">We service {b["name"]} wine coolers throughout Westchester—from undercounter units in kitchen islands to dedicated wine rooms in estate cellars. Temperature fluctuations can damage wine within hours, so we provide prompt response for all wine cooler emergencies. Our technicians understand the precise conditions wine requires and the technology {b["name"]} uses to maintain them.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Wine Cooler Repair Services:</strong> We diagnose and repair all {b["name"]} wine cooler problems: temperature control failures, compressor cycling issues, excessive vibration, humidity problems, door seal failures, lighting malfunctions, and zone temperature inconsistencies. Our technicians service compressors, thermostats, evaporator fans, condensers, gaskets, vibration dampeners, humidity controls, and control boards.</p>
<p style="margin-bottom: 12px;">Wine storage is more demanding than standard refrigeration—vibration, temperature precision, and humidity all affect wine quality. Our {b["name"]} certified technicians understand these requirements and service wine coolers with the care your collection deserves. We carry genuine parts and minimize repair time to protect your investment.</p>
'''

def get_brand_vent_hood_content(brand):
    b = BRANDS.get(brand.lower().replace(" ", "-").replace("&", ""), BRANDS.get("ge"))
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{b["name"]} Vent Hood Service Across Westchester County</strong></p>
<p style="margin-bottom: 12px;">{b["name"]} ventilation systems remove smoke, steam, and cooking odors from Westchester County kitchens. {b["history"]} When your {b["name"]} range hood stops ventilating properly, cooking fumes linger and grease accumulates on cabinets and surfaces throughout your kitchen.</p>
<p style="margin-bottom: 12px;">We service all {b["name"]} ventilation configurations in Westchester homes—wall-mounted hoods, island hoods, under-cabinet units, and downdraft systems. From professional-style kitchens in Scarsdale to condo galleys in White Plains, our technicians understand the installation and ductwork requirements that affect vent hood performance.</p>
<p style="margin-bottom: 12px;"><strong>Complete {b["name"]} Vent Hood Repair Services:</strong> We diagnose and repair all {b["name"]} vent hood problems: fans that don't run, weak airflow, excessive noise, lighting failures, controls that don't respond, grease accumulation affecting performance, motors that run without venting, and dampers that stick. Our technicians service blower motors, fan blades, light sockets, control switches, filters, dampers, wiring, capacitors, and speed controls.</p>
<p style="margin-bottom: 12px;">Proper kitchen ventilation protects your Westchester home from grease buildup and cooking odors. We inspect airflow and ductwork during every {b["name"]} vent hood service call and recommend professional duct cleaning when needed. All repairs include genuine {b["name"]} parts and our service warranty.</p>
'''

# Content generators by appliance type
APPLIANCE_CONTENT = {
    "washer-repair": get_brand_washer_content,
    "dryer-repair": get_brand_dryer_content,
    "refrigerator-repair": get_brand_refrigerator_content,
    "dishwasher-repair": get_brand_dishwasher_content,
    "oven-repair": get_brand_oven_content,
    "cooktop-repair": get_brand_cooktop_content,
    "microwave-repair": get_brand_microwave_content,
    "wine-cooler-repair": get_brand_wine_cooler_content,
    "vent-hood-repair": get_brand_vent_hood_content
}


def update_service_card(html, card_id, content):
    """Update a specific service card's expandable content."""
    if not content:
        return html

    pattern = rf'(<div id="expandable-text-{card_id}"[^>]*>)(.*?)(</div>\s*<div id="expandable-fade-{card_id}")'

    def replacer(match):
        opening = match.group(1)
        existing = match.group(2)
        closing = match.group(3)

        if "Service Across Westchester" in existing:
            return match.group(0)

        return opening + existing + content + closing

    return re.sub(pattern, replacer, html, flags=re.DOTALL)


def process_page(file_path, brand_slug, appliance_slug):
    """Process a single brand page to enhance all service cards."""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    original_html = html
    cards_updated = 0

    brand_name = brand_slug.replace("-", " ").title()
    brand_name = brand_name.replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero")
    brand_name = brand_name.replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid")
    brand_name = brand_name.replace("Fisher Paykel", "Fisher & Paykel")

    # Map appliance slugs to card IDs
    appliance_card_map = {
        "washer-repair": "washer",
        "dryer-repair": "dryer",
        "refrigerator-repair": "refrigerator",
        "dishwasher-repair": "dishwasher",
        "oven-repair": "oven",
        "cooktop-repair": "cooktop",
        "microwave-repair": "microwave",
        "wine-cooler-repair": "wine-cooler",
        "vent-hood-repair": "vent-hood"
    }

    for app_slug, content_func in APPLIANCE_CONTENT.items():
        card_id = appliance_card_map.get(app_slug, app_slug.replace("-repair", ""))
        content = content_func(brand_name)
        new_html = update_service_card(html, card_id, content)
        if new_html != html:
            html = new_html
            cards_updated += 1

    if html != original_html:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return cards_updated
    return 0


def main():
    base_path = "/Users/globalaffiliate/westchester-county-repair"
    csv_path = "/Users/globalaffiliate/Downloads/westchester-coverage-report/Table.csv"

    # Read affected URLs from CSV
    affected_urls = set()
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                affected_urls.add(row[0])

    print("=" * 60)
    print("ENHANCING BRAND PAGES (~500 words per card)")
    print(f"Processing brand pages from {len(affected_urls)} URLs")
    print("=" * 60)

    total_pages = 0
    total_cards = 0

    for url in sorted(affected_urls):
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')

        # Only process brands/brand/appliance-repair pages
        if len(path_parts) >= 3 and path_parts[0] == 'brands' and path_parts[2].endswith('-repair'):
            brand_slug = path_parts[1]
            appliance_slug = path_parts[2]

            file_path = os.path.join(base_path, *path_parts, 'index.html')

            if os.path.exists(file_path):
                cards = process_page(file_path, brand_slug, appliance_slug)
                if cards > 0:
                    total_pages += 1
                    total_cards += cards
                    print(f"Updated: {'/'.join(path_parts)}/ ({cards} cards)")

    print("\n" + "=" * 60)
    print(f"TOTAL: {total_pages} pages, {total_cards} service cards enhanced")
    print("=" * 60)


if __name__ == "__main__":
    main()
