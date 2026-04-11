#!/usr/bin/env python3
"""
Enhance unique content in show-more card sections to fix "Crawled - currently not indexed" issue.
Adds city-specific, brand-specific, and appliance-specific unique content.
"""

import os
import re
import random
from pathlib import Path

# City-specific data for Westchester County
CITIES = {
    "ardsley": {
        "name": "Ardsley",
        "population": "4,800",
        "zip_codes": ["10502"],
        "neighborhoods": ["Ardsley Park", "Ashford Avenue area", "Heatherdell"],
        "notable": "Known as 'The Village Beautiful' with its tree-lined streets and historic homes built in the early 1900s",
        "housing": "mix of Tudor-style homes, colonials, and modern residences"
    },
    "bronxville": {
        "name": "Bronxville",
        "population": "6,500",
        "zip_codes": ["10708"],
        "neighborhoods": ["Bronxville Village", "Lawrence Park", "Armour Villa Park"],
        "notable": "One of the most affluent villages in the U.S., featuring distinctive Tudor and Colonial Revival architecture",
        "housing": "prestigious estates, luxury condos, and historic Tudor homes"
    },
    "dobbs-ferry": {
        "name": "Dobbs Ferry",
        "population": "11,000",
        "zip_codes": ["10522"],
        "neighborhoods": ["Downtown", "Heights", "South Dobbs Ferry", "Wickers Creek"],
        "notable": "Charming Hudson River village with scenic waterfront and historic Main Street",
        "housing": "Victorian homes, riverfront properties, and modern condominiums"
    },
    "eastchester": {
        "name": "Eastchester",
        "population": "19,500",
        "zip_codes": ["10709", "10707"],
        "neighborhoods": ["Chester Heights", "Lake Isle", "Garth Road area", "Waverly"],
        "notable": "One of the oldest towns in Westchester, dating back to 1664",
        "housing": "single-family homes, townhouses, and garden apartments"
    },
    "elmsford": {
        "name": "Elmsford",
        "population": "5,000",
        "zip_codes": ["10523"],
        "neighborhoods": ["Downtown Elmsford", "Knollwood", "Elmsford Industrial Park area"],
        "notable": "Strategic location at the intersection of major highways with easy access to NYC",
        "housing": "affordable single-family homes, apartments, and townhomes"
    },
    "fairview": {
        "name": "Fairview",
        "population": "3,700",
        "zip_codes": ["10603"],
        "neighborhoods": ["Fairview", "Greenburgh area"],
        "notable": "Small hamlet known for its diverse community and convenient location",
        "housing": "modest single-family homes and multi-family residences"
    },
    "harrison": {
        "name": "Harrison",
        "population": "28,000",
        "zip_codes": ["10528", "10577"],
        "neighborhoods": ["Purchase", "West Harrison", "Sterling Ridge", "Silver Lake"],
        "notable": "Home to corporate headquarters and the prestigious Purchase area",
        "housing": "luxury estates, executive homes, and upscale condos"
    },
    "hartsdale": {
        "name": "Hartsdale",
        "population": "5,300",
        "zip_codes": ["10530"],
        "neighborhoods": ["East Hartsdale", "West Hartsdale", "Hartsdale Four Corners"],
        "notable": "Vibrant commercial district with diverse dining and shopping options",
        "housing": "split-levels, colonials, and apartment complexes"
    },
    "hastings-on-hudson": {
        "name": "Hastings-on-Hudson",
        "population": "8,000",
        "zip_codes": ["10706"],
        "neighborhoods": ["Downtown", "The Dale", "Hillside Woods", "Riverview Manor"],
        "notable": "Artistic community with stunning Hudson River views and historic architecture",
        "housing": "Victorian estates, artists' cottages, and modern eco-homes"
    },
    "irvington": {
        "name": "Irvington",
        "population": "6,500",
        "zip_codes": ["10533"],
        "neighborhoods": ["Downtown", "Matthiessen Park", "Ardsley-on-Hudson", "Half Moon Bay"],
        "notable": "Historic village home to Sunnyside, Washington Irving's estate",
        "housing": "historic mansions, stone cottages, and riverfront properties"
    },
    "larchmont": {
        "name": "Larchmont",
        "population": "6,200",
        "zip_codes": ["10538"],
        "neighborhoods": ["Larchmont Manor", "Murray Hill", "Orienta Point", "Premium Mill"],
        "notable": "Exclusive waterfront community with yacht club and beautiful Long Island Sound views",
        "housing": "luxury waterfront estates, Tudor homes, and Victorian mansions"
    },
    "mamaroneck": {
        "name": "Mamaroneck",
        "population": "19,000",
        "zip_codes": ["10543"],
        "neighborhoods": ["Harbor Heights", "Orienta", "Washingtonville", "Rye Neck"],
        "notable": "Vibrant harbor community with active boating culture and diverse dining scene",
        "housing": "waterfront properties, colonials, and beach cottages"
    },
    "mount-vernon": {
        "name": "Mount Vernon",
        "population": "73,000",
        "zip_codes": ["10550", "10551", "10552", "10553"],
        "neighborhoods": ["Fleetwood", "Chester Heights", "South Side", "Hutchinson"],
        "notable": "Westchester's most populous city with rich cultural heritage and diverse neighborhoods",
        "housing": "multi-family homes, apartments, and historic single-family residences"
    },
    "new-rochelle": {
        "name": "New Rochelle",
        "population": "80,000",
        "zip_codes": ["10801", "10802", "10804", "10805"],
        "neighborhoods": ["Wykagyl", "Beechmont", "Huguenot Park", "Premium Point", "North End"],
        "notable": "Major city with waterfront development, diverse communities, and proximity to NYC",
        "housing": "high-rise condos, colonials, Victorians, and beach cottages"
    },
    "pelham-manor": {
        "name": "Pelham Manor",
        "population": "5,500",
        "zip_codes": ["10803"],
        "neighborhoods": ["Pelham Manor", "North Pelham", "Shore Road area"],
        "notable": "Prestigious village known for excellent schools and stately homes",
        "housing": "Tudor estates, colonials, and grand Victorian homes"
    },
    "rye": {
        "name": "Rye",
        "population": "16,000",
        "zip_codes": ["10580"],
        "neighborhoods": ["Milton Point", "Rye Beach", "Park Avenue", "Grace Church"],
        "notable": "Affluent waterfront city with Playland amusement park and exclusive beach club",
        "housing": "waterfront estates, historic mansions, and luxury condos"
    },
    "scarsdale": {
        "name": "Scarsdale",
        "population": "18,000",
        "zip_codes": ["10583"],
        "neighborhoods": ["Fox Meadow", "Greenacres", "Heathcote", "Edgewood", "Quaker Ridge"],
        "notable": "One of America's wealthiest communities with top-ranked schools and country club lifestyle",
        "housing": "grand estates, Tudor mansions, and architect-designed modern homes"
    },
    "tarrytown": {
        "name": "Tarrytown",
        "population": "11,500",
        "zip_codes": ["10591"],
        "neighborhoods": ["Downtown", "Sleepy Hollow Manor", "Wilson Park", "Tarryhill"],
        "notable": "Historic village of Washington Irving's 'Legend of Sleepy Hollow' with charming riverfront",
        "housing": "Victorian homes, riverfront condos, and historic brownstones"
    },
    "valhalla": {
        "name": "Valhalla",
        "population": "3,500",
        "zip_codes": ["10595"],
        "neighborhoods": ["Valhalla", "Kensico", "Grasslands"],
        "notable": "Home to Westchester Medical Center and the Kensico Dam",
        "housing": "affordable single-family homes and condominiums"
    },
    "village-of-pelham": {
        "name": "Village of Pelham",
        "population": "7,000",
        "zip_codes": ["10803"],
        "neighborhoods": ["Pelham Heights", "Chester Park", "Highbrook Gardens"],
        "notable": "Charming commuter village with active downtown and historic district",
        "housing": "Victorians, colonials, and brick townhouses"
    },
    "white-plains": {
        "name": "White Plains",
        "population": "58,000",
        "zip_codes": ["10601", "10603", "10604", "10605", "10606", "10607"],
        "neighborhoods": ["Battle Hill", "Fisher Hill", "Gedney Farms", "Highlands", "North White Plains"],
        "notable": "Westchester's commercial hub with major shopping, corporate offices, and cultural venues",
        "housing": "luxury high-rises, historic homes, and modern condos"
    },
    "yonkers": {
        "name": "Yonkers",
        "population": "200,000",
        "zip_codes": ["10701", "10702", "10703", "10704", "10705", "10706", "10707", "10708", "10710"],
        "neighborhoods": ["Crestwood", "Park Hill", "Ludlow", "Nepperhan", "Getty Square", "Greystone"],
        "notable": "Fourth largest city in New York State with diverse neighborhoods and Hudson River waterfront",
        "housing": "high-rises, Victorian homes, colonials, and multi-family residences"
    }
}

# Brand-specific model information
BRAND_MODELS = {
    "samsung": {
        "refrigerator": ["Family Hub", "Bespoke", "French Door", "Side-by-Side", "4-Door Flex"],
        "washer": ["FlexWash", "Smart Dial", "Bespoke AI", "Top Load", "Front Load"],
        "dryer": ["FlexDry", "Smart Dial", "Super Speed", "Steam Sanitize+"],
        "dishwasher": ["Linear Wash", "StormWash", "AutoRelease Door", "Waterfall"],
        "oven": ["Slide-In", "Double Wall", "Flex Duo", "Smart Dial"],
        "cooktop": ["Induction", "Gas", "Electric", "Smart Cooktop"],
        "microwave": ["Over-the-Range", "Countertop", "Built-In", "PowerGrill"],
        "common_issues": "ice maker failures, water filter issues, touchscreen problems, cooling inconsistencies"
    },
    "lg": {
        "refrigerator": ["InstaView", "Craft Ice", "Door-in-Door", "French Door", "Counter-Depth"],
        "washer": ["TurboWash 360", "ThinQ", "TWINWash", "WashTower"],
        "dryer": ["TurboSteam", "Sensor Dry", "ThinQ", "WashTower"],
        "dishwasher": ["QuadWash", "TrueSteam", "ThinQ", "EasyRack Plus"],
        "oven": ["ProBake", "Double Oven", "InstaView", "Smart Oven"],
        "cooktop": ["UltraHeat", "Induction", "Gas", "Electric"],
        "microwave": ["NeoChef", "Over-the-Range", "Smart Inverter"],
        "common_issues": "compressor failures, ice maker problems, ThinQ connectivity, linear compressor noise"
    },
    "whirlpool": {
        "refrigerator": ["French Door", "Side-by-Side", "Top Freezer", "Counter-Depth"],
        "washer": ["Load & Go", "Smart Appliance", "2-in-1", "Front Load"],
        "dryer": ["Steam", "Smart Appliance", "Intuitive Touch", "Wrinkle Shield"],
        "dishwasher": ["3rd Rack", "FingerPrint Resistant", "Sensor Cycle", "Quiet"],
        "oven": ["Smart", "Double Oven", "Convection", "Scan-to-Cook"],
        "cooktop": ["Gas", "Electric", "Induction"],
        "microwave": ["Low Profile", "Over-the-Range", "Convection"],
        "common_issues": "drain pump failures, control board issues, door latch problems, timer malfunctions"
    },
    "ge": {
        "refrigerator": ["Profile", "Cafe", "French Door", "Side-by-Side", "Top Freezer"],
        "washer": ["UltraFresh", "Smart", "Space-Saving", "Top Load"],
        "dryer": ["UltraFresh", "Smart", "Space-Saving", "Sanitize Cycle"],
        "dishwasher": ["Profile", "Dry Boost", "Bottle Jets", "UltraFresh"],
        "oven": ["Profile", "Cafe", "Smart", "Air Fry"],
        "cooktop": ["Profile", "Cafe", "Gas", "Induction"],
        "microwave": ["Profile", "Over-the-Range", "Smart", "Advantium"],
        "common_issues": "motherboard failures, ice dispenser jams, heating element issues, control panel problems"
    },
    "bosch": {
        "refrigerator": ["Counter-Depth", "French Door", "Bottom Freezer"],
        "washer": ["Compact", "500 Series", "800 Series", "Home Connect"],
        "dryer": ["Compact", "Ventless", "Heat Pump", "Home Connect"],
        "dishwasher": ["100 Series", "300 Series", "500 Series", "800 Series", "Benchmark"],
        "oven": ["Wall Oven", "Speed Oven", "Steam Oven"],
        "cooktop": ["Induction", "Gas", "Electric"],
        "microwave": ["Built-In", "Speed Microwave"],
        "common_issues": "circulation pump issues, door seal problems, heating element failures, E-codes"
    },
    "miele": {
        "refrigerator": ["MasterCool", "Built-In", "Integrated"],
        "washer": ["W1", "TwinDos", "CapDos", "PowerWash"],
        "dryer": ["T1", "Heat Pump", "SteamFinish", "FragranceDos"],
        "dishwasher": ["G7000", "AutoDos", "Knock2Open", "3D MultiFlex"],
        "oven": ["Generation 7000", "Steam", "Combi-Steam", "Speed Oven"],
        "cooktop": ["Induction", "Gas", "TempControl"],
        "microwave": ["Built-In", "Speed Oven"],
        "vacuum": ["Complete C3", "Blizzard CX1", "Triflex HX1"],
        "coffee": ["CM7", "CVA7", "Built-In"],
        "common_issues": "drainage problems, dispenser issues, heating system faults, electronic control failures"
    },
    "thermador": {
        "refrigerator": ["Freedom Collection", "Built-In", "Column", "French Door"],
        "oven": ["Masterpiece", "Professional", "Steam", "Speed"],
        "cooktop": ["Star Burner", "Induction", "Freedom Induction"],
        "dishwasher": ["Star-?"," Sapphire", "Emerald", "Topaz"],
        "microwave": ["Drawer", "Built-In"],
        "common_issues": "igniter failures, star burner issues, control board problems, convection fan noise"
    },
    "sub-zero": {
        "refrigerator": ["Built-In", "Integrated", "PRO", "Designer", "Classic"],
        "freezer": ["Built-In", "Drawer", "Column"],
        "wine_cooler": ["Integrated", "Undercounter", "Built-In"],
        "common_issues": "dual refrigeration system issues, vacuum seal problems, ice maker failures, compressor noise"
    },
    "wolf": {
        "oven": ["M Series", "E Series", "Convection Steam", "Speed Oven"],
        "cooktop": ["Gas", "Induction", "Electric"],
        "range": ["Dual Fuel", "Gas", "Induction"],
        "microwave": ["Drawer", "Convection", "Standard"],
        "common_issues": "igniter problems, convection fan issues, control knob malfunctions, dual-stacked burner cleaning"
    },
    "viking": {
        "refrigerator": ["Professional", "3 Series", "5 Series", "Built-In"],
        "oven": ["Professional", "3 Series", "5 Series", "French Door"],
        "cooktop": ["Professional", "Gas", "Induction", "Electric"],
        "range": ["Professional", "3 Series", "5 Series"],
        "dishwasher": ["Professional", "3 Series"],
        "common_issues": "sealed burner issues, door alignment, igniter failures, control panel malfunctions"
    },
    "gaggenau": {
        "refrigerator": ["Vario", "Integrated", "Wine Climate"],
        "oven": ["EB", "BS", "BOP", "Combi-Steam"],
        "cooktop": ["Vario", "Full Surface Induction", "Flex Induction"],
        "dishwasher": ["400 Series", "200 Series"],
        "common_issues": "touch control issues, hinge problems, steam system faults, precision temperature calibration"
    },
    "dacor": {
        "refrigerator": ["Modernist", "Professional", "Heritage"],
        "oven": ["Modernist", "Professional", "Steam"],
        "cooktop": ["Modernist", "Professional", "Discovery"],
        "range": ["Modernist", "Professional", "Heritage"],
        "dishwasher": ["Modernist", "Heritage"],
        "microwave": ["Microwave-in-a-Drawer", "Over-the-Range"],
        "common_issues": "Wi-Fi connectivity, LCD display issues, convection system problems, sealed burner ignition"
    },
    "kitchenaid": {
        "refrigerator": ["Built-In", "Counter-Depth", "French Door", "Side-by-Side"],
        "washer": ["Front Load", "Top Load", "Smart"],
        "dryer": ["Front Load", "Smart", "Steam"],
        "dishwasher": ["FreeFlex", "Third Level", "ProWash"],
        "oven": ["Even-Heat", "True Convection", "Smart Oven+"],
        "cooktop": ["Gas", "Electric", "Induction"],
        "microwave": ["Over-the-Range", "Built-In", "Countertop"],
        "common_issues": "ice maker problems, drain issues, control board failures, door seal wear"
    },
    "jenn-air": {
        "refrigerator": ["DERA", "Rise", "Noir"],
        "oven": ["Rise", "Noir", "Connected Wall Oven"],
        "cooktop": ["Rise", "Noir", "Downdraft"],
        "range": ["Rise", "Noir", "Dual Fuel"],
        "dishwasher": ["Rise", "Noir", "TriFecta"],
        "common_issues": "downdraft motor issues, induction problems, touch control malfunctions, WiFi connectivity"
    },
    "electrolux": {
        "refrigerator": ["French Door", "Side-by-Side", "Counter-Depth"],
        "washer": ["Perfect Steam", "SmartBoost", "LuxCare"],
        "dryer": ["Perfect Steam", "Predictive Dry", "Instant Refresh"],
        "dishwasher": ["IQ-Touch", "ComfortLift", "45-Minute Wash"],
        "oven": ["Single Wall", "Double Wall", "Combination"],
        "cooktop": ["Gas", "Electric", "Induction"],
        "microwave": ["Over-the-Range", "Built-In"],
        "common_issues": "steam generator issues, SmartBoost problems, drain pump failures, door latch issues"
    },
    "maytag": {
        "refrigerator": ["French Door", "Side-by-Side", "Top Freezer"],
        "washer": ["Commercial Technology", "PowerWash", "Extra Power"],
        "dryer": ["Commercial Technology", "Extra Power", "Steam"],
        "dishwasher": ["Third Level", "PowerDry", "Dual Power Filtration"],
        "oven": ["True Convection", "AquaLift Self-Clean"],
        "cooktop": ["Gas", "Electric"],
        "microwave": ["Over-the-Range", "Countertop"],
        "common_issues": "commercial-grade motor issues, agitator problems, heating element failures, timer malfunctions"
    },
    "frigidaire": {
        "refrigerator": ["Gallery", "Professional", "French Door", "Side-by-Side"],
        "washer": ["Affinity", "Front Load", "Top Load"],
        "dryer": ["Affinity", "Front Load", "Gas", "Electric"],
        "dishwasher": ["Gallery", "BladeSpray", "OrbitClean"],
        "oven": ["Gallery", "Professional", "Convection"],
        "cooktop": ["Gallery", "Professional", "Gas", "Electric"],
        "microwave": ["Gallery", "Professional", "Over-the-Range"],
        "common_issues": "defrost system failures, ice maker issues, door seal problems, heating element wear"
    },
    "kenmore": {
        "refrigerator": ["Elite", "French Door", "Side-by-Side", "Top Freezer"],
        "washer": ["Elite", "Front Load", "Top Load"],
        "dryer": ["Elite", "Front Load", "Electric", "Gas"],
        "dishwasher": ["Elite", "Ultra Wash"],
        "oven": ["Elite", "Pro", "Convection"],
        "cooktop": ["Elite", "Gas", "Electric"],
        "microwave": ["Elite", "Over-the-Range", "Countertop"],
        "common_issues": "control board failures, motor issues, thermostat problems, electronic control malfunctions"
    },
    "amana": {
        "refrigerator": ["Top Freezer", "Side-by-Side", "Bottom Freezer"],
        "washer": ["Top Load", "High-Efficiency"],
        "dryer": ["Electric", "Gas", "High-Efficiency"],
        "dishwasher": ["Built-In", "Triple Filter"],
        "oven": ["Gas", "Electric", "Self-Cleaning"],
        "cooktop": ["Gas", "Electric"],
        "microwave": ["Over-the-Range", "Countertop"],
        "common_issues": "thermostat issues, defrost timer problems, drain pump failures, igniter malfunctions"
    },
    "fisher-paykel": {
        "refrigerator": ["ActiveSmart", "French Door", "Column", "Integrated"],
        "washer": ["SmartDrive", "Front Load", "WashSmart"],
        "dryer": ["Heat Pump", "Vented", "Condensing"],
        "dishwasher": ["DishDrawer", "Built-In"],
        "oven": ["Companion", "Minimal", "Contemporary", "Professional"],
        "cooktop": ["Gas", "Induction"],
        "common_issues": "DishDrawer motor issues, SmartDrive problems, ActiveSmart cooling faults, control panel failures"
    }
}

# Appliance-specific repair details with variations
APPLIANCE_DETAILS = {
    "washer": {
        "parts": ["drum bearings", "door boot seal", "drain pump", "motor coupling", "lid switch", "water inlet valve", "transmission", "clutch assembly", "shock absorbers", "suspension rods"],
        "symptoms": ["won't spin", "leaking water", "excessive vibration", "won't drain", "error codes", "loud noises", "won't start", "overflows", "clothes still wet", "burning smell"],
        "services": ["bearing replacement", "seal repair", "pump service", "motor diagnosis", "belt replacement", "valve repair", "balance adjustment", "control board repair"]
    },
    "dryer": {
        "parts": ["heating element", "thermal fuse", "drum rollers", "belt", "igniter", "gas valve coils", "motor", "blower wheel", "thermistor", "door switch"],
        "symptoms": ["not heating", "takes too long", "squeaking", "tumbling issues", "shuts off", "burning smell", "won't start", "noisy operation", "overheating", "drum not turning"],
        "services": ["element replacement", "fuse repair", "roller service", "belt replacement", "igniter repair", "vent cleaning", "motor service", "thermostat calibration"]
    },
    "refrigerator": {
        "parts": ["compressor", "evaporator fan", "condenser coils", "defrost heater", "thermostat", "start relay", "door gasket", "ice maker", "water filter", "control board"],
        "symptoms": ["not cooling", "frost buildup", "water leaking", "noisy operation", "ice maker issues", "warm freezer", "running constantly", "not running", "food freezing in fridge", "water dispenser problems"],
        "services": ["compressor service", "fan motor repair", "coil cleaning", "defrost system repair", "thermostat replacement", "gasket replacement", "ice maker repair", "water line service"]
    },
    "dishwasher": {
        "parts": ["circulation pump", "drain pump", "door latch", "spray arms", "float switch", "inlet valve", "heating element", "control board", "rack rollers", "door gasket"],
        "symptoms": ["not draining", "dishes dirty", "leaking", "won't start", "noisy", "door won't close", "not filling", "not drying", "error codes", "detergent not dispensing"],
        "services": ["pump repair", "spray arm cleaning", "valve replacement", "element service", "latch repair", "filter cleaning", "rack repair", "control diagnosis"]
    },
    "oven": {
        "parts": ["bake element", "broil element", "igniter", "thermostat", "control board", "door hinge", "door gasket", "convection fan", "temperature sensor", "safety valve"],
        "symptoms": ["not heating", "uneven cooking", "won't turn on", "self-clean issues", "door won't close", "temperature wrong", "error codes", "sparking", "smoke", "gas smell"],
        "services": ["element replacement", "igniter service", "thermostat calibration", "door repair", "fan motor service", "control board repair", "valve replacement", "sensor calibration"]
    },
    "cooktop": {
        "parts": ["burner caps", "igniters", "spark module", "gas valves", "heating elements", "infinite switch", "glass surface", "induction coils", "control knobs", "wiring"],
        "symptoms": ["won't ignite", "weak flame", "clicking", "not heating", "uneven heat", "cracked glass", "error codes", "hot spots", "element not working", "control issues"],
        "services": ["igniter replacement", "burner service", "valve repair", "element replacement", "switch service", "glass repair", "coil diagnosis", "wiring repair"]
    },
    "microwave": {
        "parts": ["magnetron", "high voltage capacitor", "diode", "door switch", "turntable motor", "control board", "waveguide cover", "fuse", "door latch", "touchpad"],
        "symptoms": ["not heating", "sparking", "turntable stopped", "door issues", "display problems", "buttons not working", "light out", "loud noise", "shuts off", "runs but no heat"],
        "services": ["magnetron repair", "capacitor service", "switch replacement", "motor repair", "control service", "fuse replacement", "door repair", "touchpad replacement"]
    },
    "vent-hood": {
        "parts": ["blower motor", "fan blade", "light socket", "control switch", "filters", "duct damper", "wiring", "capacitor", "speed control", "grease trap"],
        "symptoms": ["not running", "weak suction", "loud noise", "lights out", "won't turn off", "grease dripping", "vibrating", "burning smell", "speed issues", "damper stuck"],
        "services": ["motor replacement", "filter cleaning", "light repair", "switch service", "damper repair", "wiring service", "blade balancing", "duct cleaning"]
    },
    "wine-cooler": {
        "parts": ["compressor", "thermostat", "evaporator fan", "condenser", "door gasket", "shelving", "LED lights", "control board", "vibration dampeners", "humidity control"],
        "symptoms": ["not cooling", "too cold", "vibrating", "noisy", "frost buildup", "humidity issues", "lights out", "temperature fluctuating", "door seal issues", "compressor running constantly"],
        "services": ["compressor service", "thermostat calibration", "fan repair", "gasket replacement", "vibration adjustment", "humidity control service", "control diagnosis", "coil cleaning"]
    }
}


def get_city_data(city_slug):
    """Get city-specific data."""
    if city_slug in CITIES:
        return CITIES[city_slug]
    name = city_slug.replace("-", " ").title()
    return {
        "name": name,
        "population": "varies",
        "zip_codes": [],
        "neighborhoods": [],
        "notable": f"charming Westchester County community",
        "housing": "various home styles"
    }


def get_brand_models(brand_slug, appliance_type):
    """Get brand-specific model information."""
    brand_key = brand_slug.lower()
    appliance_key = appliance_type.replace("-repair", "").replace("-", "_")

    if brand_key in BRAND_MODELS:
        brand_data = BRAND_MODELS[brand_key]
        models = brand_data.get(appliance_key, brand_data.get("refrigerator", ["various models"]))
        common_issues = brand_data.get("common_issues", "various technical issues")
        return models, common_issues
    return ["various models"], "technical issues"


def get_appliance_details(appliance_slug):
    """Get appliance-specific repair details."""
    key = appliance_slug.replace("-repair", "")
    if key in APPLIANCE_DETAILS:
        return APPLIANCE_DETAILS[key]
    return APPLIANCE_DETAILS.get("washer")  # fallback


def generate_unique_city_brand_content(city_slug, brand_slug):
    """Generate unique content for city + brand pages."""
    city = get_city_data(city_slug)
    brand_name = brand_slug.replace("-", " ").title()

    # Get random subset of neighborhoods
    neighborhoods = city.get("neighborhoods", [])
    if len(neighborhoods) > 2:
        selected_neighborhoods = random.sample(neighborhoods, min(3, len(neighborhoods)))
    else:
        selected_neighborhoods = neighborhoods

    neighborhoods_text = ", ".join(selected_neighborhoods) if selected_neighborhoods else city["name"]
    zip_text = ", ".join(city.get("zip_codes", [])) if city.get("zip_codes") else ""

    content = f'''
<div style="margin-top: 25px; padding: 20px; background: rgba(0,48,135,0.03); border-radius: 10px;">
<h4 style="font-size: 18px; color: var(--blue); margin: 0 0 12px 0;">About {city["name"]}</h4>
<p style="line-height: 1.7; color: #444; font-size: 14px; margin: 0;">
{city["name"]} (population {city["population"]}) is {city["notable"]}. The area features {city["housing"]}. We provide {brand_name} repair service throughout {city["name"]}, including {neighborhoods_text}.{" Serving zip codes: " + zip_text + "." if zip_text else ""}
</p>
</div>

<div style="margin-top: 20px; padding: 20px; background: rgba(228,30,38,0.03); border-radius: 10px;">
<h4 style="font-size: 18px; color: var(--blue); margin: 0 0 12px 0;">{brand_name} Service Specialization</h4>
<p style="line-height: 1.7; color: #444; font-size: 14px; margin: 0;">
Our {city["name"]} technicians are factory-trained on {brand_name} refrigerators, washers, dryers, dishwashers, ovens, and cooktops. We stock genuine {brand_name} parts on our service vehicles for faster first-visit repairs. Most {brand_name} repairs in {city["name"]} are completed the same day.
</p>
</div>
'''
    return content


def generate_unique_brand_appliance_content(brand_slug, appliance_slug):
    """Generate unique content for brand + appliance pages."""
    brand_name = brand_slug.replace("-", " ").title()
    appliance_name = appliance_slug.replace("-repair", "").replace("-", " ").title()

    models, common_issues = get_brand_models(brand_slug, appliance_slug)
    details = get_appliance_details(appliance_slug)

    # Select random parts and symptoms for variety
    selected_parts = random.sample(details["parts"], min(4, len(details["parts"])))
    selected_symptoms = random.sample(details["symptoms"], min(4, len(details["symptoms"])))

    models_text = ", ".join(models[:5]) if models else "all models"
    parts_text = ", ".join(selected_parts)
    symptoms_text = ", ".join(selected_symptoms)

    content = f'''
<div style="margin-top: 25px; padding: 20px; background: rgba(0,48,135,0.03); border-radius: 10px;">
<h4 style="font-size: 18px; color: var(--blue); margin: 0 0 12px 0;">{brand_name} {appliance_name} Models We Service</h4>
<p style="line-height: 1.7; color: #444; font-size: 14px; margin: 0;">
We repair all {brand_name} {appliance_name.lower()} models including {models_text}. Common {brand_name} issues we fix include {common_issues}.
</p>
</div>

<div style="margin-top: 20px; padding: 20px; background: rgba(228,30,38,0.03); border-radius: 10px;">
<h4 style="font-size: 18px; color: var(--blue); margin: 0 0 12px 0;">Repair Parts & Symptoms</h4>
<p style="line-height: 1.7; color: #444; font-size: 14px; margin: 0;">
<strong>Parts we commonly replace:</strong> {parts_text}.<br>
<strong>Symptoms we diagnose:</strong> {symptoms_text}.<br>
Our technicians carry {brand_name}-specific parts for same-day repairs throughout Westchester County.
</p>
</div>
'''
    return content


def inject_content_into_expandable(html, content, section_id="1"):
    """Inject unique content into an expandable section."""
    # Find the expandable section and add content before the closing div
    pattern = rf'(<div id="expandable-text-{section_id}"[^>]*>)(.*?)(</div>\s*<div id="expandable-fade-{section_id}")'

    def replacer(match):
        opening = match.group(1)
        existing = match.group(2)
        closing = match.group(3)

        # Check if content already added
        if "About " in existing and "population" in existing:
            return match.group(0)
        if "Models We Service" in existing:
            return match.group(0)

        return opening + existing + content + closing

    return re.sub(pattern, replacer, html, flags=re.DOTALL)


def process_city_brand_pages(base_path):
    """Process all city + brand pages."""
    ny_path = os.path.join(base_path, 'ny')
    count = 0

    for city_dir in os.listdir(ny_path):
        city_path = os.path.join(ny_path, city_dir)
        if not os.path.isdir(city_path) or city_dir.startswith('.'):
            continue

        for item in os.listdir(city_path):
            if not item.endswith('-repair'):
                continue

            item_path = os.path.join(city_path, item)
            index_file = os.path.join(item_path, 'index.html')

            if os.path.exists(index_file):
                brand_slug = item.replace('-repair', '')

                with open(index_file, 'r', encoding='utf-8') as f:
                    html = f.read()

                # Generate unique content
                content = generate_unique_city_brand_content(city_dir, brand_slug)

                # Inject into expandable section
                new_html = inject_content_into_expandable(html, content, "1")

                if new_html != html:
                    with open(index_file, 'w', encoding='utf-8') as f:
                        f.write(new_html)
                    count += 1
                    print(f"Updated: ny/{city_dir}/{item}/")

    return count


def process_brand_appliance_pages(base_path):
    """Process all brand + appliance pages."""
    brands_path = os.path.join(base_path, 'brands')
    count = 0

    for brand_dir in os.listdir(brands_path):
        brand_path = os.path.join(brands_path, brand_dir)
        if not os.path.isdir(brand_path) or brand_dir.startswith('.'):
            continue

        for item in os.listdir(brand_path):
            if not item.endswith('-repair'):
                continue

            item_path = os.path.join(brand_path, item)
            index_file = os.path.join(item_path, 'index.html')

            if os.path.exists(index_file):
                with open(index_file, 'r', encoding='utf-8') as f:
                    html = f.read()

                # Generate unique content
                content = generate_unique_brand_appliance_content(brand_dir, item)

                # Inject into expandable section
                new_html = inject_content_into_expandable(html, content, "1")

                if new_html != html:
                    with open(index_file, 'w', encoding='utf-8') as f:
                        f.write(new_html)
                    count += 1
                    print(f"Updated: brands/{brand_dir}/{item}/")

    return count


if __name__ == "__main__":
    base_path = "/Users/globalaffiliate/westchester-county-repair"

    print("=" * 60)
    print("ENHANCING UNIQUE CONTENT FOR INDEXED PAGES")
    print("=" * 60)

    print("\n[1/2] Processing city + brand pages...")
    city_count = process_city_brand_pages(base_path)
    print(f"Updated {city_count} city + brand pages")

    print("\n[2/2] Processing brand + appliance pages...")
    brand_count = process_brand_appliance_pages(base_path)
    print(f"Updated {brand_count} brand + appliance pages")

    print("\n" + "=" * 60)
    print(f"TOTAL: {city_count + brand_count} pages enhanced with unique content")
    print("=" * 60)
