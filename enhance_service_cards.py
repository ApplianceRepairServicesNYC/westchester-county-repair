#!/usr/bin/env python3
"""
Enhance service card show-more sections with unique brand + city + appliance content.
"""

import os
import re
import random

# City data
CITIES = {
    "ardsley": {"name": "Ardsley", "pop": "4,800", "type": "village", "features": "tree-lined streets and Tudor homes"},
    "bronxville": {"name": "Bronxville", "pop": "6,500", "type": "village", "features": "Tudor estates and luxury condos"},
    "dobbs-ferry": {"name": "Dobbs Ferry", "pop": "11,000", "type": "village", "features": "Hudson River waterfront homes"},
    "eastchester": {"name": "Eastchester", "pop": "19,500", "type": "town", "features": "historic colonials and townhouses"},
    "elmsford": {"name": "Elmsford", "pop": "5,000", "type": "village", "features": "convenient highway access homes"},
    "fairview": {"name": "Fairview", "pop": "3,700", "type": "hamlet", "features": "diverse residential community"},
    "harrison": {"name": "Harrison", "pop": "28,000", "type": "town", "features": "luxury estates in Purchase area"},
    "hartsdale": {"name": "Hartsdale", "pop": "5,300", "type": "hamlet", "features": "split-levels and garden apartments"},
    "hastings-on-hudson": {"name": "Hastings-on-Hudson", "pop": "8,000", "type": "village", "features": "Victorian homes with river views"},
    "irvington": {"name": "Irvington", "pop": "6,500", "type": "village", "features": "historic mansions and stone cottages"},
    "larchmont": {"name": "Larchmont", "pop": "6,200", "type": "village", "features": "waterfront estates on Long Island Sound"},
    "mamaroneck": {"name": "Mamaroneck", "pop": "19,000", "type": "village", "features": "harbor community with beach cottages"},
    "mount-vernon": {"name": "Mount Vernon", "pop": "73,000", "type": "city", "features": "diverse multi-family homes"},
    "new-rochelle": {"name": "New Rochelle", "pop": "80,000", "type": "city", "features": "high-rises and waterfront condos"},
    "pelham-manor": {"name": "Pelham Manor", "pop": "5,500", "type": "village", "features": "stately Tudor and Colonial homes"},
    "rye": {"name": "Rye", "pop": "16,000", "type": "city", "features": "exclusive waterfront estates"},
    "scarsdale": {"name": "Scarsdale", "pop": "18,000", "type": "village", "features": "grand estates and modern luxury homes"},
    "tarrytown": {"name": "Tarrytown", "pop": "11,500", "type": "village", "features": "historic riverfront Victorian homes"},
    "valhalla": {"name": "Valhalla", "pop": "3,500", "type": "hamlet", "features": "affordable single-family homes"},
    "village-of-pelham": {"name": "Village of Pelham", "pop": "7,000", "type": "village", "features": "charming Victorians and colonials"},
    "white-plains": {"name": "White Plains", "pop": "58,000", "type": "city", "features": "luxury high-rises and historic homes"},
    "yonkers": {"name": "Yonkers", "pop": "200,000", "type": "city", "features": "diverse housing from high-rises to Victorians"}
}

# Brand-specific appliance details
BRAND_APPLIANCE_DATA = {
    "samsung": {
        "washer": {"models": "FlexWash, Bespoke AI, Smart Dial, AddWash", "tech": "VRT Plus vibration reduction, AI-powered cycles, Wi-Fi diagnostics", "issues": "door boot seal tears, drain pump clogs, control board failures, spider arm cracks"},
        "dryer": {"models": "FlexDry, Bespoke, Smart Dial, DVE/DVG series", "tech": "Multi-Steam technology, Sensor Dry, Smart Care app", "issues": "heating element burnout, moisture sensor errors, drum belt wear, thermal fuse failures"},
        "refrigerator": {"models": "Family Hub, Bespoke, 4-Door Flex, French Door RF series", "tech": "Twin Cooling Plus, FlexZone drawer, built-in cameras", "issues": "ice maker freezing, water filter leaks, compressor clicks, touchscreen malfunctions"},
        "dishwasher": {"models": "Linear Wash, StormWash, Waterfall, AutoRelease", "tech": "Zone Booster, Digital Leak Sensor, adjustable racks", "issues": "drainage failures, spray arm clogs, door latch problems, detergent dispenser jams"},
        "oven": {"models": "Slide-In NE/NX series, Flex Duo, Smart Dial ranges", "tech": "Dual convection, Air Fry mode, Wi-Fi connectivity", "issues": "igniter failures, uneven heating, control panel errors, convection fan noise"},
        "cooktop": {"models": "Induction NZ series, Gas NA series, Electric NE series", "tech": "Virtual Flame, Flex Zone induction, Wi-Fi control", "issues": "burner ignition problems, induction error codes, cracked glass, element failures"},
        "microwave": {"models": "Over-the-Range ME series, PowerGrill Duo, Smart Sensor", "tech": "Sensor Cook, Slim Fry, grilling element", "issues": "magnetron failures, turntable motor issues, touchpad malfunctions, door switch problems"},
        "wine-cooler": {"models": "Undercounter RW series", "tech": "Dual temperature zones, UV-protected glass", "issues": "compressor noise, temperature fluctuations, door seal deterioration"}
    },
    "lg": {
        "washer": {"models": "WashTower, TurboWash 360, TWINWash, WM series", "tech": "AI DD motor, ThinQ app, Allergiene cycle, Steam technology", "issues": "direct drive motor failures, door boot leaks, LE error codes, unbalanced load sensors"},
        "dryer": {"models": "WashTower, DLGX/DLEX series, Styler", "tech": "Dual Inverter heat pump, TurboSteam, Sensor Dry", "issues": "heating element issues, lint filter housing cracks, drum roller squeaks, moisture sensor drift"},
        "refrigerator": {"models": "InstaView, Craft Ice, Door-in-Door, LRMVS/LRFXS series", "tech": "Linear Compressor, UVnano dispenser, ThinQ diagnostics", "issues": "linear compressor clicks, craft ice maker jams, InstaView panel failures, cooling fan noise"},
        "dishwasher": {"models": "QuadWash, TrueSteam, Studio series, LDF/LDT series", "tech": "Dynamic Dry, EasyRack Plus, Inverter Direct Drive", "issues": "wash arm bearing wear, drain pump blockages, spray arm clogs, rinse aid dispenser leaks"},
        "oven": {"models": "ProBake, InstaView, LSEL/LSGL ranges", "tech": "ProBake Convection, Air Fry, EasyClean", "issues": "convection fan motor failures, bake element burnout, door hinge problems, igniter issues"},
        "cooktop": {"models": "UltraHeat, Studio, CBGJ/CBIH series", "tech": "UltraHeat 22K BTU, SmoothTouch controls", "issues": "igniter clicking, burner cap misalignment, induction coil failures, touch control errors"},
        "microwave": {"models": "NeoChef, Over-the-Range LMV series, Smart Inverter", "tech": "Smart Inverter, EasyClean interior, Sensor Cook", "issues": "inverter board failures, turntable coupling breaks, door interlock issues"}
    },
    "whirlpool": {
        "washer": {"models": "Load & Go, 2-in-1, WTW/WFW series, Smart Appliance", "tech": "Load & Go XL dispenser, Adaptive Wash, Pretreat Station", "issues": "lid lock failures, drain pump clogs, transmission wear, motor coupling breaks"},
        "dryer": {"models": "Smart Appliance, WED/WGD series, Wrinkle Shield", "tech": "Wrinkle Shield Plus, Steam Refresh, Advanced Moisture Sensing", "issues": "thermal fuse blows, drum roller squeaks, heating element failures, belt breaks"},
        "refrigerator": {"models": "French Door WRF/WRX series, Side-by-Side WRS series", "tech": "Accu-Chill temperature management, Infinity Slide shelf", "issues": "ice maker auger jams, evaporator fan failures, defrost timer issues, water inlet valve clogs"},
        "dishwasher": {"models": "3rd Rack WDT/WDF series, PowerBlast cycle", "tech": "Soil Sensor, 1-Hour Wash, Fingerprint Resistant", "issues": "circulation pump failures, door latch mechanism wear, spray arm cracks, control board errors"},
        "oven": {"models": "Smart Slide-In WEE/WEG series, Convection ranges", "tech": "True Convection, Frozen Bake, AquaLift self-clean", "issues": "surface burner igniter failures, oven sensor errors, door hinge spring breaks, control lock malfunctions"},
        "cooktop": {"models": "Gas WCG series, Electric WCE series", "tech": "SpeedHeat burner, FlexHeat element", "issues": "spark module failures, infinite switch problems, element connection burns"},
        "microwave": {"models": "Low Profile WML series, Over-the-Range WMH series", "tech": "Scan-to-Cook, Steam cooking, CleanRelease interior", "issues": "magnetron degradation, fan motor noise, control panel failures"}
    },
    "ge": {
        "washer": {"models": "UltraFresh, Profile PTW/PFW series, Smart GTW/GFW", "tech": "UltraFresh Vent, OdorBlock, Microban technology", "issues": "main control board failures, door boot mold issues, drain pump motor burnout, lid switch problems"},
        "dryer": {"models": "UltraFresh, Profile PTD/PFD series, Smart GTD/GFD", "tech": "Sanitize cycle, Wrinkle Care, WiFi connectivity", "issues": "drum bearing wear, igniter failures in gas models, thermal fuse issues, moisture sensor errors"},
        "refrigerator": {"models": "Profile PFE/PYE series, Cafe CVE/CYE series, GNE/GSS series", "tech": "TwinChill evaporators, Turbo Cool, Hands-free Autofill", "issues": "motherboard failures, ice dispenser jams, water valve leaks, condenser fan motor issues"},
        "dishwasher": {"models": "Profile PDT series, Cafe CDT series, GDF/GDT series", "tech": "Dry Boost, Bottle Jets, Deep Clean Silverware Jets", "issues": "wash motor failures, door gasket leaks, detergent cup malfunctions, control board shorts"},
        "oven": {"models": "Profile PGS/PHS series, Cafe CGS/CHS series, JB/JS ranges", "tech": "True European Convection, Air Fry mode, Precision Cooking", "issues": "bake/broil element burnout, igniter glow bar failures, oven temperature sensor drift, self-clean latch issues"},
        "cooktop": {"models": "Profile PGP series, Cafe CGP series, JP/JGP series", "tech": "Tri-Ring element, Sync-Ring burner, Edge-to-Edge grates", "issues": "surface element connections, gas valve failures, spark igniter issues"},
        "microwave": {"models": "Profile PVM series, Cafe CVM series, JVM/JNM series", "tech": "Sensor cooking, Convection mode, Advantium technology", "issues": "magnetron failures, turntable motor issues, touchpad membrane wear"}
    },
    "bosch": {
        "washer": {"models": "300/500/800 Series WAT/WAW, Compact 24-inch", "tech": "EcoSilence motor, SpeedPerfect, Home Connect", "issues": "door lock assembly failures, drain pump clogs, shock absorber wear, control module errors"},
        "dryer": {"models": "300/500/800 Series WTG/WTW, Heat Pump ventless", "tech": "Heat pump technology, AutoDry sensors, Home Connect", "issues": "heat pump compressor issues, condensate pump failures, drum bearing wear, filter housing cracks"},
        "refrigerator": {"models": "B36/B21 Counter-Depth, 800 Series French Door", "tech": "VitaFresh Pro, MultiAirFlow, Home Connect", "issues": "ice maker inlet valve freezes, fan motor noise, door seal issues, compressor relay failures"},
        "dishwasher": {"models": "100/300/500/800 Series, Benchmark SHX/SHP/SHPM", "tech": "PrecisionWash, CrystalDry, AquaStop leak protection", "issues": "circulation pump failures, E15/E24/E25 error codes, spray arm bearing wear, door latch issues"},
        "oven": {"models": "500/800 Series HBL/HBN, Benchmark HBLP", "tech": "European Convection, Self-clean, Home Connect", "issues": "convection fan motor failures, door hinge spring breaks, temperature sensor drift"},
        "cooktop": {"models": "500/800 Series NGM/NIT, FlexInduction", "tech": "FlexInduction zones, OptiSim burner, PotSense technology", "issues": "induction coil errors, touch control malfunctions, gas igniter failures"},
        "microwave": {"models": "500/800 Series HMB/HMC, Speed Oven", "tech": "Convection microwave, Sensor cooking", "issues": "magnetron failures, fan motor issues, door switch problems"}
    },
    "miele": {
        "washer": {"models": "W1 WWH/WWF/WWE series, TwinDos", "tech": "TwinDos automatic detergent, CapDosing, SteamCare", "issues": "TwinDos dispenser clogs, door hinge adjustments, drain pump blockages, motor carbon brush wear"},
        "dryer": {"models": "T1 TWF/TWI/TWJ series, Heat Pump", "tech": "FragranceDos, SteamFinish, EcoDry technology", "issues": "heat exchanger cleaning required, condenser pump failures, drum bearing noise, lint filter housing"},
        "refrigerator": {"models": "MasterCool KF/K series, Built-In", "tech": "PerfectFresh Pro, DynaCool, BrilliantLight", "issues": "ice maker water valve issues, DynaCool fan failures, door gasket replacement, compressor relay"},
        "dishwasher": {"models": "G 7000 series, AutoDos, Knock2Open", "tech": "AutoDos PowerDisk, 3D MultiFlex tray, AutoOpen drying", "issues": "AutoDos motor failures, circulation pump issues, spray arm bearing wear, drain valve blockages"},
        "oven": {"models": "H 7000 series, Generation 7000, Dialog Oven", "tech": "Moisture Plus, M Touch display, Wireless Roast Probe", "issues": "steam generator descaling, door hinge tension, catalytic liner replacement, temperature calibration"},
        "cooktop": {"models": "KM 7000 series, Induction, Gas, TempControl", "tech": "TempControl sensor, Con@ctivity, PowerFlex zone", "issues": "TempControl sensor calibration, PowerFlex coil errors, gas burner ignition"},
        "vacuum": {"models": "Complete C3, Blizzard CX1, Triflex HX1", "tech": "Vortex technology, HEPA AirClean, 3-in-1 design", "issues": "suction motor wear, brush roller tangles, battery degradation, filter housing cracks"},
        "coffee": {"models": "CM7 series, CVA 7000 Built-In", "tech": "AromaticSystem, CupSensor, OneTouch for Two", "issues": "brew unit cleaning, grinder calibration, milk system blockages, descaling requirements"}
    },
    "thermador": {
        "washer": {"models": "N/A - Thermador focuses on kitchen appliances", "tech": "", "issues": ""},
        "dryer": {"models": "N/A - Thermador focuses on kitchen appliances", "tech": "", "issues": ""},
        "refrigerator": {"models": "Freedom Collection T36/T42, Column T18/T24", "tech": "Freedom Hinge, ThermaFresh system, SuperFreeze", "issues": "compressor relay failures, ice maker valve freezes, door alignment adjustments, evaporator fan noise"},
        "dishwasher": {"models": "Star-Sapphire DWHD/STAR series, Emerald", "tech": "Star Dry system, StarSpeed cycle, Zeolite drying", "issues": "circulation pump failures, Zeolite regeneration, spray arm clogs, door latch mechanism"},
        "oven": {"models": "Masterpiece/Professional POD/PRD series, Steam", "tech": "SoftClose door, True Convection, Steam/Convection combo", "issues": "convection fan motor, steam generator descaling, door hinge tension, self-clean latch"},
        "cooktop": {"models": "Masterpiece/Professional CIT/SGS/PCG series", "tech": "Star Burner, ExtraLow simmer, Freedom Induction", "issues": "Star Burner cap alignment, igniter module failures, induction zone errors, low simmer valve"},
        "microwave": {"models": "Masterpiece MU30/MD24 Drawer, Built-In", "tech": "Sensor cooking, Drawer design, Keep Warm mode", "issues": "drawer track alignment, magnetron failures, touch control calibration"}
    },
    "sub-zero": {
        "washer": {"models": "N/A - Sub-Zero focuses on refrigeration", "tech": "", "issues": ""},
        "dryer": {"models": "N/A - Sub-Zero focuses on refrigeration", "tech": "", "issues": ""},
        "refrigerator": {"models": "BI/IT/CL series, PRO 48, Designer Column", "tech": "Dual compressors, NASA air purification, vacuum seal door", "issues": "dual compressor cycling, vacuum seal gasket wear, ice maker water valve, condenser coil cleaning"},
        "dishwasher": {"models": "Cove DW2450 series", "tech": "PowerScrub jets, Water Softener system, Dry mode plus", "issues": "circulation motor issues, water softener regeneration, spray arm bearing, drain valve"},
        "wine-cooler": {"models": "UW/IW/BW series, Designer/PRO", "tech": "Dual evaporators, UV-resistant glass, vibration dampening", "issues": "evaporator fan failures, temperature zone calibration, door gasket seal, humidity control"},
        "oven": {"models": "Wolf - sister brand for cooking", "tech": "", "issues": ""},
        "cooktop": {"models": "Wolf - sister brand for cooking", "tech": "", "issues": ""}
    },
    "wolf": {
        "washer": {"models": "N/A - Wolf focuses on cooking appliances", "tech": "", "issues": ""},
        "dryer": {"models": "N/A - Wolf focuses on cooking appliances", "tech": "", "issues": ""},
        "refrigerator": {"models": "Sub-Zero - sister brand for refrigeration", "tech": "", "issues": ""},
        "dishwasher": {"models": "Cove - sister brand for dishwashers", "tech": "", "issues": ""},
        "oven": {"models": "M/E Series, SO30/DO30, Convection Steam CSO", "tech": "VertiCross convection, Dual VertiCross, Gourmet mode", "issues": "convection fan motor wear, temperature probe calibration, door gasket replacement, steam generator maintenance"},
        "cooktop": {"models": "CG/CT/CI Series, Rangetop SRT", "tech": "Dual-Stacked burners, True Simmer, Induction Boost", "issues": "dual-stack burner cap cleaning, igniter module failures, induction error codes, burner orifice clogs"},
        "range": {"models": "GR/DF/IR Series, 36/48/60-inch", "tech": "Dual VertiCross convection, Infrared charbroiler, French Top", "issues": "infrared burner element failures, French Top calibration, dual fuel igniter issues, griddle thermostat"},
        "microwave": {"models": "MD/MDD Drawer series, Convection", "tech": "Gourmet mode, Sensor cooking, Keep Warm", "issues": "drawer mechanism alignment, magnetron failures, sensor calibration"}
    },
    "viking": {
        "washer": {"models": "N/A - Viking focuses on kitchen appliances", "tech": "", "issues": ""},
        "dryer": {"models": "N/A - Viking focuses on kitchen appliances", "tech": "", "issues": ""},
        "refrigerator": {"models": "Professional VCBB/VCSB/VCFB series, 3/5/7 Series", "tech": "ProChill temperature, Plasmacluster air purification, Theatre LED", "issues": "ProChill compressor relay, ice maker auger jams, door alignment, evaporator fan motor"},
        "dishwasher": {"models": "Professional VDWU/FDW series", "tech": "Turbo Fan Dry, Multi-Level wash, LCD display", "issues": "Turbo Fan motor failures, wash arm bearing wear, LCD display issues, drain pump blockages"},
        "oven": {"models": "Professional VGSC/VGIC/VESO series, 5/7 Series", "tech": "TruConvec convection, VariSimmer, GourmetGlo infrared", "issues": "TruConvec fan motor wear, sealed burner igniter, infrared broiler element, door hinge springs"},
        "cooktop": {"models": "Professional VGSU/VICU series", "tech": "Elevation burners, VariSimmer, MagneQuick induction", "issues": "Elevation burner cap issues, MagneQuick coil errors, gas valve failures, sealed burner igniters"},
        "range": {"models": "Professional VGCC/VGIC/VDR series", "tech": "ProFlow convection, SureSpark ignition, TruGlide racks", "issues": "ProFlow fan failures, SureSpark module issues, griddle thermostat, oven temperature calibration"},
        "microwave": {"models": "Professional VMOC/VMOS series, Drawer", "tech": "Sensor cooking, TruGlide rack, Child lock", "issues": "magnetron failures, drawer track alignment, touchpad issues"}
    },
    "kitchenaid": {
        "washer": {"models": "KFWF/KFLP Front Load, Smart series", "tech": "Optimal Dose detergent, Steam Treat, WiFi enabled", "issues": "door boot seal leaks, drain pump failures, control board errors, motor coupling issues"},
        "dryer": {"models": "KFDP/KYWD series, Smart dryers", "tech": "Advanced Moisture Sensing, Steam Refresh, Wrinkle Shield", "issues": "heating element burnout, drum roller squeaks, thermal fuse failures, belt wear"},
        "refrigerator": {"models": "KRFF/KRMF/KBSD series, Built-In", "tech": "ExtendFresh Plus, Preserva Food Care, PrintShield", "issues": "ice maker auger jams, evaporator fan failures, water filter housing cracks, compressor relay"},
        "dishwasher": {"models": "KDFE/KDTM/KDTE series, FreeFlex Third Rack", "tech": "FreeFlex Third Rack, ProWash cycle, PrintShield Finish", "issues": "circulation pump failures, spray arm clogs, control board issues, door latch mechanism"},
        "oven": {"models": "KOSE/KOCE/KSEG series, Smart Oven+", "tech": "Even-Heat True Convection, Smart Oven+ attachments, Air Fry", "issues": "convection fan motor, temperature sensor drift, door hinge issues, bake element failures"},
        "cooktop": {"models": "KCGS/KCED/KCIG series", "tech": "Even-Heat element, Torch Melt burner, SimmerMelt burner", "issues": "infinite switch failures, burner igniter problems, touch control errors"},
        "microwave": {"models": "KMHS/KMHC/KMBP series", "tech": "Sensor cooking, Crispwave technology, Convection cooking", "issues": "magnetron failures, Crispwave element issues, door switch problems"}
    },
    "jenn-air": {
        "washer": {"models": "Connected Front Load JFW series", "tech": "Optimal Dose, WiFi connectivity, Steam option", "issues": "door boot seal failures, drain pump issues, control board errors"},
        "dryer": {"models": "Connected JFD series", "tech": "Steam Refresh, Advanced Moisture Sensing, WiFi", "issues": "heating element failures, drum bearing wear, moisture sensor issues"},
        "refrigerator": {"models": "DERA Rise/Noir JB/JF series, Built-In", "tech": "Obsidian interior, Twin Fresh climate control, WiFi", "issues": "compressor cycling issues, ice maker water valve, door gasket wear, evaporator fan"},
        "dishwasher": {"models": "Rise/Noir JDPSG/JDTSS series, TriFecta", "tech": "TriFecta wash system, Precise Dry option, Noir styling", "issues": "TriFecta motor issues, spray arm blockages, control panel errors"},
        "oven": {"models": "Rise/Noir JJW/JMW series, Connected Wall Oven", "tech": "V2 Vertical Dual-Fan, Culinary Center, WiFi diagnostics", "issues": "V2 fan motor failures, Culinary Center calibration, door hinge issues"},
        "cooktop": {"models": "Rise/Noir JGC/JIC series, Downdraft", "tech": "Downdraft ventilation, Dual-Choice element, Brass burners", "issues": "downdraft motor wear, Dual-Choice element failures, burner ignition problems"},
        "range": {"models": "Rise/Noir JGRP/JDRP series, Dual-Fuel", "tech": "Chromium griddle, Twin-Fan convection, WiFi", "issues": "Twin-Fan motor issues, griddle thermostat, dual fuel igniter failures"}
    },
    "frigidaire": {
        "washer": {"models": "Affinity FAFS/FAFW series, Front/Top Load", "tech": "Fresh Water rinse, TimeWise technology", "issues": "door boot seal leaks, drain pump motor burnout, control board failures, lid switch issues"},
        "dryer": {"models": "Affinity FAQE/FASE series, Gallery", "tech": "DrySense technology, Quick Dry cycle, Steam option", "issues": "heating element failures, thermal fuse issues, drum roller wear, belt breaks"},
        "refrigerator": {"models": "Gallery FGHB/FGSS series, Professional FPBC/FPBS", "tech": "PureAir Ultra filters, SpaceWise organization, Even Temp", "issues": "ice maker water inlet valve, evaporator fan motor, defrost heater, compressor relay"},
        "dishwasher": {"models": "Gallery FGID/FGCD series, BladeSpray", "tech": "BladeSpray arm, OrbitClean spray, MaxBoost dry", "issues": "BladeSpray arm bearing, circulation pump failures, door latch issues, control board"},
        "oven": {"models": "Gallery FGEF/FGGH series, Professional FPEF", "tech": "True Convection, Quick Preheat, Air Fry option", "issues": "bake element burnout, convection fan motor, temperature sensor drift, igniter failures"},
        "cooktop": {"models": "Gallery FGGC/FGEC series, Professional", "tech": "PowerPlus burner, SpaceWise expandable element", "issues": "spark igniter module, infinite switch failures, element coil damage"},
        "microwave": {"models": "Gallery FGMV/Professional FPMO series", "tech": "Sensor cooking, SpaceWise rack, One-Touch options", "issues": "magnetron failures, turntable motor issues, touchpad membrane wear"}
    },
    "electrolux": {
        "washer": {"models": "ELFW/EFLS series, Perfect Steam", "tech": "Perfect Steam system, SmartBoost premix, LuxCare wash", "issues": "steam generator blockages, SmartBoost dispenser clogs, door boot leaks, control module"},
        "dryer": {"models": "ELFE/EFME series, Perfect Steam", "tech": "Instant Refresh cycle, Predictive Dry, Step Saver door", "issues": "steam generator issues, heating element failures, drum bearing noise, moisture sensor"},
        "refrigerator": {"models": "EI32/EW30 series, French Door", "tech": "PureAdvantage filtration, Perfect Temp drawer, Wave-Touch", "issues": "ice maker auger jams, compressor issues, evaporator fan motor, door seal"},
        "dishwasher": {"models": "EI24/EIDW series, IQ-Touch", "tech": "30-minute fast wash, SatelliteSpray arm, Perfect Dry", "issues": "SatelliteSpray motor failures, circulation pump issues, control board errors, door latch"},
        "oven": {"models": "EI30/EW30 series, Wave-Touch, IQ-Touch", "tech": "Perfect Convection3, Luxury-Glide racks, Self-clean", "issues": "convection fan failures, Luxury-Glide rack issues, bake element, door hinge"},
        "cooktop": {"models": "EI36/EW30 series, Induction, Gas", "tech": "Perfect Set controls, Infinite-Heat elements", "issues": "induction coil failures, Perfect Set control errors, igniter module issues"},
        "microwave": {"models": "EI30/EW30 series, Over-the-Range", "tech": "Sensor cooking, Wave-Touch controls, Keep Warm", "issues": "magnetron failures, Wave-Touch panel issues, fan motor noise"}
    },
    "maytag": {
        "washer": {"models": "MVW/MHW series, Commercial Technology", "tech": "PowerWash agitator, Extra Power button, Fresh Hold", "issues": "transmission failures, agitator dogs wear, lid switch problems, drain pump motor"},
        "dryer": {"models": "MED/MGD series, Commercial Technology", "tech": "Extra Power button, Wrinkle Prevent, Advanced Moisture Sensing", "issues": "drum roller failures, heating element burnout, thermal fuse issues, belt wear"},
        "refrigerator": {"models": "MFI/MSS series, Wide French Door", "tech": "PowerCold feature, BrightSeries LED, Fingerprint Resistant", "issues": "ice maker auger jams, evaporator fan motor noise, defrost heater, compressor relay"},
        "dishwasher": {"models": "MDB series, Dual Power Filtration", "tech": "PowerDry option, Dual Power Filtration, Steam Sanitize", "issues": "circulation pump failures, PowerDry fan issues, food chopper blade, control board"},
        "oven": {"models": "MER/MGR series, AquaLift Self-Clean", "tech": "Power Preheat, Precision Cooking, AquaLift clean", "issues": "bake element failures, AquaLift system issues, igniter problems, temperature sensor"},
        "cooktop": {"models": "MGC/MEC series", "tech": "Power burner, DuraClean surface, Reversible grates", "issues": "spark igniter failures, infinite switch issues, burner cap alignment"},
        "microwave": {"models": "MMV series, Over-the-Range", "tech": "Sensor cooking, 2-speed fan, Charcoal filter", "issues": "magnetron degradation, fan motor noise, touchpad failures"}
    },
    "kenmore": {
        "washer": {"models": "Elite 31/41 series, 20232/22352 Top Load", "tech": "Accela-Wash, Steam Treat, Smart Motion", "issues": "motor coupling failures, lid switch problems, transmission wear, drain pump clogs"},
        "dryer": {"models": "Elite 61/81 series, 66132/77132 models", "tech": "Accela-Steam, Smart Dry Ultra, Wrinkle Guard", "issues": "heating element burnout, thermal fuse failures, drum roller squeaks, belt breaks"},
        "refrigerator": {"models": "Elite 74/72 series, 51/52 Side-by-Side", "tech": "GeniusCool, Grab-N-Go door, SmartSense", "issues": "ice maker auger jams, compressor relay failures, evaporator fan motor, defrost issues"},
        "dishwasher": {"models": "Elite 14/12 series, Ultra Wash", "tech": "PowerWave spray arm, TurboZone option, SmartWash", "issues": "wash motor failures, spray arm bearing wear, control board issues, door latch"},
        "oven": {"models": "Elite 95/97 series, Pro 79 series", "tech": "True Convection, Precision Temp, Self-clean", "issues": "bake element failures, igniter issues, door hinge problems, temperature calibration"},
        "cooktop": {"models": "Elite 43/44 series", "tech": "Even-Heat burners, PowerBoil element", "issues": "spark igniter module, element coil failures, infinite switch issues"},
        "microwave": {"models": "Elite 80/85 series", "tech": "Sensor cooking, EasyClean interior", "issues": "magnetron failures, turntable motor, touchpad membrane wear"}
    },
    "amana": {
        "washer": {"models": "NTW/NFW series, High Efficiency", "tech": "Dual Action agitator, Deep Water Wash, Late Lid Lock", "issues": "transmission failures, lid switch problems, drain pump motor, agitator wear"},
        "dryer": {"models": "NED/NGD series, High Efficiency", "tech": "Automatic Dryness Control, Wrinkle Prevent", "issues": "heating element failures, thermal fuse issues, drum roller wear, belt breaks"},
        "refrigerator": {"models": "ABB/ART series, Bottom Freezer, Top Freezer", "tech": "Temp Assure freshness, Gallon Door bins, Humidity control", "issues": "defrost timer failures, evaporator fan motor, thermostat issues, ice maker valve"},
        "dishwasher": {"models": "ADB series, Triple Filter", "tech": "Triple Filter wash, High Temp wash, Heated Dry", "issues": "circulation pump wear, spray arm clogs, door latch failures, control board"},
        "oven": {"models": "AGR/AER series, Self-Clean, Easy-Touch controls", "tech": "Temp Assure cooking, Bake Assist, Easy-Touch", "issues": "bake element burnout, igniter failures, thermostat drift, door hinge springs"},
        "cooktop": {"models": "AGC/AEC series", "tech": "Sealed burners, Chrome drip bowls", "issues": "spark igniter failures, burner cap alignment, element coil damage"},
        "microwave": {"models": "AMV series, Over-the-Range", "tech": "Add 30 Seconds, Auto Defrost, Touch controls", "issues": "magnetron failures, touchpad issues, fan motor noise"}
    },
    "dacor": {
        "washer": {"models": "N/A - Dacor focuses on kitchen appliances", "tech": "", "issues": ""},
        "dryer": {"models": "N/A - Dacor focuses on kitchen appliances", "tech": "", "issues": ""},
        "refrigerator": {"models": "Modernist DRF/DRR series, Professional", "tech": "FreshZone drawer, LCD touchscreen, WiFi enabled", "issues": "LCD display failures, FreshZone temperature issues, compressor relay, ice maker valve"},
        "dishwasher": {"models": "Modernist DDW series, Heritage DDH", "tech": "AutoProbe sensors, WaterWall spray, RackMatic adjustment", "issues": "WaterWall motor issues, AutoProbe sensor failures, spray arm bearing, door latch"},
        "oven": {"models": "Modernist DOB/DOC/DOP series, Steam Assist", "tech": "Four-Part Pure Convection, iQ Controller, Steam Assist", "issues": "Pure Convection fan motor, iQ Controller calibration, steam system maintenance, door hinge"},
        "cooktop": {"models": "Modernist DTG/DTI series, Renaissance", "tech": "Illumina burner knobs, SimmerSear burner, Flex Induction", "issues": "Illumina LED failures, SimmerSear valve issues, induction coil errors, igniter module"},
        "range": {"models": "Modernist DOP series, Renaissance DYRP", "tech": "GreenClean Steam, iQ Controller, Dual-Stack burners", "issues": "Dual-Stack burner alignment, steam generator maintenance, iQ display issues"},
        "microwave": {"models": "Modernist DMR/DMW Drawer, Discovery", "tech": "Sensor cooking, TouchControl panel, Auto humidity sense", "issues": "drawer mechanism alignment, magnetron failures, TouchControl calibration"}
    },
    "gaggenau": {
        "washer": {"models": "N/A - Gaggenau focuses on luxury kitchen appliances", "tech": "", "issues": ""},
        "dryer": {"models": "N/A - Gaggenau focuses on luxury kitchen appliances", "tech": "", "issues": ""},
        "refrigerator": {"models": "Vario RC/RB/RW series, Wine Climate", "tech": "Fully integrated panel, Fresh Cooling, Wine Climate zones", "issues": "compressor relay failures, Wine Climate sensor calibration, door hinge tension, ice maker"},
        "dishwasher": {"models": "400/200 Series DF/DI, Fully Integrated", "tech": "Zeolite drying, Aqua Sensor, Time Light projection", "issues": "Zeolite regeneration, Aqua Sensor calibration, circulation pump, Time Light failures"},
        "oven": {"models": "400/200 Series BO/BS/BOP, Combi-Steam", "tech": "Rotisserie, Home Connect, Full-surface grill", "issues": "steam generator descaling, rotisserie motor, door hinge alignment, temperature calibration"},
        "cooktop": {"models": "400/200 Series CI/CG/VI Vario", "tech": "Flex Induction, Full-Surface Induction, Wok burner", "issues": "Flex Induction zone errors, Wok burner alignment, touch control calibration"},
        "microwave": {"models": "400/200 Series BM/CM series, Combi", "tech": "Convection microwave, Combination cooking modes", "issues": "magnetron failures, convection fan motor, touch control panel"}
    },
    "fisher-paykel": {
        "washer": {"models": "WashSmart WH/WL series, Front Load", "tech": "SmartDrive motor, Vortex Wash, Auto-sensing", "issues": "SmartDrive motor faults, door boot seal leaks, control module errors, drain pump"},
        "dryer": {"models": "DH/DE series, Heat Pump, Condensing", "tech": "Auto-sensing dry, Heat Pump energy efficiency, Reverse tumble", "issues": "heat pump compressor issues, condensate pump failures, drum bearing noise, filter housing"},
        "refrigerator": {"models": "ActiveSmart RF/RS series, French Door, Column", "tech": "ActiveSmart technology, Variable Temperature zones, Humidity control", "issues": "ActiveSmart board failures, humidity control sensor, ice maker auger, door alignment"},
        "dishwasher": {"models": "DishDrawer DD24/DD36 series, Built-In", "tech": "DishDrawer design, SmartDrive motor, Sanitize cycle", "issues": "DishDrawer motor failures, SmartDrive board issues, drawer track alignment, spray arm"},
        "oven": {"models": "OB30/OB24 series, Companion, Minimal", "tech": "Aero Pastry function, Self-cleaning pyrolytic, 11 cooking functions", "issues": "Aero fan motor failures, pyrolytic latch issues, temperature sensor drift, door hinge"},
        "cooktop": {"models": "CG/CI series, Gas, Induction", "tech": "SmartZone technology, PowerBoost, Continuous grates", "issues": "SmartZone induction errors, PowerBoost coil failures, gas igniter issues, control panel"}
    }
}

# Default brand data
DEFAULT_BRAND = {
    "washer": {"models": "various top and front load models", "tech": "advanced wash technology", "issues": "common mechanical and electronic failures"},
    "dryer": {"models": "gas and electric models", "tech": "sensor dry technology", "issues": "heating and mechanical issues"},
    "refrigerator": {"models": "French door, side-by-side, top freezer", "tech": "multi-zone cooling", "issues": "cooling and ice maker problems"},
    "dishwasher": {"models": "built-in and portable", "tech": "multi-spray wash systems", "issues": "drainage and cleaning issues"},
    "oven": {"models": "wall ovens and ranges", "tech": "convection cooking", "issues": "heating and temperature problems"},
    "cooktop": {"models": "gas, electric, and induction", "tech": "precise heat control", "issues": "burner and ignition issues"},
    "microwave": {"models": "over-the-range and built-in", "tech": "sensor cooking", "issues": "heating and control issues"},
    "wine-cooler": {"models": "undercounter and freestanding", "tech": "dual zone cooling", "issues": "temperature and compressor issues"},
    "vent-hood": {"models": "wall mount and under-cabinet", "tech": "multi-speed ventilation", "issues": "motor and airflow problems"}
}


def get_brand_appliance_info(brand_slug, appliance_type):
    """Get brand-specific appliance information."""
    brand_key = brand_slug.lower()
    appliance_key = appliance_type.replace("-repair", "").replace("-", "_").replace("vent_hood", "vent-hood")

    # Map common appliance variations
    appliance_map = {
        "vent_hood": "vent-hood",
        "wine_cooler": "wine-cooler"
    }
    appliance_key = appliance_map.get(appliance_key, appliance_key)

    if brand_key in BRAND_APPLIANCE_DATA:
        brand_data = BRAND_APPLIANCE_DATA[brand_key]
        if appliance_key in brand_data:
            return brand_data[appliance_key]

    return DEFAULT_BRAND.get(appliance_key, DEFAULT_BRAND["washer"])


def generate_enhanced_card_content(brand_slug, city_slug, appliance_type):
    """Generate enhanced content for service card show-more section."""
    brand_name = brand_slug.replace("-", " ").title()
    city = CITIES.get(city_slug, {"name": city_slug.replace("-", " ").title(), "pop": "varies", "type": "community", "features": "residential homes"})
    info = get_brand_appliance_info(brand_slug, appliance_type)
    appliance_name = appliance_type.replace("-repair", "").replace("-", " ").title()

    # Skip if no real data
    if not info.get("models") or info.get("models") == "":
        return None

    content = f'''
<p style="margin-top: 15px; margin-bottom: 12px;"><strong>{brand_name} {appliance_name} Models:</strong> {info["models"]}. Our {city["name"]} technicians are trained on {info["tech"]}.</p>
<p style="margin-bottom: 12px;"><strong>Common {brand_name} Issues:</strong> {info["issues"]}. Serving {city["name"]}'s {city["features"]} with same-day repair service.</p>
'''
    return content


def update_service_card(html, card_id, content):
    """Update a specific service card's expandable content."""
    if not content:
        return html

    # Find the expandable section for this card and append content
    pattern = rf'(<div id="expandable-text-{card_id}"[^>]*>)(.*?)(</div>\s*<div id="expandable-fade-{card_id}")'

    def replacer(match):
        opening = match.group(1)
        existing = match.group(2)
        closing = match.group(3)

        # Check if enhanced content already exists
        if "Models:</strong>" in existing:
            return match.group(0)

        return opening + existing + content + closing

    return re.sub(pattern, replacer, html, flags=re.DOTALL)


def process_page(file_path, city_slug, brand_slug):
    """Process a single page to enhance all service cards."""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    original_html = html
    cards_updated = 0

    # List of appliance types to update
    appliances = ["washer", "dryer", "refrigerator", "dishwasher", "oven", "cooktop", "microwave", "wine-cooler", "vent-hood"]

    for appliance in appliances:
        card_id = appliance
        content = generate_enhanced_card_content(brand_slug, city_slug, appliance)
        if content:
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
    ny_path = os.path.join(base_path, "ny")

    total_pages = 0
    total_cards = 0

    print("=" * 60)
    print("ENHANCING SERVICE CARD SHOW-MORE SECTIONS")
    print("=" * 60)

    for city_dir in sorted(os.listdir(ny_path)):
        city_path = os.path.join(ny_path, city_dir)
        if not os.path.isdir(city_path) or city_dir.startswith('.'):
            continue

        for item in sorted(os.listdir(city_path)):
            if not item.endswith('-repair'):
                continue

            item_path = os.path.join(city_path, item)
            index_file = os.path.join(item_path, 'index.html')

            if os.path.exists(index_file):
                brand_slug = item.replace('-repair', '')
                cards = process_page(index_file, city_dir, brand_slug)
                if cards > 0:
                    total_pages += 1
                    total_cards += cards
                    print(f"Updated: ny/{city_dir}/{item}/ ({cards} cards)")

    print("\n" + "=" * 60)
    print(f"TOTAL: {total_pages} pages, {total_cards} service cards enhanced")
    print("=" * 60)


if __name__ == "__main__":
    main()
