# Charon Freighter blueprint requirements

# Display name for the dropdown menu
display_name = "Charon Freighter"
ship_type = "Freighter"
# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Charon construction
charon_requirements = {
    "Capital Propulsion Engine": 5,
    "Capital Armor Plates": 5,
    "Capital Cargo Bay": 50,
    "Capital Construction Parts": 5,
    "R-O Trigger Neurolink Conduit": 16,
    "Gravimetric-FTL Interlink Communicator": 1,
    "Auto-Integrity Preservation Seal": 400,
    "Life Support Backup Unit": 200,
    "Capital Core Temperature Regulator": 1
}

# Total mineral requirements
charon_minerals = {
    "Tritanium": 1770000,
    "Pyerite": 6365000,
    "Mexallon": 1770000,
    "Isogen": 490000,
    "Nocxium": 47750,
    "Zydrine": 24050,
    "Megacyte": 12100
}

# Planetary and advanced material requirements
charon_pi_materials = {
    "Self-Harmonizing Power Core": 20,
    "Organic Mortar Applicators": 25,
    "Integrity Response Drones": 25,
    "Supertensile Plastics": 1600,
    "Test Cultures": 1600,
    "Viral Agent": 1600,
    "Nanites": 1600,
    "Pressurized Oxidizers": 25160,
    "Reinforced Carbon Fiber": 31660,
    "Axosomatic Neurolink Enhancer": 640,
    "Reaction-Orienting Neurolink Stabilizer": 16,
    "Chiral Structures": 5000,
    "Water": 5000
}

# Ship specifications and attributes
charon_specifications = {
    "cargohold_capacity": 300000,
    "ship_maintenance_bay": 1350000,
    "hull_hp": 54000,
    "armor_hp": 54000,
    "shield_hp": 67500,
    "sig_radius": 500,
    "max_velocity": 139,
    "mass": 890000000,
    "volume": 950000,
    "ship_class": "Freighter (Industrial)",
    "manufacturer": "ORE"
}

# Production details
charon_production_details = {
    "production_time": 172800,  # 48 hours in seconds
    "facility_requirements": ["Capital Ship Assembly Array", "Sotiyo Engineering Complex"],
    "skills_required": {
        "Industry": 5,
        "Advanced Industry": 4,
        "Capital Ship Construction": 3,
        "Science": 4
    },
    "invention": False,  # Not inventable (direct T1 production)
    "base_materials_efficiency": 0  # ME0
}
