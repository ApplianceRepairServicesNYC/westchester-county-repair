#!/usr/bin/env python3
"""
Generate truly unique content for each city+brand page.
Uses varied sentence structures and city-specific narratives.
"""

import os
import re
import csv
import random
from urllib.parse import urlparse

CITIES = {
    "ardsley": {"name": "Ardsley", "pop": "4,800", "type": "village", "character": "tree-lined suburban streets with Tudor architecture", "homes": "Tudor-style homes and Cape Cods from the 1920s", "areas": "Ardsley Park and Heatherdell", "known": "The Village Beautiful with excellent schools"},
    "bronxville": {"name": "Bronxville", "pop": "6,500", "type": "village", "character": "prestigious enclave of historic estates", "homes": "grand Tudor mansions and luxury condominiums", "areas": "Lawrence Park and Armour Villa", "known": "one of America's most affluent zip codes"},
    "dobbs-ferry": {"name": "Dobbs Ferry", "pop": "11,000", "type": "village", "character": "charming Hudson River waterfront community", "homes": "Victorian homes and riverfront properties", "areas": "the Heights and South Dobbs Ferry", "known": "scenic waterfront dining and Metro-North access"},
    "eastchester": {"name": "Eastchester", "pop": "19,500", "type": "town", "character": "historic community dating to 1664", "homes": "single-family Colonials and split-level homes", "areas": "Chester Heights and Lake Isle", "known": "one of Westchester's oldest established towns"},
    "elmsford": {"name": "Elmsford", "pop": "5,000", "type": "village", "character": "convenient commuter hub at highway crossroads", "homes": "affordable single-family homes and apartments", "areas": "Downtown and Knollwood neighborhoods", "known": "strategic location near I-87 and I-287"},
    "fairview": {"name": "Fairview", "pop": "3,700", "type": "hamlet", "character": "diverse residential area in Greenburgh", "homes": "modest single-family and multi-family residences", "areas": "central Fairview neighborhoods", "known": "welcoming diverse community atmosphere"},
    "harrison": {"name": "Harrison", "pop": "28,000", "type": "town", "character": "upscale corporate and residential area", "homes": "luxury estates and executive homes in Purchase", "areas": "Purchase, West Harrison, and Sterling Ridge", "known": "corporate headquarters and prestigious Purchase College"},
    "hartsdale": {"name": "Hartsdale", "pop": "5,300", "type": "hamlet", "character": "vibrant commercial and residential mix", "homes": "split-levels, Colonials, and garden apartments", "areas": "East Hartsdale and Four Corners", "known": "central shopping district and diverse housing"},
    "hastings-on-hudson": {"name": "Hastings-on-Hudson", "pop": "8,000", "type": "village", "character": "artistic riverfront community with creative spirit", "homes": "Victorian estates and artists' cottages", "areas": "Downtown and Hillside Woods", "known": "artistic heritage and stunning Hudson views"},
    "irvington": {"name": "Irvington", "pop": "6,500", "type": "village", "character": "historic village of literary heritage", "homes": "historic mansions and stone cottages", "areas": "Matthiessen Park and Ardsley-on-Hudson", "known": "Washington Irving's Sunnyside estate"},
    "larchmont": {"name": "Larchmont", "pop": "6,200", "type": "village", "character": "exclusive waterfront enclave on the Sound", "homes": "luxury waterfront estates and Tudor mansions", "areas": "Larchmont Manor and Orienta Point", "known": "prestigious yacht clubs and beach access"},
    "mamaroneck": {"name": "Mamaroneck", "pop": "19,000", "type": "village", "character": "vibrant harbor community with diverse culture", "homes": "waterfront properties and beach cottages", "areas": "Harbor Heights and Washingtonville", "known": "active boating culture and harbor restaurants"},
    "mount-vernon": {"name": "Mount Vernon", "pop": "73,000", "type": "city", "character": "diverse urban center with rich history", "homes": "multi-family homes and historic residences", "areas": "Fleetwood, Chester Heights, and South Side", "known": "Westchester's most populous and diverse city"},
    "new-rochelle": {"name": "New Rochelle", "pop": "80,000", "type": "city", "character": "major waterfront city with urban development", "homes": "high-rise condos and beach cottages", "areas": "Wykagyl, Beechmont, and Premium Point", "known": "significant waterfront revitalization"},
    "pelham-manor": {"name": "Pelham Manor", "pop": "5,500", "type": "village", "character": "stately residential community with top schools", "homes": "Tudor estates, Colonials, and Victorians", "areas": "Pelham Manor and Shore Road areas", "known": "exceptional public schools and quiet streets"},
    "rye": {"name": "Rye", "pop": "16,000", "type": "city", "character": "affluent waterfront community with attractions", "homes": "waterfront estates and historic mansions", "areas": "Milton Point and Rye Beach", "known": "Playland amusement park and exclusive beach clubs"},
    "scarsdale": {"name": "Scarsdale", "pop": "18,000", "type": "village", "character": "premier residential community of grand estates", "homes": "grand estates and architect-designed moderns", "areas": "Fox Meadow, Greenacres, and Heathcote", "known": "consistently ranked among America's wealthiest"},
    "tarrytown": {"name": "Tarrytown", "pop": "11,500", "type": "village", "character": "historic riverfront village of literary fame", "homes": "Victorian homes and riverfront condos", "areas": "Downtown and Sleepy Hollow Manor", "known": "Washington Irving's Legend of Sleepy Hollow"},
    "valhalla": {"name": "Valhalla", "pop": "3,500", "type": "hamlet", "character": "residential area near medical facilities", "homes": "affordable homes and condominiums", "areas": "Valhalla and Grasslands areas", "known": "Westchester Medical Center proximity"},
    "village-of-pelham": {"name": "Village of Pelham", "pop": "7,000", "type": "village", "character": "charming commuter village with character", "homes": "Victorians, Colonials, and townhouses", "areas": "Pelham Heights and Chester Park", "known": "easy Metro-North commute to Manhattan"},
    "white-plains": {"name": "White Plains", "pop": "58,000", "type": "city", "character": "Westchester's commercial and cultural center", "homes": "luxury high-rises and historic homes", "areas": "Battle Hill and Gedney Farms", "known": "county seat with major shopping and dining"},
    "yonkers": {"name": "Yonkers", "pop": "200,000", "type": "city", "character": "diverse major city with varied neighborhoods", "homes": "high-rises to Victorians across price points", "areas": "Crestwood, Park Hill, and Getty Square", "known": "fourth largest city in New York State"}
}

def get_city(slug):
    return CITIES.get(slug, {
        "name": slug.replace("-", " ").title(),
        "pop": "varies",
        "type": "community",
        "character": "quality residential neighborhood",
        "homes": "various home styles",
        "areas": "local neighborhoods",
        "known": "Westchester County living"
    })

def fix_brand(b):
    fixes = {
        "lg": "LG", "ge": "GE", "sub-zero": "Sub-Zero", "jenn-air": "Jenn-Air",
        "kitchenaid": "KitchenAid", "fisher-paykel": "Fisher & Paykel"
    }
    name = b.replace("-", " ").title()
    for k, v in fixes.items():
        if k in b.lower():
            name = name.replace(k.replace("-", " ").title(), v)
    return name

# Different intro patterns for variety
def washer_intro(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Residents of {c['name']} depend on reliable {b} washing machines to handle laundry for busy households. As a {c['type']} known for {c['known']}, {c['name']} families expect appliance repair service that matches their community's standards.",
        f"In {c['name']}, where {c['homes']} define the residential landscape, {b} washers work overtime keeping families' clothes fresh and clean. Our technicians understand the specific installation configurations found throughout {c['areas']}.",
        f"With a population of {c['pop']}, {c['name']} represents the {c['character']} that makes Westchester special. When {b} washers fail in these homes, families need prompt professional service.",
    ]
    return random.choice(patterns)

def washer_problems(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Our {c['name']} technicians resolve {b} washer failures including: drums refusing to spin leaving clothes waterlogged, drainage blockages causing water retention, excessive vibration shaking laundry rooms, water inlet problems from trickles to floods, door mechanisms preventing cycle starts, error codes halting mid-wash, grinding or banging noises during operation, leaks from seals or hoses, residue on clean clothes, and complete power failures.",
        f"Common {b} washer issues we repair throughout {c['areas']}: spin cycle failures, drainage problems, units walking across floors from imbalance, fill valve malfunctions, latch failures on front-loaders, electronic control errors, bearing noise during operation, pump leaks onto floors, incomplete cleaning cycles, and electrical faults preventing startup.",
        f"{b} washers in {c['name']} {c['type']} may experience these problems: clothes remaining wet after spin, standing water after drain cycle, violent shaking during high-speed spin, slow or no water fill, safety interlocks preventing operation, computer board glitches, mechanical grinding sounds, water escaping from multiple points, soil remaining on fabrics, and dead units with no response to controls.",
    ]
    return random.choice(patterns)

def washer_parts(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"For {c['name']} {b} washer repairs, our vehicles stock: drum bearing assemblies, door gaskets and boot seals, drain pump motors, motor coupling components, water inlet valves, transmission gears and clutches, shock absorbers and springs, main control boards, lid switches and door latches, drive belts, and water level sensors.",
        f"Our {c['name']} technicians carry {b} washer parts: tub bearings, rubber door boots, drain pump assemblies, coupler sets, fill valves, gearbox components, suspension rods, electronic boards, safety switches, serpentine belts, and pressure switches.",
        f"Stocked on our {c['name']} service trucks for {b} washers: bearing kits, seal gaskets, pump motors, flex couplings, inlet solenoids, transmission parts, damper struts, PCB modules, interlock switches, belt assemblies, and level sensors.",
    ]
    return random.choice(patterns)

def washer_trust(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Families across {c['name']} trust us because we arrive prepared with {b}-specific diagnostic equipment, carry genuine manufacturer parts, provide upfront pricing, and complete most repairs same-day. Our knowledge of {c['homes']} means we understand your installation.",
        f"Throughout {c['areas']}, {c['name']} residents choose our service for factory-trained expertise, authentic {b} components, transparent estimates, and rapid turnaround. We've serviced {b} appliances in every {c['name']} neighborhood.",
        f"In this {c['type']} of {c['pop']} residents, word spreads about quality service. Our {b} washer repair reputation in {c['name']} comes from technical expertise, quality parts, honest pricing, and commitment to same-day solutions.",
    ]
    return random.choice(patterns)

def washer_tips(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Protect your {b} washer investment: use HE detergent measured precisely, leave door ajar between loads, run monthly cleaning cycles, check inlet hoses yearly, ensure level installation, avoid overloading, and address unusual sounds promptly. {c['name']} water quality may require additional descaling attention.",
        f"Keep your {b} washer running efficiently: measure detergent for HE machines, air out the drum after washing, clean with vinegar monthly, inspect hoses for wear, level the unit, don't overload, and fix problems early. {c['name']}'s water hardness may necessitate periodic cleaning.",
        f"Extend {b} washer life with these tips: use proper HE detergent amounts, prop door open between uses, run empty hot cycles monthly, replace hoses before they fail, maintain level positioning, respect load limits, and service at first sign of trouble. Consider {c['name']} water conditions when cleaning.",
    ]
    return random.choice(patterns)


def generate_washer_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Washer Service for {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">{washer_intro(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Washer Issues We Fix in {c["name"]}</h4>
<p style="margin-bottom: 12px;">{washer_problems(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Washer Parts We Carry</h4>
<p style="margin-bottom: 12px;">{washer_parts(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Trusted by {c["name"]} Families</h4>
<p style="margin-bottom: 12px;">{washer_trust(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Maintenance Advice for {c["name"]} Homeowners</h4>
<p style="margin-bottom: 12px;">{washer_tips(brand, city)}</p>
'''


def dryer_intro(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"When your {b} dryer stops heating properly in {c['name']}, wet laundry accumulates quickly. In this {c['type']} of {c['character']}, household routines depend on functioning appliances.",
        f"{c['name']} homeowners with {c['homes']} rely on {b} dryers for efficient laundry completion. Our technicians service both gas and electric models throughout {c['areas']}.",
        f"A failing {b} dryer disrupts daily life for {c['name']}'s {c['pop']} residents. Whether you're in {c['areas']}, our same-day service restores your laundry capability.",
    ]
    return random.choice(patterns)

def dryer_problems(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"We repair these {b} dryer problems for {c['name']} customers: no heat despite drum rotation, insufficient warmth requiring multiple cycles, overheating triggering shutoffs, stationary drums, squeaking or grinding mechanics, burning odors indicating hazards, mid-cycle shutdowns, extended drying times wasting energy, gas ignition failures, and control panel errors.",
        f"{b} dryer issues common in {c['name']} {c['homes']}: heating element burnout, thermal fuse failures, worn drum rollers, broken drive belts, gas valve problems, weak airflow, motor bearing wear, lint-clogged components, moisture sensor errors, and electrical control malfunctions.",
        f"Our {c['name']} technicians diagnose {b} dryer faults: clothes staying damp, units running but not heating, fabric damage from excess heat, drum failing to turn, noisy operation getting worse, smell of burning during use, cycles ending prematurely, gas models not igniting, exhaust restrictions, and computer errors.",
    ]
    return random.choice(patterns)

def dryer_parts(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Our {c['name']} service vehicles carry {b} dryer parts: heating elements, thermal fuses, drum rollers and axles, drive belts, gas igniters and glow bars, valve solenoids, blower motors and wheels, thermistors, door switches, drum seals, idler pulleys, and control boards.",
        f"For {c['name']} {b} dryer repairs we stock: coil heaters, safety cutoffs, support rollers, serpentine belts, igniter assemblies, gas coils, exhaust fans, temperature sensors, latch mechanisms, felt gaskets, tensioner parts, and main boards.",
        f"Stocked on {c['name']} trucks for {b} dryers: element assemblies, thermal limiters, roller kits, belt replacements, glow bar igniters, solenoid valves, blower assemblies, NTC sensors, switch mechanisms, drum felts, pulley tensioners, and PCBs.",
    ]
    return random.choice(patterns)

def dryer_safety(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Dryer ventilation in {c['name']} homes requires attention. The {c['homes']} may have long vent runs through walls. Lint accumulation creates fire hazards and reduces efficiency. We inspect exhaust systems during every {b} dryer call, checking for blockages and improper materials.",
        f"In {c['name']}'s {c['homes']}, dryer vents often run through multiple floors. Clogged ducts cause fires and waste energy. Our {b} technicians check exhaust paths for lint buildup, crushed sections, and blocked terminations during service calls.",
        f"Proper venting matters in {c['name']} {c['type']}. The {c['homes']} may have complex exhaust routing. Lint-filled ducts create fire risks and force dryers to work harder. Every {b} service includes vent inspection with recommendations when needed.",
    ]
    return random.choice(patterns)

def dryer_gas_electric(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Our {c['name']} technicians handle both gas and electric {b} dryers. Gas repairs require ignition system expertise, valve testing, and combustion verification. Electric models get thorough element, thermostat, and high-voltage testing. Every repair includes complete safety verification.",
        f"We service gas and electric {b} dryers throughout {c['name']}. Gas units need igniter, burner, and valve expertise. Electric dryers require element, fuse, and circuit testing. All repairs conclude with operational and safety confirmation.",
        f"Both gas and electric {b} models are serviced by our {c['name']} team. For gas: ignition timing, flame sensing, and gas pressure checks. For electric: heating coil, thermal cutoff, and wiring inspection. We verify safe operation before completing any job.",
    ]
    return random.choice(patterns)


def generate_dryer_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dryer Repair Throughout {c["name"]}</h4>
<p style="margin-bottom: 12px;">{dryer_intro(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Dryer Failures</h4>
<p style="margin-bottom: 12px;">{dryer_problems(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dryer Parts in Stock</h4>
<p style="margin-bottom: 12px;">{dryer_parts(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Ventilation Safety in {c["name"]}</h4>
<p style="margin-bottom: 12px;">{dryer_safety(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Gas and Electric Expertise</h4>
<p style="margin-bottom: 12px;">{dryer_gas_electric(brand, city)}</p>
'''


def fridge_intro(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Your {b} refrigerator protects hundreds of dollars in groceries for your {c['name']} household. When cooling fails in one of the {c['homes']}, food safety becomes urgent.",
        f"For {c['name']}'s {c['pop']} residents, a {b} refrigerator breakdown means potential food loss and health concerns. Our emergency service reaches all {c['areas']} quickly.",
        f"In {c['name']}, {c['known']}, families trust {b} refrigerators to preserve their food. When problems arise, our same-day response protects your investment.",
    ]
    return random.choice(patterns)

def fridge_problems(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"We resolve {b} refrigerator emergencies across {c['name']}: units running but not cooling, freezers failing to maintain temperature, ice makers stopping production, water dispensers with weak flow, compressor cycling abnormally, frost accumulating excessively, water pooling inside or underneath, temperature swings affecting food, refrigerator sections freezing items, and fans making grinding noises.",
        f"{b} refrigerator problems in {c['name']} homes: cooling system failures, freezer thawing episodes, ice production halts, dispenser malfunctions, noisy compressor operation, defrost system breakdowns, mysterious leaks, inconsistent temperatures, unwanted freezing, and evaporator fan failures.",
        f"Our {c['name']} technicians handle {b} fridge issues: warm temperatures despite operation, frozen food softening, no ice output, water flow problems, unusual compressor sounds, excessive ice buildup, standing water, temperature fluctuations, frost on fresh food, and cooling fan problems.",
    ]
    return random.choice(patterns)

def fridge_parts(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"For {c['name']} {b} refrigerator repairs, we carry: compressors and starting components, evaporator and condenser fans, defrost heaters and thermostats, temperature controls, start relays, door gaskets, ice maker modules, water filters, control boards, damper assemblies, and thermistors.",
        f"Our {c['name']} trucks stock {b} fridge parts: sealed system components, circulation fans, heating elements for defrost, cold controls, PTC relays, door seals, ice production units, filtration housings, main PCBs, airflow dampers, and temperature probes.",
        f"For {b} refrigerator service in {c['name']}: compressor assemblies, fan motors, defrost components, thermostatic controls, starter devices, rubber gaskets, ice maker kits, filter cartridges, electronic boards, air dampers, and sensor arrays.",
    ]
    return random.choice(patterns)

def fridge_emergency(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Refrigerator failures in {c['name']} demand immediate attention—every hour risks food spoilage. For {c['homes']} throughout {c['areas']}, we offer priority scheduling. Our technicians arrive with common {b} parts for rapid repair. We service all configurations from built-ins to counter-depth French doors.",
        f"When {b} refrigerators fail in {c['name']}, food safety is at stake. We prioritize emergency calls for {c['homes']} in {c['areas']}, bringing commonly needed parts for same-visit repairs. All styles serviced: built-in, freestanding, side-by-side, and French door models.",
        f"Time matters when {c['name']} {b} refrigerators stop cooling. The {c['homes']} throughout {c['areas']} can request priority service. Our techs stock essential {b} components for quick restoration. We handle every configuration from custom built-ins to standard top-freezers.",
    ]
    return random.choice(patterns)

def fridge_tips(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    patterns = [
        f"Keep your {b} refrigerator running efficiently in {c['name']}: maintain proper clearance behind unit, clean condenser coils every six months, check door seals for air leaks, set correct temperatures (37°F fridge, 0°F freezer), avoid overpacking blocking vents. {c['name']}'s seasonal temperature swings make regular maintenance especially important.",
        f"Extend your {b} refrigerator life in {c['name']}: ensure adequate ventilation around the unit, vacuum condenser coils twice yearly, inspect gaskets for gaps, verify temperature settings (refrigerator 35-38°F, freezer 0°F), keep air circulation paths clear. The {c['type']}'s climate variations affect cooling demands.",
        f"Maintain your {c['name']} {b} fridge: allow space for heat dissipation, brush coils semi-annually, test door seals with paper test, dial in proper cold (37°F) and freezer (0°F) temps, don't block internal vents. {c['name']} seasonal changes require attention to cooling efficiency.",
    ]
    return random.choice(patterns)


def generate_fridge_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Refrigerator Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">{fridge_intro(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Refrigerator Problems We Solve</h4>
<p style="margin-bottom: 12px;">{fridge_problems(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Refrigerator Parts Available</h4>
<p style="margin-bottom: 12px;">{fridge_parts(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Emergency Service for {c["name"]}</h4>
<p style="margin-bottom: 12px;">{fridge_emergency(brand, city)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Refrigerator Care Tips</h4>
<p style="margin-bottom: 12px;">{fridge_tips(brand, city)}</p>
'''


# Similar generators for other appliances (dishwasher, oven, cooktop, microwave, wine, hood)
# Each uses randomized intro patterns and city-specific details

def generate_dishwasher_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    intros = [
        f"In {c['name']}, where {c['character']}, households rely on {b} dishwashers for daily convenience. When units fail to clean properly or leak water, kitchens become chaotic.",
        f"{c['name']} families with {c['homes']} expect their {b} dishwashers to perform flawlessly. Our technicians service all models throughout {c['areas']}.",
        f"For {c['pop']} residents in {c['name']}, {c['known']}, a broken {b} dishwasher means stacks of dirty dishes. We provide same-day solutions.",
    ]
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dishwasher Service in {c["name"]}</h4>
<p style="margin-bottom: 12px;">{random.choice(intros)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dishwasher Issues We Address</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} team fixes: dishes remaining dirty, drainage failures, spray arms not rotating, pump motor problems, door latch issues, water inlet failures, heating element faults, detergent dispenser jams, rack roller problems, and electronic control errors affecting {b} models.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dishwasher Components We Replace</h4>
<p style="margin-bottom: 12px;">For {c["name"]} service calls, we stock {b} parts: wash motors, drain pumps, spray arms, door latches, water inlet valves, heating elements, rack adjusters, float switches, circulation pumps, and main control boards.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Why {c["name"]} Residents Choose Us</h4>
<p style="margin-bottom: 12px;">Homeowners across {c["areas"]} select our service for {b} expertise, genuine parts, upfront estimates, and same-day availability. We understand the configurations found in {c["homes"]} throughout this {c["type"]}.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Dishwasher Maintenance Guidance</h4>
<p style="margin-bottom: 12px;">Extend your {b} dishwasher life: scrape dishes before loading, clean the filter monthly, use rinse aid for spot-free results, run hot water before starting cycles, and avoid overloading. {c["name"]} water hardness may require periodic descaling.</p>
'''


def generate_oven_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    intros = [
        f"Home cooks in {c['name']} depend on {b} ovens for family meals and entertaining. When heating problems occur in {c['homes']}, cooking becomes impossible.",
        f"Throughout {c['areas']}, {c['name']} kitchens feature {b} ovens producing everything from weeknight dinners to holiday feasts. Our technicians keep them working.",
        f"For {c['name']}'s {c['pop']} residents, a functioning {b} oven is essential to daily life. We provide prompt repair service across this {c['type']}.",
    ]
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Oven Repair for {c["name"]} Cooks</h4>
<p style="margin-bottom: 12px;">{random.choice(intros)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Oven Problems We Resolve</h4>
<p style="margin-bottom: 12px;">Common {b} oven issues in {c["name"]}: no heat, uneven baking, temperature inaccuracy, self-clean cycle failures, broiler malfunctions, door not sealing properly, control panel errors, gas ignition problems, convection fan failures, and interior light burnout.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Oven Parts We Supply</h4>
<p style="margin-bottom: 12px;">Our vehicles carry {b} oven components for {c["name"]} repairs: bake and broil elements, igniters, thermostats, temperature sensors, door hinges and gaskets, control boards, convection motors, timers, and safety valves.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Professional Service in {c["name"]}</h4>
<p style="margin-bottom: 12px;">We serve all {c["name"]} neighborhoods with factory-trained {b} oven expertise. From gas range repair to electric wall oven service, our technicians arrive prepared with diagnostic tools and genuine parts.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Oven Safety in {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">Gas oven repairs require licensed professionals. We test ignition timing, gas valve operation, and proper combustion. Electric ovens receive element testing and high-temperature safety verification. Never ignore {b} oven problems—schedule service promptly.</p>
'''


def generate_cooktop_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    intros = [
        f"From quick breakfasts to elaborate dinners, {c['name']} families rely on {b} cooktops daily. When burners fail in {c['homes']}, meal preparation stops.",
        f"In {c['name']}, {c['known']}, home chefs expect {b} cooktops to perform. Our technicians service gas, electric, and induction models across {c['areas']}.",
        f"The {c['homes']} throughout {c['name']} feature diverse {b} cooktop configurations. Our expertise covers every installation type.",
    ]
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Cooktop Service in {c["name"]}</h4>
<p style="margin-bottom: 12px;">{random.choice(intros)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Cooktop Issues We Fix</h4>
<p style="margin-bottom: 12px;">We repair {b} cooktop problems for {c["name"]} homeowners: gas burners not igniting, weak or uneven flames, electric elements not heating, induction zones showing errors, cracked glass surfaces, control knobs not adjusting properly, touch panels unresponsive, spark electrodes misfiring, gas odors, and downdraft ventilation failures.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Cooktop Parts Available</h4>
<p style="margin-bottom: 12px;">For {c["name"]} service, we stock: spark igniters, burner caps and bases, radiant elements, induction coils, glass surfaces, control knobs, touch panels, gas valves, wiring harnesses, and power boards for {b} cooktops.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Cooktop Safety First</h4>
<p style="margin-bottom: 12px;">Gas cooktop repairs require professional expertise—never attempt DIY gas work. We verify ignition, flame patterns, and connections. Electric and induction models receive thorough electrical testing. {c["name"]} homeowners can trust our safety protocols.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">All Cooktop Types Serviced</h4>
<p style="margin-bottom: 12px;">We repair every {b} cooktop configuration in {c["name"]}: built-in units in counter cutouts, rangetops on cabinet bases, island installations with downdraft, and professional-style high-BTU models. Our experience covers all {c["homes"]} styles.</p>
'''


def generate_microwave_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    intros = [
        f"Quick meals, reheating, and defrosting—{c['name']} households depend on {b} microwaves daily. When units stop heating or sparking occurs, convenience disappears.",
        f"For busy families in {c['name']}'s {c['homes']}, a functioning {b} microwave saves time every day. Our technicians restore operation quickly.",
        f"Across {c['areas']} in {c['name']}, {b} microwaves handle countless cooking tasks. We service countertop, over-range, and built-in models.",
    ]
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Microwave Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">{random.choice(intros)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Microwave Problems We Solve</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians fix: microwaves running but not heating, turntables not rotating, sparking inside cavity, door latch failures, display panel issues, button malfunctions, interior light problems, unusual humming noises, exhaust fan failures in OTR models, and error codes.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Microwave Parts We Stock</h4>
<p style="margin-bottom: 12px;">For {c["name"]} service calls: magnetrons, high-voltage diodes, capacitors, door switches, turntable motors, waveguide covers, control panels, exhaust fans, light bulbs, and thermal fuses for {b} models.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Microwave Safety Concerns</h4>
<p style="margin-bottom: 12px;">Microwave repairs involve high-voltage components requiring professional handling. Never operate a sparking microwave—disconnect immediately. Our technicians safely diagnose and repair {b} units throughout {c["name"]}.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">All Installation Types</h4>
<p style="margin-bottom: 12px;">We service every {b} microwave configuration in {c["name"]} {c["homes"]}: countertop models, over-the-range units with ventilation, built-in drawer styles, and combination convection microwaves.</p>
'''


def generate_wine_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    intros = [
        f"Wine collectors in {c['name']} invest significantly in their collections. {b} wine coolers protect these investments with precise temperature control. When cooling fails, wines are at risk.",
        f"Throughout {c['areas']}, {c['name']} homes feature {b} wine storage units preserving valuable collections. Our technicians understand the specific requirements.",
        f"In {c['name']}, {c['known']}, wine enthusiasts depend on {b} coolers. Temperature fluctuations and vibration can damage wines—prompt repair is essential.",
    ]
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Wine Cooler Service in {c["name"]}</h4>
<p style="margin-bottom: 12px;">{random.choice(intros)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Wine Cooler Issues We Address</h4>
<p style="margin-bottom: 12px;">We repair {b} wine cooler problems for {c["name"]} collectors: units not cooling properly, temperature fluctuations, compressor cycling issues, excessive vibration disturbing sediment, interior lighting failures, door seal problems, humidity concerns, digital display errors, and dual-zone temperature discrepancies.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Wine Cooler Parts Available</h4>
<p style="margin-bottom: 12px;">For {c["name"]} repairs: compressors, thermostats, fans, door gaskets, vibration dampeners, humidity controls, LED lighting, temperature sensors, control boards, and shelving components for {b} wine coolers.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Wine Storage Expertise</h4>
<p style="margin-bottom: 12px;">Proper wine storage requires precise conditions: stable temperatures (45-65°F depending on variety), appropriate humidity, minimal vibration, and UV protection. Our {b} technicians understand these requirements and repair accordingly.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Protecting Your Collection</h4>
<p style="margin-bottom: 12px;">{c["name"]} wine collectors can minimize repair time by calling promptly when issues arise. We arrive with {b} parts and complete most repairs in one visit, reducing temperature fluctuation risks to your valuable bottles.</p>
'''


def generate_hood_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    intros = [
        f"Kitchen ventilation in {c['name']} {c['homes']} relies on {b} range hoods. When fans fail or motors weaken, cooking smoke and grease accumulate throughout kitchens.",
        f"From sautéing to frying, {c['name']} home cooks generate smoke and steam. {b} vent hoods remove these from kitchens—until they break down.",
        f"Proper ventilation protects {c['name']} homes from grease buildup, excess moisture, and lingering odors. Our technicians keep {b} hoods working effectively.",
    ]
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Vent Hood Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">{random.choice(intros)}</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Vent Hood Problems We Fix</h4>
<p style="margin-bottom: 12px;">Common {b} hood issues in {c["name"]}: fans not running, weak airflow, excessive noise, lights not working, control switches failing, grease buildup affecting performance, motors burning out, vibration during operation, dampers stuck open or closed, and automatic features malfunctioning.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Vent Hood Parts We Carry</h4>
<p style="margin-bottom: 12px;">For {c["name"]} service: blower motors, fan blades, motor bearings, light sockets, control switches, grease filters, charcoal filters, duct dampers, wiring, capacitors, and touch controls for {b} hoods.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Ventilation Inspection</h4>
<p style="margin-bottom: 12px;">During every {b} hood service in {c["name"]}, we inspect ductwork for restrictions, measure actual CFM output, and check exterior terminations. Proper ventilation protects your kitchen from grease damage and moisture problems.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Hood Configurations Serviced</h4>
<p style="margin-bottom: 12px;">We repair all {b} vent hood styles found in {c["name"]} {c["homes"]}: wall-mounted chimney hoods, island hoods, under-cabinet units, downdraft systems, insert hoods in custom enclosures, and professional models with remote blowers.</p>
'''


GENERATORS = {
    "washer": generate_washer_content,
    "dryer": generate_dryer_content,
    "fridge": generate_fridge_content,
    "dishwasher": generate_dishwasher_content,
    "oven": generate_oven_content,
    "cooktop": generate_cooktop_content,
    "microwave": generate_microwave_content,
    "wine": generate_wine_content,
    "hood": generate_hood_content
}


def update_card(html, card_id, new_content):
    pattern = rf'(<div id="expandable-text-{card_id}"[^>]*>)(.*?)(</div>\s*<div id="expandable-fade-{card_id}")'
    def replacer(match):
        return match.group(1) + new_content + match.group(3)
    return re.sub(pattern, replacer, html, flags=re.DOTALL)


def process_page(file_path, city_slug, brand_slug):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # Seed random with city+brand for consistent output per page
    random.seed(f"{city_slug}{brand_slug}")

    for card_id, generator in GENERATORS.items():
        content = generator(brand_slug, city_slug)
        html = update_card(html, card_id, content)

    if html != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    base_path = "/Users/globalaffiliate/westchester-county-repair"
    csv_path = "/Users/globalaffiliate/Downloads/westchester-coverage-report/Table.csv"

    brands_list = ['samsung', 'lg', 'whirlpool', 'ge', 'frigidaire', 'bosch', 'kitchenaid', 'maytag', 'kenmore',
             'electrolux', 'thermador', 'viking', 'miele', 'sub-zero', 'wolf', 'jenn-air', 'dacor',
             'amana', 'fisher-paykel', 'gaggenau']

    affected = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                affected.append(row[0])

    print("=" * 60)
    print("GENERATING UNIQUE CONTENT WITH VARIED STRUCTURES")
    print("=" * 60)

    updated = 0
    for url in sorted(affected):
        parsed = urlparse(url)
        parts = parsed.path.strip('/').split('/')

        if len(parts) >= 3 and parts[0] == 'ny' and parts[2].endswith('-repair'):
            brand = parts[2].replace('-repair', '')
            if brand in brands_list:
                city = parts[1]
                file_path = os.path.join(base_path, *parts, 'index.html')

                if os.path.exists(file_path):
                    if process_page(file_path, city, brand):
                        updated += 1
                        print(f"Updated: /ny/{city}/{brand}-repair/")

    print("\n" + "=" * 60)
    print(f"TOTAL: {updated} city+brand pages with unique varied content")
    print("=" * 60)


if __name__ == "__main__":
    main()
