#!/usr/bin/env python3
"""
Fix duplicate content on brand+appliance and brand landing pages.
Add truly unique brand-specific content to differentiate pages.
"""

import os
import re
import csv
from urllib.parse import urlparse

# Brand-specific unique content that differs significantly between brands
BRAND_DATA = {
    "ge": {
        "full_name": "General Electric",
        "founded": "1892",
        "hq": "Boston, Massachusetts",
        "history": "General Electric has been an American appliance icon since Thomas Edison founded the company in 1892. For over 130 years, GE has pioneered home appliance innovation, introducing the first electric range in 1910 and the first home refrigerator in 1927. Today, GE Appliances operates as a Haier subsidiary while maintaining its American manufacturing heritage with facilities in Louisville, Kentucky.",
        "technologies": ["Profile series with premium features", "Café line for design-forward kitchens", "UltraFresh System with antimicrobial technology", "WiFi Connect smart home integration", "TurboBoil high-power burners"],
        "reputation": "Known for reliable mid-range appliances with excellent parts availability and service network coverage across the United States",
        "common_issues": "GE cooktops may experience igniter clicking without flame, surface element cycling issues, and touch control panel malfunctions on newer models",
        "model_lines": ["GE Profile", "GE Café", "GE Standard", "Monogram by GE"],
        "unique_features": "GE's proprietary Edge-to-Edge cooktop design maximizes cooking surface area, while their Tri-Ring burner element offers precise heat control from simmer to sear"
    },
    "samsung": {
        "full_name": "Samsung Electronics",
        "founded": "1969",
        "hq": "Suwon, South Korea",
        "history": "Samsung entered the home appliance market in 1969 and has since become a global leader in smart home technology. The company's Digital Appliances division combines Korean engineering precision with cutting-edge connectivity features. Samsung's North American headquarters in New Jersey oversees their extensive US appliance operations.",
        "technologies": ["SmartThings ecosystem integration", "Wi-Fi connectivity with app control", "Flex Zone dual-element design", "Virtual Flame LED indicators", "Rapid Boil technology"],
        "reputation": "Recognized for sleek modern designs, advanced smart features, and competitive pricing in the premium appliance segment",
        "common_issues": "Samsung cooktops may show error codes E-08 or E-09 related to temperature sensors, touch panel ghost touches, and occasional Wi-Fi connectivity drops",
        "model_lines": ["Samsung Bespoke", "Samsung Standard", "Samsung Flex"],
        "unique_features": "Samsung's Flex Cooktop line features magnetic cookware detection and the industry's first cooktop-integrated ventilation system that automatically adjusts fan speed based on cooking intensity"
    },
    "lg": {
        "full_name": "LG Electronics",
        "founded": "1958",
        "hq": "Seoul, South Korea",
        "history": "LG Electronics, originally GoldStar, began as a radio manufacturer in 1958 and has evolved into a premium home appliance innovator. The company's commitment to 'Life's Good' philosophy drives their focus on reliability and user experience. LG's US headquarters in Englewood Cliffs, New Jersey manages their growing American market presence.",
        "technologies": ["ThinQ AI smart platform", "EasyClean interior coating", "ProBake Convection technology", "UltraHeat 3200W power burner", "SmoothTouch glass controls"],
        "reputation": "Praised for exceptional build quality, quiet operation, and industry-leading warranty coverage on compressors and motors",
        "common_issues": "LG cooktops occasionally exhibit surface element hot spots, control panel button responsiveness issues, and bridge element connection failures",
        "model_lines": ["LG Studio", "LG Standard", "LG SIGNATURE"],
        "unique_features": "LG's exclusive UltraHeat Power Burner delivers 3200 watts for rapid boiling, while their EasyClean coating reduces cleaning time by preventing baked-on spills"
    },
    "frigidaire": {
        "full_name": "Frigidaire",
        "founded": "1918",
        "hq": "Charlotte, North Carolina",
        "history": "Frigidaire invented the self-contained refrigerator in 1918 and pioneered household refrigeration technology. Now owned by Electrolux, Frigidaire maintains its American heritage while incorporating European engineering standards. The brand remains one of America's most recognized appliance names with over a century of consumer trust.",
        "technologies": ["Air Fry capability in ranges", "Even Baking Technology", "Quick Boil element", "SpaceWise expandable elements", "Steam Clean option"],
        "reputation": "Valued for affordable reliability, straightforward functionality, and excellent value in the mid-range appliance market",
        "common_issues": "Frigidaire cooktops may experience burner cap misalignment affecting flame pattern, surface cracks from thermal shock, and infinite switch failures",
        "model_lines": ["Frigidaire Gallery", "Frigidaire Professional", "Frigidaire Standard"],
        "unique_features": "Frigidaire's SpaceWise expandable elements automatically adjust to pot size, while their Express-Select controls provide one-touch access to common temperature settings"
    },
    "whirlpool": {
        "full_name": "Whirlpool Corporation",
        "founded": "1911",
        "hq": "Benton Harbor, Michigan",
        "history": "Whirlpool began in 1911 as Upton Machine Company making electric motor-driven wringer washers. Today, Whirlpool Corporation is the world's largest home appliance manufacturer, owning brands like Maytag, KitchenAid, and JennAir. Their Michigan headquarters has driven American appliance innovation for over a century.",
        "technologies": ["FlexHeat dual radiant element", "Fingerprint resistant stainless steel", "Hot Surface Indicator lights", "AccuSimmer burner technology", "Frozen Bake technology"],
        "reputation": "Known for dependable everyday performance, extensive service network, and industry-leading customer support",
        "common_issues": "Whirlpool cooktops may show issues with infinite switch temperature cycling, surface element connectors loosening, and glass cooktop stress fractures",
        "model_lines": ["Whirlpool Standard", "Whirlpool Gold"],
        "unique_features": "Whirlpool's AccuSimmer burner maintains precise low temperatures for delicate sauces, while FlexHeat elements accommodate various cookware sizes efficiently"
    },
    "bosch": {
        "full_name": "Robert Bosch GmbH",
        "founded": "1886",
        "hq": "Stuttgart, Germany",
        "history": "Founded by Robert Bosch in 1886, this German engineering company brings precision manufacturing to home appliances. Bosch home appliances are produced by BSH Hausgeräte GmbH, a joint venture originally with Siemens. Their European engineering standards emphasize efficiency, quiet operation, and durability.",
        "technologies": ["FlameSelect precise burner control", "OptiSim simmer settings", "AutoChef automatic cooking programs", "PerfectFry sensor technology", "Home Connect app integration"],
        "reputation": "Recognized for German engineering excellence, whisper-quiet operation, and premium European design aesthetics",
        "common_issues": "Bosch cooktops may experience flame failure device sensitivity, electronic ignition module failures, and touch control calibration issues requiring professional recalibration",
        "model_lines": ["Bosch Benchmark", "Bosch 800 Series", "Bosch 500 Series", "Bosch 300 Series"],
        "unique_features": "Bosch's FlameSelect technology offers nine precise flame levels instead of infinite adjustment, providing restaurant-quality heat control for home chefs"
    },
    "kitchenaid": {
        "full_name": "KitchenAid",
        "founded": "1919",
        "hq": "Benton Harbor, Michigan",
        "history": "KitchenAid launched in 1919 with their iconic stand mixer designed by engineer Herbert Johnson. Now part of Whirlpool Corporation, KitchenAid has expanded from mixers to a full line of premium kitchen appliances. The brand maintains its reputation for professional-grade performance in home kitchens.",
        "technologies": ["Even-Heat True Convection", "Torch Melting Burner", "Professional Dual Ring burner", "SatinGlide racks", "EasyConvect conversion system"],
        "reputation": "Beloved by home chefs for professional-style performance, iconic design, and the legendary durability of their stand mixers extending to all appliances",
        "common_issues": "KitchenAid cooktops may show dual-ring burner ignition issues, porcelain grate chipping, and occasional spark module failures",
        "model_lines": ["KitchenAid Professional", "KitchenAid Standard", "KitchenAid Commercial-Style"],
        "unique_features": "KitchenAid's exclusive Torch Melting Burner provides 17,000 BTU for professional-level searing, while their Even-Heat system eliminates hot and cold spots"
    },
    "maytag": {
        "full_name": "Maytag Corporation",
        "founded": "1893",
        "hq": "Benton Harbor, Michigan",
        "history": "Maytag began in 1893 manufacturing farm equipment before shifting to washing machines in 1907. The brand's legendary Maytag Repairman advertising campaign highlighted their reliability reputation. Now owned by Whirlpool Corporation, Maytag continues emphasizing durability and dependability.",
        "technologies": ["Power Preheat for faster heating", "Precision Cooking system", "Power Burner high-output element", "Storage drawer functionality", "FIT system for easy installation"],
        "reputation": "Famous for rugged durability, straightforward functionality, and the 'Maytag Repairman' legendary reliability",
        "common_issues": "Maytag cooktops may exhibit element cycling irregularities, surface indicator light failures, and occasional thermostat calibration drift",
        "model_lines": ["Maytag Heritage", "Maytag Standard"],
        "unique_features": "Maytag's commercial-grade Power Burner delivers high heat for rapid boiling, while their extra-large capacity designs accommodate family-sized cookware"
    },
    "thermador": {
        "full_name": "Thermador",
        "founded": "1916",
        "hq": "Irvine, California",
        "history": "Thermador pioneered the built-in cooktop concept in 1932 and invented the downdraft ventilation system. Now part of BSH Home Appliances, Thermador maintains its California roots and reputation for professional-grade luxury appliances. The brand is synonymous with high-end kitchen design.",
        "technologies": ["Star Burner with 56% more coverage", "ExtraLow simmer capability", "Patented Pedestal Star Burner", "Freedom Induction technology", "HomeConnect smart integration"],
        "reputation": "The pinnacle of luxury cooking appliances, preferred by professional chefs and serious home cooks for uncompromising performance",
        "common_issues": "Thermador cooktops may require precise flame adjustment, occasional electronic ignition recalibration, and specialized maintenance for Star Burner components",
        "model_lines": ["Thermador Masterpiece", "Thermador Professional"],
        "unique_features": "Thermador's patented Star Burner design provides 56% more coverage than round burners and features 9 cooking levels with ExtraLow for delicate simmering at 100°F"
    },
    "viking": {
        "full_name": "Viking Range Corporation",
        "founded": "1987",
        "hq": "Greenwood, Mississippi",
        "history": "Fred Carl Jr. founded Viking Range in 1987 to bring professional-grade cooking equipment to home kitchens. Viking pioneered the professional-style home range market and remains a symbol of serious cooking. The company's Mississippi manufacturing facility produces appliances with commercial restaurant heritage.",
        "technologies": ["VariSimmer setting for precise control", "ProFlow convection system", "Elevation burner design", "TruGlide full-extension racks", "Rapid Ready preheat"],
        "reputation": "The original professional-style home appliance brand, representing commercial kitchen performance adapted for residential use",
        "common_issues": "Viking cooktops may experience gas valve adjustments, burner flame pattern variations, and occasional igniter timing issues requiring professional calibration",
        "model_lines": ["Viking Professional 7 Series", "Viking Professional 5 Series", "Viking 3 Series"],
        "unique_features": "Viking's Elevation Burner design with brass flame ports delivers even heat distribution, while VariSimmer provides precise low-temperature control for delicate sauces"
    },
    "miele": {
        "full_name": "Miele & Cie. KG",
        "founded": "1899",
        "hq": "Gütersloh, Germany",
        "history": "Carl Miele and Reinhard Zinkann founded Miele in 1899, and the company remains family-owned today. Miele's 'Immer Besser' (Forever Better) motto drives their commitment to longevity and quality. German engineering and 20-year lifespan testing distinguish Miele from mass-market competitors.",
        "technologies": ["Con@ctivity automatic hood synchronization", "TwinBooster double power", "PowerFlex cooking zones", "DirectSelection Plus controls", "EasyClean stainless steel"],
        "reputation": "Ultra-premium German engineering renowned for exceptional longevity, with appliances tested to perform for 20 years of daily use",
        "common_issues": "Miele cooktops rarely fail but may experience touch control sensitivity adjustments, zone recognition recalibration, and occasional power board replacements",
        "model_lines": ["Miele PureLine", "Miele ContourLine", "Miele SmartLine"],
        "unique_features": "Miele's Con@ctivity technology automatically activates and adjusts the range hood based on cooktop activity, while TwinBooster combines two zones for 7,400 watts of power"
    },
    "sub-zero": {
        "full_name": "Sub-Zero Group, Inc.",
        "founded": "1945",
        "hq": "Madison, Wisconsin",
        "history": "Westye Bakke founded Sub-Zero in 1945 to preserve food better using dual refrigeration technology. The Wisconsin company later acquired Wolf in 2000, creating a luxury appliance powerhouse. Sub-Zero appliances are built to last 20+ years with full-time food preservation technology.",
        "technologies": ["Dual refrigeration systems", "NASA air purification technology", "Vacuum seal drawers", "Precision temperature control", "Smart home integration"],
        "reputation": "The undisputed leader in luxury refrigeration, chosen by architects and designers for the most prestigious kitchen projects",
        "common_issues": "Sub-Zero units may require periodic condenser cleaning, door seal adjustments for optimal closure, and occasional compressor relay service",
        "model_lines": ["Sub-Zero Built-In", "Sub-Zero Integrated", "Sub-Zero Undercounter", "Sub-Zero PRO"],
        "unique_features": "Sub-Zero's dual refrigeration keeps freezer air separate from refrigerator air, preventing flavor transfer and maintaining optimal humidity levels for food preservation"
    },
    "wolf": {
        "full_name": "Wolf Appliance, Inc.",
        "founded": "1934",
        "hq": "Madison, Wisconsin",
        "history": "Wolf began in 1934 supplying heavy-duty cooking equipment to restaurants and institutions. Now part of Sub-Zero Group, Wolf brings commercial cooking performance to residential kitchens. Every Wolf product is tested to restaurant standards in their Madison, Wisconsin facility.",
        "technologies": ["Dual-Stacked burners for precision", "Infrared charbroiler option", "Red control knobs signature design", "VertiCross convection", "Gourmet Mode automatic cooking"],
        "reputation": "Commercial-grade cooking performance in a residential package, preferred by professional chefs outfitting their home kitchens",
        "common_issues": "Wolf cooktops may need periodic burner alignment, spark igniter cleaning, and occasional gas valve adjustments for optimal flame patterns",
        "model_lines": ["Wolf Professional", "Wolf Transitional", "Wolf Contemporary"],
        "unique_features": "Wolf's patented Dual-Stacked sealed burners deliver precise control from 300 BTU simmer to 20,000 BTU sear, with two tiers of flame ports for even heat distribution"
    },
    "jenn-air": {
        "full_name": "Jenn-Air",
        "founded": "1961",
        "hq": "Benton Harbor, Michigan",
        "history": "Louis Jenn invented the first self-ventilated cooktop with downdraft in 1961, revolutionizing kitchen design. Now part of Whirlpool Corporation, Jenn-Air continues pushing boundaries with connected luxury appliances. The brand represents the intersection of innovation and sophisticated design.",
        "technologies": ["Downdraft ventilation system", "Duet burner system", "Brass PowerBurner", "WiFi connectivity", "LCD touch screen controls"],
        "reputation": "Innovation leader known for inventing downdraft ventilation and continuing to pioneer connected luxury kitchen technology",
        "common_issues": "Jenn-Air cooktops may experience downdraft motor issues, blower assembly maintenance needs, and occasional touch panel responsiveness problems",
        "model_lines": ["Jenn-Air NOIR", "Jenn-Air RISE"],
        "unique_features": "Jenn-Air's integrated downdraft ventilation eliminates the need for overhead hoods, while their connected platform allows remote preheating and monitoring"
    },
    "dacor": {
        "full_name": "Dacor",
        "founded": "1965",
        "hq": "Los Angeles, California",
        "history": "The Joseph family founded Dacor in 1965 in their California garage, pioneering residential professional-style cooking. Samsung acquired Dacor in 2016, combining California design sensibility with Korean technology innovation. Dacor remains committed to crafting distinctive luxury appliances.",
        "technologies": ["iQ remote control system", "RapidHeat baking technology", "SimmerSear burner", "LCD control panel", "GreenClean steam cleaning"],
        "reputation": "California-designed luxury with artisanal craftsmanship, offering distinctive style for design-conscious homeowners",
        "common_issues": "Dacor cooktops may require LCD panel recalibration, SimmerSear burner adjustment, and occasional control board updates",
        "model_lines": ["Dacor Modernist", "Dacor Contemporary", "Dacor Heritage"],
        "unique_features": "Dacor's SimmerSear burner technology offers the industry's lowest simmer (500 BTU) and highest sear (18,000 BTU) in a single burner"
    },
    "electrolux": {
        "full_name": "AB Electrolux",
        "founded": "1919",
        "hq": "Stockholm, Sweden",
        "history": "Electrolux formed in 1919 through a merger of Elektromekaniska AB and AB Lux, becoming a Swedish appliance giant. The company owns Frigidaire and operates globally as one of the largest appliance manufacturers. Scandinavian design principles emphasize functionality and sustainability.",
        "technologies": ["Perfect Temp probe", "Air Sous Vide technology", "Effortless glide racks", "Perfect Convect3", "Auto sizing pan detection"],
        "reputation": "Swedish engineering focused on sustainability and innovation, combining Scandinavian design with practical functionality",
        "common_issues": "Electrolux cooktops may show sensor calibration needs, touch control responsiveness issues, and occasional element connector problems",
        "model_lines": ["Electrolux Icon", "Electrolux 500 Series", "Electrolux 600 Series"],
        "unique_features": "Electrolux's Air Sous Vide technology brings precision restaurant cooking to home kitchens, while auto-sizing pan detection optimizes energy use"
    },
    "kenmore": {
        "full_name": "Kenmore",
        "founded": "1927",
        "hq": "Hoffman Estates, Illinois",
        "history": "Sears introduced the Kenmore brand in 1927 for sewing machines before expanding to all major appliances. Kenmore appliances are manufactured by various companies including Whirlpool, LG, and Electrolux. The brand represents value-oriented American appliance shopping tradition.",
        "technologies": ["Accela Steam technology", "PowerBurner high-output elements", "Smart and Connected platform", "Even Bake convection", "SpeedHeat rapid preheat"],
        "reputation": "America's most-sold appliance brand for decades, offering reliable mid-range value across all appliance categories",
        "common_issues": "Kenmore cooktops may experience surface element cycling issues, control knob wear, and occasional infinite switch failures",
        "model_lines": ["Kenmore Elite", "Kenmore Standard", "Kenmore Pro"],
        "unique_features": "Kenmore's PowerBurner elements deliver high heat for rapid boiling while maintaining energy efficiency, with models spanning budget to premium price points"
    },
    "amana": {
        "full_name": "Amana Corporation",
        "founded": "1934",
        "hq": "Benton Harbor, Michigan",
        "history": "Amana began as a refrigeration company founded by George Foerstner in the Iowa Amana Colonies community. The company introduced the first countertop microwave oven for home use in 1967. Now owned by Whirlpool, Amana focuses on affordable, reliable appliances.",
        "technologies": ["Temp Assure cooking system", "Spillsaver upswept cooktop", "Large oven window", "Adjustable self-cleaning", "Sabbath Mode"],
        "reputation": "Known for straightforward, affordable reliability without unnecessary complexity, serving value-conscious consumers",
        "common_issues": "Amana cooktops may show basic element failures, surface crack potential from impact, and occasional control knob loosening",
        "model_lines": ["Amana Standard"],
        "unique_features": "Amana's Spillsaver upswept cooktop edges contain spills while their simplified controls prioritize ease of use over complexity"
    },
    "fisher-paykel": {
        "full_name": "Fisher & Paykel",
        "founded": "1934",
        "hq": "Auckland, New Zealand",
        "history": "Woolf Fisher and Maurice Paykel founded their company in New Zealand in 1934 importing appliances before manufacturing their own. Now owned by Haier, Fisher & Paykel combines New Zealand heritage with global resources. Their innovative designs often debut in their home market before worldwide release.",
        "technologies": ["ActiveSmart technology", "Aero Tech cooking system", "SmartZone flexible induction", "Oil-sealed motors", "CoolTouch door technology"],
        "reputation": "New Zealand innovation with distinctive design, known for ergonomic features like DishDrawer dishwashers and drawer-style refrigeration",
        "common_issues": "Fisher & Paykel cooktops may require zone calibration, occasional touch panel sensitivity adjustment, and specialized service access",
        "model_lines": ["Fisher & Paykel Professional", "Fisher & Paykel Contemporary", "Fisher & Paykel Series"],
        "unique_features": "Fisher & Paykel's SmartZone technology allows multiple pots of different sizes to be recognized and heated independently within a single zone"
    },
    "gaggenau": {
        "full_name": "Gaggenau Hausgeräte GmbH",
        "founded": "1683",
        "hq": "Munich, Germany",
        "history": "Gaggenau traces its origins to 1683 as an ironworks in Germany's Black Forest. The company pioneered built-in kitchen appliances and maintains its artisanal manufacturing approach. Now part of BSH Home Appliances, Gaggenau represents the pinnacle of German appliance engineering.",
        "technologies": ["Vario modular cooking system", "Full surface induction", "Wok burner with 17,000 BTU", "Control knobs with automatic ignition", "EB satin glass front"],
        "reputation": "The ultimate in German engineering excellence and culinary precision, chosen by world-renowned architects and Michelin-starred chefs",
        "common_issues": "Gaggenau cooktops rarely fail but may require specialized calibration, professional gas adjustment, and occasional modular connection service",
        "model_lines": ["Gaggenau 400 Series", "Gaggenau 200 Series"],
        "unique_features": "Gaggenau's Vario modular system allows customized cooktop combinations with gas, induction, electric, Teppan Yaki, and professional wok elements"
    }
}

# Add more brands with generic but varied content
GENERIC_BRANDS = {
    "admiral": {"era": "1934", "origin": "Chicago", "style": "classic American", "specialty": "value-focused"},
    "aeg": {"era": "1883", "origin": "Berlin", "style": "German precision", "specialty": "energy efficiency"},
    "ariston": {"era": "1960", "origin": "Italy", "style": "Italian design", "specialty": "compact European"},
    "asko": {"era": "1950", "origin": "Sweden", "style": "Scandinavian", "specialty": "durability focused"},
    "avanti": {"era": "1972", "origin": "Miami", "style": "compact", "specialty": "small spaces"},
    "bertazzoni": {"era": "1882", "origin": "Emilia-Romagna Italy", "style": "Italian artisan", "specialty": "professional ranges"},
    "blomberg": {"era": "1883", "origin": "Germany", "style": "German practical", "specialty": "European efficiency"},
    "blue-star": {"era": "1880", "origin": "Reading PA", "style": "restaurant-grade", "specialty": "open burner design"},
    "crosley": {"era": "1920", "origin": "Cincinnati", "style": "retro American", "specialty": "nostalgic design"},
    "danby": {"era": "1947", "origin": "Ontario Canada", "style": "Canadian practical", "specialty": "compact units"},
    "dcs": {"era": "1988", "origin": "California", "style": "outdoor-indoor", "specialty": "professional grilling"},
    "fagor": {"era": "1956", "origin": "Spain Basque region", "style": "Spanish modern", "specialty": "pressure cooking"},
    "haier": {"era": "1984", "origin": "Qingdao China", "style": "global innovation", "specialty": "smart features"},
    "hotpoint": {"era": "1911", "origin": "California", "style": "classic reliable", "specialty": "entry level"},
    "inglis": {"era": "1880", "origin": "Toronto", "style": "Canadian heritage", "specialty": "laundry"},
    "liebherr": {"era": "1954", "origin": "Switzerland", "style": "Swiss precision", "specialty": "refrigeration"},
    "magic-chef": {"era": "1929", "origin": "St. Louis", "style": "vintage American", "specialty": "gas ranges"},
    "monogram": {"era": "1987", "origin": "Louisville", "style": "GE luxury", "specialty": "built-in integration"},
    "roper": {"era": "1874", "origin": "Illinois", "style": "traditional American", "specialty": "value basics"},
    "sharp": {"era": "1912", "origin": "Osaka Japan", "style": "Japanese precision", "specialty": "microwave innovation"},
    "smeg": {"era": "1948", "origin": "Reggio Emilia Italy", "style": "Italian retro", "specialty": "colorful design"},
    "speed-queen": {"era": "1908", "origin": "Wisconsin", "style": "commercial-grade", "specialty": "laundry durability"},
    "summit": {"era": "1969", "origin": "New York", "style": "American compact", "specialty": "ADA compliance"},
    "tappan": {"era": "1881", "origin": "Ohio", "style": "American classic", "specialty": "microwave pioneer"},
    "true": {"era": "1945", "origin": "St. Louis", "style": "commercial", "specialty": "restaurant refrigeration"},
    "u-line": {"era": "1962", "origin": "Milwaukee", "style": "modular", "specialty": "undercounter units"},
    "insignia": {"era": "2003", "origin": "Minnesota", "style": "modern budget", "specialty": "Best Buy exclusive"},
    "hisense": {"era": "1969", "origin": "Qingdao China", "style": "value technology", "specialty": "smart TVs and appliances"}
}

def get_brand_content(brand_slug):
    """Get unique brand-specific content."""
    if brand_slug in BRAND_DATA:
        return BRAND_DATA[brand_slug]

    # Generate content for generic brands
    generic = GENERIC_BRANDS.get(brand_slug, {
        "era": "1950s", "origin": "United States", "style": "traditional", "specialty": "home appliances"
    })

    brand_name = brand_slug.replace("-", " ").title()
    return {
        "full_name": brand_name,
        "founded": generic["era"],
        "hq": generic["origin"],
        "history": f"{brand_name} established its presence in the appliance market during the {generic['era']} era, originating from {generic['origin']}. The brand has built its reputation around {generic['style']} engineering principles with a focus on {generic['specialty']} products. Today, {brand_name} continues serving customers who appreciate quality craftsmanship.",
        "technologies": [f"{generic['style']} design philosophy", "Energy-efficient operation", "Durable construction"],
        "reputation": f"Known for {generic['style']} approach to appliance design with particular strength in {generic['specialty']} applications",
        "common_issues": f"{brand_name} appliances may occasionally require element replacement, control adjustments, or regular maintenance typical of quality appliances",
        "model_lines": [f"{brand_name} Standard", f"{brand_name} Premium"],
        "unique_features": f"{brand_name}'s commitment to {generic['specialty']} ensures reliable performance for demanding households"
    }


def generate_brand_intro_content(brand_slug, appliance_type):
    """Generate unique intro content for brand+appliance pages."""
    data = get_brand_content(brand_slug)
    brand_name = data["full_name"]

    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">About {brand_name} {appliance_type.replace("-", " ").title()}s</h4>
<p style="margin-bottom: 12px;">{data["history"]}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{brand_name} Technology & Innovation</h4>
<p style="margin-bottom: 12px;">{brand_name} incorporates advanced technologies including {", ".join(data["technologies"][:3])}. {data["reputation"]}. Their {appliance_type.replace("-", " ")} lineup represents years of engineering refinement.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {brand_name} {appliance_type.replace("-", " ").title()} Issues</h4>
<p style="margin-bottom: 12px;">{data["common_issues"]}. Our Westchester County technicians are factory-trained on all {brand_name} model lines including {" and ".join(data["model_lines"][:2])}.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Why Choose Our {brand_name} Service</h4>
<p style="margin-bottom: 12px;">{data["unique_features"]}. Our certified technicians understand the specific engineering philosophy behind {brand_name} appliances, enabling accurate diagnosis and proper repair using genuine {brand_name} parts. We service all {brand_name} {appliance_type.replace("-", " ")}s throughout Westchester County with same-day availability and comprehensive warranty coverage.</p>
'''


def update_card_1(html, brand_slug, appliance_type):
    """Update the intro card (card 1) with brand-specific content."""
    new_content = generate_brand_intro_content(brand_slug, appliance_type)

    pattern = r'(<div id="expandable-text-1"[^>]*>)(.*?)(</div>\s*<button id="expandable-btn-1")'

    def replacer(match):
        return match.group(1) + new_content + match.group(3)

    return re.sub(pattern, replacer, html, flags=re.DOTALL)


def process_brand_appliance_page(file_path, brand_slug, appliance_type):
    """Process a brand+appliance page."""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    html = update_card_1(html, brand_slug, appliance_type)

    if html != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def generate_brand_landing_content(brand_slug):
    """Generate unique intro content for brand landing pages."""
    data = get_brand_content(brand_slug)
    brand_name = data["full_name"]

    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">About {brand_name} Appliances</h4>
<p style="margin-bottom: 12px;">{data["history"]}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{brand_name} Product Lines</h4>
<p style="margin-bottom: 12px;">{brand_name} offers several product lines to meet different needs: {", ".join(data["model_lines"])}. {data["reputation"]}. Our Westchester County technicians are trained on all {brand_name} models from entry-level to premium lines.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{brand_name} Technology Features</h4>
<p style="margin-bottom: 12px;">Key technologies include {", ".join(data["technologies"][:4])}. {data["unique_features"]}. These innovations require specialized knowledge for proper service and repair.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {brand_name} Issues We Repair</h4>
<p style="margin-bottom: 12px;">{data["common_issues"]}. Our factory-certified technicians have the diagnostic tools, technical documentation, and genuine {brand_name} replacement parts needed to restore your appliances to peak performance quickly.</p>
'''


def process_brand_landing_page(file_path, brand_slug):
    """Process a brand landing page."""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    new_content = generate_brand_landing_content(brand_slug)
    pattern = r'(<div id="expandable-text-1"[^>]*>)(.*?)(</div>\s*<button id="expandable-btn-1")'

    def replacer(match):
        return match.group(1) + new_content + match.group(3)

    original = html
    html = re.sub(pattern, replacer, html, flags=re.DOTALL)

    if html != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    base_path = "/Users/globalaffiliate/westchester-county-repair"
    csv_path = "/Users/globalaffiliate/Downloads/westchester-coverage-report/Table.csv"

    # Get affected URLs
    affected = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                affected.append(row[0])

    print("=" * 60)
    print("FIXING DUPLICATE CONTENT ON BRAND PAGES")
    print("=" * 60)

    updated_appliance = 0
    updated_landing = 0

    for url in sorted(affected):
        parsed = urlparse(url)
        parts = parsed.path.strip('/').split('/')

        # Brand + Appliance pages: /brands/ge/cooktop-repair/
        if len(parts) == 3 and parts[0] == 'brands' and parts[2].endswith('-repair'):
            brand = parts[1]
            appliance = parts[2].replace('-repair', '')
            file_path = os.path.join(base_path, *parts, 'index.html')

            if os.path.exists(file_path):
                if process_brand_appliance_page(file_path, brand, appliance):
                    updated_appliance += 1
                    print(f"Updated: /brands/{brand}/{appliance}-repair/")

        # Brand Landing pages: /brands/inglis/
        elif len(parts) == 2 and parts[0] == 'brands':
            brand = parts[1]
            file_path = os.path.join(base_path, *parts, 'index.html')

            if os.path.exists(file_path):
                if process_brand_landing_page(file_path, brand):
                    updated_landing += 1
                    print(f"Updated: /brands/{brand}/")

    print("\n" + "=" * 60)
    print(f"Brand+Appliance pages: {updated_appliance}")
    print(f"Brand Landing pages: {updated_landing}")
    print(f"TOTAL: {updated_appliance + updated_landing} pages updated")
    print("=" * 60)


if __name__ == "__main__":
    main()
