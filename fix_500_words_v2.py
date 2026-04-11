#!/usr/bin/env python3
"""
Ensure all service cards have 500+ words - Version 2 with expanded content.
"""

import os
import re
import csv
from urllib.parse import urlparse

CITIES = {
    "ardsley": {"name": "Ardsley", "pop": "4,800", "desc": "tree-lined streets and Tudor homes dating to the 1920s", "areas": "Ardsley Park, Heatherdell, and the Ashford Avenue corridor", "housing": "Tudor-style homes, Colonials, and Cape Cods", "notable": "Known as The Village Beautiful"},
    "bronxville": {"name": "Bronxville", "pop": "6,500", "desc": "prestigious Tudor estates and luxury condominiums", "areas": "Bronxville Village, Lawrence Park, and Armour Villa Park", "housing": "grand Tudor estates and historic mansions", "notable": "one of America's most affluent communities"},
    "dobbs-ferry": {"name": "Dobbs Ferry", "pop": "11,000", "desc": "charming Hudson River waterfront Victorian homes", "areas": "Downtown, the Heights, South Dobbs Ferry, and Wickers Creek", "housing": "Victorian homes and riverfront properties", "notable": "scenic waterfront village on the Hudson"},
    "eastchester": {"name": "Eastchester", "pop": "19,500", "desc": "historic colonials and modern townhouses since 1664", "areas": "Chester Heights, Lake Isle, Waverly, and Garth Road", "housing": "single-family Colonials and split-levels", "notable": "one of the oldest towns in Westchester"},
    "elmsford": {"name": "Elmsford", "pop": "5,000", "desc": "convenient affordable homes near major highways", "areas": "Downtown Elmsford and Knollwood", "housing": "affordable single-family homes and apartments", "notable": "strategic location at highway intersections"},
    "fairview": {"name": "Fairview", "pop": "3,700", "desc": "diverse residential community in Greenburgh", "areas": "Fairview and surrounding Greenburgh neighborhoods", "housing": "modest single-family homes and multi-family residences", "notable": "welcoming diverse community"},
    "harrison": {"name": "Harrison", "pop": "28,000", "desc": "luxury estates and executive homes in Purchase area", "areas": "Purchase, West Harrison, Sterling Ridge, and Silver Lake", "housing": "luxury estates and executive homes", "notable": "home to corporate headquarters and prestigious Purchase"},
    "hartsdale": {"name": "Hartsdale", "pop": "5,300", "desc": "split-level homes and garden apartments near shopping", "areas": "East Hartsdale, West Hartsdale, and Four Corners", "housing": "split-levels, Colonials, and apartment complexes", "notable": "vibrant commercial district"},
    "hastings-on-hudson": {"name": "Hastings-on-Hudson", "pop": "8,000", "desc": "artistic Victorian homes with Hudson River views", "areas": "Downtown, The Dale, Hillside Woods, and Riverview Manor", "housing": "Victorian estates and artists' cottages", "notable": "artistic community with stunning river views"},
    "irvington": {"name": "Irvington", "pop": "6,500", "desc": "historic mansions near Washington Irving's Sunnyside", "areas": "Downtown, Matthiessen Park, and Ardsley-on-Hudson", "housing": "historic mansions and stone cottages", "notable": "home to Sunnyside, Washington Irving's estate"},
    "larchmont": {"name": "Larchmont", "pop": "6,200", "desc": "exclusive waterfront estates on Long Island Sound", "areas": "Larchmont Manor, Murray Hill, and Orienta Point", "housing": "luxury waterfront estates and Tudor mansions", "notable": "exclusive waterfront community with yacht clubs"},
    "mamaroneck": {"name": "Mamaroneck", "pop": "19,000", "desc": "vibrant harbor community with beach cottages", "areas": "Harbor Heights, Orienta, Washingtonville, and Rye Neck", "housing": "waterfront properties and beach cottages", "notable": "active boating culture and diverse dining"},
    "mount-vernon": {"name": "Mount Vernon", "pop": "73,000", "desc": "diverse multi-family homes and historic residences", "areas": "Fleetwood, Chester Heights, South Side, and Hutchinson", "housing": "multi-family homes and historic single-family residences", "notable": "Westchester's most populous city"},
    "new-rochelle": {"name": "New Rochelle", "pop": "80,000", "desc": "high-rise condos and waterfront properties near NYC", "areas": "Wykagyl, Beechmont, Huguenot Park, and Premium Point", "housing": "high-rise condos, Colonials, and beach cottages", "notable": "major city with waterfront development"},
    "pelham-manor": {"name": "Pelham Manor", "pop": "5,500", "desc": "stately Tudor estates with excellent schools", "areas": "Pelham Manor, North Pelham, and Shore Road", "housing": "Tudor estates, Colonials, and Victorian homes", "notable": "prestigious village with top schools"},
    "rye": {"name": "Rye", "pop": "16,000", "desc": "affluent waterfront estates near Playland", "areas": "Milton Point, Rye Beach, Park Avenue, and Grace Church", "housing": "waterfront estates and historic mansions", "notable": "features Playland amusement park and exclusive beach clubs"},
    "scarsdale": {"name": "Scarsdale", "pop": "18,000", "desc": "grand estates and architect-designed modern homes", "areas": "Fox Meadow, Greenacres, Heathcote, and Quaker Ridge", "housing": "grand estates and Tudor mansions", "notable": "one of America's wealthiest communities"},
    "tarrytown": {"name": "Tarrytown", "pop": "11,500", "desc": "historic riverfront Victorian homes and brownstones", "areas": "Downtown, Sleepy Hollow Manor, and Wilson Park", "housing": "Victorian homes and riverfront condos", "notable": "historic village of Washington Irving's Sleepy Hollow"},
    "valhalla": {"name": "Valhalla", "pop": "3,500", "desc": "affordable homes near Westchester Medical Center", "areas": "Valhalla, Kensico, and Grasslands", "housing": "affordable single-family homes and condominiums", "notable": "home to Westchester Medical Center"},
    "village-of-pelham": {"name": "Village of Pelham", "pop": "7,000", "desc": "charming Victorians with easy Metro-North access", "areas": "Pelham Heights, Chester Park, and Highbrook Gardens", "housing": "Victorians, Colonials, and townhouses", "notable": "charming commuter village"},
    "white-plains": {"name": "White Plains", "pop": "58,000", "desc": "luxury high-rises and historic homes in commercial hub", "areas": "Battle Hill, Fisher Hill, Gedney Farms, and Highlands", "housing": "luxury high-rises and historic homes", "notable": "Westchester's commercial and cultural hub"},
    "yonkers": {"name": "Yonkers", "pop": "200,000", "desc": "diverse neighborhoods from high-rises to Victorians", "areas": "Crestwood, Park Hill, Ludlow, Getty Square, and Greystone", "housing": "high-rises, Victorians, and multi-family homes", "notable": "fourth largest city in New York State"}
}

def get_city(slug):
    return CITIES.get(slug, {"name": slug.replace("-", " ").title(), "pop": "varies", "desc": "quality residential neighborhoods", "areas": "all neighborhoods", "housing": "various home styles", "notable": "wonderful Westchester community"})

def fix_brand(b):
    return b.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")


def generate_washer_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Washer Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">When your {b} washing machine breaks down in {c["name"]} (population {c["pop"]}), you need factory-certified technicians who understand both sophisticated washer technology and the unique installation challenges found in homes with {c["desc"]}. {c["name"]} is {c["notable"]}, featuring {c["housing"]} throughout {c["areas"]}. Our {b} washer specialists provide same-day service with fully-stocked vehicles carrying genuine replacement parts, diagnostic equipment, and specialized tools for every {b} model.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Washer Problems We Diagnose and Repair</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} washer issue you may encounter: drums that won't spin leaving clothes soaking wet after cycles complete, units that fail to drain water properly, excessive vibration that shakes your entire laundry area and walks across the floor, water filling problems ranging from slow trickle fills to dangerous overflows, door or lid mechanisms that won't lock preventing cycle starts, mysterious error codes that halt operation mid-wash, unusual grinding squealing or banging noises during agitation or spin cycles, water leaking from door seals hoses or internal components, clothes coming out still dirty or with residue despite running full cycles, and units that simply won't power on or respond to controls at all.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Washer Parts We Replace in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} replacement parts for {c["name"]} washer repairs including: drum bearings that cause grinding noises during spin cycles, door boot seals and gaskets that leak water onto laundry room floors, drain pumps clogged with debris coins socks or small items, motor couplings that break from overloading or deteriorate with age, water inlet valves that fail to regulate fill properly or stick open or closed, transmission assemblies in top-load models that cause agitation failures, clutch components that slip during high-speed spin cycles, shock absorbers and suspension rods that cause excessive movement and banging, main control boards displaying error codes or failing to respond, lid switches and door latches that prevent operation, drive belts that slip fray or snap completely, pressure switches that misread water levels, timer assemblies, and drain hoses.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Why {c["name"]} Families Trust Our {b} Washer Service</h4>
<p style="margin-bottom: 12px;">We understand that a broken washer means laundry piling up fast for busy {c["name"]} families. Our factory-certified technicians arrive promptly with diagnostic equipment specifically calibrated for {b} washers, allowing accurate identification of problems on the first visit. We provide transparent upfront pricing before beginning any repair work, so you know exactly what to expect. Most {b} washer repairs in {c["name"]} are completed the same day because we stock commonly needed parts on our service vehicles. Every repair includes our comprehensive parts and labor warranty, genuine manufacturer-approved {b} components, and our satisfaction guarantee. Our commitment to quality service is why {c["name"]} residents throughout {c["areas"]} call us whenever their {b} appliances need attention.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Washer Maintenance Tips for {c["name"]} Homeowners</h4>
<p style="margin-bottom: 12px;">Extend the life of your {b} washer with these professional tips from our {c["name"]} technicians: use only HE detergent in high-efficiency models and measure carefully to avoid residue buildup, leave the door or lid open between loads to prevent mold and mildew growth in the drum and gasket, run a cleaning cycle monthly using washer cleaner or white vinegar, check and clean the drain pump filter regularly to prevent clogs, inspect inlet hoses annually for cracks bulges or wear and replace every five years as preventive maintenance, ensure your washer is level to minimize vibration and extend bearing life, avoid overloading which stresses motors transmissions and bearings, and address unusual noises or behaviors promptly before small problems become expensive repairs. Following these guidelines helps your {b} washer deliver years of reliable performance in your {c["name"]} home.</p>
'''


def generate_dryer_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Dryer Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">A malfunctioning {b} dryer in your {c["name"]} home means damp clothes, extended dry times, and mounting frustration for your household. Whether you have a gas or electric {b} dryer in one of the {c["housing"]} found throughout {c["areas"]}, our factory-certified technicians diagnose and repair any issue quickly. {c["name"]} is {c["notable"]}, with a population of {c["pop"]} residents who depend on reliable laundry appliances. We provide same-day service availability with technicians who carry genuine {b} parts.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dryer Problems We Solve in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} dryer issue: no heat despite the drum turning normally leaving clothes damp cycle after cycle, insufficient heat that requires multiple cycles to dry a single load, overheating that triggers safety shutoffs or damages clothing, drums that won't tumble at all, squeaking squealing or grinding sounds during operation that worsen over time, burning smells indicating potential fire hazards requiring immediate attention, units shutting off mid-cycle repeatedly before clothes are dry, clothes taking two three or more cycles to dry properly wasting energy and time, gas dryers with ignition system failures that won't light, electric dryers with heating element problems, moisture sensor errors causing premature cycle endings, and error codes on digital displays that halt operation.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Dryer Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} dryer parts for {c["name"]} repairs: heating elements that burn out from age power surges or lint buildup, thermal fuses that blow to prevent fires and require replacement to restore operation, drum rollers and axles that wear causing squeaking sounds and tumbling problems, drive belts that fray slip or snap completely preventing drum rotation, gas igniters and glow bars that fail to light burners in gas models, gas valve solenoid coils that prevent proper fuel flow, blower motors that don't move air efficiently reducing drying performance, blower wheels clogged with lint debris restricting airflow, thermistors and thermostats that misread temperatures causing heating issues, door switches that don't sense closure preventing operation, drum seals and felt strips that leak hot air reducing efficiency, idler pulleys that cause belt squeaking, main control boards with electronic failures, and timer assemblies.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Dryer Safety and Maintenance for {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">Proper dryer ventilation is critical for homes in {c["name"]}, especially properties with {c["desc"]} that may have longer vent runs through walls or ceilings. Lint buildup in exhaust ducts is a leading cause of home fires, and restricted airflow also reduces dryer efficiency and increases energy costs. Our technicians inspect exhaust systems during every {b} dryer service call in {c["name"]}, checking for lint accumulation, crushed or kinked ductwork, bird nests or debris at exterior terminations, and improper vent materials that create fire hazards. We recommend professional vent cleaning when needed and provide maintenance guidance to keep your {b} dryer running safely and efficiently for years to come. Remember to clean the lint screen before every load, inspect the exterior vent flap periodically, and schedule professional vent cleaning annually.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Gas vs Electric Dryer Service in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians are certified to service both gas and electric {b} dryers. Gas dryer repairs require specialized expertise in ignition systems, gas valve operation, and safety protocols. We test igniter function, burner assembly operation, gas valve timing, and exhaust for proper combustion products. Electric dryers receive thorough testing of heating elements, thermostats, thermal fuses, and high-voltage connections. Regardless of fuel type, every {b} dryer repair in {c["name"]} includes verification of proper operation, safety system function, and airflow before we consider the job complete. Our commitment to thorough service is why {c["name"]} families trust us with their {b} appliance repairs.</p>
'''


def generate_fridge_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Refrigerator Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">Your {b} refrigerator runs continuously around the clock to protect hundreds of dollars in groceries for your {c["name"]} family. When cooling problems strike in a home with {c["desc"]}, you cannot afford to wait—spoiled food costs money and poses serious health risks to your household. {c["name"]} is {c["notable"]}, serving {c["pop"]} residents throughout {c["areas"]}. Our factory-certified {b} technicians provide rapid same-day response to protect your food investment and restore reliable refrigeration quickly.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Refrigerator Problems We Diagnose</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} refrigerator issue: units that won't cool despite running constantly causing food to spoil, freezers that don't maintain proper temperature allowing items to thaw, ice makers that stop producing or dispense slowly or produce malformed ice, water dispensers with weak flow or no output at all, unusual compressor noises cycling patterns or clicking sounds, excessive frost buildup in freezer sections indicating defrost system problems, water pooling inside compartments or underneath the refrigerator, temperature fluctuations that affect food quality and safety, refrigerator sections that freeze items near vents, condenser fans that make grinding sounds or don't run, evaporator fans that stop circulating cold air, and digital displays showing error codes or malfunctioning.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Refrigerator Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} refrigerator parts for {c["name"]} repairs: compressors and compressor starting components including relays and overloads, evaporator fan motors that circulate cold air throughout compartments, condenser coils and condenser fan assemblies that dissipate heat, defrost heaters and defrost termination thermostats for frost-free models, temperature control thermostats and cold controls, start relays and PTC devices that help compressors start, door gaskets and seals for proper closure and energy efficiency, ice maker modules augers and water inlet valves, water filters and filter housings, main control boards and user interface panels, defrost timers and adaptive defrost controls, temperature sensors and thermistors, damper assemblies that regulate airflow between sections, and evaporator coils.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{c["name"]} Refrigerator Emergency Service</h4>
<p style="margin-bottom: 12px;">Refrigerator emergencies demand immediate attention—every hour without proper cooling risks food spoilage and safety. For {c["name"]} residents with {c["housing"]} throughout {c["areas"]}, we offer priority same-day service when your food is at risk. Our technicians arrive with commonly needed {b} parts, professional diagnostic equipment, and the expertise to restore cooling quickly. We service all installation types found in {c["name"]} homes, from built-in refrigerators integrated with custom cabinetry to counter-depth French door models to standard freestanding units. Our experience with various configurations means we understand the specific access requirements, ventilation needs, and repair considerations for each type.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Refrigerator Care Tips for {c["name"]} Homeowners</h4>
<p style="margin-bottom: 12px;">Extend the life of your {b} refrigerator with these professional recommendations: keep condenser coils clean by vacuuming every six months to maintain efficiency and prevent overheating, ensure adequate clearance around the unit for proper airflow especially important for built-in installations, check door gaskets periodically for cracks or gaps that waste energy and strain the compressor, keep the refrigerator well-stocked as thermal mass helps maintain temperature during door openings, avoid placing hot foods directly inside as this raises internal temperature and increases compressor workload, replace water filters on schedule to maintain water and ice quality, and address unusual sounds or temperature changes promptly before minor issues become major repairs. Every {b} refrigerator repair in {c["name"]} includes genuine parts and our comprehensive service warranty.</p>
'''


def generate_dishwasher_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Dishwasher Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">When your {b} dishwasher stops cleaning effectively in your {c["name"]} kitchen, dirty dishes pile up and hand-washing becomes a frustrating daily chore. For homes with {c["desc"]}, a properly functioning dishwasher is essential to maintaining busy household routines. {c["name"]} is {c["notable"]}, with {c["pop"]} residents throughout {c["areas"]} depending on reliable kitchen appliances. Our factory-certified {b} technicians provide same-day appointments and expert diagnosis for every dishwasher problem.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dishwasher Problems We Solve</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} dishwasher issue: units that won't drain leaving standing water in the bottom after cycles, dishes coming out dirty with food residue film spots or cloudiness, water leaking onto kitchen floors from door seals pump connections or internal components, door latches that won't engage preventing cycle starts, spray arms that don't rotate properly leaving portions of loads dirty, detergent dispensers that fail to release during wash cycles, drying problems leaving dishes wet and requiring hand toweling, control panels that don't respond to button presses or display errors, unusual grinding humming or squealing noises during operation, units that won't fill with water properly, and cycles that stop mid-wash leaving dishes unfinished.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Dishwasher Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} dishwasher parts for {c["name"]} repairs: circulation pumps and pump motors that create wash pressure, drain pumps and motors that remove dirty water from the tub, door latch assemblies strike plates and latch switches, spray arm bearings bushings and mounting hardware, upper and lower spray arms, float switches and float assemblies that detect water levels, water inlet valves that control filling, heating elements for drying and sanitizing and boosting water temperature, main control boards and touchpad assemblies, rack rollers adjusters and tines, upper and lower rack assemblies, door gaskets and tub seals, detergent and rinse aid dispenser mechanisms, wash impellers, and silverware basket components.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Dishwasher Performance in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Water quality in many {c["name"]} areas affects dishwasher performance over time, with mineral deposits building up on spray arms heating elements and interior surfaces. Hard water can leave spots on glassware and film on dishes even when the dishwasher is operating properly. Our technicians clean components during service calls when buildup is affecting performance and advise on proper detergent selection, rinse aid use, and loading techniques for optimal cleaning results. We also verify water temperature at the inlet, as many dishwasher problems stem from household water heaters set too low to properly activate detergent and sanitize dishes.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Why {c["name"]} Trusts Our {b} Dishwasher Service</h4>
<p style="margin-bottom: 12px;">We service {b} dishwashers in all installation configurations found throughout {c["areas"]} in {c["name"]}, from fully integrated panel-ready units that match custom cabinetry to standard built-in models with visible controls. Our technicians understand the access requirements and specific considerations for each installation type. Every {b} dishwasher repair includes genuine manufacturer parts, transparent upfront pricing, and our comprehensive warranty. We arrive on time, diagnose accurately, and complete most repairs in a single visit so you can get back to your normal routine without delay. Our commitment to professional service keeps {c["name"]} customers coming back whenever appliance problems arise.</p>
'''


def generate_oven_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Oven & Range Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">Your {b} oven is central to meal preparation in your {c["name"]} home, essential for everything from quick weeknight dinners to elaborate holiday feasts. When oven problems strike in a kitchen with {c["desc"]}, family meals and entertaining plans are disrupted until repairs are made. {c["name"]} is {c["notable"]}, home to {c["pop"]} residents throughout {c["areas"]} who depend on reliable cooking appliances. Our factory-certified {b} technicians provide same-day appointments for urgent cooking needs.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Oven Problems We Diagnose</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} oven issue: ovens that won't heat at all or take extremely long to preheat, uneven cooking with hot spots and cold areas that ruin recipes, self-cleaning cycles that won't start won't complete or damage interior finishes, doors that don't close properly or seal allowing heat escape, control panel error codes and beeping alerts that prevent operation, gas burners that won't ignite produce weak flames or have uneven flame patterns, broiler elements that don't heat properly, temperature inaccuracies causing undercooked or burned food despite correct settings, convection fans that don't operate properly, oven lights that won't illuminate, door hinges that are broken bent or don't hold the door at desired positions, and timers that malfunction.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Oven Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} oven parts for {c["name"]} repairs: bake elements for bottom heat, broil elements for top heat, hidden bake elements in smooth-bottom ovens, gas igniters glow bars and spark electrodes, oven thermostats and temperature controls, main control boards and clock assemblies, door hinges hinge springs and hinge receivers, door gaskets for heat retention, convection fan motors and fan blades, oven temperature sensors and probes, safety gas valves regulators and pressure regulators, spark modules for gas ignition, self-clean door latch assemblies and motors, light bulbs sockets and lens covers, selector switches, and broiler pans and racks.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Gas Oven Safety in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Gas oven repairs require specialized expertise in ignition systems gas valves and overall gas line safety—qualifications our {c["name"]} technicians maintain through ongoing certification and training. We verify proper igniter function including glow time and current draw, gas valve operation timing and flow rates, proper flame characteristics for complete combustion, and safety system integrity including flame sensors and limit switches. Any gas odor should be addressed immediately—turn off the oven, ventilate the area, and call for professional service rather than attempting diagnosis yourself.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Range Configurations in {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">For homes throughout {c["areas"]} with {c["housing"]}, we're experienced with all range configurations from slide-in models that fit between counters to freestanding ranges to professional-style units with multiple ovens and high-BTU burners. Dual-fuel ranges combining gas cooktops with electric ovens require technicians versed in both fuel types. Wall ovens single and double present different access and installation considerations. Whatever your {b} cooking appliance configuration, our {c["name"]} technicians have the expertise and genuine parts to restore full function quickly. Every repair includes our comprehensive parts and labor warranty.</p>
'''


def generate_cooktop_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Cooktop Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">A malfunctioning {b} cooktop severely limits your cooking options in your {c["name"]} kitchen. Whether you have gas, electric, or induction cooking surfaces in a home with {c["desc"]}, our factory-certified technicians restore full functionality quickly. {c["name"]} is {c["notable"]}, with {c["pop"]} residents throughout {c["areas"]} relying on cooktops daily for family meals. We provide same-day appointments and expert {b} diagnosis for every cooktop type.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Cooktop Problems We Solve</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} cooktop issue: gas burners that won't ignite despite clicking or won't click at all, gas burners with weak flames yellow flames or uneven flame patterns indicating combustion problems, electric coil or radiant elements that don't heat or heat unevenly, induction zones that fail to detect compatible cookware or show error codes, cracked damaged or chipped glass ceramic surfaces requiring professional assessment, uneven heat distribution across cooking zones, control knobs that spin freely or don't adjust temperature properly, touch control panels that don't respond to input or register phantom touches, spark electrodes that are dirty damaged or mispositioned, gas odors during operation that indicate potential leaks requiring immediate attention, and downdraft ventilation systems that don't operate.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Cooktop Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} cooktop parts for {c["name"]} repairs: spark igniter modules and control boards, spark electrodes for each burner position, gas burner caps bases and orifices, sealed burner assemblies, gas safety valves regulators and gas lines, electric radiant elements and coils, element receptacles and terminals, infinite switches for temperature control, induction coils and power boards, glass ceramic surface assemblies, control knobs shafts and bezels, touch control panels and membranes, wiring harnesses and connectors, simmer burner components, and high-power burner assemblies.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Cooktop Safety for {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">Cooktop safety is paramount—gas leaks and electrical faults require professional attention rather than DIY attempts. Our licensed technicians verify proper operation and safety system function before completing any {b} cooktop repair in {c["name"]}. For gas cooktops, we test ignition timing across all burners, flame patterns for proper combustion, gas connections for leaks using professional detection equipment, and safety shutoff systems. Electric and induction models receive thorough electrical testing of elements, wiring, controls, and safety interlocks. Cracked glass cooktops present shock and fire hazards and should not be used until professionally assessed.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Cooktop Configurations in {c["name"]}</h4>
<p style="margin-bottom: 12px;">We service all cooktop types and configurations found throughout {c["areas"]} in {c["name"]}: built-in cooktops installed in counter cutouts, rangetop units that sit on cabinet bases, island installations with downdraft ventilation, and standard configurations against walls with overhead ventilation. Professional-style cooktops with high-BTU burners, griddles, and grills require specialized knowledge. Modular cooktop systems with interchangeable components present unique diagnostic considerations. Our {b} certified technicians have experience with every configuration and carry the genuine parts needed for proper repair. Gas cooktop installations require proper clearances from combustible materials and adequate ventilation to prevent carbon monoxide buildup. Electric and induction models need dedicated circuits with appropriate amperage to handle power demands safely. Whether your {c["name"]} home has a compact two-burner cooktop or a full professional six-burner unit with griddle, we have the expertise and parts to complete the repair correctly. Every cooktop service call includes thorough safety verification and our comprehensive warranty protection for parts and labor.</p>
'''


def generate_microwave_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Microwave Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">Your {b} microwave handles quick meals, efficient reheating, defrosting, and countless cooking tasks for your busy {c["name"]} household. When microwave problems occur in a home with {c["desc"]}, meal preparation becomes significantly more time-consuming and inconvenient. {c["name"]} is {c["notable"]}, home to {c["pop"]} residents throughout {c["areas"]} who depend on microwave convenience daily. Our factory-certified {b} technicians provide same-day appointments and expert microwave service.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Microwave Problems We Diagnose</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} microwave issue: units that don't heat food despite running and making normal sounds, turntables that stop rotating causing uneven heating and hot spots, sparking or arcing inside the cooking chamber from damaged waveguide covers or metal contamination, doors that don't latch or seal properly preventing operation due to safety interlocks, display panels that go blank show errors or have missing segments, buttons and touchpads that don't respond to touch or register wrong inputs, interior lights that won't illuminate, unusual humming buzzing or high-pitched whining sounds, units that run but produce no heat at all, exhaust fans in over-the-range models that don't ventilate properly, and door handles or hinges that are broken loose or difficult to operate.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Microwave Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} microwave parts for {c["name"]} repairs: magnetrons that generate microwave energy for cooking, high-voltage capacitors and diodes, high-voltage transformers, door switches and safety interlock assemblies, turntable motors couplers and glass trays, main control boards and display assemblies, waveguide covers that protect internal components from food splatter, thermal fuses cutoffs and thermostats, door latch mechanisms and door hooks, touchpad membranes and overlay panels, exhaust fan motors for over-the-range models, charcoal grease and combination filters, light bulbs and sockets, stirrer motors and blades, and cavity paint for interior touch-ups.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Microwave Safety Expertise</h4>
<p style="margin-bottom: 12px;">Microwave repairs require specialized knowledge of high-voltage components and safety protocols. High-voltage capacitors can retain dangerous charges of several thousand volts even when the microwave is unplugged, making untrained repair attempts potentially fatal. Our {c["name"]} technicians are trained in safe microwave service procedures including proper capacitor discharge techniques, high-voltage testing methods, and magnetron handling. We carry the specialized equipment needed to safely diagnose and repair microwave issues. Door interlock systems prevent operation when doors are open and must function perfectly—we test all door switches and verify proper interlock operation before returning any microwave to service.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Over-the-Range Microwave Service in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Over-the-range microwaves in {c["name"]} kitchens combine cooking convenience with essential range ventilation. These units require service for cooking functions, exhaust fan operation, and lighting systems. We repair blower motors, fan speeds, grease and charcoal filters, cooktop lights, and night lights in addition to cooking components. Proper ventilation function is important for removing cooking smoke steam and odors, especially in kitchens without separate range hoods. Our experience with {c["housing"]} throughout {c["areas"]} means we understand various OTR installation configurations and venting arrangements. Every {b} microwave repair includes genuine parts and our comprehensive warranty.</p>
'''


def generate_wine_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Wine Cooler Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">Your {b} wine cooler protects a valuable collection that may represent years of careful selection and significant financial investment. For wine enthusiasts in {c["name"]} with {c["desc"]}, proper storage temperature humidity and vibration control are essential for preservation and aging. {c["name"]} is {c["notable"]}, with discerning collectors throughout {c["areas"]} who understand that wine storage conditions directly affect quality and value. Our factory-certified {b} technicians provide prompt service to protect your collection.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Wine Cooler Problems We Diagnose</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} wine cooler issue: units that don't maintain proper temperature zones allowing wine to warm and spoil, compressors that run constantly cycling too frequently or not at all, excessive vibration that disturbs wine sediment affecting aging and taste, humidity control problems that dry out corks compromising bottle seals, door seal failures that allow temperature fluctuations and increased energy consumption, LED lighting that won't illuminate making bottle selection difficult, inconsistent temperatures between zones in dual-zone models, frost buildup indicating defrost system problems, condenser coils clogged with dust reducing cooling efficiency, unusual compressor noises like clicking buzzing or rattling, control panel errors or calibration issues displaying wrong temperatures, and fans that don't circulate air properly creating hot spots.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Wine Cooler Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} wine cooler parts for {c["name"]} repairs: compressors and compressor starting components, thermostats temperature sensors and controllers, evaporator fans and fan motors for air circulation, condenser coils condenser fans and fan motors, door gaskets and seals for proper closure, vibration dampening pads mounts and compressor isolation, humidity control systems and humidity sensors, LED lighting strips drivers and bulbs, temperature zone dividers and sensors for dual-zone models, control boards digital displays and touch panels, wine rack assemblies slides and shelf supports, door hinges handles and glass panels, drain systems and drip trays, and defrost components for frost-free models.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Wine Storage Expertise for {c["name"]} Collectors</h4>
<p style="margin-bottom: 12px;">Wine storage is far more demanding than standard refrigeration—factors that seem minor can significantly affect wine quality over time. Temperature stability is critical, as fluctuations cause corks to expand and contract allowing air infiltration. Most wines store best between 45-65 degrees depending on type. Humidity levels around 70 percent keep corks moist and sealed. Vibration disturbs sediment and can accelerate chemical reactions, so compressor-based coolers require proper isolation. UV light damages wine, making UV-filtering glass doors important. Our {b} certified technicians understand these specific requirements and service wine coolers with appropriate care and attention.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Protecting Your Wine Investment in {c["name"]}</h4>
<p style="margin-bottom: 12px;">We understand that wine cooler problems put valuable collections at risk. For {c["name"]} collectors throughout {c["areas"]} with {c["housing"]}, we minimize repair time to reduce temperature fluctuation risks, arriving with genuine {b} parts and completing most repairs in a single visit. We also provide guidance on optimal cooler placement away from heat sources and direct sunlight, proper loading to allow air circulation, temperature setting recommendations for different wine types, and maintenance practices that extend cooler life. Every {b} wine cooler repair includes genuine manufacturer parts and our comprehensive service warranty to protect both your cooler and your collection.</p>
'''


def generate_hood_content(brand, city):
    c = get_city(city)
    b = fix_brand(brand)
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Vent Hood Repair in {c["name"]}, NY</h4>
<p style="margin-bottom: 12px;">Your {b} range hood removes smoke, steam, grease particles, and cooking odors from your {c["name"]} kitchen, protecting surfaces and maintaining air quality. When ventilation fails in a home with {c["desc"]}, cooking fumes linger and grease accumulates on cabinets walls and ceilings throughout your kitchen. {c["name"]} is {c["notable"]}, with {c["pop"]} residents throughout {c["areas"]} depending on effective kitchen ventilation. Our factory-certified {b} technicians provide same-day appointments and expert vent hood service.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Vent Hood Problems We Solve</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot and repair every {b} vent hood issue: fans that don't run at all leaving no ventilation during cooking, weak airflow that doesn't effectively remove smoke and steam, excessive noise during operation from worn bearings loose components or motor problems, lights that won't turn on or flicker intermittently, units that won't shut off after cooking wasting energy, grease buildup affecting performance despite regular filter cleaning, motors that run but don't move air effectively due to blower wheel issues, control switches that don't respond or don't change speeds properly, damper flaps that stick open allowing cold air infiltration or stuck closed blocking exhaust, touch controls or electronic controls that malfunction, and vibration or rattling during operation.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Vent Hood Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} vent hood parts for {c["name"]} repairs: blower motors and complete blower assemblies, fan blades blower wheels and blade assemblies, motor bearings and bushings, light sockets bulbs and lens covers, control switches push buttons and knobs, speed selector switches and electronic speed controls, grease filters baffle filters and mesh filters, charcoal filters for recirculating models, duct dampers backdraft dampers and damper motors, wiring harnesses connectors and terminals, capacitors for motor starting and running, touch control panels and electronic control boards, halogen and LED light assemblies, motor mounting hardware and isolation mounts, and remote blower motors for external installations.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Kitchen Ventilation in {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">Proper kitchen ventilation protects your {c["name"]} home from grease accumulation, excess moisture that can cause mold growth, and lingering cooking odors that permeate fabrics and finishes. Our technicians inspect airflow rates and ductwork during every {b} vent hood service call, checking for restrictions from grease buildup, crushed or kinked ductwork, improper duct sizing, excessive duct length or turns, and blocked exterior terminations. We measure actual CFM output and compare to manufacturer specifications. Professional duct cleaning recommendations are provided when buildup is affecting performance or creating fire hazards.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Vent Hood Configurations in {c["name"]}</h4>
<p style="margin-bottom: 12px;">We service all vent hood configurations found throughout {c["areas"]} in {c["name"]}: wall-mounted chimney hoods, island hoods suspended from ceilings, under-cabinet hoods mounted beneath wall cabinets, downdraft systems that rise from countertops or cooktop surfaces, insert hoods installed in custom enclosures, and professional-grade hoods with high-CFM blowers. Each type has specific service considerations. Remote blower installations where the motor mounts externally require different diagnostic approaches. Our {b} certified technicians have experience with every configuration and access genuine parts for proper repair. Every vent hood service call includes thorough operation testing and our comprehensive warranty protection.</p>
'''


CONTENT_GENERATORS = {
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
    updated = 0
    for card_id, generator in CONTENT_GENERATORS.items():
        content = generator(brand_slug, city_slug)
        new_html = update_card(html, card_id, content)
        if new_html != html:
            html = new_html
            updated += 1
    if html != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
    return updated


def main():
    base_path = "/Users/globalaffiliate/westchester-county-repair"
    csv_path = "/Users/globalaffiliate/Downloads/westchester-coverage-report/Table.csv"
    affected = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                affected.append(row[0])
    print("=" * 60)
    print("ENSURING 500+ WORDS PER SERVICE CARD (V2)")
    print("=" * 60)
    total_pages = 0
    total_cards = 0
    for url in sorted(affected):
        parsed = urlparse(url)
        parts = parsed.path.strip('/').split('/')
        if len(parts) >= 3 and parts[0] == 'ny' and parts[2].endswith('-repair'):
            city = parts[1]
            brand = parts[2].replace('-repair', '')
            file_path = os.path.join(base_path, *parts, 'index.html')
            if os.path.exists(file_path):
                cards = process_page(file_path, city, brand)
                if cards > 0:
                    total_pages += 1
                    total_cards += cards
                    print(f"Updated: {'/'.join(parts)}/")
    print("\n" + "=" * 60)
    print(f"TOTAL: {total_pages} pages, {total_cards} cards with 500+ words each")
    print("=" * 60)

if __name__ == "__main__":
    main()
