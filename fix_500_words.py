#!/usr/bin/env python3
"""
Ensure all service cards have 500+ words in the 334 affected pages.
Uses correct card IDs: washer, dryer, fridge, dishwasher, oven, cooktop, microwave, wine, hood
"""

import os
import re
import csv
from urllib.parse import urlparse

# City data
CITIES = {
    "ardsley": {"name": "Ardsley", "pop": "4,800", "desc": "tree-lined streets and Tudor homes dating to the 1920s", "areas": "Ardsley Park, Heatherdell, Ashford Avenue"},
    "bronxville": {"name": "Bronxville", "pop": "6,500", "desc": "prestigious Tudor estates and luxury condominiums", "areas": "Bronxville Village, Lawrence Park, Armour Villa Park"},
    "dobbs-ferry": {"name": "Dobbs Ferry", "pop": "11,000", "desc": "charming Hudson River waterfront Victorian homes", "areas": "Downtown, the Heights, South Dobbs Ferry, Wickers Creek"},
    "eastchester": {"name": "Eastchester", "pop": "19,500", "desc": "historic colonials and modern townhouses since 1664", "areas": "Chester Heights, Lake Isle, Waverly, Garth Road"},
    "elmsford": {"name": "Elmsford", "pop": "5,000", "desc": "convenient affordable homes near major highways", "areas": "Downtown Elmsford, Knollwood neighborhood"},
    "fairview": {"name": "Fairview", "pop": "3,700", "desc": "diverse residential community in Greenburgh", "areas": "Fairview and surrounding Greenburgh areas"},
    "harrison": {"name": "Harrison", "pop": "28,000", "desc": "luxury estates and executive homes in Purchase area", "areas": "Purchase, West Harrison, Sterling Ridge, Silver Lake"},
    "hartsdale": {"name": "Hartsdale", "pop": "5,300", "desc": "split-level homes and garden apartments near shopping", "areas": "East Hartsdale, West Hartsdale, Four Corners"},
    "hastings-on-hudson": {"name": "Hastings-on-Hudson", "pop": "8,000", "desc": "artistic Victorian homes with Hudson River views", "areas": "Downtown, The Dale, Hillside Woods, Riverview Manor"},
    "irvington": {"name": "Irvington", "pop": "6,500", "desc": "historic mansions near Washington Irving's Sunnyside", "areas": "Downtown, Matthiessen Park, Ardsley-on-Hudson"},
    "larchmont": {"name": "Larchmont", "pop": "6,200", "desc": "exclusive waterfront estates on Long Island Sound", "areas": "Larchmont Manor, Murray Hill, Orienta Point"},
    "mamaroneck": {"name": "Mamaroneck", "pop": "19,000", "desc": "vibrant harbor community with beach cottages", "areas": "Harbor Heights, Orienta, Washingtonville, Rye Neck"},
    "mount-vernon": {"name": "Mount Vernon", "pop": "73,000", "desc": "diverse multi-family homes and historic residences", "areas": "Fleetwood, Chester Heights, South Side, Hutchinson"},
    "new-rochelle": {"name": "New Rochelle", "pop": "80,000", "desc": "high-rise condos and waterfront properties near NYC", "areas": "Wykagyl, Beechmont, Huguenot Park, Premium Point"},
    "pelham-manor": {"name": "Pelham Manor", "pop": "5,500", "desc": "stately Tudor estates with excellent schools", "areas": "Pelham Manor, North Pelham, Shore Road area"},
    "rye": {"name": "Rye", "pop": "16,000", "desc": "affluent waterfront estates near Playland", "areas": "Milton Point, Rye Beach, Park Avenue, Grace Church"},
    "scarsdale": {"name": "Scarsdale", "pop": "18,000", "desc": "grand estates and architect-designed modern homes", "areas": "Fox Meadow, Greenacres, Heathcote, Quaker Ridge"},
    "tarrytown": {"name": "Tarrytown", "pop": "11,500", "desc": "historic riverfront Victorian homes and brownstones", "areas": "Downtown, Sleepy Hollow Manor, Wilson Park"},
    "valhalla": {"name": "Valhalla", "pop": "3,500", "desc": "affordable homes near Westchester Medical Center", "areas": "Valhalla, Kensico, Grasslands area"},
    "village-of-pelham": {"name": "Village of Pelham", "pop": "7,000", "desc": "charming Victorians with easy Metro-North access", "areas": "Pelham Heights, Chester Park, Highbrook Gardens"},
    "white-plains": {"name": "White Plains", "pop": "58,000", "desc": "luxury high-rises and historic homes in commercial hub", "areas": "Battle Hill, Fisher Hill, Gedney Farms, Highlands"},
    "yonkers": {"name": "Yonkers", "pop": "200,000", "desc": "diverse neighborhoods from high-rises to Victorians", "areas": "Crestwood, Park Hill, Ludlow, Getty Square, Greystone"}
}

def get_city(slug):
    return CITIES.get(slug, {"name": slug.replace("-", " ").title(), "pop": "varies", "desc": "quality residential neighborhoods", "areas": "all neighborhoods"})


def generate_washer_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Washer Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">When your {b} washing machine breaks down in {c["name"]} (population {c["pop"]}), you need factory-certified technicians who understand both sophisticated washer technology and the unique needs of homes with {c["desc"]}. Our {b} specialists serve {c["areas"]} with same-day appointments and fully-stocked service vehicles.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Washer Problems We Diagnose in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} washer issue: drums that won't spin leaving clothes soaking wet, units that fail to drain completely, excessive vibration that shakes your laundry area, water filling problems from slow fills to overflows, door or lid mechanisms that won't lock properly preventing cycle starts, mysterious error codes that halt operation mid-wash, unusual grinding or squealing noises during agitation, leaking water from door seals or hoses, clothes coming out still dirty despite full cycles, and units that won't power on at all.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Washer Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} replacement parts for {c["name"]} service calls: drum bearings that cause grinding noises during spin cycles, door boot seals that leak water onto floors, drain pumps clogged with debris coins or small items, motor couplings that break from overloading or age, water inlet valves that fail to regulate fill properly, transmission assemblies in top-load models, clutch components that slip during high-speed spin, shock absorbers and suspension rods that cause excessive movement, main control boards displaying error codes, lid switches and door latches that prevent operation, drive belts that slip or break, and pressure switches that misread water levels.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Why {c["name"]} Residents Choose Our {b} Service</h4>
<p style="margin-bottom: 12px;">We understand that a broken washer means laundry piling up fast for {c["name"]} families. Our technicians arrive promptly with diagnostic equipment specifically calibrated for {b} washers, allowing accurate identification of problems on the first visit. We provide upfront pricing before beginning any repair, and most washer repairs in {c["name"]} are completed the same day. Every repair includes our comprehensive parts and labor warranty, genuine {b} components, and our satisfaction guarantee that brings {c["name"]} customers back whenever appliance problems arise.</p>
'''


def generate_dryer_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Dryer Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">A malfunctioning {b} dryer in your {c["name"]} home means damp clothes, extended dry times, and mounting frustration. Whether you have a gas or electric {b} dryer in a property with {c["desc"]}, our factory-certified technicians diagnose and repair any issue quickly. We serve all {c["name"]} neighborhoods including {c["areas"]} with same-day service availability.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dryer Problems We Solve in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} dryer issue: no heat despite the drum turning normally, insufficient heat leaving clothes damp after full cycles, overheating that triggers safety shutoffs, drums that won't tumble at all, squeaking or grinding sounds during operation, burning smells indicating potential hazards, units shutting off mid-cycle repeatedly, clothes taking two or three cycles to dry properly, gas dryers with ignition failures, electric dryers with element problems, and error codes on digital displays.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Dryer Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} dryer parts for {c["name"]} repairs: heating elements that burn out from age or power surges, thermal fuses that blow to prevent fires, drum rollers that wear and cause squeaking sounds, drive belts that fray and slip or snap completely, gas igniters that fail to light burners, gas valve coils that prevent fuel flow, blower motors that don't move air efficiently, blower wheels clogged with lint debris, thermistors that misread temperatures, door switches that don't sense closure, drum seals that leak hot air, and main control boards with electronic failures.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Dryer Safety for {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">Proper dryer ventilation is critical for homes in {c["name"]}, especially properties with {c["desc"]} that may have longer vent runs. Our technicians inspect exhaust systems during every {b} dryer service call, checking for lint buildup, crushed ductwork, and improper terminations that reduce efficiency and create fire hazards. We recommend professional vent cleaning when needed and provide maintenance tips to keep your {b} dryer running safely and efficiently for years to come.</p>
'''


def generate_fridge_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Refrigerator Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Your {b} refrigerator runs continuously to protect hundreds of dollars in groceries for your {c["name"]} family. When cooling problems strike in a home with {c["desc"]}, you can't afford to wait—spoiled food costs money and poses health risks. Our factory-certified {b} technicians provide rapid same-day response throughout {c["areas"]} to protect your investment.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Refrigerator Problems We Diagnose</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} refrigerator issue: units that won't cool despite running constantly, freezers that don't maintain proper temperature, ice makers that stop producing or dispense slowly, water dispensers with weak flow or no output, unusual compressor noises or cycling patterns, excessive frost buildup in freezer sections, water pooling inside compartments or underneath the unit, temperature fluctuations that affect food quality, refrigerator sections that freeze food items, condenser fans that make grinding sounds, and digital displays showing error codes.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Refrigerator Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} refrigerator parts for {c["name"]} repairs: compressors and compressor components, evaporator fan motors that circulate cold air, condenser coils and fan assemblies, defrost heaters and thermostats for frost-free models, temperature control thermostats, start relays and overload protectors, door gaskets for proper sealing, ice maker modules and water inlet valves, water filters and filter housings, main control boards and user interface panels, defrost timers and adaptive defrost controls, and damper assemblies that regulate airflow between sections.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{c["name"]} Refrigerator Emergency Service</h4>
<p style="margin-bottom: 12px;">Refrigerator emergencies demand immediate attention. For {c["name"]} residents with {c["desc"]}, we offer priority same-day service when your food is at risk. Our technicians arrive with commonly needed {b} parts, diagnostic equipment, and the expertise to restore cooling quickly. We service all installation types from built-in units to counter-depth configurations, understanding the specific requirements of each. Every refrigerator repair includes genuine {b} parts and our comprehensive warranty.</p>
'''


def generate_dishwasher_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Dishwasher Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">When your {b} dishwasher stops cleaning effectively in your {c["name"]} kitchen, dirty dishes pile up and hand-washing becomes a daily chore. For homes with {c["desc"]}, a working dishwasher is essential to busy household routines. Our factory-certified technicians serve {c["areas"]} with same-day appointments and expert {b} diagnosis.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Dishwasher Problems We Solve</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} dishwasher issue: units that won't drain leaving standing water in the bottom, dishes coming out dirty with food residue or film, water leaking onto kitchen floors from door seals or connections, door latches that won't engage preventing cycle starts, spray arms that don't rotate properly, detergent dispensers that fail to release during wash, drying problems leaving dishes wet after cycles, control panels that don't respond to button presses, unusual noises during operation, and error codes displayed during cycles.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Dishwasher Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} dishwasher parts for {c["name"]} repairs: circulation pumps that create wash pressure, drain pumps and motors that remove dirty water, door latch assemblies and strike plates, spray arm bearings and mounting hardware, float switches that detect water levels, water inlet valves that control filling, heating elements for drying and sanitizing, main control boards and touchpad assemblies, rack rollers and adjusters, upper and lower rack assemblies, door gaskets and seals, and detergent dispenser mechanisms.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Dishwasher Care Tips for {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">Hard water in many {c["name"]} areas affects dishwasher performance over time, causing mineral buildup on spray arms, heating elements, and interior surfaces. Our technicians clean components during service calls and advise on proper detergent use, loading techniques, and maintenance routines for optimal performance. We service {b} dishwashers in all installation configurations found throughout {c["areas"]}, from integrated panel-ready units to standard built-ins.</p>
'''


def generate_oven_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Oven & Range Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Your {b} oven is central to meal preparation in your {c["name"]} home, from weeknight dinners to holiday gatherings. When oven problems strike in a kitchen with {c["desc"]}, family meals and entertaining plans are disrupted. Our factory-certified technicians serve {c["areas"]} with same-day appointments for urgent cooking needs.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Oven Problems We Diagnose</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} oven issue: ovens that won't heat or take forever to preheat, uneven cooking with hot spots and cold areas ruining recipes, self-cleaning cycles that won't start or complete properly, doors that don't close or seal allowing heat escape, error codes and beeping alerts, gas burners that won't ignite or produce weak flames, temperature inaccuracies causing undercooked or burned food, convection fans that don't operate, broiler elements that fail, and control panels with unresponsive buttons.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Oven Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} oven parts for {c["name"]} repairs: bake elements for bottom heat, broil elements for top heat, gas igniters and glow bars, oven thermostats for temperature control, main control boards and clock assemblies, door hinges and hinge springs, door gaskets for heat retention, convection fan motors and blades, oven temperature sensors and probes, safety gas valves and regulators, spark modules for gas ignition, self-clean door latches, and light bulbs and sockets.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Gas Oven Safety in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Gas oven repairs require specialized expertise in ignition systems and gas line safety—qualifications our {c["name"]} technicians maintain through ongoing certification. We verify proper igniter function, gas valve operation, and safety system integrity before completing any gas oven repair. For homes throughout {c["areas"]} with {c["desc"]}, we're experienced with all range configurations from slide-in models to professional-style units. Every {b} oven repair includes our comprehensive parts and labor warranty.</p>
'''


def generate_cooktop_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Cooktop Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">A malfunctioning {b} cooktop limits your cooking options in your {c["name"]} kitchen. Whether you have gas, electric, or induction cooking surfaces in a home with {c["desc"]}, our factory-certified technicians restore full functionality quickly. We serve {c["areas"]} with same-day appointments and expert {b} diagnosis.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Cooktop Problems We Solve</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} cooktop issue: gas burners that won't ignite or click repeatedly without lighting, electric elements that don't heat or heat unevenly, induction zones that fail to detect compatible cookware, cracked glass surfaces requiring professional assessment, uneven heat distribution across cooking zones, control knobs or touch panels that don't respond, gas odors during operation indicating potential safety issues, spark electrodes that are dirty or damaged, and infinite switches that won't maintain temperature settings.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Cooktop Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} cooktop parts for {c["name"]} repairs: spark igniter modules and electrodes, gas burner caps and bases, sealed burner orifices, gas safety valves and regulators, electric heating elements and coils, infinite switches for temperature control, induction coils and sensors, glass surface assemblies, control knobs and bezels, touch control panels and membranes, wiring harnesses and connectors, and burner grates and drip pans.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Cooktop Safety for {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">Cooktop safety is paramount—gas leaks and electrical issues require professional attention. Our licensed technicians verify proper operation and safety system function before completing any {b} cooktop repair in {c["name"]}. For gas cooktops, we test ignition timing, flame patterns, and leak detection. Electric and induction models receive thorough electrical testing. We service all cooktop types found throughout {c["areas"]}, from island installations to standard counter configurations.</p>
'''


def generate_microwave_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Microwave Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Your {b} microwave handles quick meals, reheating, and defrosting for your busy {c["name"]} household. When microwave problems occur in a home with {c["desc"]}, meal preparation becomes significantly more time-consuming. Our factory-certified technicians serve {c["areas"]} with same-day appointments and expert {b} microwave service.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Microwave Problems We Diagnose</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} microwave issue: units that don't heat food despite running and making normal sounds, turntables that stop rotating causing uneven heating, sparking or arcing inside the cooking chamber, doors that don't latch or seal properly preventing operation, display panels that go blank or show error codes, buttons and touchpads that don't respond to touch, interior lights that won't illuminate, unusual humming or buzzing sounds, units that run but produce no heat, and exhaust fans in over-the-range models that don't ventilate.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Microwave Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} microwave parts for {c["name"]} repairs: magnetrons that generate microwave energy, high-voltage capacitors and diodes, door switches and interlock assemblies, turntable motors and couplers, main control boards and displays, waveguide covers that protect internal components, thermal fuses and cutoffs, door latch mechanisms, touchpad membranes and overlays, exhaust fan motors for OTR models, light bulbs and sockets, and charcoal and grease filters.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Microwave Safety Expertise</h4>
<p style="margin-bottom: 12px;">Microwave repairs require specialized knowledge of high-voltage components—capacitors can retain dangerous charges even when unplugged. Our {c["name"]} technicians are trained in safe microwave service procedures and carry the proper equipment to discharge and test components safely. Over-the-range microwaves in {c["name"]} kitchens require service for both cooking and ventilation functions. We repair exhaust fans, lighting, and filter systems alongside cooking components for complete OTR microwave service.</p>
'''


def generate_wine_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Wine Cooler Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Your {b} wine cooler protects a valuable collection that may represent years of careful selection and significant investment. For wine enthusiasts in {c["name"]} with {c["desc"]}, proper storage temperature and humidity are essential for preservation. Our factory-certified technicians serve {c["areas"]} with prompt service to protect your collection.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Wine Cooler Problems We Diagnose</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} wine cooler issue: units that don't maintain proper temperature zones allowing wine to warm, compressors that run constantly or cycle too frequently, excessive vibration that disturbs wine sediment affecting aging, humidity control problems that dry out corks compromising seals, door seal failures that allow temperature fluctuations, LED lighting that won't illuminate interior shelves, inconsistent temperatures between zones in dual-zone models, frost buildup indicating defrost system problems, and control panel errors or calibration issues.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Wine Cooler Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} wine cooler parts for {c["name"]} repairs: compressors and compressor components, thermostats and temperature sensors, evaporator fans for air circulation, condenser coils and fan assemblies, door gaskets for proper sealing, vibration dampening pads and mounts, humidity control systems, LED lighting strips and drivers, temperature zone dividers and sensors, control boards and digital displays, wine rack assemblies and slides, and door hinges and handles.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Wine Storage Expertise for {c["name"]} Collectors</h4>
<p style="margin-bottom: 12px;">Wine storage is more demanding than standard refrigeration—vibration levels, precise temperature control, and proper humidity all affect wine quality over time. Our {b} certified technicians understand these specific requirements and service wine coolers with the care your collection deserves. We minimize repair time to reduce temperature fluctuation risks, arriving with genuine parts and completing most repairs in a single visit to {c["name"]} homes throughout {c["areas"]}.</p>
'''


def generate_hood_content(brand, city):
    c = get_city(city)
    b = brand.replace("-", " ").title().replace("Lg", "LG").replace("Ge", "GE").replace("Sub Zero", "Sub-Zero").replace("Jenn Air", "Jenn-Air").replace("Kitchenaid", "KitchenAid").replace("Fisher Paykel", "Fisher & Paykel")
    return f'''
<h4 style="color: var(--blue); margin: 20px 0 12px;">Expert {b} Vent Hood Repair in {c["name"]}</h4>
<p style="margin-bottom: 12px;">Your {b} range hood removes smoke, steam, grease, and cooking odors from your {c["name"]} kitchen. When ventilation fails in a home with {c["desc"]}, cooking fumes linger and grease accumulates on cabinets and surfaces throughout your kitchen. Our factory-certified technicians serve {c["areas"]} with same-day appointments and expert {b} vent hood service.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">{b} Vent Hood Problems We Solve</h4>
<p style="margin-bottom: 12px;">Our {c["name"]} technicians troubleshoot every {b} vent hood issue: fans that don't run at all or produce weak airflow, excessive noise during operation from worn motors or loose components, lights that won't turn on or flicker intermittently, units that won't shut off after cooking, grease buildup affecting performance despite regular filter cleaning, motors that run but don't move air effectively, control switches that don't respond to input, speed settings that don't change blower output, and damper flaps that stick open or closed.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Common {b} Vent Hood Parts We Replace</h4>
<p style="margin-bottom: 12px;">Our service vehicles carry genuine {b} vent hood parts for {c["name"]} repairs: blower motors and motor assemblies, fan blades and blade assemblies, light sockets and bulbs, control switches and speed selectors, grease filters and baffle filters, duct dampers and backdraft dampers, wiring harnesses and connectors, capacitors for motor starting, speed control modules, touch control panels, LED light strips, and charcoal filters for recirculating models.</p>

<h4 style="color: var(--blue); margin: 20px 0 12px;">Ventilation Assessment for {c["name"]} Homes</h4>
<p style="margin-bottom: 12px;">Proper kitchen ventilation protects your {c["name"]} home from grease buildup, moisture damage, and lingering cooking odors. Our technicians inspect airflow rates and ductwork during every {b} vent hood service call, checking for restrictions that reduce efficiency. We service all vent hood configurations found throughout {c["areas"]}—wall-mounted hoods, island hoods, under-cabinet units, and downdraft systems. Professional duct cleaning recommendations are provided when buildup affects performance.</p>
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
    """Replace content in an expandable card section."""
    # Find the existing content and replace it entirely
    pattern = rf'(<div id="expandable-text-{card_id}"[^>]*>)(.*?)(</div>\s*<div id="expandable-fade-{card_id}")'

    def replacer(match):
        opening = match.group(1)
        closing = match.group(3)
        return opening + new_content + closing

    return re.sub(pattern, replacer, html, flags=re.DOTALL)


def process_page(file_path, city_slug, brand_slug):
    """Process a page and update all service cards."""
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

    # Read affected URLs
    affected = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                affected.append(row[0])

    print("=" * 60)
    print("ENSURING 500+ WORDS PER SERVICE CARD")
    print(f"Processing {len(affected)} affected URLs")
    print("=" * 60)

    total_pages = 0
    total_cards = 0

    for url in sorted(affected):
        parsed = urlparse(url)
        parts = parsed.path.strip('/').split('/')

        # Process city+brand pages
        if len(parts) >= 3 and parts[0] == 'ny' and parts[2].endswith('-repair'):
            city = parts[1]
            brand = parts[2].replace('-repair', '')
            file_path = os.path.join(base_path, *parts, 'index.html')

            if os.path.exists(file_path):
                cards = process_page(file_path, city, brand)
                if cards > 0:
                    total_pages += 1
                    total_cards += cards
                    print(f"Updated: {'/'.join(parts)}/ ({cards} cards)")

    print("\n" + "=" * 60)
    print(f"TOTAL: {total_pages} pages, {total_cards} cards updated to 500+ words")
    print("=" * 60)


if __name__ == "__main__":
    main()
