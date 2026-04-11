#!/usr/bin/env python3
"""
Enhance service card show-more sections with ~500 words unique content per card.
Only processes the 334 affected pages from GSC CSV.
"""

import os
import re
import csv
from urllib.parse import urlparse

# City data with detailed info
CITIES = {
    "ardsley": {
        "name": "Ardsley",
        "pop": "4,800",
        "county": "Westchester County",
        "desc": "Known as 'The Village Beautiful', Ardsley features tree-lined streets and historic homes dating back to the early 1900s. This charming village combines small-town character with convenient access to New York City.",
        "homes": "Tudor-style homes, Colonials, and Cape Cods built between 1920-1960",
        "area": "Ardsley Park, Heatherdell, and the Ashford Avenue corridor"
    },
    "bronxville": {
        "name": "Bronxville",
        "pop": "6,500",
        "county": "Westchester County",
        "desc": "One of America's most affluent communities, Bronxville features distinctive Tudor and Colonial Revival architecture. This prestigious village is known for its top-ranked schools and walkable downtown.",
        "homes": "Grand Tudor estates, luxury condominiums, and historic mansions",
        "area": "Bronxville Village, Lawrence Park, and Armour Villa Park"
    },
    "dobbs-ferry": {
        "name": "Dobbs Ferry",
        "pop": "11,000",
        "county": "Westchester County",
        "desc": "A charming Hudson River village with scenic waterfront views and a vibrant Main Street. Dobbs Ferry combines historic character with modern amenities, attracting families and commuters alike.",
        "homes": "Victorian homes, riverfront properties, and modern condominiums",
        "area": "Downtown, the Heights, South Dobbs Ferry, and Wickers Creek"
    },
    "eastchester": {
        "name": "Eastchester",
        "pop": "19,500",
        "county": "Westchester County",
        "desc": "One of the oldest towns in Westchester, dating back to 1664. Eastchester offers a blend of suburban comfort and historical significance, with excellent schools and diverse housing options.",
        "homes": "Single-family Colonials, split-levels, and garden apartments",
        "area": "Chester Heights, Lake Isle, Waverly, and the Garth Road corridor"
    },
    "elmsford": {
        "name": "Elmsford",
        "pop": "5,000",
        "county": "Westchester County",
        "desc": "Strategically located at the intersection of major highways, Elmsford offers convenient access to employment centers while maintaining an affordable, family-friendly atmosphere.",
        "homes": "Affordable single-family homes, apartments, and townhomes",
        "area": "Downtown Elmsford and the Knollwood neighborhood"
    },
    "fairview": {
        "name": "Fairview",
        "pop": "3,700",
        "county": "Westchester County",
        "desc": "A small hamlet in the Town of Greenburgh known for its diverse community and convenient location near White Plains. Fairview offers affordable housing options in a welcoming neighborhood.",
        "homes": "Modest single-family homes and multi-family residences",
        "area": "Fairview and surrounding Greenburgh neighborhoods"
    },
    "harrison": {
        "name": "Harrison",
        "pop": "28,000",
        "county": "Westchester County",
        "desc": "Home to corporate headquarters and the prestigious Purchase area, Harrison combines executive-level living with excellent schools. The town offers diverse neighborhoods from West Harrison to Sterling Ridge.",
        "homes": "Luxury estates, executive homes, and upscale condominiums",
        "area": "Purchase, West Harrison, Sterling Ridge, and Silver Lake"
    },
    "hartsdale": {
        "name": "Hartsdale",
        "pop": "5,300",
        "county": "Westchester County",
        "desc": "A vibrant hamlet with a bustling commercial district featuring diverse dining and shopping. Hartsdale offers convenient commuting and a mix of housing styles for various lifestyles.",
        "homes": "Split-level homes, Colonials, and apartment complexes",
        "area": "East Hartsdale, West Hartsdale, and the Four Corners district"
    },
    "hastings-on-hudson": {
        "name": "Hastings-on-Hudson",
        "pop": "8,000",
        "county": "Westchester County",
        "desc": "An artistic community with stunning Hudson River views and eclectic architecture. Hastings-on-Hudson attracts creative professionals and families seeking character-rich homes and a strong community spirit.",
        "homes": "Victorian estates, artists' cottages, and modern eco-friendly homes",
        "area": "Downtown, The Dale, Hillside Woods, and Riverview Manor"
    },
    "irvington": {
        "name": "Irvington",
        "pop": "6,500",
        "county": "Westchester County",
        "desc": "A historic village home to Sunnyside, Washington Irving's estate. Irvington features stunning riverfront properties and a charming downtown with boutique shops and restaurants.",
        "homes": "Historic mansions, stone cottages, and luxury riverfront properties",
        "area": "Downtown, Matthiessen Park, Ardsley-on-Hudson, and Half Moon Bay"
    },
    "larchmont": {
        "name": "Larchmont",
        "pop": "6,200",
        "county": "Westchester County",
        "desc": "An exclusive waterfront community on Long Island Sound with yacht clubs and pristine beaches. Larchmont offers prestigious addresses, top schools, and a sophisticated village atmosphere.",
        "homes": "Luxury waterfront estates, Tudor mansions, and Victorian gems",
        "area": "Larchmont Manor, Murray Hill, Orienta Point, and Premium Mill"
    },
    "mamaroneck": {
        "name": "Mamaroneck",
        "pop": "19,000",
        "county": "Westchester County",
        "desc": "A vibrant harbor community with an active boating culture and diverse dining scene. Mamaroneck combines waterfront living with a walkable downtown and strong community events.",
        "homes": "Waterfront properties, Colonials, and beach cottages",
        "area": "Harbor Heights, Orienta, Washingtonville, and Rye Neck"
    },
    "mount-vernon": {
        "name": "Mount Vernon",
        "pop": "73,000",
        "county": "Westchester County",
        "desc": "Westchester's most populous city with a rich cultural heritage and diverse neighborhoods. Mount Vernon offers affordable housing options and convenient access to New York City.",
        "homes": "Multi-family homes, apartments, and historic single-family residences",
        "area": "Fleetwood, Chester Heights, South Side, and Hutchinson"
    },
    "new-rochelle": {
        "name": "New Rochelle",
        "pop": "80,000",
        "county": "Westchester County",
        "desc": "A major city with ongoing waterfront development, diverse communities, and direct Metro-North access to NYC. New Rochelle offers everything from beach living to urban amenities.",
        "homes": "High-rise condos, Colonials, Victorians, and beach cottages",
        "area": "Wykagyl, Beechmont, Huguenot Park, Premium Point, and North End"
    },
    "pelham-manor": {
        "name": "Pelham Manor",
        "pop": "5,500",
        "county": "Westchester County",
        "desc": "A prestigious village known for excellent schools and stately homes. Pelham Manor offers a suburban retreat with tree-lined streets and strong property values.",
        "homes": "Tudor estates, Colonials, and grand Victorian homes",
        "area": "Pelham Manor, North Pelham, and the Shore Road corridor"
    },
    "rye": {
        "name": "Rye",
        "pop": "16,000",
        "county": "Westchester County",
        "desc": "An affluent waterfront city featuring Playland amusement park and exclusive beach clubs. Rye combines small-city sophistication with premier recreational amenities.",
        "homes": "Waterfront estates, historic mansions, and luxury condominiums",
        "area": "Milton Point, Rye Beach, Park Avenue, and Grace Church neighborhoods"
    },
    "scarsdale": {
        "name": "Scarsdale",
        "pop": "18,000",
        "county": "Westchester County",
        "desc": "One of America's wealthiest communities with top-ranked schools and a country club lifestyle. Scarsdale features architect-designed homes and a prestigious village center.",
        "homes": "Grand estates, Tudor mansions, and architect-designed modern homes",
        "area": "Fox Meadow, Greenacres, Heathcote, Edgewood, and Quaker Ridge"
    },
    "tarrytown": {
        "name": "Tarrytown",
        "pop": "11,500",
        "county": "Westchester County",
        "desc": "Historic village of Washington Irving's 'Legend of Sleepy Hollow' with a charming riverfront downtown. Tarrytown combines literary history with scenic Hudson River living.",
        "homes": "Victorian homes, riverfront condos, and historic brownstones",
        "area": "Downtown, Sleepy Hollow Manor, Wilson Park, and Tarryhill"
    },
    "valhalla": {
        "name": "Valhalla",
        "pop": "3,500",
        "county": "Westchester County",
        "desc": "Home to Westchester Medical Center and the scenic Kensico Dam. Valhalla offers affordable housing options in a convenient location with access to major employers.",
        "homes": "Affordable single-family homes and condominiums",
        "area": "Valhalla, Kensico, and the Grasslands area"
    },
    "village-of-pelham": {
        "name": "Village of Pelham",
        "pop": "7,000",
        "county": "Westchester County",
        "desc": "A charming commuter village with an active downtown and historic district. The Village of Pelham offers easy Metro-North access and a strong sense of community.",
        "homes": "Victorians, Colonials, and brick townhouses",
        "area": "Pelham Heights, Chester Park, and Highbrook Gardens"
    },
    "white-plains": {
        "name": "White Plains",
        "pop": "58,000",
        "county": "Westchester County",
        "desc": "Westchester's commercial hub with major shopping centers, corporate offices, and cultural venues. White Plains offers urban amenities with diverse residential neighborhoods.",
        "homes": "Luxury high-rises, historic single-family homes, and modern condos",
        "area": "Battle Hill, Fisher Hill, Gedney Farms, Highlands, and North White Plains"
    },
    "yonkers": {
        "name": "Yonkers",
        "pop": "200,000",
        "county": "Westchester County",
        "desc": "New York State's fourth largest city with diverse neighborhoods and Hudson River waterfront development. Yonkers offers affordable urban living minutes from Manhattan.",
        "homes": "High-rises, Victorian homes, Colonials, and multi-family residences",
        "area": "Crestwood, Park Hill, Ludlow, Nepperhan, Getty Square, and Greystone"
    }
}

# Appliance-specific long-form content templates
def get_washer_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Washer Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">When your {brand} washing machine breaks down in {city["name"]}, you need technicians who understand both the sophisticated technology in modern washers and the specific challenges of servicing homes in {city["county"]}. {city["desc"]} The {city["homes"]} in this area often have unique installation requirements, from tight laundry closets in condos to dedicated laundry rooms in larger homes.</p>
<p style="margin-bottom: 12px;">Our factory-trained {brand} washer specialists serve all neighborhoods including {city["area"]}. We diagnose and repair the full range of washer problems: drums that won't spin or agitate, units that fail to drain leaving clothes soaking wet, excessive vibration that shakes the entire laundry area, water filling issues from slow fills to overflows, door or lid mechanisms that won't lock properly, and error codes that halt the cycle mid-wash.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Washer Repairs We Perform:</strong> Our technicians regularly replace worn drum bearings that cause grinding noises, door boot seals that leak water onto floors, drain pumps clogged with debris or coins, motor couplings that break from overloading, water inlet valves that fail to regulate flow, transmission components in top-loaders, clutch assemblies that slip during spin cycles, shock absorbers that cause excessive movement, and control boards that display error codes or fail to respond.</p>
<p style="margin-bottom: 12px;">We arrive at your {city["name"]} home with fully-stocked service vehicles carrying genuine {brand} replacement parts. Most washer repairs are completed in a single visit with our same-day service. We understand that a broken washer means laundry piling up, so we prioritize quick response times for {city["name"]} residents. All repairs include our comprehensive warranty, and we provide upfront pricing before any work begins.</p>
'''

def get_dryer_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Dryer Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">A malfunctioning {brand} dryer in your {city["name"]} home means damp clothes, extended dry times, and frustration. {city["desc"]} Whether you have a gas or electric dryer in one of the {city["homes"]} throughout {city["area"]}, our certified technicians have the expertise to diagnose and repair any issue quickly.</p>
<p style="margin-bottom: 12px;">Dryer problems range from no heat to insufficient heat to overheating—all of which we resolve daily for {city["name"]} homeowners. We troubleshoot drums that won't tumble, units that shut off mid-cycle, strange squeaking or grinding sounds, and burning smells that indicate potential hazards. Gas dryer issues require specialized knowledge of igniter systems and gas valves, while electric dryers have their own heating element and thermal fuse concerns.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Dryer Repairs We Perform:</strong> Our {city["name"]} service calls frequently involve replacing burned-out heating elements, blown thermal fuses that prevent operation, worn drum rollers that cause squeaking, frayed belts that stop the drum from turning, failed igniters in gas models, defective gas valve coils, motors that hum but don't spin, damaged blower wheels that reduce airflow, thermistors that misread temperature, and door switches that don't register when closed.</p>
<p style="margin-bottom: 12px;">Proper dryer ventilation is critical in {city["name"]} homes, especially in the {city["homes"]} with longer vent runs. We inspect ventilation during every service call and recommend cleaning when buildup restricts airflow. Our technicians carry genuine {brand} parts and complete most repairs during the first visit to your {city["name"]} home. Same-day appointments are available for urgent situations.</p>
'''

def get_refrigerator_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Refrigerator Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">Your {brand} refrigerator runs around the clock to protect hundreds of dollars in groceries for your {city["name"]} family. {city["desc"]} When cooling problems strike in the {city["homes"]} of {city["area"]}, you can't afford to wait—spoiled food and health risks demand immediate attention from qualified technicians.</p>
<p style="margin-bottom: 12px;">Our factory-trained specialists diagnose all {brand} refrigerator issues: units that won't cool or freeze properly, ice makers that stop producing or dispense slowly, water dispensers that won't flow, unusual compressor noises or constant running, excessive frost buildup in the freezer, water pooling inside or beneath the unit, and temperature fluctuations that affect food quality.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Refrigerator Repairs We Perform:</strong> {city["name"]} homeowners call us for compressor diagnosis and repair, evaporator fan motor replacement when airflow stops, condenser coil cleaning to restore efficiency, defrost system repairs for frost-free models, thermostat replacement for temperature control issues, start relay service when compressors won't kick on, door gasket replacement for proper sealing, ice maker component repairs, water filter system service, and control board diagnosis for electronic models.</p>
<p style="margin-bottom: 12px;">We understand that {city["name"]} families depend on their refrigerators daily. Our technicians arrive with commonly needed {brand} parts, and we offer same-day emergency service when your food is at risk. For the {city["homes"]} in this area, we're experienced with all installation configurations from built-in units to counter-depth models. Every repair includes our satisfaction guarantee and parts warranty.</p>
'''

def get_dishwasher_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Dishwasher Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">When your {brand} dishwasher stops cleaning effectively in your {city["name"]} home, dirty dishes pile up and hand-washing becomes a daily chore. {city["desc"]} The {city["homes"]} throughout {city["area"]} rely on efficient dishwashers to keep busy households running smoothly.</p>
<p style="margin-bottom: 12px;">Our technicians troubleshoot every {brand} dishwasher issue: units that won't drain leaving standing water, dishes that come out dirty or with food residue, water leaking onto kitchen floors, door latches that won't engage, spray arms that don't rotate properly, detergent dispensers that fail to release, drying problems leaving dishes wet, and control panels that don't respond to commands.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Dishwasher Repairs We Perform:</strong> Our {city["name"]} service calls include circulation pump replacement for weak water pressure, drain pump repair for units that won't empty, door latch mechanism service, spray arm bearing replacement, float switch adjustment for water level issues, inlet valve repair for filling problems, heating element service for drying and sanitizing, control board diagnosis, rack roller and adjuster repairs, and door gasket replacement for leak prevention.</p>
<p style="margin-bottom: 12px;">Dishwasher problems in {city["name"]} homes often relate to hard water deposits or installation issues specific to local housing. We clean spray arms and filters as part of our service and advise on proper loading and detergent use for optimal performance. Our {brand} certified technicians arrive with genuine parts and complete most repairs in one visit. Contact us for same-day service to restore your dishwasher's cleaning power.</p>
'''

def get_oven_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Oven & Range Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">Your {brand} oven is central to meal preparation in your {city["name"]} home, from weeknight dinners to holiday gatherings. {city["desc"]} When oven problems strike in the {city["homes"]} of {city["area"]}, family meals and entertaining plans are disrupted until repairs are made.</p>
<p style="margin-bottom: 12px;">Our factory-trained technicians diagnose all {brand} oven issues: ovens that won't heat or take forever to preheat, uneven cooking with hot spots and cold areas, self-cleaning cycles that won't start or complete, doors that don't close or seal properly, error codes and beeping, gas burners that won't ignite or produce weak flames, and temperature inaccuracies that ruin recipes.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Oven Repairs We Perform:</strong> {city["name"]} homeowners call us for bake element replacement when bottom heating fails, broil element service for top-heat problems, igniter replacement in gas ovens that won't light, thermostat calibration for temperature accuracy, control board diagnosis for electronic issues, door hinge repair for proper closure, door gasket replacement for heat retention, convection fan motor service, temperature sensor replacement, and safety valve repair in gas models.</p>
<p style="margin-bottom: 12px;">Gas oven repairs require specialized expertise in ignition systems and gas line safety—skills our technicians have perfected. For the {city["homes"]} in {city["name"]}, we're experienced with all configurations from slide-in ranges to double wall ovens. We carry genuine {brand} parts and provide same-day service for urgent cooking needs. All repairs include our comprehensive warranty for your peace of mind.</p>
'''

def get_cooktop_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Cooktop Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">A malfunctioning {brand} cooktop limits your cooking options in your {city["name"]} kitchen. {city["desc"]} Whether you have gas, electric, or induction cooking surfaces in the {city["homes"]} throughout {city["area"]}, our certified technicians restore full functionality quickly.</p>
<p style="margin-bottom: 12px;">We diagnose all {brand} cooktop problems: gas burners that won't ignite or click repeatedly without lighting, electric elements that don't heat or heat unevenly, induction zones that fail to detect cookware, cracked glass surfaces requiring professional assessment, uneven heat distribution across cooking zones, control knobs or touch panels that don't respond, and gas odors during operation that indicate potential safety issues.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Cooktop Repairs We Perform:</strong> Our {city["name"]} service includes spark igniter module replacement for gas burners that won't light, surface element replacement for electric cooktops, infinite switch service for temperature control problems, glass surface assessment and coordination, induction coil diagnosis and replacement, spark electrode cleaning and adjustment, gas valve repair for flow issues, burner cap alignment for proper flame pattern, touch control panel service, and wiring harness repair for electrical connections.</p>
<p style="margin-bottom: 12px;">Cooktop repairs require careful attention to both functionality and safety. For gas cooktops in {city["name"]} homes, we verify proper ignition and gas flow. Electric and induction models receive thorough electrical testing. We carry {brand} parts and complete most repairs during the first visit. Our technicians provide honest assessments and upfront pricing before beginning any work on your cooktop.</p>
'''

def get_microwave_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Microwave Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">Your {brand} microwave handles quick meals, reheating, and defrosting for your busy {city["name"]} household. {city["desc"]} When microwave problems occur in the {city["homes"]} of {city["area"]}, meal preparation becomes significantly more time-consuming.</p>
<p style="margin-bottom: 12px;">Our technicians troubleshoot all {brand} microwave issues: units that don't heat food despite running, turntables that stop rotating, sparking or arcing inside the cooking chamber, doors that don't latch or seal properly, display panels that go blank or show errors, buttons that don't respond to touch, interior lights that won't illuminate, and unusual humming or buzzing sounds.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Microwave Repairs We Perform:</strong> {city["name"]} homeowners call us for magnetron replacement when heating fails, high-voltage capacitor and diode service, door switch replacement for interlock safety, turntable motor repair for rotation issues, control board diagnosis for electronic failures, waveguide cover replacement after arcing damage, thermal fuse service, door latch mechanism repair, touchpad and membrane switch replacement, and fan motor service for ventilation problems.</p>
<p style="margin-bottom: 12px;">Over-the-range microwaves in {city["name"]} kitchens require expertise in both cooking and ventilation functions. We service the exhaust fan and lighting systems alongside cooking components. Our {brand} trained technicians carry genuine parts and understand the safety protocols required for microwave repair. Same-day service is available for most {city["name"]} locations to quickly restore your microwave convenience.</p>
'''

def get_wine_cooler_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Wine Cooler Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">Your {brand} wine cooler protects a valuable collection that may represent years of careful selection and significant investment. {city["desc"]} For wine enthusiasts in the {city["homes"]} of {city["area"]}, proper storage temperature and humidity are non-negotiable.</p>
<p style="margin-bottom: 12px;">We diagnose all {brand} wine cooler issues: units that don't maintain proper temperature zones, compressors that run constantly or cycle too frequently, excessive vibration that disturbs wine sediment, humidity control problems that dry out corks, door seal failures that allow temperature fluctuation, LED lighting that won't illuminate, and inconsistent temperatures between zones in dual-zone models.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Wine Cooler Repairs We Perform:</strong> Our {city["name"]} service includes compressor diagnosis and repair for cooling failures, thermostat calibration for accurate temperature, evaporator fan service for air circulation, condenser cleaning to maintain efficiency, door gasket replacement for proper sealing, vibration dampener adjustment or replacement, humidity control system service, LED lighting repair, temperature sensor replacement for dual-zone accuracy, and control board diagnosis for digital models.</p>
<p style="margin-bottom: 12px;">Wine storage requires precise conditions that general refrigeration doesn't provide. Our {brand} certified technicians understand the specific temperature ranges and humidity levels wine requires. For {city["name"]} collectors, we provide expert service that protects your investment. We arrive with genuine parts and complete most repairs in one visit, minimizing the time your collection is at risk.</p>
'''

def get_vent_hood_content(brand, city):
    return f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand} Vent Hood Repair Expertise in {city["name"]}</strong></p>
<p style="margin-bottom: 12px;">Your {brand} range hood removes smoke, steam, grease, and cooking odors from your {city["name"]} kitchen. {city["desc"]} When ventilation fails in the {city["homes"]} of {city["area"]}, cooking fumes linger and grease accumulates on cabinets and surfaces.</p>
<p style="margin-bottom: 12px;">Our technicians troubleshoot all {brand} vent hood problems: fans that don't run or produce weak airflow, excessive noise during operation, lights that won't turn on or flicker, units that won't shut off after cooking, grease buildup affecting performance despite filter cleaning, motors that run but don't move air, control switches that don't respond, and damper flaps that stick open or closed.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand} Vent Hood Repairs We Perform:</strong> {city["name"]} homeowners call us for blower motor replacement when ventilation fails, fan blade balancing or replacement for noise reduction, light socket and wiring repair, control switch service for speed settings, grease filter and baffle cleaning guidance, duct damper repair for proper airflow direction, capacitor replacement for motor starting issues, speed control module service, wiring harness repair, and exhaust duct inspection for blockages.</p>
<p style="margin-bottom: 12px;">Proper kitchen ventilation protects your {city["name"]} home from grease buildup, moisture damage, and lingering odors. Our {brand} trained technicians verify airflow rates and inspect ductwork during service calls. We carry genuine replacement parts and complete most vent hood repairs during the first visit. For the {city["homes"]} in this area, we understand various installation configurations from island mounts to under-cabinet units.</p>
'''


# Content generators by appliance type
APPLIANCE_CONTENT = {
    "washer": get_washer_content,
    "dryer": get_dryer_content,
    "refrigerator": get_refrigerator_content,
    "dishwasher": get_dishwasher_content,
    "oven": get_oven_content,
    "cooktop": get_cooktop_content,
    "microwave": get_microwave_content,
    "wine-cooler": get_wine_cooler_content,
    "vent-hood": get_vent_hood_content
}


def get_city_data(city_slug):
    """Get city data or return default."""
    if city_slug in CITIES:
        return CITIES[city_slug]
    name = city_slug.replace("-", " ").title()
    return {
        "name": name,
        "pop": "varies",
        "county": "Westchester County",
        "desc": f"{name} is a wonderful community in Westchester County offering quality residential neighborhoods.",
        "homes": "various residential properties",
        "area": "all neighborhoods"
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

        # Check if enhanced content already exists
        if "Expertise in" in existing:
            return match.group(0)

        return opening + existing + content + closing

    return re.sub(pattern, replacer, html, flags=re.DOTALL)


def process_page(file_path, city_slug, brand_slug):
    """Process a single page to enhance all service cards."""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    original_html = html
    cards_updated = 0

    brand_name = brand_slug.replace("-", " ").title()
    # Fix common brand name formatting
    brand_name = brand_name.replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero")
    brand_name = brand_name.replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid")
    brand_name = brand_name.replace("Fisher Paykel", "Fisher & Paykel")

    city = get_city_data(city_slug)

    for appliance, content_func in APPLIANCE_CONTENT.items():
        card_id = appliance
        content = content_func(brand_name, city)
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
        next(reader)  # Skip header
        for row in reader:
            if row:
                affected_urls.add(row[0])

    print("=" * 60)
    print("ENHANCING SERVICE CARDS (~500 words per card)")
    print(f"Processing {len(affected_urls)} affected URLs from GSC")
    print("=" * 60)

    total_pages = 0
    total_cards = 0

    for url in sorted(affected_urls):
        # Parse URL to get city and brand
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')

        # Only process ny/city/brand-repair pages
        if len(path_parts) >= 3 and path_parts[0] == 'ny' and path_parts[2].endswith('-repair'):
            city_slug = path_parts[1]
            brand_slug = path_parts[2].replace('-repair', '')

            file_path = os.path.join(base_path, *path_parts, 'index.html')

            if os.path.exists(file_path):
                cards = process_page(file_path, city_slug, brand_slug)
                if cards > 0:
                    total_pages += 1
                    total_cards += cards
                    print(f"Updated: {'/'.join(path_parts)}/ ({cards} cards)")

    print("\n" + "=" * 60)
    print(f"TOTAL: {total_pages} pages, {total_cards} service cards enhanced")
    print("=" * 60)


if __name__ == "__main__":
    main()
